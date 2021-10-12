import socketserver
import data
import utils

tokens = []

class webServer(socketserver.StreamRequestHandler):
    def handle(self):

         # Stich header and body together, then send.
        def send(headers, body):
            response = utils.makeHeader(headers)
            response += body
            self.request.sendall(response)

        def redirect(location):
                responseHeaders, responseBody = [data.status[301], "Location: " + location, utils.contentLength(0)], b''
                send(responseHeaders, responseBody)

        def notFound():
                responseBody = b'Content not found'
                responseHeaders = [data.status[404], data.cType["plain"], data.nosniff, utils.contentLength(len(responseBody))]
                send(responseHeaders, responseBody)

        def denied():
                responseBody = b"Request has been denied"
                responseHeaders = [data.status[403], data.cType["plain"], data.nosniff, utils.contentLength(len(responseBody))]
                send(responseHeaders, responseBody)


        requestHeaders = dict()

        message = self.request.recv(1024).strip().split(data.bCRLF + data.bCRLF)
        headers = message[0].decode("UTF-8").split(data.CRLF)

        if len(message) > 1:
            requestBody = message[1]
        
        request = headers.pop(0).split()
        
        for header in headers:
            header = header.split(":")
            if len(header) == 2:
                header[1] = header[1].split(";")
                value = [x.strip() for x in header[1]]
                requestHeaders[header[0]] = value

        requestType = request[0]
        requestPath = request[1]

        if requestType == "GET":            
            responseHeaders = [data.status[200]]
                
            if requestPath == "/": # Display home

                with open("home.html", "rb") as index:
                    responseBody = index.read()

                xsrfToken = utils.token()
                tokens.append(xsrfToken)
                responseBody = utils.template(responseBody, "{{XSRFToken}}", xsrfToken)
                    
                responseHeaders.append(data.cType["html"])

            elif requestPath[1:] in data.files: # files in root folder
                with open(requestPath[1:], "rb") as requestedFile:
                    responseBody = requestedFile.read()
                    
                extension = requestPath[1:].split(".")[-1]
                responseHeaders.append(data.cType[extension])

                xsrfToken = utils.token()
                tokens.append(xsrfToken)
                responseBody = utils.template(responseBody, "{{XSRFToken}}", xsrfToken)

            elif (requestPath[:7] == "/image/" and requestPath[7:] in data.images) or (requestPath[:15] == "/image/uploads/"): # Any jpegs in /image folder
                with open(requestPath[1:], "rb") as requestedImage:
                    responseBody = requestedImage.read()
                responseHeaders.append(data.cType["jpg"])

            else: # Content not found
                responseBody = b'Content not found'
                responseHeaders = [data.status[404], data.cType["plain"]]

            # If sending content, always add data.nosniff and content-length tag
            responseHeaders.extend([data.nosniff, utils.contentLength(len(responseBody))])            
            send(responseHeaders, responseBody)
            
        elif requestType == "POST":
            length = int(requestHeaders['Content-Length'][0])
            
            delimiter = b"--" + bytes(requestHeaders['Content-Type'][1][10:], encoding = "utf-8")

            while len(requestBody) < length:
                requestBody += self.request.recv(2048)
                
            requestBody = requestBody[(2*len(data.CRLF)):].split(delimiter)
            requestBody = list(filter(None, requestBody))
            
            formData = [x.split(data.bCRLF + data.bCRLF) for x in requestBody]
            form = dict()

            for item in formData:
                # Very descriptive variables
                item = [x.strip() for x in item]
                if item == [b'--']:
                    continue
                temp = item[0].split(b":")
                temp[1] = temp[1].split(b";")
                temp[1][1] = temp[1][1].split(b"=")
                name = temp[1][1][1].replace(b'"', b'')
                name = utils.escapeHTML(name).decode("UTF-8")

                content = item[1].rstrip().replace(b"\r\n-", b"")
                form[name] = content

            token = form['xsrf_token']
            if token not in tokens:
                denied()
                    

        else:
            print("Error, request type not recognized")
        



if __name__ == "__main__":
    address = ("localhost", 8001)
    server = socketserver.TCPServer(address, webServer)
    server.serve_forever()
