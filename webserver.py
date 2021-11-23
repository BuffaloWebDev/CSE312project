import socketserver

import utils
import routes
import parse

newline = "\r\n"
skipLine = "\r\n\r\n"



class WebServer(socketserver.StreamRequestHandler):


    def send(self, message):
        self.request.sendall(message)

    def stitch(self, headerList, body=b''):
        if isinstance(body, int):
            body = str(body)
        if isinstance(body, str):
            body = body.encode()
        print(headerList, flush=True)

        response = utils.makeHeader(headerList)
        print(response, flush=True)
        response += body
        self.send(response)


    def redirect(self, location):
        responseHeaders = [utils.status[301], "Location: " + location, utils.contentLength(0)]
        self.stitch(responseHeaders)


    def sendMessage(self, msg, code, contentType):
        responseHeaders = [utils.status[code], utils.cType[contentType], utils.nosniff, utils.contentLength(len(msg))]
        self.stitch(responseHeaders, msg)


    def notFound(self):
        self.sendMessage(b"Content not found", 404, "plain")


    def denied(self):
        self.sendMessage(b"Request has been denied", 403, "plain")


    def handle(self):
        # Start of parsing. Receive request and put headers into dict

        message = self.request.recv(1024)

        if len(message) == 0:
            return

        splitter = message.find(skipLine.encode())

        headers = message[:splitter].decode("ASCII").split(newline)
        request = headers.pop(0).split()
        requestHeaders = parse.requestHeaders(headers)

        requestBody = message[splitter:]

        requestType = request[0]
        requestPath = request[1]

        routes.route(requestHeaders, requestBody, requestType, requestPath, self)


if __name__ == "__main__":
    address = ("0.0.0.0", 8000)
    server = socketserver.ThreadingTCPServer(address, WebServer)
    server.serve_forever()
