#!/usr/bin/env python

from __future__ import unicode_literals
import cgi, cgitb, os
cgitb.enable()

response = "Hello"

if __name__=="__main__":
	print "Content-type: text/html"
	print
	print response