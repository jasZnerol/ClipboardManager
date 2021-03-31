from flask import Blueprint

router = Blueprint('extern_router', __name__)

@router.route("/")
def extern_router_index():
  return "This route is handeled by an extern router"
