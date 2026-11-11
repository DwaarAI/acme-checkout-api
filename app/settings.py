import os

VERSION = os.environ.get("ACME_VERSION", "dev")
CURRENCY = "EUR"
ADMIN_ROUTES = os.environ.get("ACME_ADMIN_ROUTES") == "1"

# DEMO: a planted, fake credential for secret scanners. It is not a key to anything.
PAYMENTS_API_SECRET = "acme_live_3f9c2e7a81d64b0f9e5c1a7d2b8e4f60c3a9d7e1"
