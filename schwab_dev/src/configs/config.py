
import dotenv
from easydict import EasyDict

from pydantic import BaseModel, ConfigDict
from pydantic.dataclasses import dataclass, Field

envs = dotenv.dotenv_values()
# config = dotenv.dotenv_values()
# envs = EasyDict(config) # dot notation


@dataclass
class URLConfigSchema:
    """ Configuration schema for URLs.  """
    token_url: str = "https://api.schwabapi.com/v1/oauth/token"
    callback_url: str = "https://127.0.0.1"

@dataclass
class PathConfigSchema:
    """ Configuration schema for file paths. """
    # non-default argument should preceed default argument
    token_file: str = Field(default="configs/.tokens.json")

class SchwabCredentials(BaseModel):
    """ Configuration schema for Charl Schwab Dev APIs.  """ 
    app_key: str = envs["APP_KEY"]
    app_secret: str = envs["APP_SECRET"]

class MetadataConfigs:
    """
    Hierarchical Configurations:
    """
    urls: URLConfigSchema = URLConfigSchema()
    paths: PathConfigSchema = PathConfigSchema()
    envs: SchwabCredentials = SchwabCredentials()
