import flask
from retinaface import RetinaFace
import cv2
import numpy as np

app = flask.Flask(__name__)

@app.route('/detect_faces', methods=['POST'])
def detect_faces():
    if 'image' not in flask.request.files:
        return flask.jsonify({'error': 'No image file provided'}), 400
    
    image_file = flask.request.files['image']
    image_bytes = image_file.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    faces = []

    # Validate image shape
    if len(image.shape) != 3 or np.prod(image.shape) == 0:
        raise ValueError("Input image needs to have 3 channels at must not be empty.")

    obj = RetinaFace.detect_faces(
        img_path=image, threshold=0.9, model=None, allow_upscaling=True
    )

    if isinstance(obj, dict): 
        for _, identity in obj.items():
            facial_area = identity["facial_area"]

            left = facial_area[0]
            top = facial_area[1]
            width = facial_area[2] - left
            height = facial_area[3] - top

            faces.append(
                {"ltwh": f"{left},{top},{width},{height}"}
            )
    
    return flask.jsonify({'face_bounds': faces})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

