# Components

## Front End

A web application would have a user interact with it and use a number of technologies such as _HTML, CSS, and JavaScript_ to do this.

1. **HTML (Hypertext Markup Language)** is a foundational aspect of web applications. It is a set of instructions or code that instructs a web browser on what to display and how to display it.
2. **CSS (Cascading Style Sheets)** in web applications describes a standard appearance, such as certain colors, types of text, and layouts.
3. **JS (JavaScript)** is part of a web application front end that enables more complex activity in the web browser. Whereas HTML can be considered a simple set of instructions on what to display, JavaScript is a more advanced set of instructions that allows choices and decisions to be made on what to display.


## Back End

The Back End of a web application is things you don’t see within a web browser but are important for the web application's functionality.

1. A **Database** is where information can be stored, modified, and retrieved. A web application may want to store and retrieve information about a visitor's preferences on what to show or not; this would be stored in a database.
2. There are many other **Infrastructure components** underpinning Web Applications, such as web servers, application servers, storage, various networking devices, and other software that support the web application.
3. **WAF (Web Application Firewall)** is an optional component for web applications. It helps filter out dangerous requests away from the Web Server and provides an element of protection.


## Uniform Resource Locator

A **Uniform Resource Locator (URL)** is a web address that lets you access all kinds of online content - whether it’s a webpage, a video, a photo, or other media. It guides your browser to the right place on the Internet.

URL has the following format:

```txt
http://auth_details@domin.com:port/path?id=val#fragment
```

1. **Schema:** The scheme is the protocol used to access the website. The most common are _HTTP (HyperText Transfer Protocol) and HTTPS (Hypertext Transfer Protocol Secure)._ HTTPS is more secure because it encrypts the connection, which is why browsers and cyber security experts recommend it. Websites often enforce HTTPS for added protection.
2. **Login Secrets:** Can be supplied to authenticate on the web server/host. Rarely used these days dur to obvious issues.
3. **Host/Domain:** The host or domain is the most important part of the URL because it tells you which website you’re accessing. Every domain name has to be unique and is registered through domain registrars. From a security standpoint, look for domain names that appear almost like real ones but have small differences (this is called typosquatting).
4. **Port:** The port number helps direct your browser to the right service on the web server. It’s like telling the server which doorway to use for communication. Port numbers range from 1 to 65,535, but the most common are 80 for HTTP and 443 for HTTPS.
5. **Path:** The path points to the specific file or page on the server that you’re trying to access. It’s like a roadmap that shows the browser where to go.
6. **Query String:** The query string is the part of the URL that starts with a question mark (?). It’s often used for things like search terms or form inputs. Since users can modify these query strings, it’s important to handle them securely to prevent attacks like injections, where malicious code could be added.
7. **Fragment:** The fragment starts with a hash symbol (#) and helps point to a specific section of a webpage—like jumping directly to a particular heading or table.