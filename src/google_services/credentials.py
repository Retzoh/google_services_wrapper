import sys
from pathlib import Path
from google_services._utilities import memoize, logger
from google_services.config import default_credential_path, default_scopes

# The different components of the python google-api-wrapper
from oauth2client import file, client, tools


@memoize
def get_creds(
        config_path=default_credential_path,
        scopes=default_scopes):
    logger.info('loading token')
    config_path = Path(config_path).expanduser()
    # Oauth2 token:
    # lets the script use your google account identity with...
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
