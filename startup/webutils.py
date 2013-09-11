import webnotes

def get_website_settings(context):
	out = []
	added = []
	for t in webnotes.conn.sql("""select distinct local_name, parent from 
		`tabTree Species Local Name` where ifnull(local_name,'')!='' 
		order by local_name asc""", as_dict=1):
		if not t.local_name in added:
			out.append(t)
			added.append(t.local_name)
	
	context.update({
		"tree_species": out
	})