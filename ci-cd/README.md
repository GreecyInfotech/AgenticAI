# CI/CD Platform

Production CI/CD configuration for the BFSI Agentic AI Platform.

## Components

| Path | Purpose |
|------|---------|
| `.github/workflows/ci.yml` | Main CI pipeline (build, test, SonarQube, compose validate) |
| `.github/workflows/release.yml` | Tag-based release artifacts |
| `ci-cd/sonarqube/` | SonarQube project properties |
| `ci-cd/argo-cd/` | Argo CD application and K8s manifests |
| `ci-cd/nexus/` | Maven settings for Nexus artifact repository |

## CI Pipeline

Triggered on push/PR to `main` and `develop`:

1. **build-and-test** — `mvn verify` + frontend `npm run build`
2. **sonar** — SonarQube scan on main (requires `SONAR_TOKEN` secret)
3. **docker-compose-validate** — Validates infrastructure compose file

## Release

Push a version tag (`v*.*.*`) to trigger release artifact upload.

## Argo CD

```bash
kubectl apply -f ci-cd/argo-cd/application.yaml
```

Deploys `ci-cd/argo-cd/manifests/platform.yaml` to the `bfsi-platform` namespace.

## SonarQube (local)

```bash
mvn verify sonar:sonar -Dsonar.projectKey=bfsi-agentic-ai-platform
```

## Nexus

```bash
mvn deploy -s ci-cd/nexus/settings.xml \
  -DNEXUS_URL=https://nexus.yourbank.com \
  -DNEXUS_USERNAME=ci \
  -DNEXUS_PASSWORD=***
```

## Required GitHub Secrets

| Secret | Purpose |
|--------|---------|
| `SONAR_TOKEN` | SonarQube authentication |

## Optional GitHub Variables

| Variable | Purpose |
|----------|---------|
| `SONAR_HOST_URL` | SonarQube server URL |
