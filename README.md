Introduction
============

Command-line script to upload videos to Youtube using theYoutube [APIv3](https://developers.google.com/youtube/v3/). It should work on any platform (GNU/Linux, BSD, OS X, Windows, ...) that runs Python.

Dependencies
============
  * [Python 3.10](http://www.python.org) (maybe it works on lower versions, I haven't tested them though; and it definitely doesn't work with <=3.5).
  * tqdm, google-api-python-client, oauth2client and click. They'll be automatically installed by makepkg/setuptools/pip, though

```
pip install --user -r requirements.txt
```
or
```
python setup.py install
```

Installing
==========
```
git clone https://github.com/brunofauth/youtube-upload.git
cd youtube-upload
sudo python setup.py install
```

Setup
=====

You'll see that there is no email/password options. Instead, the Youtube API uses [OAuth 2.0](https://developers.google.com/accounts/docs/OAuth2) to authenticate the upload. The first time you try to upload a video, you will be asked to follow a URL in your browser to get an authentication token. If you have multiple channels for the logged in user, you will also be asked to pick which one you want to upload the videos to. You can use multiple credentials, just use the option ```--credentials-file```. Also, check the [token expiration](https://developers.google.com/youtube/v3/) policies.

The package used to include a default ```client_secrets.json``` file. It does not work anymore, Google has revoked it. So you now must [create and use your own OAuth 2.0 file](https://developers.google.com/youtube/registering_an_application), it's a free service. Steps:

* Go to the Google [console](https://console.developers.google.com/).
* _Create project_.
* Side menu: _APIs & auth_ -> _APIs_
* Top menu: _Enabled API(s)_: Enable all Youtube APIs.
* Side menu: _APIs & auth_ -> _Credentials_.
* _Create a Client ID_: Add credentials -> OAuth 2.0 Client ID -> Other -> Name: youtube-upload -> Create -> OK
* _Download JSON_: Under the section "OAuth 2.0 client IDs". Save the file to your local system. 
* Use this JSON as your credentials file: `--client-secrets=CLIENT_SECRETS` or copy it to `~/client_secrets.json`.

*Note: ```client_secrets.json``` is a file you can download from the developer console, the credentials file is something auto generated after the first time the script is run and the google account sign in is followed, the file is stored at ```~/.youtube-upload-credentials.json```.*

Get available categories
========================

* Go to the [API Explorer](https://developers.google.com/apis-explorer)
- Search "youtube categories" -> *youtube.videoCategories.list*
- This bring you to [youtube.videoCategories.list service](https://developers.google.com/apis-explorer/#search/youtube%20categories/m/youtube/v3/youtube.videoCategories.list)
- part: `id,snippet`
- regionCode: `es` (2 letter code of your country)
- _Authorize and execute_

And see the JSON response below. Note that categories with the attribute `assignable` equal to `false` cannot be used.

Using [shoogle](https://github.com/tokland/shoogle):

```
$ shoogle execute --client-secret-file client_secret.json \
                  youtube:v3.videoCategories.list <(echo '{"part": "id,snippet", "regionCode": "es"}')  | 
    jq ".items[] | select(.snippet.assignable) | {id: .id, title: .snippet.title}"
```

Notes for developers
====================

* Main logic of the upload: [main.py](youtube_upload/main.py) (function ```upload_video```).
* Check the [Youtube Data API](https://developers.google.com/youtube/v3/docs/).
* Some Youtube API [examples](https://github.com/youtube/api-samples/tree/master/python) provided by Google.

Alternatives
============

* [shoogle](https://github.com/tokland/shoogle) can send requests to any Google API service, so it can be used not only to upload videos, but also to perform any operation regarding the Youtube API.

