from flask_pymongo import PyMongo

mongo = PyMongo()


def initialize_mongodb(app):
    mongo.init_app(app)
