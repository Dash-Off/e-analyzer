from flask import Flask, request
from client import RPCClient


app = Flask(__name__)


@app.route("/get_scores")
def get_scores():
  body = {"raw": "When the young people returned to the ballroom, it presented a decidedly changed appearance. Instead of an interior scene, it was a winter landscape.The floor was covered with snow-white canvas, not laid on smoothly, but rumpled over bumps and hillocks, like a real snow field. The numerous palms and evergreens that had decorated the room, were powdered with flour and strewn with tufts of cotton, like snow. Also diamond dust had been lightly sprinkled on them, and glittering crystal icicles hung from the branches.At each end of the room, on the wall, hung a beautiful bear-skin rug.These rugs were for prizes, one for the girls and one for the boys. And this was the game.The girls were gathered at one end of the room and the boys at the other, and one end was called the North Pole, and the other the South Pole. Each player was given a small flag which they were to plant on reaching the Pole.This would have been an easy matter, but each traveller was obliged to wear snowshoes.", "dashOffId": "123"}
  server = RPCClient('0.0.0.0', 8080)
  server.connect()

  print(server.getResult(raw=body["raw"], dashOffId=body["dashOffId"]))

  server.disconnect()
  return {"message": "JOb recieved"}
