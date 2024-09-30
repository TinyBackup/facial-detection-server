import flask
from retinaface import RetinaFace
import cv2
import numpy as np

app = flask.Flask(__name__)

@app.route('/detect_faces', methods=['POST'])
def hash_image():
    if 'image' not in flask.request.files:
        return flask.jsonify({'error': 'No image file provided'}), 400
    
    image_file = flask.request.files['image']
    image_bytes = image_file.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Compute the perceptual hash of the image
    faces = retinaface_extract_faces(image)
    
    return flask.jsonify({'face_bounds': str(faces)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


# A modification of the retinaface package's extract_faces function so that
# it will return the cropped faces and also the cooordinates of the face
def retinaface_extract_faces(
    img: np.ndarray,
) -> list:
    resp = []

    # Validate image shape
    if len(img.shape) != 3 or np.prod(img.shape) == 0:
        raise ValueError("Input image needs to have 3 channels at must not be empty.")

    obj = RetinaFace.detect_faces(
        img_path=img, threshold=0.9, model=None, allow_upscaling=True
    )

    if not isinstance(obj, dict):
        return resp

    for _, identity in obj.items():
        facial_area = identity["facial_area"]

        left = facial_area[0]
        top = facial_area[1]
        width = facial_area[2] - left
        height = facial_area[3] - top

        resp.append(
            {"ltwh": f"{left},{top},{width},{height}"}
        )

    return resp
