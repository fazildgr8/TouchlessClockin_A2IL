import cv2
import numpy as np 
import face_recognition as fr
import db


def get_encoding(img):
    rgb_frame = img[:, :, ::-1] # Convert BGR to RGB
    face_locations = fr.face_locations(rgb_frame) # Get list of Face Locations
    face_encodings = fr.face_encodings(rgb_frame, face_locations) # List of Face encodings
    print(face_encodings)
    return face_encodings[0]


def recognize(img):
    known_face_names = db.getNamelist()
    known_face_encodings = db.getFaceIdlist()

    rgb_frame = img[:, :, ::-1] # Convert BGR to RGB
    face_locations = fr.face_locations(rgb_frame) # Get list of Face Locations
    face_encodings = fr.face_encodings(rgb_frame, face_locations) # List of Face encodings
    print(face_encodings)
        # Loop the found face locations and encodings throught the Known Faces
    distance = 0
    if len(face_locations) > 0:
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = fr.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            # the known face with the smallest distance to the new face

            face_distances = fr.face_distance(known_face_encodings, face_encoding)
            if face_distances.any():
                best_match_index = np.argmin(face_distances)
                distance = face_distances[best_match_index]
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
            else:
                best_match_index = 0
            location = [top, right, bottom, left]
            print('Face Found - ['+name+'] -',distance)
            if(distance > 0.4):
                name = 'Unknown'
            return name,distance,face_encodings
    else:
        return 'No Faces','0.0',face_encodings