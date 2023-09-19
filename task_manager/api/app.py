import os

from api.exceptions import InvalidStateTransition, ResourceNotFound
from api.tasks import initialize_routes as initialize_tasks
from flask import Flask, Response, jsonify
from flask_restful import Api


def create_app(database: str = os.environ["MONGODB_DATABASE"]) -> Flask:
    app = Flask(__name__)

    MONGO_URI = "mongodb://{}:{}@{}:{}/{}?authSource=admin".format(
        os.environ["MONGODB_USERNAME"],
        os.environ["MONGODB_PASSWORD"],
        os.environ["MONGODB_HOSTNAME"],
        os.environ["MONGODB_PORT"],
        database,
    )
    app.config["MONGO_URI"] = MONGO_URI

    app.url_map.strict_slashes = False
    register_error_handlers(app)

    api = Api(app)
    initialize_tasks(api)
    return app


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(Exception)
    def handle_exception_error(e: Exception) -> Response:
        return jsonify({"message": "Internal server error."}), 500

    @app.errorhandler(405)
    def handle_405_error(e: Exception) -> Response:
        return jsonify({"message": "Method not allowed."}), 405

    @app.errorhandler(403)
    def handle_403_error(e: Exception) -> Response:
        return jsonify({"message": "Forbidden error."}), 403

    @app.errorhandler(404)
    def handle_404_error(e: Exception) -> Response:
        return jsonify({"message": "Not Found error."}), 404

    @app.errorhandler(ResourceNotFound)
    def handle_object_not_found_error(e: Exception) -> Response:
        return jsonify({"message": str(e)}), 404

    @app.errorhandler(InvalidStateTransition)
    def handle_invalid_state_transition_error(e: Exception) -> Response:
        return jsonify({"message": str(e)}), 400
