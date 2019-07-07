# Common Face Service
Returns the best image of the most common face in a list of images.

## Usage
Run the service:
```bash
$ python face_service.py
```
Run a simple client:
```bash
$ curl --header "Content-Type: application/json" --request GET --data "{\"images\":[<list of images>]}" http://127.0.0.1:5000/common_faces
```
