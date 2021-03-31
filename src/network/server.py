from flask import Flask, request, Response
"""

GET   /api/clipboard/available  - Prüfe ob neue Daten vorhanden sind
GET   /api/clipboard            - Erhalte neues Clipboard
POST  /api/clipboard            - Lade neues Clipboard hoch bzw. sende Neuerungen an Server

"""
app = Flask(__name__)


# Default route with nothing to it
@app.route('/')
def hello_world():
  return 'Hello world'


# Route using query parameters
@app.route('/params')
def query_params():
  # To get a specific parameter: request.args.get('paramName')
  args = request.args
  res = 'I got those parameters:'
  for arg in args:
    res += '{0} = {1} '.format(arg, args[arg]) 
  return res


# Only allows POST request. With no specification only GET is allowed
@app.route('/post-only', methods=['POST'])
def only_post():
  # Getting the body-text of the request as a JSON
  body = request.get_json() # .get_data() for raw data
  res = 'This is the body of the request: {0}'.format(body) 
  return res


# Setting the response status code and generally more response-parameters
@app.route('/complex-response')
def get_complex_response():
  # Creating a more complex response object
  res = Response(response="OK", status=200, mimetype='text/plain')
  # Setting response headers and cookies
  res.headers['some_value'] = 'new_header_value'
  res.set_cookie('some_value', 'new_cookie_value')
  return res

# Using router from different file
from network.router import router
app.register_blueprint(router, url_prefix='/prefix')

