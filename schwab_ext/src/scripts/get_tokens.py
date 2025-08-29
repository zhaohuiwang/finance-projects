

"""
Schwab employs the Oauth2 protocol to secure services from unauthorized access. 
Prerequisit: Developer account, Trader API, authorizations, APP key and secret.
```bash
(active-venv) username@hostname:/dev/finance-projects$ uv run -m schwab_dev.src.scripts.get_tokens
```
Step 1: App Authorization. 
Request Template - Authorization URL
https://api.schwabapi.com/v1/oauth/authorize?client_id={CONSUMER _KEY}&redirect_uri={APP_CALLBACK_URL}

 This should pop up a browser. If not, you need to manually open this URL in your browser > login > accept terms and conditions > select accounts to link > copy the the response URL 

Response Template - Final landing URL
https://{APP_CALLBACK_URL}/?code={AUTHORIZATION_CODE_GENERATED}&session={SESSION_ID}

Step 2: Access Token Creation.
POST https://api.schwabapi.com/v1/oauth/token
and the `AUTHORIZATION_CODE_GENERATED` from step 1.

The tokens will be save as `../scripts/.tokens.json`

Terminal Code to activate the virtual environment and execute the script as a Python module
$ source /mnt/e/zhaohuiwang/dev/venvs/uv-venvs/finance/.venv/bin/activate
python -m schwab_ext.src.scripts.get_tokens
"""
import base64
import json
from pathlib import Path
import requests

from urllib.parse import urlparse, parse_qs

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, parse_qs
from schwab_ext.src.configs.config import MetadataConfigs
from schwab_ext.src.utils import setup_logger, find_directory

# Logger setup
# Searches for the first occurrence of 'logs/' dir by traversing up the directory tree. Create one if not found.
logs_dir = find_directory(target_dir_name="logs")
if logs_dir:
    log_fpath = Path(logs_dir)/'app.log'
else:
    log_fpath = Path(__file__).parent.parent.parent/'logs/app.log'
    log_fpath.parent.mkdir(parents=True, exist_ok=True)

logger = setup_logger(
    logger_name=__name__,
    log_file=log_fpath
    )

logger.info(f"Running at: {Path.cwd()}")

# Load configuration
cfg = MetadataConfigs()

# Configure Chrome options to avoid detection
chrome_options = Options()
# critical: Makes the browser appear as if it's being operated by a human rather than an automation tool or bot. By disabling the AutomationControlled feature, the Selenium-driven Chrome instance is less likely to be flagged by anti-bot measures. 
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


# Construct the authorization URL
params = {
        "client_id": cfg.envs.app_key,
        "redirect_uri": cfg.urls.callback_url
    }
auth_url = "https://api.schwabapi.com/v1/oauth/authorize?" + "&".join(f"{k}={v}" for k, v in params.items())

try:
    # Open the authorization URL
    driver.get(auth_url)

    # Wait for the redirect (the URL to change or contain the redirect url)
    WebDriverWait(driver, 120).until(
        EC.url_contains(cfg.urls.callback_url)  
    )

    # Get the current URL after redirect
    redirected_url = driver.current_url

    # Parse the URL to extract code and session
    parsed_url = urlparse(redirected_url)
    query_params = parse_qs(parsed_url.query)

    auth_code = query_params.get('code', [''])[0]
    session = query_params.get('session', [''])[0]

    if auth_code and session:
        logger.info(f"Successfully extracted `auth_code` and `session`")
    else:
        logger.error("Failed to extract auth_code or session. Check the URL.")

except Exception as e:
    logger.error(f"Error during automation: {e}")
finally:
    # Clean up by closing the browser
    driver.quit()

credentials = f"{cfg.envs.app_key}:{cfg.envs.app_secret}"
base64_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    
# Prepare headers and payload
headers = {
    "Authorization": f"Basic {base64_credentials}",
    "Content-Type": "application/x-www-form-urlencoded"
}
payload = {
    # gets access and refresh tokens using authorization code
    "grant_type": "authorization_code",
    #'grant_type': 'refresh_token', # refreshes the access token
    "code": auth_code,
    "redirect_uri": cfg.urls.callback_url
}
    
# Make POST request to token endpoint
try:
    response = requests.post(cfg.urls.token_url, headers=headers, data=payload)
    response.raise_for_status()  # Raise exception for bad status codes
    tokens = response.json()
    logger.info("Tokens retrieved successfully, including:\n", list(tokens.keys()))

except requests.RequestException as e:
    logger.error(f"Error exchanging authorization code: {e}")
    logger.debug(f"Response: {response.text}")

token_path = Path(__file__).parent.parent/cfg.paths.token_file
if tokens:
    try:
        with open(token_path, "w") as f:
            json.dump(tokens, f, indent=4)
            logger.info(f"Tokens saved to {token_path}")
    except Exception as e:
        logger.error(f"Error saving tokens to {token_path}: {e}")
else:
    logger.info("No tokens to save.")


