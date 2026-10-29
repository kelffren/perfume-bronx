"""OUD BRONX local development API. Python 3 stdlib + SQLite; binds localhost only.
Not a public production server. No customer PII or payment data.
Run: python3 commerce/local-server.py
"""
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import json,sqlite3,uuid,datetime,os
DB=Path(os.environ.get("OUD_LOCAL_DB",str(Path(__file__).with_name("commerce-local.sqlite3"))))
PORT=int(os.environ.get("OUD_LOCAL_PORT","8765"))
ALLOWED={"yara":25,"khamrah":35,"asad":35}
def connect():
 db=sqlite3.connect(DB)
 db.execute("CREATE TABLE IF NOT EXISTS orders (id TEXT PRIMARY KEY, created_at TEXT NOT NULL, status TEXT NOT NULL, items TEXT NOT NULL)")
 return db
class Handler(BaseHTTPRequestHandler):
 def send(self,status,data):
  body=json.dumps(data).encode()
  self.send_response(status)
  self.send_header("Content-Type","application/json; charset=utf-8")
  self.send_header("Cache-Control","no-store")
  self.send_header("Access-Control-Allow-Origin","http://localhost:8765")
  self.send_header("Content-Length",str(len(body)))
  self.end_headers()
  self.wfile.write(body)
 def do_GET(self):
  if urlsplit(self.path).path=="/health":return self.send(200,{"ok":True,"mode":"local-sqlite"})
  if urlsplit(self.path).path!="/orders":return self.send(404,{"error":"not found"})
  with connect() as db:rows=db.execute("SELECT id,created_at,status,items FROM orders ORDER BY created_at DESC LIMIT 200").fetchall()
  self.send(200,[{"id":a,"createdAt":b,"status":c,"items":json.loads(d)} for a,b,c,d in rows])
 def do_POST(self):
  if urlsplit(self.path).path!="/orders":return self.send(404,{"error":"not found"})
  try:
   size=int(self.headers.get("Content-Length","0"))
   if size<1 or size>8192:return self.send(413,{"error":"invalid body size"})
   payload=json.loads(self.rfile.read(size))
   items=payload.get("items")
   if not isinstance(items,list) or not 1<=len(items)<=20:raise ValueError("invalid items")
   validated=[]
   for item in items:
    sku=item["sku"];qty=item["quantity"]
    if sku not in ALLOWED or type(qty)!=int or not 1<=qty<=20:raise ValueError("invalid product or quantity")
    validated.append({"sku":sku,"quantity":qty,"unitPrice":ALLOWED[sku]})
   record={"id":str(uuid.uuid4()),"createdAt":datetime.datetime.now(datetime.timezone.utc).isoformat(),"status":"draft","items":validated}
   with connect() as db:db.execute("INSERT INTO orders VALUES (?,?,?,?)",(record["id"],record["createdAt"],record["status"],json.dumps(validated)))
   self.send(201,record)
  except (ValueError,KeyError,TypeError,json.JSONDecodeError):self.send(400,{"error":"invalid order"})
if __name__=="__main__":
 print(f"Local SQLite API at http://localhost:{PORT}; DB={DB}")
 ThreadingHTTPServer(("127.0.0.1",PORT),Handler).serve_forever()
