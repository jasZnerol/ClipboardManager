from network.request import Request
import pickle

updateID = 0

client = Request("localhost", 5000)

def update_exists():
  res = client.request("GET", "/clipboard/available")
  return str(updateID) == res["body"]

  
def get_clipboard():
  res = client.request("GET", "/clipboard")
  return res["body"]
  
  
def update_clipboard(data):
  global updateID
  client.request("POST", "/clipboard", data=pickle.dumps(data))
  updateID =+  1

def clear_clipboard():
  client.requests("DELETE", "clipboard")
  updateID = 0




import time
start = time.time()
data = {(13, 'f"{base_url}/clipbasdasdoard"'), (1, b'f"{base_url}/casdasdlipboard"'), (7, b'f"{base_url}/cliasdasdpboard"')}
update_clipboard(data)
print(get_clipboard())
print(time.time() - start, "seconds")