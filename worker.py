import dill
from flask import Flask, request

app = Flask(__name__)

class FuncStorer:
    def __init__(self):
        self.func = lambda : "No function loaded yet..."
    
    def setFunc(self, func):
        self.func = func
    
    def getFunc(self):
        return self.func

storer = FuncStorer()

@app.route("/load")
def load():
    storer.setFunc(dill.loads(request.form.get('func').encode('latin1')))
    return "Loaded function {}".format(storer.getFunc())

@app.route("/run")
def run():
    result = storer.getFunc()(*dill.loads(request.form.get('input').encode("latin1")))

    return str(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5001, debug=True)

