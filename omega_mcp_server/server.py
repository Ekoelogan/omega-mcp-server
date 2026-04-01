"""omega-mcp-server — FastMCP server exposing 108+ omega-cli OSINT tools to AI assistants.

Transports:
  - stdio (default): for GitHub Copilot CLI
  - sse: for VS Code / web clients

Usage:
  omega-mcp                    # stdio mode
  omega-mcp --transport sse    # SSE mode on port 8080
"""
from __future__ import annotations

import io
import json
import importlib
import sys
from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "omega-mcp-server",
    instructions="OSINT & passive recon toolkit — 108+ security tools accessible via MCP",
)


# ── Helper: run an omega module and capture output ───────────────────────────

def _run_omega_module(module_path: str, func_name: str, *args, **kwargs) -> dict:
    """Import and run an omega-cli module, capturing structured output."""
    try:
        mod = importlib.import_module(module_path)
        func = getattr(mod, func_name)
        result = func(*args, **kwargs)
        if isinstance(result, (dict, list)):
            return {"status": "ok", "result": result}
        return {"status": "ok", "result": str(result) if result else "completed"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ── Core Recon Tools ─────────────────────────────────────────────────────────

@mcp.tool()
def omega_whois(target: str) -> str:
    """WHOIS lookup for a domain or IP. Returns registrant, dates, nameservers."""
    result = _run_omega_module("omega_cli.modules.whois_lookup", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_dns(target: str, record_type: str = "ALL") -> str:
    """DNS record enumeration. Returns A, AAAA, MX, NS, TXT, SOA, CNAME records."""
    result = _run_omega_module("omega_cli.modules.dns_lookup", "run", target, record_type)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_subdomains(target: str) -> str:
    """Subdomain enumeration via multiple sources (crt.sh, DNS brute, etc.)."""
    result = _run_omega_module("omega_cli.modules.subdomain", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_ipinfo(target: str) -> str:
    """IP intelligence — geolocation, ASN, organization, abuse contacts."""
    result = _run_omega_module("omega_cli.modules.ipinfo", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_headers(target: str) -> str:
    """HTTP security header analysis. Checks CSP, HSTS, X-Frame-Options, etc."""
    result = _run_omega_module("omega_cli.modules.headers", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_ssl(target: str) -> str:
    """SSL/TLS certificate analysis — issuer, expiry, protocol, cipher suites."""
    result = _run_omega_module("omega_cli.modules.ssl_check", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_ports(target: str, port_range: str = "common") -> str:
    """Port scanner — discovers open ports and services."""
    result = _run_omega_module("omega_cli.modules.portscan", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_crtsh(target: str) -> str:
    """Certificate Transparency search via crt.sh — finds related domains/certs."""
    result = _run_omega_module("omega_cli.modules.crtsh", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_tech(target: str) -> str:
    """Technology fingerprinting — identifies web frameworks, CMS, libraries."""
    result = _run_omega_module("omega_cli.modules.techfp", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_dorks(target: str) -> str:
    """Google dorks generation — creates targeted search queries for OSINT."""
    result = _run_omega_module("omega_cli.modules.dorks", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_wayback(target: str) -> str:
    """Wayback Machine history — archived snapshots and URL patterns."""
    result = _run_omega_module("omega_cli.modules.wayback", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Web Application Tools ───────────────────────────────────────────────────

@mcp.tool()
def omega_cors(target: str) -> str:
    """CORS misconfiguration detection — checks cross-origin policies."""
    result = _run_omega_module("omega_cli.modules.corscheck", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_jscan(target: str) -> str:
    """JavaScript secret scanner — finds API keys, tokens in JS files."""
    result = _run_omega_module("omega_cli.modules.jscan", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_crawl(target: str) -> str:
    """Web crawler — discovers links, forms, endpoints on a website."""
    result = _run_omega_module("omega_cli.modules.crawl", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_spider(target: str) -> str:
    """Web spider — deep link extraction and sitemap building."""
    result = _run_omega_module("omega_cli.modules.spider", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_spoofcheck(target: str) -> str:
    """Email spoofing check — SPF, DKIM, DMARC validation."""
    result = _run_omega_module("omega_cli.modules.spoofcheck", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Cloud & Infrastructure ──────────────────────────────────────────────────

@mcp.tool()
def omega_cloud(target: str) -> str:
    """Cloud asset discovery — S3 buckets, Azure blobs, GCP storage."""
    result = _run_omega_module("omega_cli.modules.cloudrecon", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_buckets(target: str) -> str:
    """S3 bucket enumeration and permission checking."""
    result = _run_omega_module("omega_cli.modules.buckets", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_asn(target: str) -> str:
    """ASN reconnaissance — autonomous system lookup, IP ranges, peers."""
    result = _run_omega_module("omega_cli.modules.asnrecon", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_reverseip(target: str) -> str:
    """Reverse IP lookup — finds other domains on the same server."""
    result = _run_omega_module("omega_cli.modules.reverseip", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Vulnerability & Threat Intel ────────────────────────────────────────────

@mcp.tool()
def omega_cve(keyword: str) -> str:
    """CVE lookup — search NVD for vulnerabilities by keyword or CVE ID."""
    result = _run_omega_module("omega_cli.modules.nvd_cve", "run", keyword)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_vuln(target: str) -> str:
    """Vulnerability scanning — checks for common misconfigurations and CVEs."""
    result = _run_omega_module("omega_cli.modules.vuln2", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_ioc(source: str) -> str:
    """IOC extraction — extracts indicators of compromise from text/URLs."""
    result = _run_omega_module("omega_cli.modules.ioc", "run", source)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_hunt(target: str) -> str:
    """Threat hunting — MITRE ATT&CK TTP mapping from findings."""
    result = _run_omega_module("omega_cli.modules.hunt", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_malware(target: str) -> str:
    """Malware analysis — VirusTotal lookup, hash reputation check."""
    result = _run_omega_module("omega_cli.modules.malware", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Identity & Social ──────────────────────────────────────────────────────

@mcp.tool()
def omega_email(target: str) -> str:
    """Email OSINT — breach checks, reputation, related accounts."""
    result = _run_omega_module("omega_cli.modules.email_osint", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_username(target: str) -> str:
    """Username search — check presence across 100+ platforms."""
    result = _run_omega_module("omega_cli.modules.username", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_social(target: str) -> str:
    """Social media OSINT — Reddit, HackerNews, Pastebin, Twitter/X."""
    result = _run_omega_module("omega_cli.modules.social", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_breach(target: str) -> str:
    """Breach/leak check — searches HIBP and other breach databases."""
    result = _run_omega_module("omega_cli.modules.breachcheck", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Automated Workflows ─────────────────────────────────────────────────────

@mcp.tool()
def omega_auto(target: str) -> str:
    """Full automated recon — runs all passive modules and generates report."""
    result = _run_omega_module("omega_cli.modules.autorecon", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_recon(target: str) -> str:
    """Quick reconnaissance — WHOIS + DNS + IP info summary."""
    result = _run_omega_module("omega_cli.modules.recon", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── AI Agent Integration ────────────────────────────────────────────────────

@mcp.tool()
def omega_agent_run(agent_name: str, target: str) -> str:
    """Run a specialist AI agent (recon-agent, web-agent, vuln-agent, cloud-agent, etc.)."""
    try:
        from omega_cli.agents.manager import AgentManager
        from omega_cli.config import load
        mgr = AgentManager(config=load())
        result = mgr.run_agent(agent_name, target)
        return json.dumps(result.to_dict(), indent=2, default=str)
    except Exception as e:
        return json.dumps({"status": "error", "error": str(e)})


@mcp.tool()
def omega_autopilot(task: str, target: str) -> str:
    """Run multi-agent AI autopilot workflow. Tasks: recon, bug-bounty, pentest, osint, threat-hunt."""
    try:
        from omega_cli.agents.manager import AgentManager
        from omega_cli.config import load
        mgr = AgentManager(config=load())
        results = mgr.run_task(task, target)
        return json.dumps([r.to_dict() for r in results], indent=2, default=str)
    except Exception as e:
        return json.dumps({"status": "error", "error": str(e)})


@mcp.tool()
def omega_agents_list() -> str:
    """List all available AI agents and their capabilities."""
    try:
        from omega_cli.agents.manager import AgentManager
        from omega_cli.config import load
        mgr = AgentManager(config=load())
        return json.dumps(mgr.list_agents(), indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "error": str(e)})


@mcp.tool()
def omega_memory_search(query: str) -> str:
    """Search agent memory for past findings matching a query."""
    try:
        from omega_cli.agents.memory import AgentMemory
        mem = AgentMemory()
        results = mem.search(query)
        return json.dumps(results, indent=2, default=str)
    except Exception as e:
        return json.dumps({"status": "error", "error": str(e)})


# ── Resources ────────────────────────────────────────────────────────────────

@mcp.resource("omega://targets")
def get_targets() -> str:
    """List all targets that have been scanned."""
    try:
        from omega_cli.agents.memory import AgentMemory
        mem = AgentMemory()
        targets = mem.get_targets()
        return json.dumps(targets, indent=2, default=str)
    except Exception as e:
        return json.dumps([])


@mcp.resource("omega://findings/{target}")
def get_findings(target: str) -> str:
    """Get all findings for a specific target."""
    try:
        from omega_cli.agents.memory import AgentMemory
        mem = AgentMemory()
        findings = mem.get_findings(target=target, limit=200)
        return json.dumps(findings, indent=2, default=str)
    except Exception as e:
        return json.dumps([])


@mcp.resource("omega://stats")
def get_stats() -> str:
    """Get agent memory statistics."""
    try:
        from omega_cli.agents.memory import AgentMemory
        mem = AgentMemory()
        return json.dumps(mem.stats(), indent=2)
    except Exception as e:
        return json.dumps({})


# ── Prompts ──────────────────────────────────────────────────────────────────

@mcp.prompt()
def recon_workflow(target: str) -> str:
    """Generate a comprehensive OSINT reconnaissance workflow for a target."""
    return f"""You are an expert OSINT analyst using omega-cli tools. Perform a full passive
reconnaissance on {target}.

Execute these tools in order:
1. omega_whois("{target}") — Get registrant info
2. omega_dns("{target}") — Enumerate DNS records
3. omega_subdomains("{target}") — Find subdomains
4. omega_ssl("{target}") — Check SSL certificate
5. omega_headers("{target}") — Analyze security headers
6. omega_tech("{target}") — Fingerprint technologies
7. omega_cloud("{target}") — Check cloud assets
8. omega_spoofcheck("{target}") — Check email security

After each tool, analyze the results and note key findings.
Conclude with a risk assessment and recommended next steps."""


@mcp.prompt()
def bug_bounty_workflow(target: str) -> str:
    """Generate a bug bounty recon workflow for a target."""
    return f"""You are a bug bounty hunter using omega-cli. Perform comprehensive recon on {target}.

Phase 1 — Enumeration:
1. omega_subdomains("{target}") — Map the attack surface
2. omega_dns("{target}") — Find DNS misconfigurations
3. omega_crtsh("{target}") — Certificate transparency

Phase 2 — Web Analysis:
4. omega_headers("{target}") — Missing security headers
5. omega_cors("{target}") — CORS misconfigurations
6. omega_jscan("{target}") — Leaked secrets in JS
7. omega_tech("{target}") — Tech stack for CVE lookup

Phase 3 — Vulnerability:
8. omega_cve("<tech_found>") — Look up CVEs for detected tech
9. omega_cloud("{target}") — Check for exposed buckets
10. omega_spoofcheck("{target}") — Email spoofing

Analyze all results and produce a bug bounty report with severity ratings."""


@mcp.prompt()
def vuln_assessment(target: str) -> str:
    """Generate a vulnerability assessment workflow."""
    return f"""Perform a passive vulnerability assessment on {target} using omega-cli.

1. omega_ports("{target}") — Identify open services
2. omega_ssl("{target}") — Check for weak TLS
3. omega_headers("{target}") — Security header gaps
4. omega_cve("<services>") — Map CVEs to services
5. omega_vuln("{target}") — Run vulnerability checks

Produce a risk-ranked report with CVSS scores where applicable."""


# ── Entry point ──────────────────────────────────────────────────────────────

def main():
    """Run the MCP server."""
    import argparse
    parser = argparse.ArgumentParser(description="omega-mcp-server")
    parser.add_argument("--transport", choices=["stdio", "sse", "streamable-http"],
                        default="stdio")
    args = parser.parse_args()
    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
