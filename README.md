# Athletica

Single-user AI fitness analytics and recommendation system.

## Stack

- FastAPI + SQLAlchemy + PostgreSQL
- Celery + Redis
- ML: pandas, scikit-learn, LightGBM, MLflow
- React + Vite + TailwindCSS + Recharts
- Docker Compose + Nginx

## Local Development

### 1) Secrets

This repo does not allow plaintext secrets. Use SOPS:

```bash
sops --decrypt secrets.prod.enc.yaml > secrets.prod.dec.yaml
```

Export env vars (example using `yq`):

```bash
export $(sops -d secrets.prod.enc.yaml | yq -r 'to_entries|map("ATHLETICA_" + (.key|ascii_upcase) + "=" + (.value|tostring))|.[]')
```

### 2) Run with Docker

```bash
docker-compose up --build
```

- API: `http://localhost:8000`
- UI: `http://localhost:5173`

## Whoop OAuth Flow

1. Call `GET /whoop/auth` to get the Whoop authorization URL.
2. Open the URL in a browser and authorize the app.
3. Whoop redirects to `ATHLETICA_WHOOP_REDIRECT_URL` with `code` + `state`.
4. The callback `GET /whoop/callback` exchanges the code and stores tokens.

## Sync (API-only, no webhooks)

The system uses scheduled polling (cron). For hourly sync, install the cron file:

```bash
sudo cp infra/cron/athletica.cron /etc/cron.d/athletica
```

This triggers:

```bash
POST /whoop/sync
```

## Project Structure

```
backend/   FastAPI + ML + Whoop integration
frontend/  React dashboard
infra/     Nginx config and cron
scripts/   Utility checks
```

## Notes

- Whoop OAuth is required for data sync.
- Recommendations are explainable and versioned.
- Only one active goal at a time.
