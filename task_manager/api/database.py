from flask_pymongo import PyMongo

mongo = PyMongo()


def initialize_mongodb(app):  # type: ignore
    mongo.init_app(app)
