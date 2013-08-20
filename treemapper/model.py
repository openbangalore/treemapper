import auth
import database

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

	return "inserted"