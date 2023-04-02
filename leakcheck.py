"""
Copyright (c) 2018-2023 LeakCheck Security Services LTD
Licensed under MIT license
Github: https://github.com/LeakCheck/leakcheck-api
Created with <3
"""

import requests
import sys
import platform
import os.path
import json

version = "1.0.2"

class LeakCheckAPI:
	'''
	User agent with software & system version
	'''
	headers = {"User-Agent": "PyLCAPI/{}, Python {} on {}".format(version, sys.version.split(" ")[0], platform.version())}

	'''
	Set initial variables
	'''
	def __init__(self):
		self.cfgname = ".pylcapi"
		self.cfgpath = os.path.expanduser('~') + "/" + self.cfgname
		self.config = self.__getCfg()
		self.url = "https://leakcheck.io"
		self.key = self.config.get("key")
		self.proxy = self.config.get("proxy")

	'''
	Load or create a config file with an API key and proxy
	* since 1.0.2: created inside a home folder instead of a working directory
	'''
	def __getCfg(self):
		if os.path.isfile(self.cfgpath):
			with open(self.cfgpath) as cfg:
				return json.load(cfg)
		else:
			with open(self.cfgpath, 'w') as cfg:
				data = {'key': '', 'proxy': ''}
				json.dump(data, cfg)
				return data

	'''
	Function to set a proxy
	HTTP/HTTPS/SOCKS4/SOCKS5 supported
	Handled by requests[socks], requests[proxy]
	'''
	def set_proxy(self, proxy):
		self.proxy = proxy

	'''
	Function to set an API key
	'''
	def set_key(self, key):
		assert (len(key) == 40), "A key is invalid, it must be 40 characters long"
		self.key = key

	'''
	Main function
	Sends a request to the server after everything else is prepared
	* since 1.0.1: query and lookup type now passed via function parameters
	''' 
	def lookup(self, query, lookup_type = "auto"):
		assert(self.key != ""), f"A key is missing, use LeakCheckAPI.set_key() or specify it in config ({self.cfgpath})"

		data = {'key': self.key, 'type': lookup_type, "check": query}
		request = requests.get(self.url + "/api",
			data, 
			headers = self.headers,
			proxies = {'https': self.proxy}
		)

		status_code = request.status_code
		assert (status_code == 200), f"Invalid response code ({status_code}) instead of 200"
		
		result = request.json()
		if result.get("success") == False:
			assert (result.get("error") == "Not found"), request.json().get("error")
			return []
		else:
			return result.get("result")
	
	'''
	Function to get your account limits
	'''
	def getLimits(self):
		assert (self.key != ""), f"A key is missing, use LeakCheckAPI.set_key() or specify it in config ({self.cfgpath})"

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