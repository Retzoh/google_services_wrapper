from google_services import drive
from pathlib import Path


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


def test_create_file_relative_path():
    path = 'test_create_file_relative_path'
    Path(path).write_text('some content')
    drive.create_file(
        path, 'test_create_file_relative_path')
    Path(path).unlink()


def test_create_file_absolute_path():
    path = str(Path('~/test_create_file_absolute_path').expanduser())
    Path(path).write_text('some content')
    drive.create_file(
        path, 'test_create_file_absolute_path')
    Path(path).unlink()


def test_create_file_absolute_path_from_home():
    path = '~/test_create_file_absolute_path_from_home'
    Path(path).expanduser().write_text(
        'some content')
    drive.create_file(
        path, 'test_create_file_absolute_path_from_home')
    Path(path).expanduser().unlink()


def test_download():
    file_id = drive.get_files(
        'name="test_create_file_absolute_path_from_home"'
    )[0]["id"]
    assert drive.download_file(file_id) == b'some content'


def test_create_file_absolute_path_no_name():
    path = '~/test_create_file_absolute_path_no_name'
    Path(path).expanduser().write_text(
        'some content')
    drive.create_file(
        path)
    Path(path).expanduser().unlink()


def test_update_file_absolute_path_no_name():
    file_id = drive.get_files(
        'name="test_create_file_absolute_path_no_name"'
    )[0]["id"]

    path = '~/test_create_file_absolute_path_no_name'
    Path(path).expanduser().write_text(
        'some other content')
    drive.update_file(
        path, file_id)
    Path(path).expanduser().unlink()


def test_create_file_absolute_path_parent_folder():
    folder_id = drive.get_files(
        'name="test_folder" and mimeType="application/vnd.google-apps.folder"'
    )[0]["id"]
    path = '~/test_create_file_absolute_path_no_name'
    Path(path).expanduser().write_text(
        'some content')
    drive.create_file(
        path, parent_folder_id=folder_id)
    Path(path).expanduser().unlink()


def test_delete_file():
    files = drive.get_files('name contains "test"')
    for file in files:
        drive.delete_file(file["id"])
