from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
# data: list = json.load(open(json_url))

with open(json_url, 'r') as file:
    data = json.load(file)

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return picture
    return {"message": "picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.json

    if not new_picture:
        return {"Message": "Invalid input parameter"}, 422

    for picture in data:
        if new_picture["id"] == picture["id"]:
            return {"Message": f"picture with id {new_picture['id']} already present"}, 302

    try:
        data.append(new_picture)

        with open(json_url, 'w') as file:
            json.dump(data, file, indent=4)

    except NameError:
        return {"Message": "data not defined"}, 500

    return jsonify(new_picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_picture = request.json
    for picture in data:
        if picture["id"] == id:
            picture.update(new_picture)

            with open(json_url, 'w') as file:
                json.dump(data, file, indent=4)

            return {"message":f"{id}"}, 200
    return {"message": "picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for picture in data:
        if picture["id"] == id:
            data.remove(picture)

            with open(json_url, 'w') as file:
                json.dump(data, file, indent=4)

            return {"message":"no content found"}, 204

    return {"message": "picture not found"}, 404
