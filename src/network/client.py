import requests
import urllib3
import pickle

http = urllib3.PoolManager()

base_url = "http://localhost:5000"
updateID = 0


def update_exists():
  return str(updateID) == requests.get(f"{base_url}/clipboard/available").text

  
def get_clipboard():
  return  http.request("GET", f"{base_url}/clipboard").data
  
  
def update_clipboard(data):
  requests.post(f"{base_url}/clipboard", data=pickle.dumps(data))
  updateID += 1

def clear_clipboard():
  requests.delete("f{base_url}/clipboard")
  updateID = 0


data = {(13, 'f"{base_url}/clipboard"'), (1, b'f"{base_url}/clipboard"'), (7, b'f"{base_url}/clipboard"')}
# update_clipboard(data)
get_clipboard()
print("reahced")