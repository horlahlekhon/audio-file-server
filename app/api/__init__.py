from flask_restx import Api
from flask import Blueprint

from .audio.controller import api as audio_ns

# Import controller APIs as namespaces.
api_bp = Blueprint("audio", __name__)

api = Api(api_bp, title="Audio server", description="Main routes.")

# API namespaces
api.add_namespace(audio_ns)