"""OUD BRONX local development API. Python 3 stdlib + SQLite; binds localhost only.
Not a public production server. No customer PII or payment data.
Run: python3 commerce/local-server.py
"""
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import json,sqlite3,uuid,datetime,os,secrets,hmac
from inventory import reserve,cancel_reservation
DB=Path(os.environ.get("OUD_LOCAL_DB",str(Path(__file__).with_name("commerce-local.sqlite3"))))
PORT=int(os.environ.get("OUD_LOCAL_PORT","8765"))
CATALOG_PATH=Path(__file__).with_name("catalog.json")
def prices():
 return {p["sku"]:p["price"] for p in json.loads(CATALOG_PATH.read_text())["products"]}
ADMIN_TOKEN=os.environ.get("OUD_LOCAL_ADMIN_TOKEN","")
LOCAL_ORIGINS=("http://localhost:8000","http://127.0.0.1:8000")
def admin_authorized(handler):
 origin=handler.headers.get("Origin","")
 token=handler.headers.get("X-OUD-Admin-Token","")
 return bool(ADMIN_TOKEN) and origin in LOCAL_ORIGINS and hmac.compare_digest(token,ADMIN_TOKEN)
def catalog_rows(db):
 rows=db.execute("SELECT sku,name,price,stock FROM products ORDER BY sku").fetchall()
 return [{"sku":a,"name":b,"price":c,"stock":d} for a,b,c,d in rows]
def connect():
 db=sqlite3.connect(DB)
 db.execute("CREATE TABLE IF NOT EXISTS orders (id TEXT PRIMARY KEY, created_at TEXT NOT NULL, status TEXT NOT NULL, items TEXT NOT NULL)")
 db.execute("CREATE TABLE IF NOT EXISTS products (sku TEXT PRIMARY KEY,name TEXT NOT NULL,price REAL NOT NULL CHECK(price>=0),stock INTEGER NOT NULL CHECK(stock>=0))")
 if db.execute("SELECT COUNT(*) FROM products").fetchone()[0]==0:
  data=json.loads(CATALOG_PATH.read_text())["products"]
  db.executemany("INSERT INTO products VALUES (?,?,?,?)",[(p["sku"],p["name"],p["price"],p["stock"]) for p in data])
 db.commit()
 return db
class Handler(BaseHTTPRequestHandler):
 def send(self,status,data):
  body=json.dumps(data).encode()
  self.send_response(status)
  self.send_header("Content-Type","application/json; charset=utf-8")
  self.send_header("Cache-Control","no-store")
  self.send_header("Access-Control-Allow-Origin",self.headers.get("Origin","null") if self.headers.get("Origin") in ("http://localhost:8000","http://127.0.0.1:8000","https://kelffren.github.io") else "null")
  self.send_header("Access-Control-Allow-Headers","Content-Type, X-OUD-Admin-Token")
  self.send_header("Content-Length",str(len(body)))
  self.end_headers()
  self.wfile.write(body)
 def do_OPTIONS(self):
  self.send_response(204)
  self.send_header("Access-Control-Allow-Origin",self.headers.get("Origin","null") if self.headers.get("Origin") in ("http://localhost:8000","http://127.0.0.1:8000","https://kelffren.github.io") else "null")
  self.send_header("Access-Control-Allow-Methods","GET, POST, PUT, OPTIONS")
  self.send_header("Access-Control-Allow-Headers","Content-Type, X-OUD-Admin-Token")
  self.end_headers()
 def do_GET(self):
  if urlsplit(self.path).path=="/catalog":
   with connect() as db:return self.send(200,{"products":catalog_rows(db),"mode":"local-sqlite"})
  if urlsplit(self.path).path=="/admin/catalog":
   if not admin_authorized(self):return self.send(403,{"error":"local admin authorization required"})
   with connect() as db:return self.send(200,{"products":catalog_rows(db)})
  if urlsplit(self.path).path=="/health":return self.send(200,{"ok":True,"mode":"local-sqlite"})
  if urlsplit(self.path).path!="/orders":return self.send(404,{"error":"not found"})
  with connect() as db:rows=db.execute("SELECT id,created_at,status,items FROM orders ORDER BY created_at DESC LIMIT 200").fetchall()
  self.send(200,[{"id":a,"createdAt":b,"status":c,"items":json.loads(d)} for a,b,c,d in rows])
 def do_PUT(self):
  if not urlsplit(self.path).path.startswith("/admin/products/"):return self.send(404,{"error":"not found"})
  if not admin_authorized(self):return self.send(403,{"error":"local admin authorization required"})
  try:
   size=int(self.headers.get("Content-Length","0"))
   if size<2 or size>2048:return self.send(413,{"error":"invalid size"})
   item=json.loads(self.rfile.read(size))
   price=item["price"];stock=item["stock"]
   if type(price) not in (int,float) or not 0<=price<=100000 or type(stock)!=int or not 0<=stock<=100000:raise ValueError("invalid values")
   sku=urlsplit(self.path).path.rsplit("/",1)[-1]
   with connect() as db:
    changed=db.execute("UPDATE products SET price=?,stock=? WHERE sku=?",(round(price,2),stock,sku)).rowcount
    if not changed:return self.send(404,{"error":"unknown product"})
   self.send(200,{"sku":sku,"price":round(price,2),"stock":stock})
  except (ValueError,KeyError,TypeError,json.JSONDecodeError):self.send(400,{"error":"invalid product"})
 def do_POST(self):
  route=urlsplit(self.path).path
  cancel=route.startswith("/admin/reservations/") and route.endswith("/cancel")
  if route not in ("/orders","/admin/reservations") and not cancel:return self.send(404,{"error":"not found"})
  if (route=="/admin/reservations" or cancel) and not admin_authorized(self):return self.send(403,{"error":"local admin authorization required"})
  if cancel:
   try:
    order_id=route.split("/")[3]
    with connect() as db:result=cancel_reservation(db,order_id)
    return self.send(200,result)
   except ValueError as exc:return self.send(409,{"error":str(exc)})
  try:
   size=int(self.headers.get("Content-Length","0"))
   if size<1 or size>8192:return self.send(413,{"error":"invalid body size"})
   payload=json.loads(self.rfile.read(size))
   items=payload.get("items")
   if route=="/admin/reservations":
    try:
     with connect() as db:record=reserve(db,items)
     return self.send(201,record)
    except ValueError as exc:return self.send(409,{"error":str(exc)})
   if not isinstance(items,list) or not 1<=len(items)<=20:raise ValueError("invalid items")
   with connect() as db:allowed={p["sku"]:p["price"] for p in catalog_rows(db)}
   validated=[]
   for item in items:
    sku=item["sku"];qty=item["quantity"]
    if sku not in allowed or type(qty)!=int or not 1<=qty<=20:raise ValueError("invalid product or quantity")
    validated.append({"sku":sku,"quantity":qty,"unitPrice":allowed[sku]})
   record={"id":str(uuid.uuid4()),"createdAt":datetime.datetime.now(datetime.timezone.utc).isoformat(),"status":"draft","items":validated}
   with connect() as db:db.execute("INSERT INTO orders VALUES (?,?,?,?)",(record["id"],record["createdAt"],record["status"],json.dumps(validated)))
   self.send(201,record)
  except (ValueError,KeyError,TypeError,json.JSONDecodeError):self.send(400,{"error":"invalid order"})
if __name__=="__main__":
 print(f"Local SQLite API at http://localhost:{PORT}; DB={DB}")
 ThreadingHTTPServer(("127.0.0.1",PORT),Handler).serve_forever()
