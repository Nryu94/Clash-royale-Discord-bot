import os
import ssl
import certifi
import clashapi

tokens = clashapi.cr(os.getenv("email"), os.getenv("password"))
ssl_context = ssl.create_default_context(cafile=certifi.where())
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer {}".format(tokens[0])
}