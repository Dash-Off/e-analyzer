import json
import socket
import inspect
from threading import Thread

SIZE = 1024 * 3

class RPCServer:
  def __init__(self, host, port) -> None:
    self.host = host
    self.port = port
    self.address = (host, port)
    self._methods = {}
  
  def register_call(self, function):
    try:
      self._methods.update({function.__name__: function})
    except:
      raise Exception("Registration failed: Non-function")
  
  def register_instance(self, instance=None):
    try:
      for call_name, call in inspect.getmembers(instance, predicate=instance.ismethod):
        if not call_name.startswith("__"):
          self._methods.update({call_name: call})
    except:
      raise Exception("Registering instance failed: Non-RPC class")
  
  def __handle__(self, client, address):
    print(f"Handling request from {address}")
    call_name = args = kwargs = None
    while True:
      try:
        data = client.recv(SIZE).decode()
        data = json.loads(data)
        call_name = data["name"]
        args = data["args"].values()
        kwargs = data["args"]
      except Exception as e:
        #raise e
        print(f"Client {address} disconnected")
        break
      print(f"Invoked: {call_name}({args})")
      response = None
      try:
        Thread(target=self._methods[call_name], args=args).start()
        #response = self._methods[call_name](*args)
      except Exception as e:
        client.sendall(json.dumps(str(e)).encode())
      else:
        response = {"message": "Job received"} if not response else response
        client.sendall(json.dumps(response).encode())

    print("Completed request from {address}")
    client.close()
  
  def run(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
      sock.bind(self.address)
      sock.listen()

      print(f"Server {self.address} running")
      while True:
        try:
          client, address = sock.accept()
          Thread(target=self.__handle__, args=[client, address]).start()
        except KeyboardInterrupt:
          print(f"Server {self.address} interrupted")
          break
