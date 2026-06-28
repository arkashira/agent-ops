# dataflow.md

## System Dataflow Architecture for **agent‑ops**

```
┌───────────────────────┐
│  External Data Sources │
│  (Agents, APIs, Logs)  │
└──────────────┬────────┘
               │
               ▼
┌───────────────────────┐
│   Ingestion Layer      │
│  (Kafka / Pulsar)      │
└───────┬───────┬───────┘
        │       │       │
        ▼       ▼       ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  Auth Gate  │ │  Auth Gate  │ │  Auth Gate  │
│ (OAuth2)    │ │ (API Key)   │ │ (JWT)       │
└───────┬─────┘ └───────┬─────┘ └───────┬─────┘
        │             │             │
        ▼             ▼             ▼
┌───────────────────────────────────────┐
│  Processing / Transform Layer          │
│  (Flink / Spark Structured Streaming) │
│  - Agent state enrichment              │
│  - Reachability checks                 │
│  - Alert & metric aggregation          │
└───────┬───────────────────────────────┘
        │                               │
        ▼                               ▼
┌───────────────────────┐   ┌───────────────────────┐
│  Storage Tier          │   │  Storage Tier          │
│  (Kafka topics)        │   │  (PostgreSQL + Timescale│
│  (Raw events)          │   │   for time‑series)     │
└───────┬───────┬───────┘   └───────┬───────┬───────┘
        │       │       │           │       │       │
        ▼       ▼       ▼           ▼       ▼       ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  Raw Events │ │  Enriched   │ │  Metrics    │ │  Alerts     │
│  (Kafka)    │ │  Events     │ │  (Timescale)│ │  (Kafka)    │
└───────┬─────┘ └───────┬─────┘ └───────┬─────┘ └───────┬─────┘
        │             │             │             │
        ▼             ▼             ▼             ▼
┌───────────────────────────────────────────────────────┐
│  Query / Serving Layer                                 │
│  (PostgreSQL, Timescale, ClickHouse, GraphQL API)      │
│  - REST/GraphQL endpoints                               │
│  - Auth: JWT + RBAC                                    │
│  - Rate limiting, caching (Redis)                      │
└───────┬───────────────────────────────────────────────┘
        │                                               │
        ▼                                               ▼
┌───────────────────────┐                       ┌───────────────────────┐
│  Egress to User       │                       │  Egress to User       │
│  (Web UI, CLI, SDK)   │                       │  (Webhook, Email)     │
│  - Auth: OAuth2       │                       │  - Auth: API Key      │
│  - TLS, CORS          │                       │  - TLS                 │
└───────────────────────┘                       └───────────────────────┘
```

### 1. External Data Sources
- **Agent Daemons**: Lightweight agents running on target hosts, emitting telemetry (status, metrics, logs) via HTTPS or gRPC to ingestion endpoints.
- **Third‑party APIs**: Cloud provider health endpoints, network monitoring services.
- **System Logs**: Syslog, Windows Event Log, container logs forwarded to ingestion.

### 2. Ingestion Layer
- **Kafka / Pulsar**: High‑throughput, fault‑tolerant message broker.
- **Auth Gate**:  
  - OAuth2 token validation for agent endpoints.  
  - API Key verification for third‑party sources.  
  - JWT verification for system logs.

### 3. Processing / Transform Layer
- **Stream Processing Engine**: Flink or Spark Structured Streaming.
- **Functions**:
  - Enrich agent events with metadata (host, region, tags).  
  - Compute reachability (ping, TCP handshake).  
  - Aggregate metrics (CPU, memory, network).  
  - Detect anomalies and generate alerts.

### 4. Storage Tier
| Tier | Storage | Use‑case |
|------|---------|----------|
| **Raw Events** | Kafka topics | Immutable audit trail, replayable. |
| **Enriched Events** | PostgreSQL | Structured queries, joins. |
| **Metrics** | TimescaleDB | Time‑series analytics, down‑sampling. |
| **Alerts** | Kafka + PostgreSQL | Real‑time alert stream + persistence. |

### 5. Query / Serving Layer
- **Databases**: PostgreSQL + Timescale for relational + TS data; ClickHouse for high‑volume analytics.
- **API Layer**: GraphQL + REST endpoints, protected by JWT + RBAC.
- **Caching**: Redis for hot metrics and session data.
- **Rate Limiting**: Token bucket per API key.

### 6. Egress to User
- **Web UI**: React/Vue SPA, OAuth2 login, TLS, CORS.
- **CLI/SDK**: Go/Python libraries, API Key auth.
- **Webhooks**: JSON payloads over HTTPS, signed with HMAC.
- **Email/Slack**: Alert notifications, authenticated via SMTP/Slack API.

### Auth Boundaries
1. **Agent → Ingestion**: OAuth2 bearer token, TLS client cert.
2. **Ingestion → Processing**: Internal service mesh mTLS, ACLs.
3. **Processing → Storage**: Service‑to‑service JWT, role‑based access.
4. **Storage → Query Layer**: PostgreSQL/Timescale roles, network ACLs.
5. **Query Layer → Egress**: JWT + RBAC, API key rotation policy.
6. **Egress → User**: OAuth2 for UI, API Key for SDK/webhooks, TLS everywhere.

---