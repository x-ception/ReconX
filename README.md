# 🔎 ReconX – Elite Recon Automation for Bug Bounty Hunters

ReconX is a clean, powerful, and fully automated bug bounty recon framework that performs A–Z reconnaissance on a given target domain. It is built to save your time, eliminate repetitive tasks, and immediately notify you of potential vulnerabilities directly on Discord.

![Python](https://img.shields.io/badge/python-3.7%2B-blue?style=flat-square)
![Recon](https://img.shields.io/badge/recon-automation-critical?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-success?style=flat-square)

---

## 🚀 Features

- ✅ **Subdomain Enumeration** using `subfinder`
- 🌐 **Live Host Probing** using `httpx`
- 📜 **JavaScript File Extraction** and Secret Keyword Search
- 📂 **Wayback Machine Historical URL Collection**
- 🎯 **GF Pattern Scanning** (`xss`, `sqli`, `ssrf`, `idor`, `rce`, `redirect`)
- 🔔 **Discord Webhook Alerts** for Critical Findings
- 📁 **Neatly Structured Output Directory** for Every Scan

---

## 🛠 Requirements

Ensure the following tools are installed and added to your `$PATH`:

- `subfinder`
- `httpx`
- `waybackurls`
- `gf`
- `curl`
- **Python 3.7+**
- Python module: `discordwebhook`
  Install using:
pip install discordwebhook


---

## 📦 Installation

Clone the repo:
```bash
git clone https://github.com/yourusername/ReconX.git && cd ReconX
```

Make the script executable:
```bash
chmod +x reconx.py
```

---

## ⚙️ Configuration

Open the `reconx.py` file and replace:

```python
discord = Discord(url="YOUR_DISCORD_WEBHOOK_URL")
```
with your actual Discord webhook URL.


🧪 Usage
Run the script and enter your domain when prompted:
```python
python3 reconx.py
```
Output will be saved inside a directory named like:
```
recon-example_com/
Inside you’ll find:

subdomains.txt

live.txt

js_files/

wayback.txt
```
Discord alerts if secrets or GF matches are found
🤖 Discord Alerts Example
You'll get real-time notifications like:
```
[example.com] 🚀 Starting Subdomain Enumeration...
[example.com] 🎯 Potential XSS found: [https://example.com/search?q=](https://example.com/search?q=)<script>
[example.com] ⚠️ Possible secrets found in [https://sub.example.com/assets/app.js](https://sub.example.com/assets/app.js)
```
🤝 Contribution
PRs are welcome to improve modules or add elite recon features. Want to add nuclei, GitHub dorks, or permutation modules? Fork it, modify it, and open a pull request!

🧠 Philosophy
“Don’t just automate… automate like a beast.”
ReconX gives power to bug hunters who want complete visibility in their recon without losing control. You hunt. Let ReconX prep the battlefield.

📄 License
MIT License – use it, modify it, abuse it.

🔥 Created by YourName
