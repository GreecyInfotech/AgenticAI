# Canonical CI workflow — deployed copy at ../../.github/workflows/ci.yml
# GitHub Actions reads workflows from .github/workflows/ at repository root.

See ../../.github/workflows/ci.yml for the active pipeline.

## Jobs

1. **build-and-test** — Maven verify + frontend production build
2. **sonar** — SonarQube analysis on main (requires SONAR_TOKEN secret)
3. **docker-compose-validate** — Validates docker-compose.yml syntax

## Local equivalent

```bash
mvn verify -DskipITs
cd frontend && npm ci && npm run build
docker compose config
```
