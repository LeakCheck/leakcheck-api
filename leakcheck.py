import requests

class LeakCheckAPI:

	version = "0.1.3f"
	headers = {"User-Agent": "PyLCAPI/{}".format(version)}
	allowed_types = ["auto", "email", "mass", "login", "phone", "mc", "pass_email", "domain_email", "pass_login", "pass_phone", "pass_mc"]

	def __init__(self):
		self.url = "https://leakcheck.net"
		self.key = ""
		self.proxy = ""
		self.type = ""
		self.query = ""

	def set_proxy(self, proxy):
		self.proxy = proxy

	def set_key(self, key):
		assert (len(key) == 40), "set_key returned an exception: key is invalid, it must be 40 characters long"
		self.key = key

	def set_type(self, type):
		assert (type in self.allowed_types), "set_type returned an exception: type is invalid"
		self.type = type

	def set_query(self, query):
		self.query = query

	def use_mirror(self):
		self.url = "https://leakcheck.io"

	def lookup(self, with_sources = 0):
		assert(self.key != ""), "Key is missing, use LeakCheckAPI.set_key()"
		assert(self.type != ""), "Type is missing, use LeakCheckAPI.set_type()"
		assert(self.query != ""), "Query is missing, use LeakCheckAPI.set_query()"

		data = {'key': self.key, 'type': self.type, "check": self.query, "with_sources": with_sources}
		request = requests.get(self.url + "/api/",
			data, 
			headers = self.headers,
			proxies = {'https': self.proxy}
		)
		status_code = request.status_code
		assert (status_code == 200), "lookup returned an exception: invalid response code ({}) instead of 200".format(status_code)
		
		result = request.json()
		if result.get("success") == False:
			assert (result.get("error") == "Not found"), request.json().get("error")
			return []
		else:
			return result.get("result")
			
	def getLimits(self):
		assert (self.key != ""), "Key is missing, use LeakCheckAPI.set_key()"

		data = {'key': self.key, 'type': 'limits'}
		request = requests.get(self.url + "/api/",
			data, 
			headers = self.headers,
			proxies = {'https': self.proxy}
		)

		assert (request.json().get("success") == True), request.json().get("error")
		
		return request.json().get("limits")

	def getIP(self):
		return requests.post(self.url + "/ip", 
			headers = self.headers, 
			proxies = {'https': self.proxy}
		).text