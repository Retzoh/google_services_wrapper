class _Config:
    # Oauth2 token:
    # lets the script use your google account identity with...
    # ...the following restrictions
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


default = _Config()

