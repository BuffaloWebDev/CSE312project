# data.py
# Constants

version = "HTTP/1.1 "

# HTTP Status codes
status = {  200   : "200 OK",
            301   : "301 Moved Permanently",
            304   : "Not Modified",
            403   : "403 Forbidden",
            404   : "404 Not Found",
            500   : "500 Internal Server Error"}

# MIME content types
cType = {   "plain" : "Content-Type: text/plain;charset=UTF-8",
            "txt"   : "Content-Type: text/plain;charset=UTF-8",
            "html"  : "Content-Type: text/html;charset=UTF-8",
            "css"   : "Content-Type: text/css;charset=UTF-8",
            "js"    : "Content-Type: text/javascript;charset=UTF-8",
            "png"   : "Content-Type: image/png",
            "jpg"   : "Content-Type: image/jpeg",
            "jpeg"  : "Content-Type: image/jpeg",
            "mp4"   : "Content-Type: video/mp4"}

# All user accessible files in root directory
files = []

# User accessible files in /image directory
images = []

nosniff = "X-Content-Type-Options: nosniff"

CRLF = "\r\n"
bCRLF = b"\r\n"
