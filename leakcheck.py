import requests
import sys
import platform
import os.path
import json

version = "1.0.0"

class LeakCheckAPI:
	'''
	User agent with software & system version
	'''
	headers = {"User-Agent": "PyLCAPI/{}, Python {} on {}".format(version, sys.version.split(" ")[0], platform.version())}

	'''
	Set initial variables
	'''
	def __init__(self):
		self.cfgname = "PyLCAPI.json"
		self.config = self.__getCfg()
		self.url = "https://leakcheck.net"
		self.type = "auto"
		self.query = ""
		self.endpoint = "/"
		self.key = self.config.get("key")
		self.proxy = self.config.get("proxy")

	'''
	Load or create a config file with an API key and proxy
	'''
	def __getCfg(self):
		if os.path.isfile(self.cfgname):
			with open(self.cfgname) as cfg:
				return json.load(cfg)
		else:
			with open(self.cfgname, 'w') as cfg:
				data = {'key': '', 'proxy': ''}
				json.dump(data, cfg)
				return data

	'''
	Function to set a secondary domain as main
	'''
	def use_mirror(self):
		self.url = "https://leakcheck.io"

	'''
	Function to set a proxy
	HTTP/HTTPS/SOCKS4/SOCKS5 supported
	Handled by requests[socks], requests[proxy]
	'''
	def set_proxy(self, proxy):
		self.proxy = proxy

	'''
	Function to set an endpoint
	/ for extended API, /public for public API
	Defaults to /
	'''
	def set_endpoint(self, endpoint):
		self.endpoint = endpoint

	'''
	Function to set an API key
	Public key can be also used here
	'''
	def set_key(self, key):
		assert (len(key) == 40), "set_key returned an exception: key is invalid, it must be 40 characters long"
		self.key = key

	'''
	Function to set a query type
	Defaults to auto
	'''
	def set_type(self, type):
		self.type = type

	'''
	Function to set a query
	'''
	def set_query(self, query):
		self.query = query

	'''
	Main function
	Sends a request to the server after everything else is prepared
	''' 
	def lookup(self):
		assert(self.key != ""), "Key is missing, use LeakCheckAPI.set_key() or specify it in config"
		assert(self.query != ""), "Query is missing, use LeakCheckAPI.set_query()"

		data = {'key': self.key, 'type': self.type, "check": self.query}
		request = requests.get(self.url + "/api" + self.endpoint,
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
			return result.get({'/': 'result', '/public': 'sources', '/hasbreached': 'breached'}[self.endpoint])
	
	'''
	Function to get your account limits
	'''
	def getLimits(self):
		assert (self.key != ""), "Key is missing, use LeakCheckAPI.set_key() or specify it in config"

		data = {'key': self.key, 'type': 'limits'}
		request = requests.get(self.url + "/api",
			data, 
			headers = self.headers,
			proxies = {'https': self.proxy}
		)

		assert (request.json().get("success") == True), request.json().get("error")
		
		return request.json().get("limits")

	'''
	Function to get your IP
	Useful when you link an IP for the first time
	'''
	def getIP(self):
		return requests.post(self.url + "/ip", 
			headers = self.headers, 
			proxies = {'https': self.proxy}
		).text

	'''
	Function to get software version
	Used in CLI
	'''
	def getVersion(self):
		return version