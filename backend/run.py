from flaskapp import create_app, db
from flaskapp.config import DevelopmentConfig

app = create_app(DevelopmentConfig)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
