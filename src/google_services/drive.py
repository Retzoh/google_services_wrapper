from google_services.credentials import get_creds
from google_services._utilities import memoize, apply_defaults, logger

# The different components of the python google-api-wrapper
from googleapiclient.discovery import build
from httplib2 import Http


@memoize
def default_service():
    """Lazy getter for the default drive-api-service to use
    """
    logger.debug("instantiating google drive service")
    return build('drive', 'v3', http=get_creds().authorize(Http()))


@apply_defaults(service=default_service)
def get_files(query, service=None):
    """Query google drive for files matching `query`

    If no accessible file matches the query, returns an empty list.
    Args:
        query (str): a drive-file-search-query. Documentation link:
            https://developers.google.com/drive/api/v3/search-parameters
        service (optional, drive-api-service): the service to use. Default:
            the result of `default_service()`
    Returns:
        list of dict, file information records. Contains the name & id
        of the first file in the drive matching the query
        and accessible within the oauth permissions of the script
    """
    logger.debug('getting files')
    page_token = None
    files = []
    # We have to cycle on all the pages of the drive,
    while True:
        file_candidates = service.files().list(
            q=query,
            fields="nextPageToken, files(id, name)",
            pageToken=page_token).execute()
        files += file_candidates.get('files', [])

        page_token = file_candidates.get('nextPageToken', None)
        if page_token is None:
            break
    return files


@apply_defaults(service=default_service)
def create_folder(folder_name, service=None):
    """Create a new folder in the user's drive
    Args:
        folder_name (str):
        service (optional, drive-api-service): the service to use. Default:
            the result of `default_service()`

    Returns:
        dict, id and name of the folder
    """
    logger.debug('creating folder')
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    return service.files().create(body=file_metadata,
                                  fields='id, name').execute()


@apply_defaults(service=default_service)
def copy_file(source_file_id, new_file_name, parent_folder_id=None,
              service=None):
    """copy a file in the user's drive

    Args:
        source_file_id (str):
        new_file_name (str):
        parent_folder_id (str):
        service (optional, drive-api-service): the service to use. Default:
            the result of `default_service()`
    Returns:
        dict, id and name of the created file
    """
    logger.debug('copying file')
    request_body = {
        "name": new_file_name,
    }
    if parent_folder_id is not None:
        request_body["parents"] = [parent_folder_id]
    return service.files().copy(fileId=source_file_id,
                                body=request_body).execute()


@apply_defaults(service=default_service)
def delete_file(file_id, service=None):
    """copy a file in the user's drive

    Args:
        file_id (str):
        service (optional, drive-api-service): the service to use. Default:
            the result of `default_service()`
    Returns:
        an empty string if successful
    """
    logger.debug("deleting file")
    return service.files().delete(fileId=file_id).execute()

