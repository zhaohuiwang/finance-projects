

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

### References
* [Schwabdev Documentation](https://tylerebowers.github.io/Schwabdev/?source=pages%2Fwelcome.html)
* [Github - Schwabdev scripts/docs/examples](https://github.com/tylerebowers/Schwabdev)

* [dotenv - Python Package Index (PyPI) repository](https://pypi.org/project/python-dotenv/)
* [schwabdev - PyPI repository](https://pypi.org/project/schwabdev/)

* [Hithub - schwab-py](https://github.com/alexgolec/schwab-py)
* [schwab-py - PyPI repository](https://pypi.org/project/schwab-py/)