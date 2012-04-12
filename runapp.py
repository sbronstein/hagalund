import os

from waitress import serve
from pyramid.paster import get_app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app = get_app(os.path.join(os.path.dirname(__file__), 'production.ini'))

    serve(app, host='0.0.0.0', port=port)
