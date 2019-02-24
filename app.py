import subprocess
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
	proc = subprocess.Popen(["python -V"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	return out

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)
