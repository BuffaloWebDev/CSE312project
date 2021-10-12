# Utils.py
# Useful little functions that don't do much

import data
import secrets

def contentLength(length):
    return "Content-Length: " + str(length)

# Creates HTTP header, complete with double CRLF at end. Must have status code as first header, but no requirements beyond that
def makeHeader(headers):
    header = data.version
    for line in headers:
        header += (line + data.CRLF)
    header += data.CRLF

    return header.encode('ASCII')

def escapeHTML(byteString):
    byteString = byteString.replace(b'&', b"&amp;")
    byteString = byteString.replace(b'<', b"&lt;")
    byteString = byteString.replace(b'>', b"&gt;")

    return byteString

def template(file, old, new):
    file = file.replace(old.encode("UTF-8"), new)
    return file

def token():
    return secrets.token_urlsafe(64).encode("UTF-8")

