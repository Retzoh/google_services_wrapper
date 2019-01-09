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
def get_labels(service=None):
    """Fetches all existing labels in the user's inbox
    Args:
        service (optional, gmail-api-service): the service to use. Default:
            the result of `default_service()`
    Returns:
        list of dict, label information records. The id and name for each
        label existing in the user's inbox.
    """
    logger.debug('fetching labels')
    return service.users().labels().list(userId='me').execute().get(
        'labels', [])


@apply_defaults(service=default_service)
def create_label(label_name, service=None):
    """Create a label with the specified name in the user's inbox
    Args:
        label_name(str):
        service (optional, gmail-api-service): the service to use. Default:
            the result of `default_service()`
    Returns:
        dict, id and name of the created label
    """
    logger.debug('creating labels')
    service.users().labels().create(
        userId='me',
        body={
            'messageListVisibility': 'show',
            'name': label_name,
            'labelListVisibility': 'labelShow'}).execute()


# https://stackoverflow.com/questions/37201250/sending-email-via-gmail-python
def create_mail(sender, to, subject, msg_html, msg_plain):
    """Create an email message.
    Args:
        sender (str): mail adress of sender
        to (str): destination mail adress
        subject (str): mail subject
        msg_html (str): html content for the mail
        msg_plain (str): string version of the mail
    Returns:
        Message body in mime format
    """
    logger.debug('creating mail')
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


# https://stackoverflow.com/questions/37201250/sending-email-via-gmail-python
@apply_defaults(service=default_service)
def send(user_id, mime_msg, service=None):
    logger.debug('sending mail')
    """Send an email message.
    Args:
        user_id (str): User's email address. The special value
            "me" can be used to indicate the authenticated user.
        mime_msg (mime message): Message to be sent
        service (optional, gmail-api-service): the service to use. Default: 
            the result of `default_service()`
    Returns:
        dict, information about the message sent, including it's id
    """
    result = service.users().messages().send(
        userId=user_id, body=mime_msg).execute()
    return result


@apply_defaults(service=default_service)
def send_file(mail_adress, project_name, file_id, service=None):
    """Send a mail with a link to a google doc
    Args:
        mail_adress (str):
        project_name (str):
        file_id (str):
        service (optional, gmail-api-service): the service to use. Default:
            the result of `default_service()`
    Returns:
        dict, information about the message used to send the file, including
        it's id
    """
    logger.debug('sending file')
    message = create_mail(
        "project_setup@gtd.system",
        mail_adress,
        project_name,
        f"<a href=https://docs.google.com/document/d/{file_id}>"
        f"Project description</a>",
        f"https://docs.google.com/document/d/{file_id}")
    return send('me', message, service)


@apply_defaults(service=default_service)
def archive_message(message_id, project_label_id, service=None):
    """Mark a message with a label, as read and archive it
    Args:
        message_id (str):
        project_label_id (str):
        service (optional, gmail-api-service): the service to use. Default:
            the result of `default_service()`
    Returns:
        the api request's result
    """
    logger.debug('archiving mail')
    return service.users().messages().modify(
        id=message_id,
        userId='me', body={
            "addLabelIds": [
                project_label_id
            ],
            "removeLabelIds": [
                'UNREAD', 'INBOX'
            ]
        }).execute()
