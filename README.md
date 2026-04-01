# omega-mcp-server

MCP (Model Context Protocol) server that exposes **108+ omega-cli OSINT tools** to AI assistants like GitHub Copilot, Claude, and VS Code extensions.

## Quick Start

```bash
# Install
pip install omega-mcp-server

# Run (stdio for Copilot CLI)
omega-mcp

# Run (SSE for VS Code)
omega-mcp --transport sse --port 8080
```

## Register with Copilot CLI

Add to `~/.copilot/mcp-config.json`:

```json
{
  "mcpServers": {
    "omega": {
      "command": "omega-mcp",
      "args": [],
      "env": {}
    }
  }
}
```

## Register with VS Code

Add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "omega": {
      "command": "omega-mcp",
      "args": ["--transport", "sse", "--port", "8080"]
    }
  }
}
```

## Available Tools (30+ exposed)

### Core Recon
- `omega_whois` — WHOIS lookup
- `omega_dns` — DNS enumeration
- `omega_subdomains` — Subdomain discovery
- `omega_ipinfo` — IP intelligence
- `omega_headers` — Security headers
- `omega_ssl` — SSL/TLS analysis
- `omega_ports` — Port scanning
- `omega_crtsh` — Certificate transparency
- `omega_tech` — Technology fingerprinting
- `omega_dorks` — Google dorks
- `omega_wayback` — Wayback Machine

### Web Application
- `omega_cors` — CORS check
- `omega_jscan` — JS secret scan
- `omega_crawl` — Web crawler
- `omega_spider` — Deep spider
- `omega_spoofcheck` — Email spoof check

### Cloud & Infrastructure
- `omega_cloud` — Cloud asset discovery
- `omega_buckets` — S3 bucket enum
- `omega_asn` — ASN recon
- `omega_reverseip` — Reverse IP

### Vulnerability & Threat
- `omega_cve` — CVE lookup
- `omega_vuln` — Vuln scan
- `omega_ioc` — IOC extraction
- `omega_hunt` — Threat hunting
- `omega_malware` — Malware analysis

### Identity & Social
- `omega_email` — Email OSINT
- `omega_username` — Username search
- `omega_social` — Social OSINT
- `omega_breach` — Breach check

### AI Agents
- `omega_agent_run` — Run specialist agent
- `omega_autopilot` — Multi-agent workflow
- `omega_agents_list` — List agents
- `omega_memory_search` — Search findings

## Resources

- `omega://targets` — All scanned targets
- `omega://findings/{target}` — Findings for a target
- `omega://stats` — Memory statistics

## Prompts

- `recon_workflow` — Full OSINT recon playbook
- `bug_bounty_workflow` — Bug bounty methodology
- `vuln_assessment` — Vulnerability assessment

## License

MIT
