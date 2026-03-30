"""Flask application entrypoint."""

import logging
import os
from datetime import UTC, datetime

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from marshmallow import ValidationError as MarshmallowValidationError

from config import Config
from extensions import db
from routes import ai_bp, forms_bp, responses_bp
from services.errors import AppError

# Load .env file for local development
load_dotenv()



def create_app(config_object=Config):
	app = Flask(__name__)
	app.config.from_object(config_object)

	configure_logging(app)
	register_extensions(app)
	register_blueprints(app)
	register_error_handlers(app)
	register_request_hooks(app)

	# Allow frontend origin (set CORS_ORIGINS env var in production)
	allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
	CORS(app, origins=allowed_origins, supports_credentials=True)

	# Auto-create tables on startup
	with app.app_context():
		db.create_all()

	@app.route("/")
	def home():
		return {"message": "API is running 🚀"}

	@app.route("/health")
	def health_check():
		return jsonify({"status": "ok", "timestamp": datetime.now(UTC).isoformat()}), 200

	return app


def configure_logging(app: Flask):
	log_level = getattr(logging, app.config.get("LOG_LEVEL", "INFO").upper(), logging.INFO)
	logging.basicConfig(
		level=log_level,
		format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
	)
	app.logger.setLevel(log_level)


def register_extensions(app: Flask):
	db.init_app(app)


def register_blueprints(app: Flask):
	app.register_blueprint(forms_bp)
	app.register_blueprint(responses_bp)
	app.register_blueprint(ai_bp)


def register_request_hooks(app: Flask):
	@app.before_request
	def log_request_start():
		app.logger.info("Incoming request %s %s", request.method, request.path)

	@app.after_request
	def log_request_end(response):
		app.logger.info(
			"Request completed %s %s with status %s",
			request.method,
			request.path,
			response.status_code,
		)
		return response


def register_error_handlers(app: Flask):
	@app.errorhandler(AppError)
	def handle_app_error(error: AppError):
		app.logger.warning("Application error: %s", error.message)
		return jsonify({"error": error.message}), error.status_code

	@app.errorhandler(MarshmallowValidationError)
	def handle_schema_error(error: MarshmallowValidationError):
		app.logger.warning("Schema validation error: %s", error.messages)
		return jsonify({"error": "Validation failed", "details": error.messages}), 422

	@app.errorhandler(404)
	def handle_not_found(_error):
		return jsonify({"error": "Not found"}), 404

	@app.errorhandler(Exception)
	def handle_unexpected_error(error: Exception):
		app.logger.exception("Unexpected server error: %s", str(error))
		return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
	app = create_app()
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, debug=False)

