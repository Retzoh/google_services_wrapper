# ...the following restrictions
default_scopes = [
    # Create & delete gmail labels
    'https://www.googleapis.com/auth/gmail.labels',
    # Possibility to create files in your drive and access all files
    'https://www.googleapis.com/auth/drive',
    # Send mails
    'https://www.googleapis.com/auth/gmail.send',
    # Assign & remove labels to mails
    'https://www.googleapis.com/auth/gmail.modify']


default_credential_path = '~/.google_services_wrapper/'
