from google_services import drive


def test_default_service():
    assert drive.default_service() is not None


def test_get_files():
    assert len(drive.get_files(
        'name="Project description template"')) > 0


def test_create_folder():
    drive.create_folder('test_folder')


def test_copy_file():
    drive.copy_file('1B91DlZUvPuNXBlAd5KLinuUpBGyUx8D-K_RUZK91BFc',
                    'test_copy', None)


def test_copy_in_folder():
    folder_id = drive.get_files(
        'name="test_folder" and mimeType="application/vnd.google-apps.folder"'
    )[0]["id"]
    drive.copy_file('1B91DlZUvPuNXBlAd5KLinuUpBGyUx8D-K_RUZK91BFc',
                    'test_copy', folder_id)


def test_delete_file():
    files = drive.get_files('name contains "test"')
    for file in files:
        drive.delete_file(file["id"])
