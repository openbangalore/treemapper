import webnotes

def get_context():
	return {
		"species": webnotes.conn.sql("""select name from `tabTree Species`
			where publish = 1
			order by name asc""", as_dict=1)
	}