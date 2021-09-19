from flask import Blueprint

test_content = None

test_blueprint = Blueprint(
    'test_bp', __name__
)


@test_blueprint.route('/test')
def test():
    return test_content