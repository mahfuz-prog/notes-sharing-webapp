from flaskapp import create_app
from flaskapp.config import ProductionConfig

app = create_app(ProductionConfig)
