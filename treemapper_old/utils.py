class _dict(dict):
	"""dict like object that exposes keys as attributes"""
	def __getattr__(self, key):
		return self.get(key)
	def __setattr__(self, key, value):
		self[key] = value
	def __getstate__(self): 
		return self
	def __setstate__(self, d): 
		self.update(d)
	def update(self, d):
		"""update and return self -- the missing dict feature in python"""
		super(_dict, self).update(d)
		return self
	def copy(self):
		return _dict(super(_dict, self).copy())

def get_csv_data(fname):
	import csv
	content = get_file_content(fname)
	if content:
		reader = csv.reader(content.splitlines())
		csvrows = [[col for col in row] for row in reader]
		return csvrows
	else:
		return None
		
def get_file_content(fname):
	if fname.startswith("."):
		return None
	with open(fname, "r") as datafile:
		content = datafile.read()
		for encoding in ["utf-8", "windows-1250", "windows-1252"]:
			try:
				content = unicode(content, encoding=encoding)
				break
			except UnicodeDecodeError, e:
				continue
			
			content = unicode(content, errors="ignore")
		return content.encode("utf-8")