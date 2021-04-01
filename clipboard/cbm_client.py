from network.request import Request
import pickle

updateID = 0

client = Request("localhost", 5000)

def update_exists():
  res = client.request("GET", "/clipboard/available")
  return str(updateID) == res["body"]

  
def get_clipboard():
  res = client.request("GET", "/clipboard")
  return pickle.loads(res["body"])
  
  
def update_clipboard(data):
  global updateID
  client.request("POST", "/clipboard", data=pickle.dumps(data))
  updateID =+  1

def clear_clipboard():
  client.request("DELETE", "clipboard")
  updateID = 0

def benchmark():
  times = []
  requests = 1000
  prct = 0
  import time
  for i in range(requests):
    start = time.time()
    data = {(13, 'f"{base_url}/clipbasdasdoard"'), (1, b'f"{base_url}/casdasdlipboard"'), (7, b'f"{base_url}/cliasdasdpboard"')}
    update_clipboard(data)
    get_clipboard()
    times.append(time.time() - start)
    if (i % 100 == 0):
      clear_clipboard()
      print("{0} of requests finished".format(i))

  print("The average request took {0} seconds".format(sum(times) / len(times)))
  print("Longest request was the {0}-th request with {1} seconds.".format(times.index(max(times)), max(times)))
  print("Shortes request was the {0}-th request with {1} seconds.".format(times.index(min(times)), min(times)))
  print("Total duration for all {0} requests was {1} seconds".format(requests, sum(times)))

benchmark()