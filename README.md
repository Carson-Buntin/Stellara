# Stellara
A unified observability and intelligence platform for modern software systems. We help engineering teams monitor applications in real time using logs, metrics, and distributed traces while applying AI to detect anomalies, predict failures, and surface root causes before they impact users.

---

# APM Platform (MVP)

A multi-tenant observability platform for logs, metrics, and distributed traces.

Built for modern distributed systems with a foundation compatible with OpenTelemetry-style instrumentation.

---

## What this is

This platform lets you:

- Ingest logs, metrics, and traces from any application
- Separate all data by tenant (multi-tenant SaaS design)
- Store and query observability data in real time
- Provide the foundation for future AIOps and predictive reliability features

---

## Core concept

App → Ingestion API → Database → Dashboard

Future vision:
App → OpenTelemetry SDK → Ingestion API → Processing Layer → AI Insights → Dashboard

---

## Features (MVP)

- Multi-tenant architecture (API key based)
- Logs ingestion API
- Metrics ingestion API
- Traces ingestion API
- PostgreSQL storage backend
- Basic observability dashboard (in progress)

---

## Authentication

Every request must include an API key:

api_key: sk_test_xxx

Each API key maps to a single tenant. All data is isolated per tenant.

---

## Quickstart

### 1. Run the backend

docker-compose up

---

### 2. Send a log

curl -X POST http://localhost:8000/v1/logs \
  -H "api_key: sk_test_123" \
  -H "Content-Type: application/json" \
  -d '{
    "service_name": "api-service",
    "level": "error",
    "message": "database connection failed"
  }'

---

### 3. Send a metric

curl -X POST http://localhost:8000/v1/metrics \
  -H "api_key: sk_test_123" \
  -H "Content-Type: application/json" \
  -d '{
    "service_name": "api-service",
    "metric_name": "request_latency",
    "value": 132.5
  }'

---

### 4. Send a trace span

curl -X POST http://localhost:8000/v1/traces \
  -H "api_key: sk_test_123" \
  -H "Content-Type: application/json" \
  -d '{
    "trace_id": "abc123",
    "span_id": "span1",
    "service_name": "api-service",
    "operation": "GET /users",
    "duration_ms": 120,
    "status": "ok"
  }'

---

## Data model

Log:
- service_name
- level
- message
- trace_id (optional)
- timestamp

Metric:
- service_name
- metric_name
- value
- timestamp

Trace:
- trace_id
- span_id
- service_name
- operation
- duration_ms
- status

---

## Architecture

Application → API Layer (FastAPI) → Auth (API Key → Tenant) → PostgreSQL → Dashboard

---

## Multi-tenancy

All data is isolated using a tenant_id derived from the API key.

Every request is automatically scoped to a single tenant.

---

## Roadmap

Phase 1:
- Ingestion APIs
- Multi-tenant backend
- PostgreSQL storage

Phase 2:
- OpenTelemetry integration
- Trace-log correlation
- Improved dashboard

Phase 3:
- Alerting system
- Service maps
- Aggregated metrics

Phase 4:
- AIOps layer (anomaly detection, failure prediction)
- Root cause analysis
- Intelligent observability assistant

---

## Vision

A unified observability and intelligence platform that helps engineering teams:

- Understand system behavior in real time
- Detect anomalies automatically
- Predict failures before they impact users
- Connect production signals with engineering and QA systems

---

## Status

MVP — actively in development
