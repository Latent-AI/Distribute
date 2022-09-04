import logging
import threading
import redis
import os
import time

# import dill
# from flask import Flask, request

# app = Flask(__name__)

# class FuncStorer:
#     def __init__(self):
#         self.func = lambda : "No function loaded yet..."
    
#     def setFunc(self, func):
#         self.func = func
    
#     def getFunc(self):
#         return self.func

# storer = FuncStorer()

# @app.route("/load")
# def load():
#     storer.setFunc(dill.loads(request.form.get('func').encode('latin1')))
#     return "Loaded function {}".format(storer.getFunc())

# @app.route("/run")
# def run():
#     result = storer.getFunc()(*dill.loads(request.form.get('input').encode("latin1")))

#     return str(result)

def init_worker(r):
    worker_lock = redis.lock.Lock(r, "worker_lock")
    worker_lock.acquire()
    logging.info("Acquired lock")

    num_workers = r.get("num_workers")
    if not num_workers:
        num_workers = 0
    else:
        num_workers = int(num_workers)
        
    num_workers += 1
    r.set("num_workers", num_workers)

    worker_lock.release()
    logging.info("Released lock")

    return num_workers

def heartbeat(r, worker_id):
    heartbeat = 0
    while True:
        logging.info("Idling...")
        heartbeat += 1
        r.set("worker_heartbeat_{}".format(worker_id), heartbeat)
        time.sleep(10)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    # app.run(host="0.0.0.0", port = 5000, debug=True)
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

    worker_id = init_worker(r)

    heartbeat_thread = threading.Thread(target=heartbeat, args=(r, worker_id,))
    heartbeat_thread.start()

    
        
    

    

