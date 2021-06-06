"""
Name - IPSY Camara ( IP Camara for Desktop )
Version - 1.0 Alhpa
Author - @DimalJay
Github - https://githuub.com/Dimaljay

"""

import time
import cv2 
from flask import Flask, render_template, Response
from socket import gethostbyname, gethostname
import pyfiglet

app = Flask(__name__)

IP = gethostbyname(gethostname())
PORT = 9990
def intro():
    figlet = pyfiglet.Figlet()
    text = figlet.renderText("IPSY CAMARA")
    print(text)
    meta = """Name - IPSY Camara ( IP Camara for Desktop )
Version - 1.0 Alhpa
Author - @DimalJay
Github - https://githuub.com/Dimaljay
"""
    print(meta)

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    cap = cv2.VideoCapture(0)

    while(cap.isOpened()):
        ret, img = cap.read()
        if ret == True:
            img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)
        else: 
            break
        

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    intro()
    print(f"Starting server http://{IP}:{PORT}")
    app.run(host=IP, port=PORT)