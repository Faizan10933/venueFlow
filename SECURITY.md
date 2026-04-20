# Security Policy

## Supported Versions

Only the latest version of VenueFlow is supported for security updates.

## Reporting a Vulnerability

We take the security of our stadium fans seriously. If you find a security vulnerability, please do not report it publicly. Instead, contact the maintainers directly or open a private issue in the GitHub repository.

### Security Implementation Highlights:
- **CORS Protection**: Strict origin validation.
- **WebSocket Security**: Heartbeat monitoring and payload sanitization.
- **Content Security Policy**: Strict browser-level script and style source enforcement.
- **Rate Limiting**: Protection against DDoS and API abuse using `slowapi`.
