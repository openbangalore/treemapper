import auth, database, json, treemapper, os
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
	return "inserted"
	
def get_tree_details(form, cookies):
	from jinja2 import Environment, FileSystemLoader

	data = database.sql("""select * from Species where local_name=%s""", form.local_name)
	if data:
		treemapper.response.status = "okay"

		jenv = Environment(loader = FileSystemLoader("../templates"))
		html = jenv.get_template("includes/tree-details.html").render({
			"item": data[0]
		})

		treemapper.response.html = html
	else:
		treemapper.response.status = "not found"

def save(form, cookies):
	import base64, shutil
	rebuild = False
	
	email = auth.verify(form, cookies)
	if not email:
		treemapper.response.action = "refresh"
		return
		
	# save tree
	database.insert("Tree", {"local_name": form.local_name, "point_x": form.latitude, 
		"point_y": form.longitude, "user": email.encode("utf-8")})
	treeid = database.sql("select last_insert_id() as id")[0].id
	
	# save files
	treefilepath = os.path.join("img", "data", str(treeid) + "-tree.jpg")
	with open(treefilepath, "w+") as treefile:
		treefile.write(base64.b64decode(form.tree_img))
		database.sql("update Tree set tree_img=%s where id=%s", (treefilepath, treeid))

	# set files in master (if not set)
	if not database.sql("select tree_img from Species where local_name=%s", form.local_name)[0].tree_img:
		masterfilepath = os.path.join("img", "master", 
			form.local_name.replace(" ", "_").lower() + "-tree.jpg")
		shutil.copyfile(treefilepath, masterfilepath)
		database.sql("update Species set tree_img=%s where local_name=%s", (masterfilepath, form.local_name))
		rebuild = True

	if form.leaf_img:
		leaffilepath = os.path.join("img", "data", str(treeid) + "-tree.jpg")
		with open(leaffilepath, "w+") as leaffile:
			leaffile.write(base64.b64decode(form.leaf_img))
		database.sql("update Tree set leaf_img=%s where id=%s", (leaffilepath, treeid))

		if not database.sql("select leaf_img from Species where local_name=%s", form.local_name)[0].leaf_img:
			masterfilepath = os.path.join("img", "master", 
				form.local_name.replace(" ", "_").lower() + "-leaf.jpg")
			shutil.copyfile(leaffilepath, masterfilepath)
			database.sql("update Species set leaf_img=%s where local_name=%s", (masterfilepath, form.local_name))
			rebuild = True
			
	database.commit()
	
	if rebuild:
		import build
		build.rebuild_tree_pages(database.sql("""select * from Species where local_name=%s""", form.local_name))
	
	treemapper.response.status = "okay"
	
import unittest

if __name__=="__main__":
	unittest.main()
	