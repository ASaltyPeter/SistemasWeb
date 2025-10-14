# Netflix Catalog (Serverless Local)

Arquitetura simulada com AWS (API Gateway + Lambdas + DynamoDB + SQS) usando LocalStack para desenvolvimento local.

## Requisitos
- Docker e Docker Compose
- Python 3.11+

## Setup rápido
```bash
cp .env.example .env
docker compose up -d
python -m venv .venv && .venv/Scripts/activate
pip install -r requirements.txt
python scripts/setup_dynamodb.py
python scripts/setup_sqs.py
python scripts/seed_data.py
```

## Executar API local
```bash
python -c "from app import create_app; create_app().run(port=8000, debug=True)"
```

## Endpoints
- GET `/catalog`
- GET `/catalog/<id>`
- POST `/watch` {"userId":"u1","itemId":"<id>"}
- GET `/recommendations/<userId>`

## Testes
```bash
pytest -q
```




