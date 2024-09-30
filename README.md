# Face Detection Server
An HTTP server for getting face bounding boxes in an image!

This is a very bare bones server, it is meant to be once piece of a greater server architecture. It does not implement any queues or caching, this should be done by the caller.

Running with Docker:

```
docker build -t face-detection-server .
docker run -p 5000:5000 face-detection-server
```

Running with Python:

```
pip install -r requirements.txt
python app.py
```
