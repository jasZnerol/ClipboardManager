"""
Routes

GET     /clipboard            - Erhalte neues Clipboard
POST    /clipboard            - Lade neues Clipboard hoch bzw. sende Neuerungen an Server
DELETE  /clipboard            - Clear the entire clipboard

GET     /clipboard/available  - Prüfe ob neue Daten vorhanden sind

GET     /file?fid=<file_id>   - Lade eine Datei vom Server runter die im ClipboardManager vorgemerkt ist

"""

# Handle request asynchrounosly
from gevent import monkey
monkey.patch_all()

from bottle import Bottle, run, request, response
import pickle

app = Bottle()

clipboard = []
index = 0
updateID = 0

@app.get("/clipboard")
def get_clipboard():
  global clipboard, updateID, index
  response.headers["updateID"] = updateID
  response.headers["Content-Type"] = "application/python-pickle"
  response.headers["Clipboard-Index"] = index
  # Serialize clipboard to sent to client
  return pickle.dumps(clipboard)

@app.post("/clipboard")
def post_clipboard():
  global clipboard, updateID, index
  update = pickle.loads(request.body.read())
  index = int(request.headers["Client-Index"])
  clipboard.append(update)
  updateID += 1 
  response.headers["Content-Type"] = "text/plain"
  return str(updateID)


@app.delete("/clipboard")
def delete_clipboard():
  global clipboard, updateID, index
  clipboard = []
  updateID, index = 0
  return str(updateID)


@app.get("/clipboard/available")
def get_clipboard_available():
  global updateID
  response.headers["Content-Type"] = "text/plain"
  return str(updateID)



if __name__ == '__main__':
  run(app, reloader=True, host='localhost', port=5000, server="gevent")