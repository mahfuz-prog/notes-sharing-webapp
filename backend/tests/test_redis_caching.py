from flaskapp import redis_client
import flaskapp.main.service as main_service


def test_homepage_caching(app):
    redis_client.setex("total_char", 1, 500)
    data = main_service.homepage_stats()
    assert data["totalChar"] == 500
