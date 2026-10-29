import importlib.util,unittest,tempfile,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
spec=importlib.util.spec_from_file_location("local_server",Path(__file__).with_name("local-server.py"))
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class TestLocalStorage(unittest.TestCase):
 def test_schema(self):
  with tempfile.TemporaryDirectory() as d:
   mod.DB=Path(d)/"test.sqlite3"
   with mod.connect() as db:
    db.execute("INSERT INTO orders VALUES (?,?,?,?)",("test","2026-10-29T00:00:00Z","draft",'[{"sku":"yara","quantity":1,"unitPrice":25}]'))
    self.assertEqual(db.execute("SELECT COUNT(*) FROM orders").fetchone()[0],1)
 def test_atomic_reservation(self):
  from inventory import reserve
  with tempfile.TemporaryDirectory() as d:
   mod.DB=Path(d)/"test.sqlite3"
   with mod.connect() as db:
    db.execute("UPDATE products SET stock=3 WHERE sku='yara'")
    db.commit()
   with mod.connect() as db:
    result=reserve(db,[{"sku":"yara","quantity":2}])
    self.assertEqual(result["status"],"reserved-test")
   with mod.connect() as db:
    self.assertEqual(db.execute("SELECT stock FROM products WHERE sku='yara'").fetchone()[0],1)
    with self.assertRaisesRegex(ValueError,"insufficient stock"):
     reserve(db,[{"sku":"yara","quantity":2}])
    self.assertEqual(db.execute("SELECT stock FROM products WHERE sku='yara'").fetchone()[0],1)
    self.assertEqual(db.execute("SELECT COUNT(*) FROM orders").fetchone()[0],1)
 def test_cancel_restores_stock_once(self):
  from inventory import reserve,cancel_reservation
  with tempfile.TemporaryDirectory() as d:
   mod.DB=Path(d)/"test.sqlite3"
   with mod.connect() as db:
    db.execute("UPDATE products SET stock=4 WHERE sku='asad'")
    db.commit()
   with mod.connect() as db:
    order=reserve(db,[{"sku":"asad","quantity":3}])
    self.assertEqual(db.execute("SELECT stock FROM products WHERE sku='asad'").fetchone()[0],1)
    first=cancel_reservation(db,order["id"])
    second=cancel_reservation(db,order["id"])
    self.assertFalse(first["alreadyCancelled"])
    self.assertTrue(second["alreadyCancelled"])
    self.assertEqual(db.execute("SELECT stock FROM products WHERE sku='asad'").fetchone()[0],4)
 def test_prices(self):
  self.assertEqual(mod.prices(),{"yara":25,"khamrah":35,"asad":35})
if __name__=="__main__":unittest.main()
