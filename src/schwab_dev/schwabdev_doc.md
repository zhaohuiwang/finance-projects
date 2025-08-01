

#### Sensitive environment variables
```bash
cp .env.example .env
chmod 600 .env          # makes the file readable/writable only by the owner
echo "*.env" >> .gitignore
```
The 600 in `chmod 600 .env` is an octal representation of the permissions. In this notation, permissions are broken down for three categories: owner, group, and others.
- The first digit (6) represents the owner's permissions. In octal, 6 is the sum of 4 (read) and 2 (write), meaning the owner has both read and write access.
- The second digit (0) represents the group's permissions, meaning the group has no access.
- The third digit (0) represents "others'" permissions, meaning other users also have no access.


A **callback** function, in computer programming, is a function passed as an argument to another function, intended to be executed at a later point in time by that other function. The term "callback" arises from the idea that the function being passed is "called back" by the receiving function after some operation or event has occurred.

In a web application or Client-Server apps (client-server model), the **client** refers to the user's device (like a web browser on a computer or phone) that requests information and interacts with the application. The **server** is the computer that hosts the web application and provides the requested data and functionality. Essentially, the client asks for something, and the server provides it. 

In modern web integrations, **callback URL** (a.k.a redirect URI) provide a means (virtual communication channels) for applications to communicate asynchronously. A callback URL is an address that receives notification from server when a specific event occurs, and any computer in the Internet/private network can POST data to it.

In general web development, callback URLs are used in scenarios such as:
- OAuth Authentication: When a user logs into a service using a third-party account (like their Google account), the third-party service will redirect the user back to the application using a callback URL after successful authentication.
- Payment Gateway Processes: After completing a transaction, a payment service will redirect the user back to the merchant's website using a callback URL, often adding transaction details in the query parameters.
- Asynchronous Operations: When an API operation doesn't yield an immediate response, it might accept a callback URL to notify the calling application once the operation is complete.



### References
* [Schwabdev Documentation](https://tylerebowers.github.io/Schwabdev/?source=pages%2Fwelcome.html)
* [Github - Schwabdev scripts/docs/examples](https://github.com/tylerebowers/Schwabdev)

* [dotenv - Python Package Index (PyPI) repository](https://pypi.org/project/python-dotenv/)
* [schwabdev - PyPI repository](https://pypi.org/project/schwabdev/)

* [Hithub - schwab-py](https://github.com/alexgolec/schwab-py)
* [schwab-py - PyPI repository](https://pypi.org/project/schwab-py/)

* [Mozilla Developer Web Docs](https://developer.mozilla.org/en-US/docs/Learn_web_development)