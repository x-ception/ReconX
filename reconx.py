import os
import subprocess
from discordwebhook import Discord
from urllib.parse import urlparse
import time

# === CONFIGURATION ===
discord = Discord(url="YOUR_DISCORD_WEBHOOK_URL")  # Replace with actual webhook
domain = input("Enter domain (e.g. target.com): ").strip()
output_dir = f"recon-{domain.replace('.', '_')}"
os.makedirs(output_dir, exist_ok=True)

def notify(msg):
    """Send notifications to Discord and print locally."""
    try:
        discord.post(content=f"[{domain}] {msg}")
    except Exception as e:
        print(f"[!] Discord Error: {e}")
    print(msg)

def run_cmd(command, outfile=None):
    """Run a shell command and optionally write output to file."""
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
        output = result.stdout.decode('utf-8', errors='ignore')
        if outfile:
            with open(outfile, "w", encoding='utf-8') as f:
                f.write(output)
        return output
    except subprocess.TimeoutExpired:
        notify(f"⚠️ Timeout while running: `{command}`")
        return ""
    except Exception as e:
        notify(f"❌ Error while running `{command}`: {str(e)}")
        return ""

# === MODULES ===

def subdomain_enum():
    notify("🚀 Starting Subdomain Enumeration with Subfinder...")
    subfinder_file = os.path.join(output_dir, "subdomains.txt")
    output = run_cmd(f"subfinder -d {domain} -all -recursive", subfinder_file)
    if output:
        notify(f"✅ Subdomains saved to `{subfinder_file}`")
    else:
        notify("⚠️ Subfinder did not return any results.")

def probe_http():
    notify("🔍 Probing live hosts using Httpx...")
    sub_file = os.path.join(output_dir, "subdomains.txt")
    live_file = os.path.join(output_dir, "live.txt")
    if not os.path.exists(sub_file):
        notify("❌ Subdomains file missing. Skipping httpx.")
        return
    run_cmd(f"httpx -silent -status-code -title -threads 100 -o {live_file} -l {sub_file}")
    notify(f"🌐 Live hosts saved to `{live_file}`")

def extract_js_and_secrets():
    notify("📦 Extracting JavaScript & scanning for secrets...")
    live_file = os.path.join(output_dir, "live.txt")
    js_dir = os.path.join(output_dir, "js_files")
    os.makedirs(js_dir, exist_ok=True)

    if not os.path.exists(live_file):
        notify("❌ Live hosts missing. Skipping JS extraction.")
        return

    with open(live_file, "r") as f:
        for url in f:
            url = url.strip()
            parsed = urlparse(url)
            clean_host = parsed.netloc.replace(':', '_')
            js_outfile = os.path.join(js_dir, f"{clean_host}.html")
            content = run_cmd(f"curl -s {url}", js_outfile)

            if any(secret in content.lower() for secret in ["apikey", "secret", "token", "authorization"]):
                notify(f"🔐 Possible secret in: `{url}`")

def discover_params():
    notify("📚 Pulling historical URLs using Waybackurls...")
    sub_file = os.path.join(output_dir, "subdomains.txt")
    wayback_file = os.path.join(output_dir, "wayback.txt")

    if not os.path.exists(sub_file):
        notify("❌ Subdomains file missing. Skipping Wayback.")
        return

    all_urls = []
    with open(sub_file, "r") as f:
        for sub in f:
            sub = sub.strip()
            urls = run_cmd(f"echo {sub} | waybackurls")
            all_urls.extend(urls.strip().splitlines())

    with open(wayback_file, "w", encoding='utf-8') as f:
        f.write("\n".join(all_urls))

    notify(f"📜 Wayback data saved to `{wayback_file}`")

def gf_patterns():
    notify("🧠 Scanning wayback data for vulnerable patterns using `gf`...")
    wayback_file = os.path.join(output_dir, "wayback.txt")
    if not os.path.exists(wayback_file):
        notify("❌ Wayback file missing. Skipping GF patterns.")
        return

    patterns = ['xss', 'sqli', 'redirect', 'ssrf', 'idor', 'rce']
    for pattern in patterns:
        try:
            matches = run_cmd(f"cat {wayback_file} | gf {pattern}")
            if matches.strip():
                for line in matches.strip().splitlines():
                    notify(f"🎯 Potential `{pattern.upper()}` → {line}")
        except:
            continue

def save_summary():
    notify("✅ Recon complete. All results saved in:")
    notify(f"`{output_dir}/` 📁")

# === MAIN ===

def run_all():
    start = time.time()
    notify(f"🔎 Starting full recon on `{domain}`...")
    subdomain_enum()
    probe_http()
    extract_js_and_secrets()
    discover_params()
    gf_patterns()
    save_summary()
    end = time.time()
    notify(f"⏱ Recon finished in {round(end - start, 2)} seconds.")

run_all()
