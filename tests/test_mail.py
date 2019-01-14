from google_services import mail


def test_default_service():
    assert mail.default_service() is not None


def test_create_label():
    mail.create_label('test_label')


def test_get_label():
    assert len(mail.get_labels()) > 0


def test_create_mail():
    assert mail.create_mail('services.wrapper@gmail.com',
                            'services.wrapper@gmail.com',
                            'test_subject',
                            'test_html',
                            'test_plain') is not None


def test_send_mail():
    mime_msg = mail.create_mail('services.wrapper@gmail.com',
                                'services.wrapper@gmail.com',
                                'test_subject',
                                'test_html',
                                'test_plain')

    mail.send('me', mime_msg)


def test_send_file():
    mail.send_file('services.wrapper@gmail.com',
                   'test_subject',
                   '1B91DlZUvPuNXBlAd5KLinuUpBGyUx8D-K_RUZK91BFc')


def test_get_messages():
    assert len(mail.get_messages('subject: "test_subject"')) > 0


def test_archive_message():
    test_messages = mail.get_messages('subject: "test_subject"')
    labels = mail.get_labels()
    extra_label = [l['id'] for l in labels if l['name'] == 'test_label'][0]

    for message in test_messages:
        mail.archive_message(message['id'], extra_labels=extra_label)


def test_put_to_trash():
    test_messages = mail.get_messages('subject: "test_subject"')

    for message in test_messages:
        mail.move_to_trash(message['id'])


def test_delete_label():
    labels = mail.get_labels()
    for label in labels:
        if label['name'] == 'test_label':
            mail.delete_label(label['id'])
