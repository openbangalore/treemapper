import database, utils, os

def import_files():
	for table in ("species", "tree"):
		for fname in os.listdir(os.path.join("data", table)):
			if fname.endswith(".csv"):
				print fname + "..."
				data = utils.get_csv_data(os.path.join("data", table, fname))
				colnames = ['`%s`' % d.strip() for d in data[0]]
				for d in data[1:]:
					database.sql("""insert ignore into `%s` (%s) values (%s)""" % (table, 
						", ".join(colnames), ", ".join(["%s"] * len(colnames))), d)
	
				database.sql("commit")