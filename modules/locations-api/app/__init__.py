from flask import Flask, jsonify, g, Response
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from kafka import KafkaConsumer
import json

db = SQLAlchemy()
TOPIC_NAME = 'location-events'
KAFKA_SERVER = 'localhost:9092'


def create_app(env=None):
    from .config import config_by_name
    from .routes import register_routes
    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])
    api = Api(app, title="UdaConnect Locations API", version="0.1.0")

    CORS(app)  # Set CORS for development

    register_routes(api, app)
    db.init_app(app)

    @app.route("/health")
    def health():
        return jsonify("healthy")

    @app.before_request
    def before_request():
        # setup Kafka consumer
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=[KAFKA_SERVER],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            auto_commit_interval_ms=2000,
            group_id='location_reader',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            consumer_timeout_ms=3000)

        # Setting Kafka to g enables us to use this
        # in other parts of our application
        g.kafka_consumer = consumer

    return app
