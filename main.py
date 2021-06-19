from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databse.db' #relative path
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        '''
        Object representation
        '''
        return f"Video(name = {name}, views = {views}, likes = {likes})"

# db.create_all()

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Please enter the name of the video", required=True)
video_put_args.add_argument("views", type=int, help="Please enter the number of views on the video", required=True)
video_put_args.add_argument("likes", type=int, help="Plese enter the number of likes on the video", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Please update the name of the video")
video_update_args.add_argument("views", type=int, help="Please update the number of views on the video")
video_update_args.add_argument("likes", type=int, help="Plese update the number of likes on the video")


'''
Defining the fields in the dictionary model which can be returned
'''
resource_fields = {
        'id': fields.String,
        'name': fields.Integer,
        'views': fields.Integer,
        'likes': fields.Integer
}

'''
Resource:
Overwrite the wanted method
The API has to return json serializable objects, like a dictionary.
Pass arguments (int, string) in the URL
'''

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()

        if not result:
            abort(404, message="A video with the specified ID doesn't exist in the database :/")

        '''
        Querying the database returns a database instance which isn't json serializable.
        Using resource fields and marshallwith
        '''
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])

        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="An entry with the specified Video ID already exists :/")

        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()

        if not result:
            abort(404, message="A video with the specified ID doesn't exist in the database :/")

        if args['name']:
            result.name = args['name']

        if args['views']:
            result.name = args['views']

        if args['likes']:
            result.likes = args["likes"]

        '''
        The if is triggered as long as it isn't a None type object.
        '''

        db.session.commit()

        return result

    def delete(self, video_id):
        self.video_id_exists(video_id)
        del videos[video_id]
        return '', 204


# class helloworld(Resource):
#     def get(self, dum):
#         return {"s": dum}
#
# api.add_resource(hw, "/helloworld/<int:dum>")

# videos = {}

# class VideoWithoutDatabase(Resource):
#     def video_id_exists(self, video_id):
#         if video_id not in videos:
#             abort(404, message="Not an existing video ID :/")
#
#     def video_id_doesnt_exist(self, video_id):
#         if video_id in videos:
#             abort(409, message="This is an existing video ID :/")
#
#     def get(self, video_id):
#         self.video_id_exists(video_id)
#         '''
#         Sent information is visible in the url
#         '''
#         return videos[video_id]
#
#     def put(self, video_id):
#         self.video_id_doesnt_exist(video_id)
#         args = video_put_args.parse_args()
#         print('!', flush=True)
#         videos[video_id] = args
#         print('!!', flush=True)
#         return videos[video_id], 201
#         '''
#         The sent information can be passed as data,
#         not publicly visible in the url.
#         '''
#
#     def delete(self, video_id):
#         self.video_id_exists(video_id)
#         del videos[video_id]
#         return '', 204

api.add_resource(Video, "/video/<int:video_id>")
'''
Resource route - how the endpoint resource can be accessed.
'''

if __name__ == "__main__":
    app.run(debug=True)
