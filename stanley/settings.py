import os

SLACK_API_TOKEN = os.environ.get("SLACK_API_TOKEN")
SLACK_VERIFICATION_TOKEN = os.environ.get("SLACK_VERIFICATION_TOKEN")
FEEDBACK_MEMBERS = os.environ.get("FEEDBACK_MEMBERS")
REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/0")
SENTRY_DSN = os.environ.get("SENTRY_DSN")

# redis key for list of person that already provided feedback
REDIS_KEY_SEND_FEEDBACK = "SEND_FEEDBACK"
REDIS_KEY_RECEIVE_FEEDBACK = "RECEIVE_FEEDBACK"
