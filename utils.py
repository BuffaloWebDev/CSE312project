# Utils.py
# Useful little functions that don't do much

from secrets import token_urlsafe

newLine = "\r\n"


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
