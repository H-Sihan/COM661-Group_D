from flask import Flask
from flask_cors import CORS

from businesses.businesses import businesses_bp
from reviews.reviews import review_bp
from auth.auth import auth_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(businesses_bp)
app.register_blueprint(review_bp)
app.register_blueprint(auth_bp)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
