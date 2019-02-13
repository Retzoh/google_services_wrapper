"""High-level wrapper around the google-drive api

"""

from google_services.credentials import get_creds
from google_services._utilities import memoize, apply_defaults, logger

# The different components of the python google-api-wrapper
from googleapiclient.discovery import build
from httplib2 import Http

# The components letting us send email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64


@memoize
def default_service():
    """Lazy getter for the default gmail-api-service to use
    """
    logger.info("instantiating gmail service")
    return build('gmail', 'v1', http=get_creds().authorize(Http()))


@apply_defaults(service=default_service)
def get_labels(service=None)->list:
    """Fetches all existing labels in the user's inbox

    Args:
        service (optional, gmail-api-service): the service to use. Default:
            the result of `default_service()`
    Returns:
        list of dict, label information records. The id and name for each
        label existing in the user's inbox.
    """
    logger.info('fetching labels')
    return service.users().labels().list(userId='me').execute().get(
        'labels', [])


@apply_defaults(service=default_service)
def create_label(label_name: str, service=None)->dict:
    """Create a label with the specified name in the user's inbox

    Args:
        label_name(str): Name of the label to create
        service (optional, gmail-api-service): the service to use. Default:
            the result of `default_service()`
    Returns:
        dict containing the id and name of the created label
    """
    logger.info('creating label')
    label = service.users().labels().create(
        userId='me',
        body={
            'messageListVisibility': 'show',
            'name': label_name,
            'labelListVisibility': 'labelShow'}).execute()
    return label


@apply_defaults(service=default_service)
def delete_label(label_id: str, service=None)->dict:
    """Delete the label with the specified id

    Args:
        label_id(str): Id of the label to delete
        service (optional, gmail-api-service): the service to use. Default:
            the result of `default_service()`
    Returns:
        dict containing the id and name of the created label
    """
    service.users().labels().delete(id=label_id, userId='me').execute()


# https://stackoverflow.com/questions/37201250/sending-email-via-gmail-python
def create_mail(sender: str, to: str, subject: str, msg_html: str,
                msg_plain: str)->dict:
    """Create an email message.

    I got this to work thanks to
    https://stackoverflow.com/questions/37201250/sending-email-via-gmail-python

    Args:
        sender (str): Mail address of sender
        to (str): Destination mail address
        subject (str): Mail subject
        msg_html (str): Html content for the mail
        msg_plain (str): String version of the mail
    Returns:
        Message body in mime format
    """
    logger.info('creating mail')
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(msg_plain, 'plain'))
    msg.attach(MIMEText(msg_html, 'html'))
    raw = base64.urlsafe_b64encode(msg.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}
    return body


@apply_defaults(service=default_service)
def send(user_id: str, mime_msg: dict, service=None)->dict:
    logger.info('sending mail')
    """Send an email message.
    
    Args:
        user_id (str): User's email address. The special value
            "me" can be used to indicate the authenticated user.
        mime_msg (mime message): Message to be sent
        service (optional, gmail-api-service): the service to use. Default: 
            the result of `default_service()`
    Returns:
        dict containing information about the message sent, including it's id
    """
    result = service.users().messages().send(
        userId=user_id, body=mime_msg).execute()
    return result


@apply_defaults(service=default_service)
def send_file(mail_address: str, mail_subject: str, file_id: str,
              service=None, sender: str='send.file@google.api')->dict:
    """Send a mail with a link to a google doc

    Args:
        mail_address (str): Destination mail address
        mail_subject (str): Mail subject
        file_id (str): Id of the file to send
        service (optional, gmail-api-service): the service to use. Default:
            the result of `default_service()`
        sender (str): Mail address of the sender
    Returns:
        dict, information about the message used to send the file, including
        it's id
    """
    logger.info('sending file')
    message = create_mail(
        sender,
        mail_address,
        mail_subject,
        f"<a href=https://docs.google.com/document/d/{file_id}>"
        f"Project description</a>",
        f"https://docs.google.com/document/d/{file_id}")
    return send('me', message, service=service)


@apply_defaults(service=default_service)
def get_messages(query: str, service=None)->list:
    """List messages matching the specified query
    Args:
        query (str): a gmail-message-search-query. Documentation link:
            https://support.google.com/mail/answer/7190?hl=en
        service (optional, gmail-api-service): the service to use. Default:
            the result of `default_service()`
    Returns:
        List of Messages that match the criteria of the query. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate ID to get the details of a Message.
    """
    logger.info('getting mails')
    response = service.users().messages().list(userId='me',
                                               q=query).execute()
    messages = []
    if 'messages' in response:
        messages.extend(response['messages'])

    while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        response = service.users().messages().list(
            userId='me', q=query, pageToken=page_token).execute()
        messages.extend(response['messages'])

    return messages


@apply_defaults(service=default_service)
def archive_message(message_id: str, extra_labels: str=None, service=None):
    """Mark a message with a label, as read and archive it
    Args:
        message_id (str): Id of the message to archive
        extra_labels (str): Labels to add to the message in the form
            "label_1,label2"
        service (optional, gmail-api-service): the service to use. Default:
            the result of `default_service()`
    Returns:
        the api request's result
    """
    logger.info('archiving mail')
    body = {
            "removeLabelIds": [
                'UNREAD', 'INBOX'
            ]
        }
    if extra_labels is not None:
        body["addLabelIds"] = [extra_labels]
    return service.users().messages().modify(
        id=message_id,
        userId='me', body=body).execute()


@apply_defaults(service=default_service)
def move_to_trash(message_id: str, service=None):
    """Mark a message with a label, as read and archive it
    Args:
        message_id (str): Id of the message to trash
        service (optional, gmail-api-service): the service to use. Default:
            the result of `default_service()`
    Returns:
        the api request's result
    """
    logger.info('moving mail to trash')

    return service.users().messages().modify(
        id=message_id,
        userId='me', body={
            "addLabelIds": [
                'TRASH',
            ]
        }).execute()
