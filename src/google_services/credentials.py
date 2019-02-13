"""Manage integration with the google-api SSO

"""

import sys
from pathlib import Path
from google_services._utilities import memoize, logger
from google_services.config import default, Config

# The different components of the python google-api-wrapper
from oauth2client import file, client, tools


@memoize
def get_creds(
        config: Config=default):
    """Check that the SSO token is valid. If not, asks for a new one.

    Asking for a new token is done by opening the sing-in-with-google-tab in
    the browser. The google account linked to in client_id.json is
    pre-selected.

    The `client_id.json` corresponds to what you can download from
    https://console.developers.google.com/apis/credentials.

    I took this function almost as is from the official google gmail api doc:
    https://developers.google.com/gmail/api/quickstart/python.

    Note: `oauth2client.tools` bugs if `sys.argv` are specified. This
    function fixes that.

    Args:
        config: a config element as defined in the `config.py` package

    Returns:
        credentials that the api can work with
    """
    config_path = config.credential_path
    scopes = config.scopes

    logger.info('loading token')
    logger.debug(f'config_path: {config_path}')
    config_path = Path(config_path).expanduser()
    store = file.Storage(config_path/'token.json')
    creds = store.get()

    if not creds or creds.invalid:
        # Ask the user to give the correct permissions.
        logger.info('loading credentials')
        flow = client.flow_from_clientsecrets(
            config_path/'client_id.json',
            scopes)

        arguments = sys.argv
        sys.argv = sys.argv[0:1]
        # This line is why we need to remove the arguments from sys.argv
        # If you find a better way to get it to work, i'm buying it
        creds = tools.run_flow(flow, store)
        sys.argv = arguments

    return creds
