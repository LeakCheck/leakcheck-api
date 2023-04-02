# LeakCheck API

![LeakCheck <3 Python](https://i.imgur.com/G30V91m.png)
<p align="center">
<img alt="Discord" src="https://img.shields.io/discord/626798391162175528">
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/leakcheck">
<img alt="PyPI" src="https://img.shields.io/pypi/v/leakcheck">
<img alt="Uptime Robot ratio (30 days)" src="https://img.shields.io/uptimerobot/ratio/m787582856-3411c8623fccb7e99d3dfc1f">
<img alt="GitHub" src="https://img.shields.io/github/license/leakcheck/leakcheck-api">
</p>

## Dependencies:

 - Python >= 3.5
 - requests
 - tabulate
 - pysocks
 - setuptools
 - wheel

## Installation:

    pip3 install leakcheck

Or download tarball / `git clone` and execute

    python3 setup.py install

## First start:

To start working with this package you need to obtain personal API key [from here](https://leakcheck.net/api_s) and link IP address of your server or personal computer. It can be IPv6 as well as IPv4.

Public API can be used without IP linking.

Package automatically creates "PyLCAPI.json" file in the working directory on the first startup. Then, API key and/or proxy settings can be loaded from there.

## Using as a CLI:

    usage: leakcheck [-h] [--key KEY] [--proxy PROXY] [--type TYPE] [-lo] [-p]
                 query

    CLI version of LeakCheck API (v1.0.2). Licensed under MIT license

    positional arguments:
    query          What are we going to search?

    optional arguments:
    -h, --help     show this help message and exit
    --key KEY      Set an API key (taken from config by default)
    --proxy PROXY  Set proxy (supported: HTTP/HTTPS/SOCKS4/SOCKS5, default:
                    empty)
    --type TYPE    Set a type of the query (default: auto)
    -lo            Print lines only (default: False
    -p             Lookup privately (hashes data with SHA256, then truncates
                    hash to 24 characters; works for email, pass_email only,
                    default: False)
        
## Using as a library:

    from leakcheck import LeakCheckAPI
    
    # Initialising API class
    api = LeakCheckAPI()
    
    # API key setting
    api.set_key("YOUR_KEY")
    
    # Now we're ready to make our first request
    # A lookup type is detected automatically. To explicitly set it, see below
    result = api.lookup("example@example.com") # list of dicts

    # A request with the lookup type
    result = api.lookup("example@example.com", "email") # list of dicts

## Using a proxy:

    # HTTP/HTTPS/SOCKS4/SOCKS5 supported
    # Handled by requests[proxy], requests[socks]
    api.set_proxy("socks5://127.0.0.1:8123")

## Getting your IP:

    from leakcheck import LeakCheckAPI
    
    # Initialising API class
    api = LeakCheckAPI()
    
    ip = api.getIP() # string

## Getting your limits:

    from leakcheck import LeakCheckAPI
    
    # Initialising API class
    api = LeakCheckAPI()

    # API key setting
    api.set_key("YOUR_KEY")
    
    limits = api.getLimits() # dict

## Response errors:

| Error | Description |
|--|--|
| Missing params (key, check, type) | Some params haven't passed in the request |
| Invalid type | Type you provide is invalid |
| API Key is wrong | Key you provide is invalid |
| API Key is blocked | Your key is blocked due to some reasons, contact support |
| No license on this key | Key you provide does not have a license |
| Your query contains invalid characters | There are some forbidden characters in your query |
| Enter at least 3 characters to search | Query passed without minimal number of characters |
| Invalid email | E-mail type is specified, but your query is not a mail |
| IP linking is required | IPs are not linked or invalid |
| Not found | There are no results |
| Too many entries, try to concretize your query | You made a search that contains too many entries, try to search "alex@" instead of "alex" |

## Server Errors:
| Error | Description | Resolution |
|--|--|--|
| 429 Too Many Requests | Your server is sending too many automated requests. API is limited by 3 requests/second per one IP. | Try to reduce amount of sendings.
