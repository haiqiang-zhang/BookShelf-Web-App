from flask import Blueprint



test_blueprint = Blueprint(
    'test_bp', __name__
)

test_content = "Loading"


def get_test_content(content):
    global test_content
    test_content = content

@test_blueprint.route('/test')
def test():
    return test_content