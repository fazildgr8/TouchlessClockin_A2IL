from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api

import json
from bson import json_util

from json import dumps
from flask_jsonpify import jsonify
from PIL import Image
import cv2

import numpy as np
from binascii import a2b_base64
import db

#########################
import face_recognition as fr
import face_functions 
import io
import base64



app = Flask(__name__)
api = Api(app)


CORS(app)

@app.route("/")
def hello():
    return jsonify({'text':'Hello User, the backend is up and ready!'})


class Person_Detail(Resource):



    def post(self):
        json_data = request.get_json(force=True)
        img=json_data['image']
        b=img
        z = b[b.find('/9'):]
        im = Image.open(io.BytesIO(base64.b64decode(z))).save('temp.jpg')
        image = cv2.imread('temp.jpg')

        found_name,distance, face_encoding = face_functions.recognize(image)

        print('In Post')
        print('In Post')
        status=""
        if found_name == 'Unknown':
            status = "Face Not Recognised"
        elif found_name == 'No Faces':
            status = "No-Face"
        else:
            status = "Logged-In"
        return jsonify({'empName':found_name,'status':status})

    def get(self):
        return jsonify({'name':'Gautam','status':'Recognised'})


class LogIn(Resource):
    def post(self):
        login_data=request.get_json(force=True)
        print("In Login")
        return jsonify({'email':'user@email.com','password':'12345','status':'True','msg':''})

class Employee(Resource):

    def post(self):
        emp_data=request.get_json(force=True)
        print("In Employee Post")
        db.saveEmp(emp_data)
        return jsonify({'status':'submitted'})

    def get(self):
        print("In Employee GET")
        emps = db.getAllEmp()
        json_docs = [json.dumps(doc, default=json_util.default) for doc in emps]
        return jsonify(json_docs)



api.add_resource(Person_Detail, '/detail')
api.add_resource(LogIn, '/login')
api.add_resource(Employee, '/emp')

if __name__ == '__main__':
   app.run(port=443, host = "0.0.0.0",ssl_context='adhoc')
# ,ssl_context='adhoc'
