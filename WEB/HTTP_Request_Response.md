# HTTP Messages

**HTTP messages** are packets of data exchanged between a user (the client) and the web server.

There are two types of HTTP messages:
1. _HTTP Requests:_ Sent by the user to trigger actions on the web application.
2. _HTTP Responses:_ Sent by the server in response to the user’s request.


## Message Components

1. **Start Line:** The start line is like the introduction of the message. It tells you what kind of message is being sent—whether it's a request from the user or a response from the server. This line also gives important details about how the message should be handled.
2. **Headers:** Headers are made up of key-value pairs that provide extra information about the HTTP message. They give instructions to both the client and the server handling the request or response.
3. **Empty Line:** The empty line is a little divider that separates the header from the body. It’s essential because it shows where the headers stop and where the actual content of the message begins.
4. **Body:** The body is where the actual data is stored. 
   1. In a request, the body might include data the user wants to send to the server (like form data). 
   2. In a response, it’s where the server puts the content that the user requested (like a webpage or API data).


## HTTP Requests

An _HTTP request_ is what a user sends to a web server to interact with a web application and make something happen. Since these requests are often the first point of contact between the user and the web server.

### Request Line

The request line (or start line) is the first part of an HTTP request and tells the server what kind of request it’s dealing with. It has three main parts: _the HTTP method, the URL path, and the HTTP version_.

**Format:**

```
METHOD /path HTTP/version
```

1. **Methods:** The HTTP method tells the server what action the user wants to perform on the resource identified by the URL path. 
   1. _GET_: Used to fetch data from the server without making any changes.
   2. _POST_: Sends data to the server, usually to create or update something.
   3. _PUT_: Sends data to the server, usually to create or update something.
   4. _DELETE_: Sends data to the server, usually to delete something.
   5.  _HEAD_: Works like GET but only retrieves headers, not the full content.
   6.  _OPTIONS_: Tells you what methods are available for a specific resource, helping clients understand what they can do with the server.
   7.  _TRACE_: Similar to OPTIONS, it shows which methods are allowed, often for debugging. Many servers disable it for security reasons.
   8. _PATCH_: Sends data to the server, usually to patch something par tof the service. Updates part of a resource. It’s useful for making small changes without replacing the whole thing, but always validate the data to avoid inconsistencies.
   9. _CONNECT_: Used to create a secure connection, like for HTTPS.
2.  **URL Path:** The URL path tells the server where to find the resource the user is asking for.
3.  **HTTP Version:** The HTTP version shows the protocol version used to communicate between the client and server.
    1.  _HTTP/0.9 (1991):_ The first version, only supported GET requests.
    2.  _HTTP/1.1 (1997):_ Brought persistent connections, chunked transfer encoding, and better caching. It’s still widely used today.
    3. _HTTP/2 (2015):_ Introduced features like multiplexing, header compression, and prioritisation for faster performance.
    4. _HTTP/3 (2022):_ Built on HTTP/2, but uses a new protocol (QUIC) for quicker and more secure connections.


### HEADERS

Request Headers allow extra information to be conveyed to the web server about the request. 

**Common Headers:**
1. _Host_: Specifies the name of the web server the request is for.
2. _User-Agent_: Shares information about the web browser the request is coming from.
3. _Referer_: Indicates the URL from which the request came from.
4. _Cookie_: Information the web server previously asked the web browser to store is held in cookies.
5. _Content-Type_: Describes what type or format of data is in the request.

### BODY

In HTTP requests such as POST and PUT, where data is sent to the web server as opposed to requested from the web server, the data is located inside the HTTP Request Body. The formatting of the data can take many forms, but some common ones are _URL Encoded, Form Data, JSON, or XML_.

**Common Content Types:** 
1. **URL Encoded:** _application/x-www-form-urlencoded_: A format where data is structured in pairs of key and value where (`key=value`). Multiple pairs are separated by an (&) symbol, such as `key1=value1&key2=value2`. Special characters are percent-encoded.
2. **Form Data:** _multipart/form-data_: Allows multiple data blocks to be sent where each block is separated by a boundary string. The boundary string is the defined header of the request itself. This type of formatting can be used to send binary data, such as when uploading files or images to a web server.
3. **JSON:** _application/json_: In this format, the data can be sent using the JSON (JavaScript Object Notation) structure. Data is formatted in pairs of name : value. Multiple pairs are separated by commas, all contained within curly braces { }.
4. **XML:** _application/xml_: In XML formatting, data is structured inside labels called tags, which have an opening and closing. These labels can be nested within each other. 


## HTTP Responses

The server sends back an _HTTP response_ to let you know whether your request was successful or something went wrong. These responses include a status code and a short explanation (called the Reason Phrase) that gives insight into how the server handled your request.

### Status Line

The first line in every HTTP response is called the Status Line. It gives you three key pieces of info:

1. **HTTP Version:** This tells you which version of HTTP is being used.
2. **Status Code:** A three-digit number showing the outcome of your request.
3. **Reason Phrase:** A short message explaining the status code in human-readable terms.

**Status Code and Reason Phrases:**
1. _Informational Responses (100-199)_ 
   1. These codes mean the server has received part of the request and is waiting for the rest. It’s a "keep going" signal.
   2. Common: 101(Continue)
2. _Successful Responses (200-299)_
   1. These codes mean everything worked as expected. The server processed the request and sent back the requested data. 
   2. Common: 200(OK)
3. _Redirection Messages (300-399)_
   1. These codes tell you that the resource you requested has moved to a different location, usually providing the new URL.
   2. Common: 301(Moved Permanently)
4. _Client Error Responses (400-499)_
   1. These codes indicate a problem with the request. Maybe the URL is wrong, or you’re missing some required info, like authentication.
   2. Common: 404(Not Found)
5. _Server Error Responses (500-599)_
   1. These codes mean the server encountered an error while trying to fulfil the request. These are usually server-side issues and not the client’s fault.
   2. Common: 500(Internal Server Error)


### HEADERS

Basically key-value pairs. These headers provide important info about the response and tell the client (usually the browser) how to handle it.

**Common Headers:**
1. _Content-Type_: It tells the client what kind of content it’s getting, like whether it’s HTML, JSON, or something else. It also includes the character set (like UTF-8) to help the browser display it properly.
2. _Date_: This header shows the exact date and time when the response was generated by the server. for Timing attacks.
3. _Server_: This header shows what kind of server software is handling the request. It’s good for debugging, but it can also reveal server information that might be useful for attackers, so many people remove or obscure this one.
4. _Content-Length_: Tells us about the length of the response body or content.
5. _Set-Cookie_: This one sends cookies from the server to the client, which the client then stores and sends back with future requests. To keep things secure, make sure cookies are set with the **HttpOnly flag (so they can’t be accessed by JavaScript) and the Secure flag (so they’re only sent over HTTPS)**.
6. _Cache-Control_: This header tells the client how long it can cache the response before checking with the server again. It can also prevent sensitive info from being cached if needed **(using no-cache).**
7. _Location_: This one’s used in redirection (3xx) responses. It tells the client where to go next if the resource has moved. If users can modify this header during requests, be careful to validate and sanitize it.

### BODY

The HTTP response body is where the actual data lives—things like HTML, JSON, images, etc., that the server sends back to the client. To prevent injection attacks like Cross-Site Scripting (XSS), always sanitise and escape any data (especially user-generated content) before including it in the response.