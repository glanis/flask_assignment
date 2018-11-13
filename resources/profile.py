from flask_restful import Resource, reqparse
from flask import jsonify
#
from flask_login import login_required
from models.profile import ProfileModel
from flask_jwt import jwt_required


class Profile(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('profession',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('age',
        type=int,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('address',
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    @jwt_required()
    def get(self, name):
        print(name)
        profile = ProfileModel.find_by_name(name)
        if profile:
            return profile.json()
        return {'message': 'profile not found'}, 404

    def post(self, name):
        data = Profile.parser.parse_args()
        profile = ProfileModel.find_by_name(name)
        if profile is None:
            profile = ProfileModel(name,  **data)
            profile.save_to_db()
            return jsonify({"message": "Profile Created"})
        return jsonify({"message": "Profile with this name already exists"})

    @jwt_required()
    def delete(self, name):
        profile = ProfileModel.find_by_name(name)
        if profile:
            profile.delete_from_db()
        return {'message': 'Item deleted'}, 200

    @jwt_required()
    def put(self, name):
        data = Profile.parser.parse_args()

        profile = ProfileModel.find_by_name(name)

        if profile is None:
            profile = ProfileModel(name, **data)
        if data['profession']:
            profile.profession = data['profession']
        if data['age']:
            profile.age = data['age']
        if data['address']:
            profile.address = data['address']

        profile.save_to_db()
        return profile.json()


class ProfileList(Resource):
    def get(self):
        return jsonify({'Profiles': list(map(lambda x: x.json(), ProfileModel.query.all()))})