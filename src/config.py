"""
config.py

This file keeps track of the number of requests the user has left in a given hour to avoid hitting
any rate limits, which result in temporary blocking of API access.
"""

REQUESTS_LEFT = 1000
LAST_TIME_QUERIED = ""
API_KEY = "D11hPzUZP5OlJBUqiyHVmXFDuDYfN6dT9zFiDU7v"