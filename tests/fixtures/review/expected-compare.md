## ApplicationSet Compare: `guestbook-matrix` -> `guestbook-matrix`

Added applications: 1
Removed applications: 1
Changed destinations: 1
Findings: 2

### Added
- `guestbook-prod-canary` -> `https://prod-west.example.com` / `guestbook-prod`

### Removed
- `guestbook-in-cluster` from `https://kubernetes.default.svc` / `guestbook`

### Changed
- `guestbook-staging-west` moved from `https://staging-west.example.com` / `guestbook-staging` to `https://prod-west.example.com` / `guestbook-prod`

### Findings
- `guestbook-prod-canary`: `new_production_application` (high) - new application is introduced directly into a production destination
- `guestbook-staging-west`: `production_expansion` (high) - application now targets a production destination
