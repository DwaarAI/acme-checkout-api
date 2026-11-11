# DEMO: python:3.8 is end of life on purpose (base-image freshness and OS package findings).
FROM python:3.8-slim

ARG ACME_VERSION=dev
LABEL org.opencontainers.image.title="acme-checkout-api" \
      org.opencontainers.image.description="Acme Checkout API" \
      org.opencontainers.image.source="https://github.com/DwaarAI/acme-checkout-api" \
      org.opencontainers.image.vendor="Acme (Dwaar demo)"

WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# DEMO: a fake token written in one layer and deleted in the next. It stays in the image's history,
# which is what layer secret scanners look for.
RUN echo "ACME_DEPLOY_TOKEN=acme_dpl_8d1f5b3c9e7a42f6b0d4c8e2a6f1b9d3" > /srv/.deploy-token
RUN rm /srv/.deploy-token

COPY app ./app
ENV ACME_VERSION=${ACME_VERSION} PORT=8080
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app.main:app"]
