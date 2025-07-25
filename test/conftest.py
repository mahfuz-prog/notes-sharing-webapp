import json
import pytest
import requests

with open('../frontend_config.json', 'r') as config_file:
    conf = json.load(config_file)

# Fixture for the base URL of the API
@pytest.fixture
def api_base_url():
    return conf.get("SERVER_ADDR")


# Fixture for the API client (requests session)
@pytest.fixture
def api_client(api_base_url):
    session = requests.Session()
    session.base_url = api_base_url
    yield session
    session.close()