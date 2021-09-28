# LeakCheck API

## Dependencies:

 - Python >= 3.5
 - requests >= 2.23.0
 - pysocks >= 1.7.1
 - setuptools >= 46.1.3
 - wheel >= 0.34.2

## Installation:

    pip3 install leakcheck

Or download tarball / `git clone` and execute

    python3 setup.py install

## First start:

To start working with this package you need to obtain personal API key [from here](https://leakcheck.net/api_s) and link IP address of your server or personal computer. It can be IPv6 as well as IPv4.

Public API can be used without API linking.

Package automatically creates "PyLCAPI.json" file in the working directory on the first startup. Then, API key and/or proxy settings can be loaded from there.

## Using as a CLI:

    usage: leakcheck [-h] [--key KEY] [-m] [--proxy PROXY] [--endpoint ENDPOINT]
                 [--type TYPE] [-lo] [-p]
                 query

    CLI version of LeakCheck API (v1.0.0). Licensed under MIT license

    positional arguments:
        query                What are we going to search?

    optional arguments:
        -h, --help           show this help message and exit
        --key KEY            Set an API key (taken from config by default)
        -m                   Use mirror (leakcheck.io instead of leakcheck.net, default: False)
        --proxy PROXY        Set proxy (supported: HTTP/HTTPS/SOCKS4/SOCKS5, default: empty)
        --endpoint ENDPOINT  Set an endpoint (default: /)
         --type TYPE          Set a type of the query (default: auto)
        -lo                  Print lines/sources only (useful if you process them later or save, default: False)
        -p                   Lookup privately (hashes data with SHA256, then truncates hash to 24 characters; works for email, pass_email only, default: False)
        
## Using as a library:

    from leakcheck import LeakCheckAPI
    
    # Initialising API class
    api = LeakCheckAPI()
    
    # API key setting
    api.set_key("YOUR_KEY")
    
    # Type setting
    api.set_type("email")
    # Or login / mass / etc

    # Search setting
    api.set_query("example@example.com")
    
    # Query prepared. Now we're ready to make our first request
    result = api.lookup() # list of dicts

## Using mirror or proxy:

    # HTTP/HTTPS/SOCKS4/SOCKS5 supported
    # Handled by requests[proxy], requests[socks]
    api.set_proxy("socks5://127.0.0.1:8123")
    
    # This will use leakcheck.io instead of leakcheck.net
    api.use_mirror()

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