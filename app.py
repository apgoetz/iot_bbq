from flask import Flask
from flask import render_template
from flask import send_file
import io
import matplotlib
matplotlib.use('cairo') 
import matplotlib.pyplot as plt
import numpy as np
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/latest.png")
def latest():
    N = 1024
    t = np.linspace(0,1,N)
    y = np.random.randn(N)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(t,y)
    ax.set_xlabel('time')
    ax.set_ylabel('temp')
    ax.set_title('Current Temperature')
    
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    
    return send_file(buf)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
