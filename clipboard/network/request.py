import network.client as client


class Request(object):

  def __init__(self, host : str, port : int, default_headers = None): # Anotate dict for default_headers
    self.host = host
    self.port = port
    self.default_headers = {
      "Content-Type": "text/plain; charset=UTF8",
    }
    self.headers = self.default_headers

  def set_header(key : str, value : str):
    self.headers[key] = value


  def request(self, method : str, route : str, data : str = None) -> client.HTTPResponse:
    allowed_methods = [
      "GET",
      "POST",
      "PUT",
      "DELETE"
    ]
    if (method not in allowed_methods):
      return None

    # Create connection and initialize request
    conn = client.HTTPConnection(self.host, self.port)

    # Create request and reset headers for next request
    conn.request(method, route, body=data, headers=self.headers)  
    self.headers = self.default_headers

    # Signal that the request is finished and return the response
    res = conn.getresponse()
    response = {
      "status": res.status,
      "headers": res.getheaders(),
      "body": res.read()
    }
    conn.close()
    return response


# r = Request("localhost", 5000)
# print(r.default_headers)
# print(r.request("GET", "/clipboard").read())

# import pickle
# conn = client.HTTPConnection("localhost", 5000)
# conn.request("GET", "/clipboard", body=None, headers={})  
# res = conn.getresponse()
# print(pickle.loads(res.read()))
# conn.close()

