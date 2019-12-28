# vk-friends
Site based on flask, uses vk oauth to get list of user friends.

## Requirements:
- python module `flask`
- python module `requests`
- vk app `Application ID`, `Secure key` and `Service token`

## Preparation:
You shoud create file `private.py` containing:

    CLIENT_ID = 'xxx' # Application ID for get access token and create authorize url
    CLIENT_SECRET = 'xxx' # Secure key for get access token
    CLIENT_SERVISE_KEY = 'xxx' # Service token for get city name by id

## Run:
###### on Windows
    set FLASK_APP=main.py
    flask run
###### on nix
    FLASK_APP=main.py flask run
