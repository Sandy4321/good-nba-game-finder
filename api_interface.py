import json
import subprocess

# unpacks the data from a given url and returns it as a dict
def fetch(url, token):
    response = subprocess.Popen(['curl', '-H', token, url], stdout=subprocess.PIPE).communicate()[0]
    return json.loads(response)

