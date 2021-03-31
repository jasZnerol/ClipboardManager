import clipboard.ClipboardManager as CBM
from network.server import app

if __name__ == "__main__":
  import threading
  threading.Thread(target=CBM.start_clipboardManager).start()
  app.run(port=5000)