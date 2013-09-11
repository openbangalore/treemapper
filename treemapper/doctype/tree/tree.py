# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd.
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.utils.file_manager import save_file

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl
		
	def validate(self):
		import base64, shutil
		
		for img_name in ("tree_image", "leaf_image"):
			if self.doc.fields.get(img_name) and len( self.doc.fields.get(img_name)) > 100:
				setattr(self, img_name, base64.b64decode(self.doc.fields.get(img_name)))
				self.doc.fields[img_name] = None
				
	def on_update(self):
		if getattr(self, "tree_image", None):
			webnotes.conn.set_in_doc(self.doc, "tree_image", save_file(self.doc.name + "-tree", 
				self.tree_image, self.doc.doctype, self.doc.name).fname)

		if getattr(self, "leaf_image", None):
			webnotes.conn.set_in_doc(self.doc, "leaf_image", save_file(self.doc.name + "-leaf", 
				 self.leaf_image, self.doc.doctype, self.doc.name).fname)
