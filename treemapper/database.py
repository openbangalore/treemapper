import MySQLdb

from utils import _dict
from settings import *

cursor = None

def connect(cname=None, cpass=None):
	import getpass
	global cursor
	if cname=="root":
		cpass = rootpass or getpass.getpass("Enter Root Password:")
	else:
		cname = dbname
		cpass = dbpass
		
	conn = MySQLdb.connect(user=cname, host="localhost", passwd=cpass, use_unicode=True, charset='utf8')
	conn.converter[246]=float
	cursor = conn.cursor()
	
	if cname!="root":
		sql("use %s" % cname)

def sql(query, values=(), as_list=False, debug=False):
	if not cursor:
		connect()
	
	# execute
	if values!=():
		if isinstance(values, dict):
			values = dict(values)
		if debug:
			try:
				print(query % values)
			except TypeError:
				print([query, values])
		
		cursor.execute(query, values)
		
	else:
		cursor.execute(query)

	# scrub output if required
	ret = list(cursor.fetchall())
	if not as_list and cursor.description and ret:
		colnames = [i[0] for i in cursor.description]
		for i, r in enumerate(ret):
			ret[i] = _dict(zip(colnames, r))

	return ret

def commit():
	sql("commit")
	
def create_table(tablename, columns, primary_key, data):
	defs = [] 
	for i, c in enumerate(columns):
		ctype = guess_type([d[i] for d in data[1:10]])
		keys = ""
		if c==primary_key:
			keys = "primary key not null"
		defs.append("`%s` %s %s" % (c.lower().strip(), ctype, keys))
	sql("""drop table if exists `%s`""" % (tablename,))
	sql("""create table `%s` (%s) engine=InnoDB character set=utf8""" % (tablename, ", ".join(defs)))
	
def guess_type(data):
	is_int, is_float = True, True
	for d in data:
		if is_int:
			try:
				if not int(d)==float(d):
					is_int = False
			except ValueError, e:
				is_int = False
				
		if is_float:
			try:
				float(d)
			except ValueError, e:
				is_float = False
				
	if is_int:
		return "int(15)"
	elif is_float:
		return "decimal(18, 10)"
	else:
		return "varchar(255)"
					