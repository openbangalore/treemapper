import os, database, json

from jinja2 import Environment, FileSystemLoader

def make_html():
	jenv = Environment(loader = FileSystemLoader("templates"))

	for fname in os.listdir("templates"):
		if fname.endswith(".html"):
			print "building " + fname
			start = database.sql("""select avg(point_x) as x, avg(point_y) as y from Tree""")[0]
			trees = database.sql("""select point_x, point_y, scientific, address from Tree""")
			args = {
				"start_x": start.x,
				"start_y": start.y,
				"trees": json.dumps(trees)
			}
			html = jenv.get_template(fname).render(args)
			with open(os.path.join("public", fname), "w") as outfile:
				outfile.write(html)
				
if __name__=="__main__":
	database.connect()
	make_html()
