from flask import Flask, request, render_template
from flask_ngrok import run_with_ngrok
from pyngrok import ngrok, conf
import cv2
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import module1, module2, module3

app = Flask(__name__)

# Thay thế YOUR_NGROK_AUTH_TOKEN bằng token của bạn
ngrok.set_auth_token('2XdC6VQLIBTYiopzNhcMTuSP5P5_6rNGgGCwLbbDmMrwerWht')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        image = request.files['image']
        image = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        original_image = image.copy()  # Save the original image
        operation = request.form.get('operation')
        value = int(request.form.get('value'))

        if operation == 'rotate':
            image = module1.rotate_image(image, value)
        elif operation == 'flip':
            image = module2.flip_image(image, value)
        elif operation == 'zoom':
            image = module3.zoom_image(image, value)

        _, buffer = cv2.imencode('.jpg', original_image)
        original_image = base64.b64encode(buffer).decode('utf-8')

        _, buffer = cv2.imencode('.jpg', image)
        image = base64.b64encode(buffer).decode('utf-8')

        return render_template('index.html', original_image=original_image, image=image)

    return render_template('index.html')


if __name__ == '__main__':
    public_url = ngrok.connect(5000).public_url
    print(" * Running on ngrok ", public_url)
    app.run(debug=True)