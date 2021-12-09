# websocket.py

from hashlib import sha1
from base64 import b64encode

import parse
import utils
import database
import routes
import webserver
import accounts

all_sockets = []


def establish(handler, randKey):

    key = f"{randKey}258EAFA5-E914-47DA-95CA-C5AB0DC85B11".encode()
    accept_response = b64encode(sha1(key).digest()).strip().decode("ASCII")
    responseHeaders = ["Connection: Upgrade", "Upgrade: websocket", utils.nosniff,
                       f"Sec-WebSocket-Accept: {accept_response}"]
    handler.stitch(101, responseHeaders)
    serve(handler)


def serve(handler):

    all_sockets.append(handler)
    while True:
        incomingMessage = bytearray(handler.request.recv(2048).strip())
        if incomingMessage != b'':
            responseBody = getPayload(incomingMessage).decode()
            if responseBody == "Close Connection" or responseBody == b"Close Connection":
                #all_sockets.remove(handler)
                accounts.removeOnlineUser(handler)
                break
            if responseBody[-1:] != "}":
                responseBody += "}"
            if responseBody[-2:] != '"':
                responseBody = responseBody[:-2] + '"' + responseBody[-1:]

            responseBody = parse.decodeJSON(responseBody)
            if "msg" in responseBody:
                responseBody["msg"] = utils.escapeHTML(responseBody["msg"].encode()).decode()
            if "from" in responseBody:
                responseBody["from"] = utils.escapeHTML(responseBody["from"].encode()).decode()
            if "to" in responseBody:
                responseBody["to"] = utils.escapeHTML(responseBody["to"].encode()).decode()

            responseBody = parse.encodeJSON(responseBody)

            headers = prepareHeaders(responseBody)
            sendToAll(headers, responseBody)


def getPayload(incomingMessage):
    firstByte = incomingMessage[0]
    fin = firstByte >> 7
    rsv = firstByte & 0b01110000
    opcode = firstByte & 0b00001111

    if opcode == 8:
        return b"Close Connection"

    secondByte = incomingMessage[1]

    mask = secondByte >> 7
    payloadLen = secondByte & 0b01111111
    currByte = 2

    if payloadLen == 126:
        payloadLen = getNextBytes(incomingMessage, 2, currByte)
        currByte = 4
    elif payloadLen == 127:
        payloadLen = getNextBytes(incomingMessage, 4, currByte)
        currByte = 6

    payload = b""

    if type(payloadLen) == bytes:
        payloadLen = int.from_bytes(payloadLen, "big")

    if mask == 1:
        maskingKey = getNextBytes(incomingMessage, 4, currByte)
        currByte += 4
        remaining = payloadLen
        while remaining > 0:
            numBytes = min(remaining, 4)
            nextBytes = getNextBytes(incomingMessage, numBytes, currByte)
            currByte += numBytes
            remaining -= numBytes
            payload += bytes([x ^ y for x, y, in zip(nextBytes, maskingKey)])

    return payload


def prepareHeaders(payload):
    length = len(payload)
    responseHeader = bytearray()
    responseHeader.append(0b10000001)

    if length < 126:
        temp = length.to_bytes(1, 'big')
        responseHeader += temp
    elif length < 65536:
        responseHeader.append(0b01111110)
        responseHeader += (length.to_bytes(2, 'big'))
    else:
        responseHeader.append(0b01111111)
        responseHeader += (length.to_bytes(8, 'big'))

    return responseHeader


def sendToAll(headers, body):
    message = headers + body
    for socket in all_sockets:
        try:
            socket.request.sendall(message)
        except:
            pass


def getNextBytes(message, n, currByte):
    return message[currByte: currByte + n]
