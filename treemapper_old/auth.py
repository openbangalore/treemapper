import treemapper, database, requests, json, os

def login(form, cookies):
	# The request has to have an assertion for us to verify
	if 'assertion' not in form:
		raise Exception, e

	# Send the assertion to Mozilla's verifier service.
	data = {
		'assertion': form.assertion, 
		'audience': os.environ["HTTP_HOST"]
	}
	resp = requests.post('https://verifier.login.persona.org/verify', data=data, verify=True)

	# Did the verifier respond?
	if resp.ok:
		# Parse the response
		verification_data = json.loads(resp.content)

		# Check if the assertion was valid
		treemapper.response.status = verification_data['status']
		
		if verification_data['status'] == 'okay':
			# Log the user in by setting a secure session cookie
			make_session(verification_data['email'])
			
def make_session(email):
	import hashlib, time, Cookie
	sid = hashlib.sha224(str(time.time())).hexdigest()
	
	if not database.sql("""select email from user where email=%s""", email):
		database.sql("""insert into `user` (email) values (%s)""", email)
	
	database.sql("""insert into `session` (id, email) values (%s, %s)""", (sid, email))
	
	treemapper.response_cookies = Cookie.SimpleCookie()	
	treemapper.response_cookies["sid"] = sid
	treemapper.response_cookies["email"] = email

	database.commit()

def verify(form, cookies):
	sid = cookies.get("sid")
	if sid:
		session = database.sql("""select email from `session` where id=%s""", sid)
		if session:
			if form.cmd == "verify":
				treemapper.response.session_status = "okay"
				treemapper.response.session_email = session[0].email
			else:
				return session[0].email

def logout(form, cookies):
	import Cookie
	sid = cookies.get("sid")
	if sid:
		database.sql("""delete from session where id=%s""", sid)

		treemapper.response_cookies = Cookie.SimpleCookie()	
		treemapper.response_cookies["sid"] = ""
		treemapper.response_cookies["email"] = ""

		database.commit()