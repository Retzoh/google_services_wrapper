"""Configuration elements for the google-api SSO integration

"""


class Config:
    """Runtime editable configuration

    Attributes:
        scopes (list): list of scopes that the google-SSO should give access
            to. For a list of available scopes, see:
            gmail -> https://developers.google.com/gmail/api/auth/scopes
            drive -> https://developers.google.com/drive/api/v3/about-auth

        credential_path (str): path to the folder in which to look for the
            google-api SSO token. It will be looked into for a `client_id.json`
            or a `token.json` file. The `client_id.json` corresponds to what
            you can download from
            https://console.developers.google.com/apis/credentials
    """
    # Oauth2 token:
    # lets the script use your google account identity with the following
    # restrictions
    scopes = [
        # Create & delete gmail labels
        'https://www.googleapis.com/auth/gmail.labels',
        # Possibility to create files in your drive and access all files
        'https://www.googleapis.com/auth/drive',
        # Send mails
        'https://www.googleapis.com/auth/gmail.send',
        # Assign & remove labels to mails
        'https://www.googleapis.com/auth/gmail.modify']

    credential_path = '~/.google_services_wrapper/'


default = Config()
