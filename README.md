# flask_google_authenticator

## Google Authenticator for the web
## Introduction
This web application mimics the function of google authenticator app on android or iphone (or any other authenticator apps which implement the RFC6328 TOTP protocol). It can be used to register the secrets and then the web interface can be used to get the one time codes.

## Usage
To install
1. Create python virtual environment
2. Install necessary packages from requirements.txt
3. Run flask application
4. Open the homepage endpoint on a browser.

## Note
Web deployment is not included in this implementation. However, it should be fairly similar to any other flask web application.

## Sources

The code to google auth adapted from Graham Mitchell's git. https://github.com/grahammitchell/google-authenticator
