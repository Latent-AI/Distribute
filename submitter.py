import dill
import requests

def example(x, y):
    return x - y

func_pkl = dill.dumps(example)

resp = requests.get("http://127.0.0.1:5001/load", data={'func': func_pkl.decode('latin1')})
print(resp.content)

input_pkl = dill.dumps((5, 45))

resp = requests.get("http://127.0.0.1:5001/run", data={'input': input_pkl.decode('latin1')})
print(resp.content)