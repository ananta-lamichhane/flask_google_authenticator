# Authn Web

## Google Authenticator for the web
## Introduction
Simple web app to be able to scan qr codes for 2fa authentication and view them on a web-page.

## Usage
### To install
1. Create python virtual environment
2. Install necessary packages from requirements.txt
3. Run flask application
4. Open the homepage endpoint on a browser.

## Adding secret keys
To add secret keys, you have to generate it in relevant services (e.g. google, microsoft, etc.). After generating, add the secret key into secrets.json file. Provide a appropriate label to identify the service (e.g. email address, username, etc.). \
Scan the QR code while generating 2FA code on your service (eg. Google) to automatically add it to the list.

## TODO
1. Add encryption to the secrets saved in the app.
2. UI improvements.
3. Package into Docker application.
4. Make a standalone variant without flask necessary.

## Note
Web deployment is not included in this implementation. However, it should be fairly similar to any other flask web application.

## Sources

The code to google auth adapted from Graham Mitchell's git. https://github.com/grahammitchell/google-authenticator
