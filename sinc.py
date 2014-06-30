import pymongo

from flask import Flask, jsonify, request
import os, sys
import uuid
import redis
import http

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

client = MongoClient('mongodb://localhost:27017/')


db = client['prod']

users = db['users']
foods = db['foods']
restaurants = db['restaurants']

import datetime

app = Flask(__name__)

def getNextSequence(name):
    ret = db['counters'].find_and_modify(
        query={"_id" : name},
        update={"$inc" : {"seq" : 1}},
        new=True
    )
    return ret['seq']


@app.route('/authenticate', methods = ['POST'])
def authenticate():
    body = request.form

    if body['method'] == 'login':
        email = body['email']
        password = body['password']

        user = users.find_one({"email" : email, "password" : password})

        if user:
            token = generate_token()
            users.update({"email" : email}, {"$set" : {"token" : token}})
            return jsonify("data", user)
        else:
            return jsonify({"error" : {"message" : "Invalid credentials."}})


    elif body['method'] == 'signup':
        email = body['email']
        password = body['password']
        if 'first_name' in body:
            first_name = body['first_name']
        if 'last_name' in body:
            last_name = body['last_name']
        if 'profile_picture' in body:
            profile_picture = body['profile_picture']


        if users.find_one({"email" : email}):
            return jsonify({"error" : {"message" : "Username taken."}})
        else:
            token = generate_token()
            user = {
                    "_id" : getNextSequence("userid"),
                    "email" : email,
                    "password" : password,
                    "first_name" : first_name,
                    "last_name" : last_name,
                    "token" : token
                    }
            users.insert(user)
            return jsonify({"data": user})


    elif body['method'] == 'facebook':
        facebook_token = body['facebook_token']


        # get email from graph api using token
        facebook_email = "hello"

        user = users.find_one({"facebook_email" : facebook_email})
        if user:
            return jsonify({"data" : user})
        else:
            user = users.find_one({"email" : facebook_email})
            return jsonify({"data" : None})

        return jsonify({"data" : {"token" : token}})


    elif body['method'] == 'twitter':

        return jsonify({"error" : {"message" : "twitter login not yet implemented"}})
    else:
        return jsonify({"error" : {"message" : "Failure bad auth."}})


# @app.route('/requestdata', methods = ['GET'])



def generate_token():
    return str(uuid.uuid1())



@app.route('/mainfeed', methods = ['GET'])
def photos():
    # get thumbnails for displaying
    authenticate_request()

    user_id = request.args['user_id']

    user_id = request.args['location']
    return jsonify({"data" : {}})



@app.route('/api/v1/user/<id>/mainfeed', methods = ['GET'])
def mainFeed():
    authenticate_request()


@app.route('/user', methods = ['GET'])
def user():
    authenticate_request()

    return jsonify({"data" : {}})


@app.route('/restaurant/<id>', methods = ['GET', 'POST'])
def restaurant(id):
    authenticate_request()

    return jsonify({"restaurant": {}})


@app.route('/menu/', methods = ['GET'])
def menu():
    authenticate_request()

    return jsonify({"menu" : {}})



def authenticate_request(http_method):
    return None

if __name__ == '__main__':
    app.run(debug = True)
