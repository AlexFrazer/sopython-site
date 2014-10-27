from flask import Blueprint

bp = Blueprint('chat', __name__)

@bp.record_once
def register(state):
    from sopy.chat import starboard
