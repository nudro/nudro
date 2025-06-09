from threading import Thread

import jetson_inference
import jetson_utils

from flask import Flask

app = Flask(__name__)


class Inferencer(Thread):
    def __init__(self):
        super().__init__()
        self.net = jetson_inference.detectNet("peoplenet-pruned")
        #self.net = jetson_inference.detectNet()
        self.camera = jetson_utils.videoSource('/dev/video0')  # usb webcam
        self.display = jetson_utils.videoOutput('rtp://10.136.89.17:1234')  # the big screen
#        self.display = jetson_utils.videoOutput('rtp://10.136.89.160:8554')  # my laptop
#        self.display = jetson_utils.videoOutput('rtp://10.136.89.30:1234')  # bighorn nx2
        self.is_on = True

    def run(self):
        while self.is_on:
            img = self.camera.Capture()
            detections = self.net.Detect(img)
            self.display.Render(img)

    def on(self):
        self.start()

    def off(self):
        self.is_on = False


class InferenceContainer:
    def __init__(self):
        self.inferencer = None

    def on(self):
        if not self.inferencer or not self.inferencer.is_alive():
            self.inferencer = Inferencer()
            self.inferencer.on()

    def off(self):
        if self.inferencer and self.inferencer.is_alive():
            self.inferencer.off()
            self.inferencer = None


inference_container = InferenceContainer()


@app.route("/on")
def on():
    print('on!')
    inference_container.on()
    return 'okay! inference container on!'


@app.route("/off")
def off():
    print('off!')
    inference_container.off()
    return 'okay! inference container off!'


if __name__ == "__main__":
    app.run(host='0.0.0.0')
#    uvicorn.run(app, host="0.0.0.0", port=5000)
