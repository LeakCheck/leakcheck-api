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

## Using:

To start working with this package you need to obtain personal API key [from here](https://leakcheck.net/api_s) and link IP address of your server or personal computer. It can be IPv6 as well as IPv4.

## Using mirror or proxy:

    # Using proxy if it's required due to various reasons
    api.set_proxy("socks5://127.0.0.1:8123")
    
    # Using leakcheck.io mirror instead of leakcheck.net if it's banned in your country or you're expecting difficulties with connection
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

## Making requests:

    from leakcheck import LeakCheckAPI
    
    # Initialising API class
    api = LeakCheckAPI()
    
    # API key setting
    api.set_key("YOUR_KEY")
    
    # Type setting
    # Can be used with these values: auto, email, mass, login, phone, mc, pass_email, domain_email, pass_login, pass_phone, pass_mc, hash
    api.set_type("email")
    
    # Search setting
    api.set_query("leakcheck@aol.com")
    
    # Query prepared. Now we're ready to make our first request
    # Use with_sources=1 as an argument to see sources of breached entries
    result = api.lookup() # list

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
| Too many entries, try to concretize your query | You made a search that contains too many entries, try to search "alex@" instead of "alex" (for example) |

## Server Errors:
| Error | Description | Resolution |
|--|--|--|
| 429 Too Many Requests | Your server is sending too many automated requests. API is limited by 3 requests/second per one IP. | Try to reduce amount of sendings.