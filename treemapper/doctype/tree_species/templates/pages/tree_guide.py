import webnotes

def get_context():
	local_names = {}
	for parent, local_name in webnotes.conn.sql("""select parent, local_name from 
		`tabTree Species Local Name`"""):
		local_names.setdefault(parent, []).append(local_name)
	for key in local_names:
		local_names[key] = ", ".join(local_names[key])
	return {
		"species": webnotes.conn.sql("""select name, tree_image, leaf_image, wikipedia_link from `tabTree Species`
			where publish = 1
			order by name asc""", as_dict=1),
		"local_names": local_names
	}