import database
	
def make_db():
	print "creating %s..." % database.dbname
	database.connect("root")
	database.sql("""drop database if exists %s""" % database.dbname)
	try: 
		database.sql("""drop user %s@localhost""" % database.dbname)
	except: pass
	
	
	database.sql("""create database %s""" % database.dbname)
	database.sql("""create user %s@localhost identified by '%s'""" % (database.dbname, database.dbpass))
	database.sql("""grant all privileges on %s.* to %s@localhost""" % (database.dbname, database.dbname))
	database.sql("""flush privileges""")
	database.sql("""use %s""" % database.dbname)

	database.sql("""create table `user` (
		email varchar(180) primary key not null,
		first_name varchar(180),
		last_name varchar(180)) engine=InnoDB character set=utf8""")

	database.sql("""create table `session` (
		id varchar(180) primary key not null,
		email varchar(180)) engine=InnoDB character set=utf8""")

def make_tables():
	from utils import get_csv_data
	tables = {
		"Species": {
			"filename": "data/species/tree_list.csv", 
			"primary_key": "code",
			"add_fields": ["tree_img varchar(255)", "leaf_img varchar(255)"]
		},
		"Tree": {
			"filename": "data/tree/PUNE3_TreesOTM.csv", 
			"primary_key": "ID",
			"auto_increment": True,
			"add_fields": ["local_name varchar(255)", "tree_img varchar(255)", 
				"leaf_img varchar(255)", "user varchar(255)"]
		}
	}
	
	for tablename, opts in tables.items():
		data = get_csv_data(opts["filename"])
		database.create_table(tablename, data[0], opts.get("primary_key"), 
			add_fields=opts.get("add_fields"), data=data, auto_increment = opts.get("auto_increment"))
	
if __name__=="__main__":
	make_db()
	make_tables()
	
	from importer import import_files
	import_files()
	
	from build import make_html
	make_html()