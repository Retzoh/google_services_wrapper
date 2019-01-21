import sys
from pathlib import Path
from google_services._utilities import memoize

# The different components of the python google-api-wrapper
from oauth2client import file, client, tools

# ...the following restrictions
DEFAULT_SCOPES = [
    # Create & delete gmail labels
    'https://www.googleapis.com/auth/gmail.labels',
    # Possibility to create files in your drive and access all files
    'https://www.googleapis.com/auth/drive',
    # Send mails
    'https://www.googleapis.com/auth/gmail.send',
    # Assign & remove labels to mails
    'https://www.googleapis.com/auth/gmail.modify']


DEFAULT_CONFIG_PATH = '~/.google_services_wrapper/'


@memoize
def get_creds(
        config_path=DEFAULT_CONFIG_PATH,
        scopes=DEFAULT_SCOPES):
    config_path = Path(config_path).expanduser()
    # Oauth2 token:
    # lets the script use your google account identity with...
    store = file.Storage(config_path/'token.json')
    creds = store.get()

    if not creds or creds.invalid:
        # Ask the user to give the correct permissions.
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
