from flask import Blueprint

journey_bp = Blueprint("journey_bp", __name__)

from app.journey import routes