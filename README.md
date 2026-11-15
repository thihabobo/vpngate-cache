# VPNGate Auto-Mirror & Cache

Automated, high-availability mirror for [VPN Gate](https://www.vpngate.net/) public VPN servers, built specifically for anti-censorship and DPI bypass in Myanmar and other restricted networks.

Auto-updated every 30 minutes via GitHub Actions and delivered globally via enterprise Anycast CDNs.

---

## 🚀 CDN Endpoints

### 1. Global Enterprise CDN (jsDelivr)
*Near-zero block rate in Myanmar — distributed across Cloudflare, Fastly, and Akamai.*

* **All Global Servers**:
  ```
  https://cdn.jsdelivr.net/gh/thihabobo/vpngate-cache@main/servers.csv
  ```
* **Japan-Only Servers**:
  ```
  https://cdn.jsdelivr.net/gh/thihabobo/vpngate-cache@main/japan_servers.csv
  ```
* **Status & Metadata**:
  ```
  https://cdn.jsdelivr.net/gh/thihabobo/vpngate-cache@main/metadata.json
  ```

### 2. GitHub Raw Fallback
* **All Global Servers**:
  ```
  https://raw.githubusercontent.com/thihabobo/vpngate-cache/main/servers.csv
  ```
* **Japan-Only Servers**:
  ```
  https://raw.githubusercontent.com/thihabobo/vpngate-cache/main/japan_servers.csv
  ```

---

## ⚡ Features
- 🔄 **Autonomous 30-min Schedule**: Automatically syncs active server pools from VPNGate.
- 🛡️ **Anti-DPI & Firewall Resilient**: Delivered via HTTPS CDN, bypassing ISP blocklists targeting `vpngate.net`.
- 🎌 **Clean Segmentation**: Cleanly splits global servers and prioritized Japan servers.
- 📊 **Realtime Metadata**: Exposes JSON metrics with total servers, country counts, and timestamps.
