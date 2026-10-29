"""Atomic inventory reservation for local prototype; no payments or customer data."""
import json,uuid,datetime,sqlite3
def reserve(db,items):
 if not isinstance(items,list) or not 1<=len(items)<=20:raise ValueError("invalid items")
 quantities={}
 for item in items:
  if not isinstance(item,dict):raise ValueError("invalid item")
  sku=item.get("sku");qty=item.get("quantity")
  if not isinstance(sku,str) or type(qty)!=int or not 1<=qty<=20:raise ValueError("invalid quantity")
  quantities[sku]=quantities.get(sku,0)+qty
 try:
  db.execute("BEGIN IMMEDIATE")
  validated=[]
  for sku,qty in quantities.items():
   row=db.execute("SELECT price,stock FROM products WHERE sku=?",(sku,)).fetchone()
   if row is None:raise ValueError("unknown product")
   price,stock=row
   if stock<qty:raise ValueError("insufficient stock: "+sku)
   db.execute("UPDATE products SET stock=stock-? WHERE sku=? AND stock>=?",(qty,sku,qty))
   validated.append({"sku":sku,"quantity":qty,"unitPrice":price})
  record={"id":str(uuid.uuid4()),"createdAt":datetime.datetime.now(datetime.timezone.utc).isoformat(),"status":"reserved-test","items":validated}
  db.execute("INSERT INTO orders VALUES (?,?,?,?)",(record["id"],record["createdAt"],record["status"],json.dumps(validated)))
  db.commit()
  return record
 except (ValueError,sqlite3.Error):
  db.rollback()
  raise

def cancel_reservation(db,order_id):
 """Release stock once; repeated cancellation is a no-op."""
 if not isinstance(order_id,str) or len(order_id)>100:raise ValueError("invalid order id")
 try:
  db.execute("BEGIN IMMEDIATE")
  row=db.execute("SELECT status,items FROM orders WHERE id=?",(order_id,)).fetchone()
  if row is None:raise ValueError("unknown order")
  status,serialized=row
  if status=="cancelled-test":
   db.rollback()
   return {"id":order_id,"status":"cancelled-test","alreadyCancelled":True}
  if status!="reserved-test":raise ValueError("order is not a reservation")
  items=json.loads(serialized)
  for item in items:
   db.execute("UPDATE products SET stock=stock+? WHERE sku=?",(item["quantity"],item["sku"]))
  db.execute("UPDATE orders SET status='cancelled-test' WHERE id=?",(order_id,))
  db.commit()
  return {"id":order_id,"status":"cancelled-test","alreadyCancelled":False}
 except (ValueError,sqlite3.Error):
  db.rollback()
  raise
