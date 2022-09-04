import logging
import threading
import redis
import os
import time
import dill
from flask import Flask, request

app = Flask(__name__)

REDIS_HOST = os.environ.get("LATENT_STORE_SERVICE_PORT_6379_TCP_ADDR")
logging.info("Redis host at {}", REDIS_HOST)

while True:
    try: 
        r = redis.Redis(host=REDIS_HOST, port=6379)
        logging.info("Connected to redis!")
        break
    except: 
        logging.error("Failed to connect to redis, retrying")
        pass

@app.route("/num_workers")
def num_workers():
    return r.get("num_workers")

@app.route("/heartbeat/<id>")
def heartbeat(id):
    return str(r.get("worker_heartbeat_{}".format(id)))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000, debug=True)

    

