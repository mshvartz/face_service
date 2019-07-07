

from settings import SUBSCRIPTOPN_KEY, FACE_DETECT_BASE_URL
import cognitive_face as CF
from face_metadata import FaceMetaData


class FaceAPI(object):
    def __init__(self, image_files):
        self.faces = {}
        CF.Key.set(SUBSCRIPTOPN_KEY)
        CF.BaseUrl.set(FACE_DETECT_BASE_URL)
        self.get_faces_data(image_files)

    def get_faces_data(self, image_files):
        for image in image_files:
            faces = CF.face.detect(image, landmarks=True, attributes='age,gender,headPose,smile,facialHair,glasses,'
                                                                     'emotion,hair,makeup,occlusion,accessories,blur,'
                                                                     'exposure,noise')
            for face in faces:
                face_id = face['faceId']
                self.faces[face_id] = FaceMetaData(face_id, face, image)

    def get_similar_faces(self, face_id, face_ids=[], max_faces_batch=1000, confidence=0.6):
        if max_faces_batch > 1000:
            raise Exception("max_faces_batch must be less than 1000")
        face_ids = face_ids or self.faces.keys()
        similar_faces = []
        for i in xrange(len(face_ids)/max_faces_batch + 1):
            similar_faces.extend(CF.face.find_similars(face_id=face_id,
                                                       face_ids=face_ids[i*max_faces_batch:min(len(face_ids),
                                                                                               (i+1)*max_faces_batch)],
                                                       max_candidates_return=max_faces_batch))
        return [s_face['faceId'] for s_face in similar_faces if s_face['confidence'] >= confidence]

    def get_max_face_groups(self):
        face_ids = self.faces.keys()
        len_face_ids = len(face_ids)
        if len_face_ids < 2:
            return [face_ids]
        if len_face_ids == 2:
            return [face_ids] if CF.face.verify(face_ids[0], face_ids[1])['isIdentical'] else []
        if len_face_ids < 1000:
            groups_res = CF.face.group(face_ids)
            i = 0
            for i in range(len(groups_res['groups'])):
                if groups_res['groups'][i] < groups_res['groups'][0]:
                    break
            return groups_res['groups'][:i+1]
        max_similar = 0
        max_similar_faces = []
        for i in range(len(self.faces.keys())):
            cur_similar_faces = self.get_similar_faces(face_ids[i], face_ids[i:])
            max_similar = max(max_similar, len(cur_similar_faces))
            max_similar_faces.append(cur_similar_faces)
        return [sf for sf in max_similar_faces if len(sf) == max_similar]

    def get_best_face(self, face_ids):
        max_relation = 0
        best_face_id = None
        for face_id in face_ids:
            if face_id not in self.faces:
                raise Exception("Missing metadata for face_id: %s" % face_id)
            if self.faces[face_id].face_relation > max_relation:
                max_relation = self.faces[face_id].face_relation
                best_face_id = face_id
        return best_face_id

    def get_face_image(self, face_id):
        if face_id not in self.faces:
            raise Exception("Missing metadata for face_id: %s" % face_id)
        face_data = self.faces[face_id]
        return {
            'face_metadata': face_data.metadata,
            'image_file_name': face_data.image.file_name
        }
