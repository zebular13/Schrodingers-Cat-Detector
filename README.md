# Meeting Room #
This app looks in the box for you and tells you if Schrodinger's cat is alive or dead.
It's an example of an integration between Walabot and Alexa.

## Questions you can ask Alexa ##
* Alexa, how is your cat?
* How is Schrodinger's cat?
* Is Schrodinger's cat dead?
* Are you alive or dead?

## Getting started ##
 * Go to the repo folder
 * Run `python main.py` 
 * Run `ngrok http 5000`
 * Copy the URL output from the previous step and use it in the configuration tabe at https://developer.amazon.com.
 
## Testing without Walabot ##
 * Go to repo folder
 * Run python
 * Run `import json, socket`
 * Run `s = socket.socket()`
 * Run `s.connect(("127.0.0.1", 9999))`
 * Run `s.send(json.dumps({"cat_status_field": 1}).encode('UTF-8'))`
 * For testing with live cats, please repeat the previous step setting "cat_status_field" to 2
