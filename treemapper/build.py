import os, database, json, time

from jinja2 import Environment, FileSystemLoader

timestamps = {}

def make_html():
	global timestamps
	jenv = Environment(loader = FileSystemLoader("templates"))

	start = database.sql("""select avg(point_x) as x, avg(point_y) as y from Tree limit 100""")[0]
	trees = database.sql("""select point_x, point_y, scientific, address from Tree limit 100""")

	species = {}
	species_list = database.sql("""select * from Species
			where ifnull(local_name, "")!="" order by local_name""")
	local_names = list(set([s.local_name for s in species_list]))
	local_names.sort()

	for s in species_list:
		species[s.local_name] = s

	args = {
		"start_x": start.x,
		"start_y": start.y,
		"trees": json.dumps(trees),
		"species": species,
		"species_list": species_list,
		"local_names": local_names
	}


	for fname in os.listdir("templates"):
		if fname.endswith(".html"):
			source_file_path = os.path.join("templates", fname)
			out_file_path = os.path.join("public", fname)
			
			if is_same(source_file_path):
				continue
			
			print "building " + fname
			
			html = jenv.get_template(fname).render(args)
			with open(out_file_path, "w") as outfile:
				outfile.write(html)
				timestamps[source_file_path] = os.path.getmtime(source_file_path)
	
	# tree page generator
	rebuild_tree_pages(species_list)

def rebuild_tree_pages(species_list):		
	source_file_path = os.path.join(os.path.dirname(__file__), "..", "templates", "generators", "tree-info.html")
	templates_path = os.path.join(os.path.dirname(__file__), "..", "templates")
	if not is_same(source_file_path):
		jenv = Environment(loader = FileSystemLoader(templates_path))
		for item in species_list:
			out_file_path = os.path.join("public", item.local_name.replace(" ", "_").lower() + ".html")
			html = jenv.get_template("generators/tree-info.html").render({"item": item})
			
			with open(out_file_path, "w") as outfile:
				outfile.write(html)
		
		timestamps[source_file_path] = os.path.getmtime(source_file_path)
		
def is_same(source_file_path):
	global timestamps
	return timestamps.get(source_file_path) == os.path.getmtime(source_file_path)

def watch():
	while True:
		time.sleep(1)
		make_html()
				
if __name__=="__main__":
	database.connect()
	watch()
