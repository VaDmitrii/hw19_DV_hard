from flask import request
from flask_restx import Resource, Namespace
from marshmallow import Schema, fields

from hw19_DV_hard.helpers.decorators import auth_required, admin_required
from hw19_DV_hard.implemented import movie_service

movie_ns = Namespace('movies')


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()


@movie_ns.route('/')
class MoviesView(Resource):

    @auth_required
    def get(self):
        director = request.args.get("director_id")
        genre = request.args.get("genre_id")
        year = request.args.get("year")
        filters = {
            "director_id": director,
            "genre_id": genre,
            "year": year,
        }
        all_movies = movie_service.get_all(filters)
        res = MovieSchema(many=True).dump(all_movies)
        return res, 200

    @admin_required
    def post(self):
        req_json = request.json
        movie = movie_service.create(req_json)
        return "", 201, {"location": f"/movies/{movie.id}"}


@movie_ns.route('/<int:mid>')
class MovieView(Resource):

    @auth_required
    def get(self, mid):
        b = movie_service.get_one(mid)
        sm_d = MovieSchema().dump(b)
        return sm_d, 200

    @admin_required
    def put(self, mid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = mid
        movie_service.update(req_json)
        return "", 204

    @admin_required
    def delete(self, mid):
        movie_service.delete(mid)
        return "", 204
