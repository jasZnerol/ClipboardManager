import client
conn = client.HTTPConnection("localhost", 5000)
conn.putrequest("GET", "/clipboard")
conn.endheaders(encode_chunked=True)
res = conn.getresponse()


print(res.read())