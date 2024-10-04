# LeakCheck API Python Wrapper v2.0.0

This Python wrapper allows you to interact with the LeakCheck API for checking leaked data using the official API. It includes support for both the private (authenticated) API and the public (unauthenticated) API endpoints. This wrapper has been updated to work with API v2.
<p align="center">
<img alt="Discord" src="https://img.shields.io/discord/626798391162175528">
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/leakcheck">
<img alt="PyPI" src="https://img.shields.io/pypi/v/leakcheck">
<img alt="Uptime Robot ratio (30 days)" src="https://img.shields.io/uptimerobot/ratio/m787582856-3411c8623fccb7e99d3dfc1f">
<img alt="GitHub" src="https://img.shields.io/github/license/leakcheck/leakcheck-api">
</p>

## Features

- Lookup email addresses, usernames, and other identifiers against leaked databases.
- Supports both the **private API v2** (authenticated via API key) and the **public API**.
- Proxy support for both HTTP and HTTPS queries.
- Customizable request limits and offsets for paginated queries.

## Installation

You can install the wrapper using `pip`:

```bash
pip install leakcheck
```

## Usage

### Private API (Authenticated) - `LeakCheckAPI_v2`

To use the private API, you need an API key from LeakCheck. You can pass the API key directly or set it via an environment variable.

#### Example:

```python
from leakcheck_api import LeakCheckAPI_v2

# Initialize with API key (or set LEAKCHECK_APIKEY in environment variables)
api = LeakCheckAPI_v2(api_key='your_api_key_here')

# Perform a lookup
result = api.lookup(query="example@example.com", query_type="email", limit=100)

print(result)
```

#### Environment Variables

You can set the following environment variables for better flexibility:
- `LEAKCHECK_APIKEY`: Your API key for authentication (must be at least 40 characters long).
- `LEAKCHECK_PROXY`: Optional, to route your requests through a proxy.

#### Parameters for `lookup()`:

- `query`: The identifier to look up (email, username, etc.).
- `query_type`: (Optional) Specify the type of query (e.g., "email", "username"). If not provided, it will be auto-detected.
- `limit`: (Optional) Limit the number of results (maximum 1000, default is 100).
- `offset`: (Optional) Offset for the results (maximum 2500, default is 0).

#### Error Handling

- If the API key is invalid or not provided, an error will be raised.
- The method checks for valid `limit` and `offset` parameters.
- Handles exceptions related to network or request issues.

### Public API (Unauthenticated) - `LeakCheckAPI_Public`

The public API does not require authentication but offers limited access. You can use this for simple email or username queries.

#### Example:

```python
from leakcheck_api import LeakCheckAPI_Public

# Initialize without an API key
public_api = LeakCheckAPI_Public()

# Perform a public lookup
result = public_api.lookup(query="example@example.com")

print(result)
```

#### Parameters for `lookup()`:

- `query`: The identifier to look up (email, email hash, or username).

### Proxy Support

Both the private and public API wrappers support proxy configurations. You can set the proxy by calling `set_proxy()`:

```python
# Set proxy for private API
api.set_proxy("http://proxy.example.com:8080")

# Set proxy for public API
public_api.set_proxy("http://proxy.example.com:8080")
```

## Accepted Data Types for Lookup Queries

The **LeakCheck API v2** accepts the following data types for lookups. Some data types can be automatically detected, while others must be explicitly specified.

| **Query Type** | **Sample**                                 | **Notes**                                                                                  |
|----------------|--------------------------------------------|--------------------------------------------------------------------------------------------|
| **auto**       | `example@example.com`, `example`, `12345678`, `31c5543c1734d25c7206f5fd` | Automatically detects email, username, phone number, and hash. Other types must be explicit.|
| **email**      | `example@example.com`                      |                                                                                            |
| **domain**     | `gmail.com`                                |                                                                                            |
| **keyword**    | `example`                                  |                                                                                            |
| **username**   | `example`                                  |                                                                                            |
| **phone**      | `12063428631`                              |                                                                                            |
| **hash**       | `31c5543c1734d25c7206f5fd`                 | SHA256 hash of lower-cased email, can be truncated to 24 characters.                       |
| **phash**      | `31c5543c1734d25c7206f5fd`                 | SHA256 hash of password, can be truncated to 24 characters (Enterprise only).               |
| **origin**     | `example.com`                              | For Enterprise accounts only.                                                              |
| **password**   | `example`                                  | For Enterprise accounts only.                                                              |

### Example Queries:

```python
# Auto-detect type
result = api.lookup(query="example@example.com")

# Lookup by email
result = api.lookup(query="example@example.com", query_type="email")

# Lookup by domain
result = api.lookup(query="gmail.com", query_type="domain")

# Lookup by phone
result = api.lookup(query="12063428631", query_type="phone")

# Lookup by SHA256 hash
result = api.lookup(query="31c5543c1734d25c7206f5fd", query_type="hash")
```

### Auto-Detection of Query Types

If the `query_type` parameter is not provided, the API will attempt to auto-detect the type of query based on the input format. For instance, if the query looks like an email, the API will treat it as such.

## Error Handling and Returned Errors

The **LeakCheck API v2** provides detailed error messages in case something goes wrong with your query. These error messages are based on specific conditions. Below are common error codes and their corresponding descriptions:

| **Error Code** | **Description**                                                                 | **Notes**                                                                                  |
|----------------|---------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| **401**        | Missing X-API-Key                                                               | No API key provided in the request header.                                                 |
| **400**        | Invalid X-API-Key                                                               | The API key provided is invalid.                                                           |
| **400**        | Invalid type                                                                    | The `query_type` parameter is not valid.                                                   |
| **400**        | Invalid email                                                                   | The email format is incorrect.                                                             |
| **400**        | Invalid query                                                                   | The query format is invalid.                                                               |
| **400**        | Invalid domain                                                                  | The domain format is invalid.                                                              |
| **400**        | Too short query (< 3 characters)                                                | The query must be at least 3 characters long.                                              |
| **400**        | Invalid characters in query                                                     | The query contains invalid characters.                                                     |
| **429**        | Too many requests                                                               | You have exceeded the rate limit.                                                          |
| **403**        | Active plan required                                                            | A paid plan is required to make this request.                                              |
| **403**        | Limit reached                                                                   | You have reached your plan’s usage limit.                                                  |
| **422**        | Could not determine search type automatically                                   | The system was unable to automatically detect the query type, requiring an explicit type.   |

### Example of Error Handling in Code:

```python
try:
    result = api.lookup(query="example@example.com", query_type="email", limit=100)
    print(result)
except ValueError as e:
    print(f"An error occurred: {str(e)}")
```

The `lookup()` function raises a `ValueError` when the API returns an error. This makes it easy to handle and debug any issues that arise from invalid requests or API responses.

## API Endpoints

- **Private API Base URL (v2):** `https://leakcheck.io/api/v2`
- **Public API Base URL:** `https://leakcheck.io/api/public`

## Version

This wrapper supports **LeakCheck API v2**.

## License

This project is licensed under the MIT License.
