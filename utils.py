# Utils.py
# Useful little functions that don't do much

from secrets import token_urlsafe

newLine = "\r\n"
nosniff = "X-Content-Type-Options: nosniff"

# MIME content types
cType = {"plain": "Content-Type: text/plain;charset=UTF-8",
         "txt": "Content-Type: text/plain;charset=UTF-8",
         "html": "Content-Type: text/html;charset=UTF-8",
         "css": "Content-Type: text/css;charset=UTF-8",
         "js": "Content-Type: text/javascript;charset=UTF-8",
         "png": "Content-Type: image/png",
         "jpg": "Content-Type: image/jpeg",
         "jpeg": "Content-Type: image/jpeg",
         "mp4": "Content-Type: video/mp4"}

# HTTP Status codes
status = {101: "101 Switching Protocols",
          200: "200 OK",
          201: "201 Created",
          204: "204 No Content",
          301: "301 Moved Permanently",
          304: "Not Modified",
          403: "403 Forbidden",
          404: "404 Not Found",
          500: "500 Internal Server Error"}


def contentLength(length):
    return "Content-Length: " + str(length)


# Creates HTTP header, complete with double CRLF at end.
# Must have status code as first header, but no requirements beyond that
def makeHeader(headers):
    header = "HTTP/1.1 "
    for line in headers:
        if isinstance(line, int):
            line = str(line)
        print(line, flush=True)

        header += (line + newLine)
    header += newLine

    return header.encode('ASCII')


def escapeHTML(byteString):
    byteString = byteString.replace(b'&', b"&amp;")
    byteString = byteString.replace(b'<', b"&lt;")
    byteString = byteString.replace(b'>', b"&gt;")

    return byteString


def template(file, replacements):
    for i in replacements:
        old = i[0]
        new = i[1]

        if isinstance(new, int):
            new = str(new)

        if isinstance(new, str):
            new = new.encode("UTF-8")

        if isinstance(old, str):
            old = old.encode("UTF-8")

        file = file.replace(old, new)
    return file


def token():
    return token_urlsafe(64).encode("UTF-8")
