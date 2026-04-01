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


# ── AI & Analysis ───────────────────────────────────────────────────────────

@mcp.tool()
def omega_ai_analyst(target: str) -> str:
    """AI-powered analysis of OSINT findings for a target."""
    result = _run_omega_module("omega_cli.modules.ai_analyst", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_aiassist(target: str) -> str:
    """AI assistant for OSINT operations — suggests next steps and findings."""
    result = _run_omega_module("omega_cli.modules.aiassist", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_aisummary(target: str) -> str:
    """AI-generated summary of all collected OSINT data."""
    result = _run_omega_module("omega_cli.modules.aisummary", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_mldetect(target: str) -> str:
    """ML-based anomaly and threat detection from scan results."""
    result = _run_omega_module("omega_cli.modules.mldetect", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── API OSINT ───────────────────────────────────────────────────────────────

@mcp.tool()
def omega_apiosint(target: str) -> str:
    """API-based OSINT gathering — aggregates data from public APIs."""
    result = _run_omega_module("omega_cli.modules.apiosint", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Archive & History ───────────────────────────────────────────────────────

@mcp.tool()
def omega_archive(target: str) -> str:
    """Web archive snapshot retrieval and analysis."""
    result = _run_omega_module("omega_cli.modules.archive", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Asset & Infrastructure Mapping ──────────────────────────────────────────

@mcp.tool()
def omega_assetmap(target: str) -> str:
    """Asset mapping — builds inventory of discovered hosts and services."""
    result = _run_omega_module("omega_cli.modules.assetmap", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_infra(target: str) -> str:
    """Infrastructure analysis — hosting, CDN, WAF, load balancer detection."""
    result = _run_omega_module("omega_cli.modules.infra", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_network(target: str) -> str:
    """Network topology analysis — traceroute, hop mapping, latency."""
    result = _run_omega_module("omega_cli.modules.network", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_satellite(target: str) -> str:
    """Satellite and geospatial infrastructure reconnaissance."""
    result = _run_omega_module("omega_cli.modules.satellite", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Attack Surface & Red Team ──────────────────────────────────────────────

@mcp.tool()
def omega_attackmap(target: str) -> str:
    """Attack surface mapping — visualizes potential attack vectors."""
    result = _run_omega_module("omega_cli.modules.attackmap", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_c2(target: str) -> str:
    """C2 infrastructure detection — identifies command-and-control indicators."""
    result = _run_omega_module("omega_cli.modules.c2", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_deception(target: str) -> str:
    """Deception and honeypot detection — identifies decoy services."""
    result = _run_omega_module("omega_cli.modules.deception", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_redteam(target: str) -> str:
    """Red team reconnaissance — attack path analysis and enumeration."""
    result = _run_omega_module("omega_cli.modules.redteam", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_fuzzer(target: str) -> str:
    """Web fuzzer — discovers hidden paths, parameters, and endpoints."""
    result = _run_omega_module("omega_cli.modules.fuzzer", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Automation & Correlation ────────────────────────────────────────────────

@mcp.tool()
def omega_autocorr(target: str) -> str:
    """Auto-correlation — links findings across modules to surface patterns."""
    result = _run_omega_module("omega_cli.modules.autocorr", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_chain(target: str) -> str:
    """Chained module execution — runs a sequence of modules in pipeline."""
    result = _run_omega_module("omega_cli.modules.chain", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_compare(target: str) -> str:
    """Compare scan results — diffs findings between runs for change detection."""
    result = _run_omega_module("omega_cli.modules.compare", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Briefing & Reporting ───────────────────────────────────────────────────

@mcp.tool()
def omega_briefing(target: str) -> str:
    """Intelligence briefing generation — structured threat summary."""
    result = _run_omega_module("omega_cli.modules.briefing", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_executive(target: str) -> str:
    """Executive summary — high-level risk overview for stakeholders."""
    result = _run_omega_module("omega_cli.modules.executive", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_pdfreport(target: str) -> str:
    """PDF report generation from collected findings."""
    result = _run_omega_module("omega_cli.modules.pdfreport", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_reportgen(target: str) -> str:
    """General report generation — markdown/text format."""
    result = _run_omega_module("omega_cli.modules.reportgen", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_reporthtml(target: str) -> str:
    """HTML report generation with interactive charts and tables."""
    result = _run_omega_module("omega_cli.modules.reporthtml", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_dashboard(target: str) -> str:
    """Dashboard data generation — metrics and KPIs for visualization."""
    result = _run_omega_module("omega_cli.modules.dashboard", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_livedash(target: str) -> str:
    """Live dashboard — real-time scan progress and findings stream."""
    result = _run_omega_module("omega_cli.modules.livedash", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Certificate & Cryptography ─────────────────────────────────────────────

@mcp.tool()
def omega_certhunt(target: str) -> str:
    """Certificate hunting — discovers certs across CT logs and hosts."""
    result = _run_omega_module("omega_cli.modules.certhunt", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_crypto(target: str) -> str:
    """Cryptographic analysis — cipher strength, key exchange evaluation."""
    result = _run_omega_module("omega_cli.modules.crypto", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_cryptoosint(target: str) -> str:
    """Cryptocurrency OSINT — wallet tracing, blockchain analysis."""
    result = _run_omega_module("omega_cli.modules.cryptoosint", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Cloud (Advanced) ───────────────────────────────────────────────────────

@mcp.tool()
def omega_cloud2(target: str) -> str:
    """Advanced cloud recon — multi-provider asset discovery and analysis."""
    result = _run_omega_module("omega_cli.modules.cloud2", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Code & Secrets ─────────────────────────────────────────────────────────

@mcp.tool()
def omega_codetrace(target: str) -> str:
    """Code tracing — finds code repos, commits, and developer footprints."""
    result = _run_omega_module("omega_cli.modules.codetrace", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_creds(target: str) -> str:
    """Credential discovery — finds exposed credentials in public sources."""
    result = _run_omega_module("omega_cli.modules.creds", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_secrets(target: str) -> str:
    """Secret scanning — API keys, tokens, and passwords in repos and pages."""
    result = _run_omega_module("omega_cli.modules.secrets", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_leaked(target: str) -> str:
    """Leaked data search — finds exposed data in paste sites and dumps."""
    result = _run_omega_module("omega_cli.modules.leaked", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── CVE & Vulnerability Mapping ────────────────────────────────────────────

@mcp.tool()
def omega_cvemap(target: str) -> str:
    """CVE mapping — maps discovered services and tech to known CVEs."""
    result = _run_omega_module("omega_cli.modules.cvemap", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_cvssrank(target: str) -> str:
    """CVSS ranking — scores and prioritizes vulnerabilities by severity."""
    result = _run_omega_module("omega_cli.modules.cvssrank", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Dark Web & Tor ─────────────────────────────────────────────────────────

@mcp.tool()
def omega_dark(target: str) -> str:
    """Dark web intelligence — searches .onion sites and dark web sources."""
    result = _run_omega_module("omega_cli.modules.dark", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_deepweb(target: str) -> str:
    """Deep web search — discovers content not indexed by search engines."""
    result = _run_omega_module("omega_cli.modules.deepweb", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_torcheck(target: str) -> str:
    """Tor network check — detects Tor exit nodes and hidden services."""
    result = _run_omega_module("omega_cli.modules.torcheck", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── DNS (Advanced) ─────────────────────────────────────────────────────────

@mcp.tool()
def omega_dnsbrute(target: str) -> str:
    """DNS brute forcing — discovers subdomains via wordlist enumeration."""
    result = _run_omega_module("omega_cli.modules.dnsbrute", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Document & Image OSINT ─────────────────────────────────────────────────

@mcp.tool()
def omega_docosint(target: str) -> str:
    """Document OSINT — extracts metadata from PDFs, Office docs, images."""
    result = _run_omega_module("omega_cli.modules.docosint", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_imgosint(target: str) -> str:
    """Image OSINT — EXIF extraction, reverse image search, geolocation."""
    result = _run_omega_module("omega_cli.modules.imgosint", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Dossier & Intelligence ─────────────────────────────────────────────────

@mcp.tool()
def omega_dossier(target: str) -> str:
    """Target dossier — comprehensive profile compilation from all sources."""
    result = _run_omega_module("omega_cli.modules.dossier", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_ipdossier(target: str) -> str:
    """IP dossier — detailed intelligence report for an IP address."""
    result = _run_omega_module("omega_cli.modules.ipdossier", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_intel(target: str) -> str:
    """Intelligence gathering — aggregated threat and context data."""
    result = _run_omega_module("omega_cli.modules.intel", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_osintdb(target: str) -> str:
    """OSINT database — stores and queries collected intelligence."""
    result = _run_omega_module("omega_cli.modules.osintdb", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Email & Phone Security ─────────────────────────────────────────────────

@mcp.tool()
def omega_mailsec(target: str) -> str:
    """Mail security analysis — SPF, DKIM, DMARC, MTA-STS evaluation."""
    result = _run_omega_module("omega_cli.modules.mailsec", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_phoneosint(target: str) -> str:
    """Phone number OSINT — carrier, location, VoIP detection."""
    result = _run_omega_module("omega_cli.modules.phoneosint", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_phishcheck(target: str) -> str:
    """Phishing detection — checks URLs and domains for phishing indicators."""
    result = _run_omega_module("omega_cli.modules.phishcheck", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Finance ────────────────────────────────────────────────────────────────

@mcp.tool()
def omega_finance(target: str) -> str:
    """Financial OSINT — company filings, SEC data, financial records."""
    result = _run_omega_module("omega_cli.modules.finance", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Firmware & Mobile ──────────────────────────────────────────────────────

@mcp.tool()
def omega_firmware(target: str) -> str:
    """Firmware analysis — extracts and analyzes embedded device firmware."""
    result = _run_omega_module("omega_cli.modules.firmware", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_mobile(target: str) -> str:
    """Mobile app analysis — APK/IPA scanning for secrets and endpoints."""
    result = _run_omega_module("omega_cli.modules.mobile", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Geolocation ────────────────────────────────────────────────────────────

@mcp.tool()
def omega_geoint(target: str) -> str:
    """Geolocation intelligence — IP geolocation, physical site mapping."""
    result = _run_omega_module("omega_cli.modules.geoint", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Git Reconnaissance ─────────────────────────────────────────────────────

@mcp.tool()
def omega_gitrecon(target: str) -> str:
    """Git repository recon — exposed repos, commit history, author info."""
    result = _run_omega_module("omega_cli.modules.gitrecon", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Graph & Visualization ──────────────────────────────────────────────────

@mcp.tool()
def omega_graph(target: str) -> str:
    """Relationship graphing — entity links, infrastructure connections."""
    result = _run_omega_module("omega_cli.modules.graph", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_viz(target: str) -> str:
    """Data visualization — generates charts and visual summaries."""
    result = _run_omega_module("omega_cli.modules.viz", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_timeline(target: str) -> str:
    """Timeline generation — chronological view of events and findings."""
    result = _run_omega_module("omega_cli.modules.timeline", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_timeline3d(target: str) -> str:
    """3D timeline visualization — interactive temporal event mapping."""
    result = _run_omega_module("omega_cli.modules.timeline3d", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Harvesting ─────────────────────────────────────────────────────────────

@mcp.tool()
def omega_harvester(target: str) -> str:
    """Email and subdomain harvester — gathers contacts and hosts."""
    result = _run_omega_module("omega_cli.modules.harvester", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Identity & Organization ────────────────────────────────────────────────

@mcp.tool()
def omega_identity(target: str) -> str:
    """Identity resolution — correlates identities across platforms."""
    result = _run_omega_module("omega_cli.modules.identity", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_persona(target: str) -> str:
    """Persona profiling — builds composite profile from OSINT data."""
    result = _run_omega_module("omega_cli.modules.persona", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_org(target: str) -> str:
    """Organization intelligence — org structure, employees, tech stack."""
    result = _run_omega_module("omega_cli.modules.org", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Monitoring & Alerting ──────────────────────────────────────────────────

@mcp.tool()
def omega_monitor(target: str) -> str:
    """Continuous monitoring — tracks changes to target infrastructure."""
    result = _run_omega_module("omega_cli.modules.monitor", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_watcher(target: str) -> str:
    """Web change watcher — detects content and configuration changes."""
    result = _run_omega_module("omega_cli.modules.watcher", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_pastewatch(target: str) -> str:
    """Paste site monitoring — watches Pastebin and similar for leaks."""
    result = _run_omega_module("omega_cli.modules.pastewatch", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_notifier(target: str) -> str:
    """Alert notifications — sends alerts when new findings are detected."""
    result = _run_omega_module("omega_cli.modules.notifier", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── OPSEC & Exfiltration ───────────────────────────────────────────────────

@mcp.tool()
def omega_opsec(target: str) -> str:
    """Operations security check — evaluates target's OPSEC posture."""
    result = _run_omega_module("omega_cli.modules.opsec", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_exfil(target: str) -> str:
    """Data exfiltration detection — identifies potential data leak channels."""
    result = _run_omega_module("omega_cli.modules.exfil", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_pivot(target: str) -> str:
    """Pivot analysis — discovers lateral movement paths between assets."""
    result = _run_omega_module("omega_cli.modules.pivot", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Plugin & Proxy ─────────────────────────────────────────────────────────

@mcp.tool()
def omega_plugin(target: str) -> str:
    """Plugin manager — loads and runs community omega plugins."""
    result = _run_omega_module("omega_cli.modules.plugin", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_proxy(target: str) -> str:
    """Proxy and anonymization tools — route scans through proxies."""
    result = _run_omega_module("omega_cli.modules.proxy", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Risk Scoring ───────────────────────────────────────────────────────────

@mcp.tool()
def omega_riskcore(target: str) -> str:
    """Risk scoring engine — calculates aggregate risk score from findings."""
    result = _run_omega_module("omega_cli.modules.riskcore", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Screenshot ─────────────────────────────────────────────────────────────

@mcp.tool()
def omega_screenshot(target: str) -> str:
    """Web page screenshot — captures visual snapshots of target pages."""
    result = _run_omega_module("omega_cli.modules.screenshot", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Shodan ─────────────────────────────────────────────────────────────────

@mcp.tool()
def omega_shodan(target: str) -> str:
    """Shodan search — internet-wide scan data for hosts and services."""
    result = _run_omega_module("omega_cli.modules.shodan_lookup", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Social Media Intelligence ──────────────────────────────────────────────

@mcp.tool()
def omega_socmint(target: str) -> str:
    """Social media intelligence — deep platform analysis and profiling."""
    result = _run_omega_module("omega_cli.modules.socmint", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── STIX ───────────────────────────────────────────────────────────────────

@mcp.tool()
def omega_stix(target: str) -> str:
    """STIX format export — converts findings to STIX 2.1 threat intel."""
    result = _run_omega_module("omega_cli.modules.stix", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Supply Chain ───────────────────────────────────────────────────────────

@mcp.tool()
def omega_supply(target: str) -> str:
    """Supply chain analysis — third-party risk and dependency mapping."""
    result = _run_omega_module("omega_cli.modules.supply", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Threat Intelligence ────────────────────────────────────────────────────

@mcp.tool()
def omega_threatfeed(target: str) -> str:
    """Threat feed integration — checks target against threat intelligence feeds."""
    result = _run_omega_module("omega_cli.modules.threatfeed", "run", target)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def omega_threatintel(target: str) -> str:
    """Threat intelligence — comprehensive threat context and attribution."""
    result = _run_omega_module("omega_cli.modules.threatintel", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Typosquatting ──────────────────────────────────────────────────────────

@mcp.tool()
def omega_typosquat(target: str) -> str:
    """Typosquatting detection — finds look-alike and misspelled domains."""
    result = _run_omega_module("omega_cli.modules.typosquat", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Web Crawling (Advanced) ────────────────────────────────────────────────

@mcp.tool()
def omega_webcrawl(target: str) -> str:
    """Advanced web crawling — recursive site crawl with content extraction."""
    result = _run_omega_module("omega_cli.modules.webcrawl", "run", target)
    return json.dumps(result, indent=2, default=str)


# ── Wordlist ───────────────────────────────────────────────────────────────

@mcp.tool()
def omega_wordlist(target: str) -> str:
    """Wordlist generation — builds custom wordlists from target content."""
    result = _run_omega_module("omega_cli.modules.wordlist", "run", target)
    return json.dumps(result, indent=2, default=str)


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


@mcp.resource("omega://reports/{target}")
def get_report(target: str) -> str:
    """Get stored findings for a target from omega reports directory."""
    import os
    try:
        reports_dir = os.path.expanduser("~/.omega/reports")
        report_file = os.path.join(reports_dir, f"{target}.json")
        if os.path.isfile(report_file):
            with open(report_file, "r") as f:
                return f.read()
        # Try matching partial filenames
        if os.path.isdir(reports_dir):
            for fname in sorted(os.listdir(reports_dir), reverse=True):
                if target in fname:
                    with open(os.path.join(reports_dir, fname), "r") as f:
                        return f.read()
        return json.dumps({"status": "not_found", "message": f"No report found for {target}"})
    except Exception as e:
        return json.dumps({"status": "error", "error": str(e)})


@mcp.resource("omega://config")
def get_config() -> str:
    """Get current omega configuration."""
    try:
        from omega_cli.config import load
        config = load()
        if hasattr(config, "to_dict"):
            return json.dumps(config.to_dict(), indent=2, default=str)
        return json.dumps(config if isinstance(config, dict) else str(config), indent=2, default=str)
    except Exception as e:
        return json.dumps({"status": "error", "error": str(e)})


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


@mcp.prompt()
def full_recon(target: str) -> str:
    """Comprehensive passive reconnaissance workflow."""
    return f"Run full passive recon on {target}: Start with omega_whois, omega_dns, omega_subdomains, omega_crtsh, omega_ssl, omega_headers, omega_tech. Then analyze all findings for security issues."


@mcp.prompt()
def bug_bounty(target: str) -> str:
    """Bug bounty recon workflow."""
    return f"Bug bounty recon on {target}: Run omega_headers, omega_cors, omega_ssl, omega_jscan, omega_crtsh, omega_cloud, omega_crawl. Focus on finding misconfigurations, exposed secrets, and CORS issues."


@mcp.prompt()
def threat_hunt(target: str) -> str:
    """Threat hunting workflow."""
    return f"Threat hunt for {target}: Run omega_auto, then omega_ioc, omega_hunt for ATT&CK TTP mapping. Identify IOCs and map to MITRE framework."


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
