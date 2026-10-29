import importlib.util,unittest,tempfile
from pathlib import Path
spec=importlib.util.spec_from_file_location("local_server",Path(__file__).with_name("local-server.py"))
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class TestLocalStorage(unittest.TestCase):
 def test_schema(self):
  with tempfile.TemporaryDirectory() as d:
   mod.DB=Path(d)/"test.sqlite3"
   with mod.connect() as db:
    db.execute("INSERT INTO orders VALUES (?,?,?,?)",("test","2026-10-29T00:00:00Z","draft",'[{"sku":"yara","quantity":1,"unitPrice":25}]'))
    self.assertEqual(db.execute("SELECT COUNT(*) FROM orders").fetchone()[0],1)
 def test_prices(self):
  self.assertEqual(mod.ALLOWED,{"yara":25,"khamrah":35,"asad":35})
if __name__=="__main__":unittest.main()
