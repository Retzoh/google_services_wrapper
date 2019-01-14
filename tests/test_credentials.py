from google_services import credentials as creds


def test_get_creds():
    """Credentials exist and are valid for the default scopes and location
    """
    creds.get_creds()
