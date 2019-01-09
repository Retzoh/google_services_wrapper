import sys
from google_services._utilities import memoize

# The different components of the python google-api-wrapper
from oauth2client import file, client, tools

# ...the following restrictions
SCOPES = [
    # Create & delete gmail labels
    'https://www.googleapis.com/auth/gmail.labels',
    # Possibility to create files in your drive and edit THOSE ONLY
    'https://www.googleapis.com/auth/drive.file',
    # Send mails
    'https://www.googleapis.com/auth/gmail.send',
    # Assign & remove labels to mails
    'https://www.googleapis.com/auth/gmail.modify']


@memoize
def get_creds():
    # TODO: token.json and credentials should args
    # Oauth2 token:
    # lets the script use your google account identity with...
    store = file.Storage('token.json')
    creds = store.get()

    if not creds or creds.invalid:
        # Ask the user to give the correct permissions.
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        # This line is why we need to remove the arguments from sys.argv
        # If you find a better way to get it to work, i'm buying it
        arguments = sys.argv
        sys.argv = sys.argv[0:1]
        creds = tools.run_flow(flow, store)
        sys.argv = arguments

    return creds
