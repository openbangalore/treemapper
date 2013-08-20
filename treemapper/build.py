import os, database, json, time

from jinja2 import Environment, FileSystemLoader

timestamps = {}

def make_html():
	global timestamps
	jenv = Environment(loader = FileSystemLoader("templates"))

	for fname in os.listdir("templates"):
		if fname.endswith(".html"):
			source_file_path = os.path.join("templates", fname)
			out_file_path = os.path.join("public", fname)
			
			if os.path.exists(out_file_path) and \
				timestamps.get(out_file_path) == os.path.getmtime(source_file_path):
					continue
			
			print "building " + fname
			start = database.sql("""select avg(point_x) as x, avg(point_y) as y from Tree limit 100""")[0]
			trees = database.sql("""select point_x, point_y, scientific, address from Tree limit 100""")
			species = database.sql("""select distinct local_name from Species
					where ifnull(local_name, "")!="" order by local_name""")
			
			args = {
				"start_x": start.x,
				"start_y": start.y,
				"trees": json.dumps(trees),
				"species": species
			}
			html = jenv.get_template(fname).render(args)
			with open(out_file_path, "w") as outfile:
				outfile.write(html)
				timestamps[out_file_path] = os.path.getmtime(source_file_path)
				
def watch():
	while True:
		time.sleep(1)
		make_html()
				
if __name__=="__main__":
	database.connect()
	watch()
