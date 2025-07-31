#On mac, Path to venv: /Users/zhaohuiwang/dev/venvs/uv-venvs/pytorch/.venv/bin/python

import schwabdev #import the package

client = schwabdev.Client('Your app key', 'Your app secret')  #create a client

print(client.account_linked().json()) #make api calls



# https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv

# The function `load_dotenv`` loads environment variables from a .env file into your application's environment, making them accessible via os.getenv() or os.environ.By default, it looks for .env in the current directory.
load_dotenv()
load_dotenv(".env")
# You can specify a different path
load_dotenv(".path/to/.env")


from dotenv import dotenv_values
from easydict import EasyDict

# The function `dotenv_values` works more or less the same way as `load_dotenv`, except it doesn't touch the environment, it just returns a dict with the values parsed from the .env file.
config = dotenv_values(".env")  
# config = {"USER": "foo", "EMAIL": "foo@example.org"}
cfg = EasyDict(config)
print(cfg.USER) # foo

import os
import dotenv
import schwabdev

dotenv.load_dotenv()
client = schwabdev.Client(os.getenv("SCHWAB_APP_KEY"), os.getenv("SCHWAB_APP_SECRET"))


# SSL (Secure Sockets Layer) certificates, also known as TLS (Transport Layer Security) certificates
import certifi
print(certifi.where())
# /Users/zhaohuiwang/dev/venvs/uv-venvs/finance/.venv/lib/python3.13/site-packages/certifi/cacert.pem

# Python’s ssl module relies on OpenSSL. Homebrew’s Python installations typically include OpenSSL
import ssl
print(ssl.OPENSSL_VERSION)