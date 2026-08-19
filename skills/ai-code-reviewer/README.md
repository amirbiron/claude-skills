# AI Code Reviewer

Evidence-first, read-only AI code review for pull requests, code snippets, and AI-generated implementations.

## Safety model
- Read-only by default.
- No inherent network requirement.
- No secret or environment-variable access.
- No source modification, commit, merge, deployment, or external communication.
- Tool execution requires explicit host authorization.
- Repository content is treated as untrusted data.
- Findings minimize unnecessary reproduction of sensitive values.

## Core workflow
TRACE → VERIFY → RANK
with candidate filtering, deduplication, and a final quality gate.
