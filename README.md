# Schrodinger's Cat Detector #
This app looks in the box for you and tells you if Schrodinger's cat is alive or dead.
It's an example of an integration between Walabot and Alexa.
Full instructions are here: https://www.hackster.io/monica/schrodinger-s-cat-detector-498e1b

## Questions you can ask Alexa ##
* Alexa, how is your cat?
* How is Schrodinger's cat?
* Is Schrodinger's cat dead?
* Are you alive or dead?

## Build the project ##
### Install Python ###
* On Windows, if you don't have Python installed, download the latest version of either Python 2 or 3. 
* Run the installer and select "custom install."
* Leave everything checked. This will install pip along with Python. Check "install for all users" so that it will be installed in Program Files, rather than AppData (installing it here will cause problems later on.) 
* Check "Add to environmental variables." This will allow you to access python and pip from the command line.

### Install the Walabot API for Python ###
This is downloded with the SDK. It needs to be installed before it can be used.
* Run cmd as administrator. Enter this command:

`python -m pip install “C:/Program Files/Walabot/WalabotSDK/python/WalabotAPI-1.0.35.zip”`

* The Walabot API should now be available on your computer here: 

`C:/Program Files/Walabot/WalabotSDK/python/WalabotAPI`

## Install Plugins/Packages ##
Our Alexa app will be using Flask-ask. Flask-ask is a Python module that makes it easy to develop Alexa Skills. There's a great tutorial for it here that I followed when making this app.
Flask-ask requires Flask. Install Flask.

`pip install flask` 

### Install Flask-ask ###
`pip install flask-ask`

I had a lot of trouble installing flask-ask. I kept getting the error "Cannot open include file: 'openssl/opensslv.h': No such file or directory." Flask-ask requires a cryptography module in order to do https, and for some reason it wasn't installing on its own. Here's how I fixed it:
* Install Perl.
* Install openSSL 1.1.0 or greater from a binary and then set the LIB and INCLUDE paths like this:

`C:\> set LIB=C:\OpenSSL-win64\lib;%LIB%` 
`C:\> set INCLUDE=C:\OpenSSL-win64\include;%INCLUDE%` 
`C:\> pip install cryptography` 

* I ended up having to unstall flask-ask (run CMD as administrator):
`pip uninstall flask-ask`
* and reinstall version 0.9.1, since it was giving me an error "TypeError: Can't compile non template nodes jinja."
(run CMD as administrator):

`sudo pip install -Iv flask-ask==0.9.2`

### Install tinydb ###
tinydb lets us make a little database for our app. We'll use the database to store differnt values (0, 1, and 2) according to whether the cat is present and moving. We'll then query tinydb each time we ask Alexa how Schrodinger's cat is doing.
`pip install tinydb`

### Install ngrok ###
You can just install this from the binary. 
ngrok exposes a local server behind a NAT or firewall to the internet.  This lets us test our skill without deploying it.

## Getting started ##
 * Go to the repo folder
 * Run `python main.py` 
 * Run `ngrok http 5000`
 * Copy the URL output from the previous step and use it in the configuration tab at https://developer.amazon.com.
 
## Testing without Walabot ##
 * Go to repo folder
 * Run python
 * Run `import json, socket`
 * Run `s = socket.socket()`
 * Run `s.connect(("127.0.0.1", 9999))`
 * Run `s.send(json.dumps({"cat_status_field": 1}).encode('UTF-8'))`
 * For testing with live cats, please repeat the previous step setting "cat_status_field" to 2
