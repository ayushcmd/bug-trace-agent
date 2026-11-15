# Changelog

## v2.0.0

### Added

- Standalone HTML, CSS, and JavaScript demo in `docs/`, ready for GitHub Pages without a build step.
- Responsive workspace for tracing the sample authentication bug, inspecting a predefined fix, reviewing browser checks, and downloading the proposal after local approval.
- Static hosting instructions and a rewritten README covering both interfaces, configuration, API routes, verification, and current limitations.

### Fixed

- Windows launcher startup failure caused by emoji output in terminals using a legacy encoding.
- Outdated repository links, broken documentation references, and unsupported feature claims in the README.

### Included backend

- Modular FastAPI application with health, run creation, status, history, and simulated approval endpoints.
- Deterministic Python demo that temporarily applies a sample fix, verifies it with pytest, and restores the original file.
- Experimental Gemini and Vertex AI provider paths.

### Verification and limitations

- Four API integration tests passed in demo mode during local verification.
- Browser tracing, checks, approval, and reset were verified; JavaScript syntax checking passed.
- The website is a deterministic browser demo, not an AI service. Python execution requires the separate backend.
- Live AI workflows remain incomplete. Approval does not push or merge code; run state is in memory.

This release is published from the `static-website` branch. GitHub Pages must be configured separately to publish its `/docs` directory.
