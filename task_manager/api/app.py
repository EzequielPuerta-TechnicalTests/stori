import os

from api.exceptions import ResourceNotFound
from api.tasks import initialize_routes as initialize_tasks
from flask import Flask, jsonify
from flask_restful import Api


def create_app():
    app = Flask(__name__)

    MONGO_URI = "mongodb://{}:{}@{}:{}/{}?authSource=admin".format(
        os.environ["MONGODB_USERNAME"],
        os.environ["MONGODB_PASSWORD"],
        os.environ["MONGODB_HOSTNAME"],
        os.environ["MONGODB_PORT"],
        os.environ["MONGODB_DATABASE"],
    )
    app.config["MONGO_URI"] = MONGO_URI

    app.url_map.strict_slashes = False
    register_error_handlers(app)

    api = Api(app, catch_all_404s=True)
    initialize_tasks(api)
    return app


def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception_error(e):
        return jsonify({"msg": f"Internal server error: {str(e)}"}), 500

    @app.errorhandler(405)
    def handle_405_error(e):
        return jsonify({"msg": "Method not allowed"}), 405

    @app.errorhandler(403)
    def handle_403_error(e):
        return jsonify({"msg": "Forbidden error"}), 403

    @app.errorhandler(404)
    def handle_404_error(e):
        return jsonify({"msg": "Not Found error"}), 404

    @app.errorhandler(ResourceNotFound)
    def handle_object_not_found_error(e):
        return jsonify({"msg": str(e)}), 404
