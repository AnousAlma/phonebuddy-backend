# How to use the backend

## Startup
First create a secrets.json file to the main folder.

secrets.json should be formatted in the following way:

      

    {
    "DB_URI": "YOUR_DB_URI",
    "type": "YOUR FIREBASE ACCOUNT TYPE",
    "project_id": "YOUR FIREBASE PROJECT ID",
    "private_key_id": "YOUR FIREBASE PRIVATE KEY ID",
    "private_key": "YOUR FIREBASE PRIVATE KEY",
    "client_email": "YOUR FIREBASE CLIENT_EMAIL",
    "client_id": "YOUR FIREBASE CLIENT_ID",
    "auth_uri": "YOUR FIREBASE AUTH_URI",
    "token_uri": "YOUR FIREBASE TOKEN_URI",
    "auth_provider_x509_cert_url": "YOUR FIREBASE AUTH_PROVIDER",
    "client_x509_cert_url": "YOUR FIREBASE CLEINT URL",
    "universe_domain": "googleapis.com"
    }

## Create files and folders

After you are done with setup all you have to do is run

    python ./app.py
in the console and thats it :)
