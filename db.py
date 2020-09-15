import pymongo
from pymongo import MongoClient
import json
from bson import json_util
import io
from PIL import Image
import base64
from face_functions import *
import cv2
import numpy as np

cluster = MongoClient("mongodb+srv://gautam:123@cluster0.esinm.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority")
db  = cluster["employee"]
collection = db["timeclock"]




def convertToImage(img):
    b=img
    z = b[b.find('/9'):]
    im = Image.open(io.BytesIO(base64.b64decode(z))).save('result.jpg')
    return im



def saveEmp(obj):
    convertToImage(obj['face'])

    with open("result.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    img = cv2.imread('result.jpg')
    face_encoding = get_encoding(img).tolist()

    dict = {
    "companyName" : obj['companyName'],
    "empName"     : obj['empName'],
    "email"       : obj['email'],
    "Position"    : obj['Position'],
    "empId"       : obj['empId'],
    "faceId"      : face_encoding ,
    "face"        : encoded_string,
    "checkin": {
                "date": "",

                "timestatus":[{
                             "logIn":"",
                             "logOut":"",
                             "status":"",
                             "face":""
                             }]
                }
    }


    # print(dict)
    collection.insert_one(dict)

def getByEmail(email):
    query = { "email": email }
    mydoc = collection.find_one(query)
    return mydoc

def getByFaceId(faceid):
    query = { "faceId": faceid }
    mydoc = collection.find_one(query)
    return mydoc

def getAllEmp():
    mydocs=collection.find()
    main_list = []
    for doc in mydocs:
        main_list.append(doc)
    print('Number of Users - ',len(main_list))
    # Returns a list of dictionaries
    return main_list

def getFaceIdlist():
    mydocs=collection.find()
    main_list = []
    for doc in mydocs:
        main_list.append(doc['faceId'])
    print('Number of Users - ',len(main_list))
    # Returns a List of Face ID
    return main_list

def getNamelist():
    mydocs=collection.find()
    main_list = []
    for doc in mydocs:
        main_list.append(doc['empName'])
    print('Number of Users - ',len(main_list))
    # Returns a List of Face ID
    return main_list