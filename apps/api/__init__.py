from flask import Blueprint, jsonify

from packages.exceptions.exceptions import AivenApiException

api = Blueprint('api', __name__)


@api.errorhandler(AivenApiException)
def aiven_exception_handlers(e):
    return jsonify(e.to_dict()), e.status_code
