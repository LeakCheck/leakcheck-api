import requests

class APIException(Exception):
	pass

class MissingParamsException(Exception):
	pass

class InvalidParamsException(Exception):
	pass

class InvalidStatusCodeException(Exception):
	pass

class LeakCheckAPI:

	version = "0.1.3"
	headers = {"User-Agent": "PyLCAPI/{}".format(version)}
	allowed_types = ["auto", "email", "mass", "login", "phone", "mc", "pass_email", "domain_email", "pass_login", "pass_phone", "pass_mc", "hash"]

	def __init__(self):
		self.url = "https://leakcheck.net"
		self.key = ""
		self.proxy = ""
		self.type = ""
		self.query = ""

	def set_proxy(self, proxy):
		self.proxy = proxy

	def set_key(self, key):
		if len(key) != 40:
			raise InvalidParamsException("set_key returned an exception: key is invalid, it must be 40 characters long")
		self.key = key

	def set_type(self, type):
		if type not in self.allowed_types:
			raise InvalidParamsException("set_type returned an exception: type is invalid")
		self.type = type

	def set_query(self, query):
		self.query = query

	def use_mirror(self):
		self.url = "https://leakcheck.io"

	def lookup(self, with_sources = 0):
		if self.key is "":
			raise MissingParamsException("Key is missing, use LeakCheckAPI.set_key()")
		elif self.type is "":
			raise MissingParamsException("Type is missing, use LeakCheckAPI.set_type()")
		elif self.query is "":
			raise MissingParamsException("Query is missing, use LeakCheckAPI.set_query()")
		data = {'key': self.key, 'type': self.type, "check": self.query, "with_sources": with_sources}
		request = requests.get(self.url + "/api/",
			data, 
			headers = self.headers,
			proxies = {'https': self.proxy}
		)
		status_code = request.status_code
		if status_code != 200:
			raise InvalidStatusCodeException("lookup returned an exception: invalid response code ({}) instead of 200".format(status_code))
		else:
			result = request.json()
			if result.get("success") == False:
				if result.get("error") == "Not found":
					return []
				else:
					raise APIException(request.json().get("error"))
			else:
				return result.get("result")
			
	def getLimits(self):
		if self.key == "":
			raise MissingParamsException("Key is missing, use LeakCheckAPI.set_key()")
			data = {'key': self.key, 'type': 'limits'}
			request = requests.get(self.url + "/api/",
				data, 
				headers = self.headers,
				proxies = {'https': self.proxy}
				)
			if request.json().get("success") == False:
				raise APIException(request.json().get("error"))
			else:
				return request.json().get("limits")

	def getIP(self):
		return requests.post(self.url + "/ip", 
			headers = self.headers, 
			proxies = {'https': self.proxy}
		).text