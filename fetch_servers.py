#!/usr/bin/env python3
"""
VPNGate Auto-Mirror & Cache Fetcher
Fetches active servers from official VPNGate API, validates,
and exports:
  1. servers.csv (All active global servers)
  2. japan_servers.csv (Japan servers prioritized)
  3. metadata.json (Status, timestamps, stats)
"""

import urllib.request
import csv
import io
import json
import datetime
import sys

VPNGATE_API_URL = "http://www.vpngate.net/api/iphone/"

def fetch_servers():
    print(f"[{datetime.datetime.now(datetime.timezone.utc).isoformat()}] Fetching servers from {VPNGATE_API_URL}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    req = urllib.request.Request(VPNGATE_API_URL, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            raw_text = response.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"Error fetching VPNGate data: {e}", file=sys.stderr)
        sys.exit(1)

    lines = raw_text.splitlines()
    if not lines or not lines[0].startswith("*vpn_servers"):
        print("Invalid response format received from VPNGate.", file=sys.stderr)
        sys.exit(1)

    # Clean lines: remove empty lines and VPNGate trailing footer comments
    clean_lines = []
    header_found = False
    header_cols = []
    all_servers = []
    japan_servers = []
    countries = {}

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("*"):
            continue
        if stripped.startswith("#"):
            header_found = True
            header_cols = stripped.lstrip("#").split(",")
            continue
        if not header_found:
            continue

        cols = stripped.split(",")
        if len(cols) < 7:
            continue

        country_short = cols[6].strip().upper()
        country_long = cols[5].strip()
        countries[country_short] = countries.get(country_short, 0) + 1

        all_servers.append(stripped)
        if country_short == "JP" or "japan" in country_long.lower():
            japan_servers.append(stripped)

    print(f"Successfully parsed {len(all_servers)} servers ({len(japan_servers)} Japan servers).")
    print(f"Discovered countries: {sorted(countries.items(), key=lambda x: -x[1])}")

    header_str = "#" + ",".join(header_cols)
    
    # 1. Write servers.csv
    with open("servers.csv", "w", encoding="utf-8") as f:
        f.write("*vpn_servers\n")
        f.write(header_str + "\n")
        for s in all_servers:
            f.write(s + "\n")

    # 2. Write japan_servers.csv
    with open("japan_servers.csv", "w", encoding="utf-8") as f:
        f.write("*vpn_servers\n")
        f.write(header_str + "\n")
        for s in japan_servers:
            f.write(s + "\n")

    # 3. Write metadata.json
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    metadata = {
        "last_updated_utc": now,
        "total_servers": len(all_servers),
        "japan_servers": len(japan_servers),
        "countries": countries,
        "status": "healthy"
    }
    with open("metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print("Successfully exported servers.csv, japan_servers.csv, and metadata.json.")

if __name__ == "__main__":
    fetch_servers()
