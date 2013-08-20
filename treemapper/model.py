import auth, database, json, treemapper
from utils import _dict

def add_tree(form, cookies):
	email = auth.verify(form, cookies)
	if not email:
		treemapper.response.action = "refresh"
		return
	
	data = form.tree
	if isinstance(data, basestring):
		data = json.loads(data)
	
	database.insert("Tree", data)
	database.commit()
	
def get_species(form, cookies):
	data = database.sql("""select * from Species where local_name=%s""", form.local_name)
	if data:
		treemapper.response.status = "okay"
		treemapper.response.data = json.dumps(data[0])
	else:
		treemapper.response.status = "not found"

import unittest

class TestModel(unittest.TestCase):
	def test_get_species(self):
		get_species(_dict({"local_name": "test"}), None)
		self.assertEquals(treemapper.response.status, "not found")

		get_species(_dict({"local_name": "Pachunda"}), None)
		data = _dict(json.loads(treemapper.response.data))
		self.assertEquals(data.code, "CAGR")
		
if __name__=="__main__":
	unittest.main()
	
		
