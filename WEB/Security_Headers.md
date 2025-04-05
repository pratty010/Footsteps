# Security Headers

HTTP Security Headers help improve the overall security of the web application by providing mitigations against attacks like Cross-Site Scripting (XSS), clickjacking, and others.

## Content-Security-Policy (CSP)

A CSP header is an additional security layer that can help mitigate against common attacks like _Cross-Site Scripting (XSS)._ Malicious code could be hosted on a separate website or domain and injected into the vulnerable website. A CSP provides a way for administrators to say what domains or sources are considered safe and provides a layer of mitigation to such attacks.

**Main Options:**

1. _default-src_ which specifies the default policy of self, which means only the current website.
2. _script-src_ which specifics the policy for where scripts can be loaded from, which is self along with scripts hosted on mentioned url.
3. _style-src_ which specifies the policy for where style CSS style sheets can be loaded from the current website (self)

```
Content-Security-Policy: default-src 'self'; script-src 'self' https://cdn.tryhackme.com; style-src 'self'
```

## Strict-Transport-Security (HSTS)

The HSTS header ensures that web browsers will always connect over HTTPS.

```
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
```

1. _max-age_: This is the expiry time in seconds for this setting.
2. _includeSubDomains_: An optional setting that instructs the browser to also apply this setting to all subdomains.
3. _preload_: This optional setting allows the website to be included in preload lists. Browsers can use preload lists to enforce HSTS before even having their first visit to a website.


## X-Content-Type-Options
The X-Content-Type-Options header can be used to instruct browsers not to guess the _MIME(Multipurpose Internet Mail Extensions (MIME) is an Internet standard that extends the format of email messages to support text in character sets other than ASCII, as well as attachments of audio, video, images, and application programs.)_ time of a resource but only use the Content-Type header.

## Referrer-Policy
This header controls the amount of information sent to the destination web server when a user is redirected from the source web server, such as when they click a hyperlink. The header is available to allow a web administrator to control what information is shared. 

**Common options:**
1. _no-referrer_: This completely disables any information being sent about the referrer.
2. _same-origin_: This policy will only send referrer information when the destination is part of the same origin. This is helpful when you want referrer information passed when hyperlinks are within the same website but not outside to external websites.
3. _strict-origin_: This policy only sends the referrer as the origin when the protocol stays the same. So, a referrer is sent when an HTTPS connection goes to another HTTPS connection.
4. _strict-origin-when-cross-origin_: This is similar to strict-origin except for same-origin requests, where it sends the full URL path in the origin header.

