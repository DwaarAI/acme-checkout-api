# Acme Checkout API

The catalogue and orders API behind the Acme storefront ([acme-checkout-web](https://github.com/DwaarAI/acme-checkout-web)).

> **Dwaar demo.** Acme is fictional. This repository is part of a security demo for
> [Dwaar](https://dwaar.ai) and is **deliberately insecure**: old dependencies, an end-of-life base image,
> unsafe code in `app/admin.py` (never registered in a deployment), a planted fake secret, an insecure
> workflow (GitHub Actions is disabled here) and misconfigured infrastructure. Do not reuse any of it.

| Path | What |
|---|---|
| `app/` | Flask service: `/health`, `/api/products`, `/api/orders` |
| `Dockerfile` | Image published to `ghcr.io/dwaarai/acme-checkout-api` and Amazon ECR |
| `deploy/stack.yaml` | CloudFormation: the ECS Fargate service it runs as |
| `.github/workflows/build.yml` | How the image is built, pushed and deployed |

Run it locally:

```sh
docker build -t acme-checkout-api . && docker run --rm -p 8080:8080 acme-checkout-api
curl localhost:8080/api/products
```
