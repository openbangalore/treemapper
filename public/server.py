#!/usr/bin/env python

from __future__ import unicode_literals
import cgi, cgitb, os, sys, json
cgitb.enable()
sys.path.append("..")

import treemapper
import treemapper.user

response = "Hello"

def get_cgi_fields():
	from treemapper.utils import _dict
	cgi_fields = cgi.FieldStorage(keep_blank_values=True)
	form = _dict()
	
	for key in cgi_fields.keys():
		form[key] = cgi_fields.getvalue(key)
		
	return form
	
def get_cookies():
	import Cookie
	simplecookie = Cookie.SimpleCookie()
	cookies = {}
	if 'HTTP_COOKIE' in os.environ:
		c = os.environ['HTTP_COOKIE']
		simplecookie.load(c)
		for c in simplecookie.values():
			cookies[c.key] = c.value
		
	return cookies

if __name__=="__main__":
	form = get_cgi_fields()
	cookies = get_cookies()
	if form.cmd=="login":
		treemapper.user.login(form)
	elif form.cmd=="logout":
		treemapper.user.logout(cookies)
	elif form.cmd:
		treemapper.user = treemapper.user.verify_session(cookies)
	
	print "Content-type: text/html"
	if treemapper.response_cookies:
		print treemapper.response_cookies
	print
	print json.dumps(treemapper.response)