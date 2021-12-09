# parse.py
# All your parsing and encoding needs

import utils
from json import loads, dumps

newLine = "\r\n"
skipLine = "\r\n\r\n"


def form(requestBody, delimiter):
    requestBody = requestBody[(2 * len(newLine)):].split(delimiter)
    requestBody = list(filter(None, requestBody))

    formData = [x.split(skipLine.encode()) for x in requestBody]
    parsedForm = dict()

    for item in formData:
        # Very descriptive variables
        item = [x.strip() for x in item]
        if item == [b'--'] or item == [b'-']:
            continue
        temp = item[0].split(b":")
        temp[1] = temp[1].split(b";")
        temp[1][1] = temp[1][1].split(b"=")
        name = temp[1][1][1].replace(b'"', b'')
        name = utils.escapeHTML(name).decode("UTF-8")

        content = item[1].rstrip().replace(b"\r\n-", b"")
        parsedForm[name] = content

    return parsedForm


def requestHeaders(headers):
    requestHeaders = {}
    for header in headers:
        header = header.split(":")
        if len(header) == 2:
            header[1] = header[1].split(";")
            value = [x.split(",") for x in header[1]]
            temp = []
            for y in value:
                for z in y:
                    temp.append(z.strip())
            requestHeaders[header[0]] = temp
    return requestHeaders


def URLEncoding(pairs):
    query = dict()
    for pair in pairs:
        pair = pair.split("=")
        query[pair[0]] = pair[1].split("+")

    return query


def encodeJSON(value):
    return dumps(value).encode("UTF-8")


def decodeJSON(value):
    temp = loads(value)
    return temp


def userToDict(user):
    return rowToDict(user, ["id", "email", "username"])


def rowToDict(row, headers):
    return {headers[i]: row[i] for i in range(len(row))}

def cookies(cookieHeader):
    if cookieHeader is not None:
        cookies = [cookie.split("=") for cookie in cookieHeader]
        return {cookie[0]:cookie[1] for cookie in cookies if len(cookie) == 2}