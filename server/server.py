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

# Server state
clipboard = []
index = 0
updateID = 0



"""
#############################
######## Clipboard###########
#############################
"""

# Return the clipboard as a serialized object 
@app.get("/clipboard")
def get_clipboard():
  global clipboard, updateID, index
  response.headers["Content-Type"] = "application/python-pickle"
  response.headers["updateID"] = updateID
  # Serialize clipboard to sent to client
  return pickle.dumps(clipboard)


# Updated the shared clipboard by appending it with the deserialization of the body and return the new ID of the current update
@app.post("/clipboard")
def post_clipboard():
  global clipboard, updateID, index
  response.headers["Content-Type"] = "application/python-pickle"
  update = pickle.loads(request.body.read())
  clipboard.append(update)
  updateID += 1 
  return pickle.dumps(updateID)

# Clear the entire clipboard if no index is given and return the new ID of the current update serialized.
# If the index is given via a query parameter remove that particular element from the clipboard memory.
# If the index is invalid return 400 bad request and a serialized -1 for the updateID
@app.delete("/clipboard")
def delete_clipboard():
  global clipboard, updateID, index
  response.headers["Content-Type"] = "application/python-pickle"
  # Found an index therefore only delete one
  if "index" in request.query:
    try:
      i = int(request.query["index"])
    except Exception:
      i = -1
    # Invalid index
    if i < 0 or i >= len(clipboard):
      response.status = 400
      return pickle.dumps(-1)
    # Valid index
    else:
      index = i
      clipboard.pop(i)
      updateID += 1
      return pickle.dumps(updateID)
  # No index found clear the entire clipboard
  else:
    clipboard = []
    updateID, index = 0, 0
    return pickle.dumps(updateID)



"""
#############################
########## Index ############
#############################
"""

# Update the index of the active element of the clipboard memory and return the new value serialized
# The index is given via the body.
# If the index is invalid return 400 bad request and a serialized -1 for the index.
@app.post("/index")
def post_index():
  global index
  response.headers["Content-Type"] = "application/python-pickle"
  index = pickle.loads(request.body.read())
  if index < 0  or index >= len(clipboard):
    return pickle.dumps(-1)
  return pickle.dumps(index)


"""
#############################
######## Available ##########
#############################
"""

# Return the current ID of the update and the index serialized in a tuple
@app.get("/clipboard/available")
def get_clipboard_available():
  global updateID, index
  response.headers["Content-Type"] = "application/python-pickle"
  return pickle.dumps((updateID, index))



if __name__ == '__main__':
  run(app, reloader=True, host='localhost', port=5000, server="gevent")