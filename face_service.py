from flask import Flask, jsonify, request

from face_api import FaceAPI

app = Flask(__name__)


@app.route('/common_faces', methods=['GET'])
def common_faces():
    request_json = request.get_json()
    if 'images' not in request_json:
        return jsonify({'error': 'Missing images in request'})
    cface = FaceAPI(request_json.get('images'))
    similar_faces_groups = cface.get_max_face_groups()
    best_face_id = cface.get_best_face([face_id for similar_group in similar_faces_groups for face_id in similar_group] or
                                   cface.faces.keys())
    return jsonify(
        cface.get_face_image(best_face_id)
    )


if __name__ == '__main__':
    app.run()