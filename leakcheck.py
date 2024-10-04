"""
Copyright (c) 2018-2024 LeakCheck Security Services LTD
Licensed under MIT license
Github: https://github.com/LeakCheck/leakcheck-api
Created with <3
"""
import requests
import json
import os
import sys
import platform

version = "2.0.0"

class LeakCheckAPI_v2:
    def __init__(self, api_key=None, base_url='https://leakcheck.io/api/v2'):  # Updated base URL for V2
        # Load API key and proxy from configuration file in the home directory
        self.api_key = os.getenv('LEAKCHECK_APIKEY') or api_key
        self.proxy = os.getenv('LEAKCHECK_PROXY')
        
        if not self.api_key or len(self.api_key) < 40:
            raise ValueError("API key is missing, empty, or invalid (must be at least 40 characters long) in the configuration file or provided parameter.")
        
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': self.api_key,  # API key is now required in the header
            "User-Agent": "PyLCAPI/{}, Python {} on {}".format(version, sys.version.split(" ")[0], platform.version())
        })
        # Set proxy if provided
        if self.proxy:
            self.set_proxy(self.proxy)

    def set_proxy(self, proxy):
        """
        Set a proxy for the session.

        :param proxy: Proxy URL (can be HTTP, HTTPS, or SOCKS5).
        """
        self.session.proxies.update({'http': proxy, 'https': proxy})

    def lookup(self, query, query_type=None, limit=100, offset=0):
        """
        Perform a lookup query.

        :param query: The main value to search (email, username, etc.).
        :param query_type: Type of query ('email', 'username', etc.). If missing, it will be detected automatically.
        :param limit: Limit number of results (maximum 1000).
        :param offset: Offset for the results (maximum 2500).
        :return: Parsed result from API.
        """
        if limit > 1000:
            raise ValueError("Limit cannot be greater than 1000.")
        if offset > 2500:
            raise ValueError("Offset cannot be greater than 2500.")

        endpoint = f"{self.base_url}/query/{query}"
        params = {
            'limit': limit,
            'offset': offset
        }
        # Adding optional parameters if provided
        if query_type:
            params['type'] = query_type

        try:
            response = self.session.get(endpoint, params=params)
        except requests.exceptions.RequestException as e:
            # Handle any request-related exceptions, including client and server errors
            raise ValueError(f"API responded with an error: {str(e)}") from e

        result = response.json()
        if not result.get('success', False):
            raise ValueError(f"API responded with an error: {result.get('error', 'Unknown error')}")

        return result.get('result')

class LeakCheckAPI_Public:
    def __init__(self, base_url='https://leakcheck.io/api/public'):  # Base URL for the public API
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "PyLCAPI/{}, Python {} on {}".format(version, sys.version.split(" ")[0], platform.version())
        })
        # Set proxy if provided
        self.proxy = None

    def set_proxy(self, proxy):
        """
        Set a proxy for the session.

        :param proxy: Proxy URL (can be HTTP, HTTPS, or SOCKS5).
        """
        self.session.proxies.update({'http': proxy, 'https': proxy})
        self.proxy = proxy

    def lookup(self, query):
        """
        Perform a public lookup query.

        :param query: The main value to search (email, email hash, or username).
        :return: Parsed result from API.
        """
        try:
            endpoint = f"{self.base_url}?check={query}"
            response = self.session.get(endpoint)
        except requests.exceptions.RequestException as e:
            # Handle any request-related exceptions, including client and server errors
            raise ValueError(f"API responded with an error: {str(e)}") from e

        result = response.json()
        if not result.get('success', False):
            raise ValueError(f"API responded with an error: {result.get('error', 'Unknown error')}")

        return result