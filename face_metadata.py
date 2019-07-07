from PIL import Image


class ImageMetaData(object):
    def __init__(self, name,  height, width):
        self.name = name
        self.height = height
        self.width = width

    @property
    def area(self):
        return self.width*self.height

    @property
    def file_name(self):
        path_delimeter='\\'
        slash_idx = self.name.rfind(path_delimeter)
        return self.name[slash_idx+len(path_delimeter):] if slash_idx > 0 else self.name


class FaceMetaData(object):
    def __init__(self, face_id, metadata, image_name):
        self.face_id = face_id
        self.metadata = metadata
        self.height = metadata['faceRectangle']['height']
        self.width = metadata['faceRectangle']['width']
        im = Image.open(image_name)
        im_width, im_height = im.size
        self.image = ImageMetaData(image_name, im_height, im_width)

    @property
    def face_relation(self):
        return float(self.height*self.width)/self.image.area

    def __str__(self):
        return "face_id: {0}\nmetadata: {1}"\
                   .format(self.face_id, self.metadata)
