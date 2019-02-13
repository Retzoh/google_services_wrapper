Google services, python framework
=================================

This repository is a pip package acting as a high-level wrapper for the
[google api client](https://developers.google.com/api-client-library/python/start/get_started).

It provides high-level access (ex `drive.create_folder(folder_name)`)
to some functionalities of the
[drive](https://developers.google.com/drive/api) and
[gmail](https://developers.google.com/gmail/api) apis.

It is also a collection of working use cases for those apis.
This is useful since the official google documentation for the apis
is difficult to use in practice because of incomplete examples.

### Usage

- Generate and download an SSO token from the
[google developer console](https://console.developers.google.com/apis/credentials).
  - Select a project or create one (top-left of the window)
  - Go to the
  [API library](https://console.developers.google.com/apis/library),
  select `drive` and activate the api
  - Create a project ID
    - For the drive api
    - For a platform with user-interface
    - With access to the user's data
  - Activate the `gmail` api
  - Go to your
  [project-credential page](https://console.developers.google.com/apis/credentials)
  - Download the OAuth ID
- Install this package
  - Clone
  [this repository](https://github.com/Retzoh/google_services_wrapper.git)
  - Install the dependencies
    - I recommend using
    [anaconda](https://www.anaconda.com/distribution/#download-section)
    (python 3.7)
    - run `conda env update -n base` from the repository folder
  - Install the package by running `pip install .` from the repository
  folder
  - Import it with `import google_services`
  - Set `google_services.config.default.credential_path` to the folder
  containing the OAuth ID file

Subscribe to updates by sending a mail to
~retzoh/google-services-wrapper-updates+subscribe@lists.sr.ht

#### git.sh.ht repository
[https://git.sr.ht/~retzoh/google_services_wrapper](https://git.sr.ht/~retzoh/google_services_wrapper)
#### github repository
[https://github.com/Retzoh/google_services_wrapper](https://github.com/Retzoh/google_services_wrapper)

The master branches on sr.ht and github are synchronized through this
[manifest](https://git.sr.ht/~retzoh/google_services_wrapper/tree/master/.build.yml)
at each commit on master

### Contributing
#### Issue tracker
[https://todo.sr.ht/~retzoh/google-services-wrapper-discussions](https://todo.sr.ht/~retzoh/google-services-wrapper-discussions)

#### Submit patches
Send your patches to
~retzoh/google-services-wrapper-contributing@lists.sr.ht

#### Reviewing
Submitted patches can be found there:
[https://lists.sr.ht/~retzoh/google-services-wrapper-contributing](https://lists.sr.ht/~retzoh/google-services-wrapper-contributing)


Send a mail to
~retzoh/google-services-wrapper-contributing+subscribe@lists.sr.ht to be
notified of new patches.