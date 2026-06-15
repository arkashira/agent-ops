# TECH_SPEC.md

## Technical Specification

### Architecture Overview
The `agent-ops` service provides an automated management and reachability tool for the Axentx AI workforce. It operates as a centralized control plane that orchestrates the lifecycle of role-agents, monitors their operational status, and ensures high availability. The architecture is designed as a microservices-based system with a RESTful API and a PostgreSQL database for state persistence.

The system is composed of the following core components:
1.  **Agent Management Service**: Handles CRUD operations for agent metadata and configurations.
2.  **Reach
