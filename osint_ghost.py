#!/usr/bin/env python3
# -*- coding: utf-8 -*-                                    
"""
OSINT Ghost Root - No Proxy Version

- Animasi asli dipertahankan
- Clear screen otomatis saat start
- Deteksi status akun: active, private, inactive, not_found, error
- Generate variasi username                                - Simpan hasil scan ke JSON                                - Tanpa proxy
"""

import aiohttp
import asyncio
import json
import re
import os
import sys
import time
import random
from collections import defaultdict, OrderedDict
from aiohttp import ClientTimeout
from colorama import Fore, Style, init                     
init(autoreset=True)


SITES = OrderedDict({
    "Twitter":   {"url": "https://twitter.com/{username}",
                  "check": lambda t, u: 'data-testid="UserName"' in t},
    "Instagram": {"url": "https://www.instagram.com/{username}/",
                  "check": lambda t, u: '"biography"' in t or '"edge_followed_by"' in t or f'profilePage_{u}' in t},
    "TikTok":    {"url": "https://www.tiktok.com/@{username}",
                  "check": lambda t, u: re.search(rf'"uniqueId"\s*:\s*"{re.escape(u)}"', t, re.I) is not None or u in t},
    "Facebook":  {"url": "https://www.facebook.com/{username}",
                  "check": lambda t, u: "facebook" in t.lower()},
    "YouTube":   {"url": "https://www.youtube.com/@{username}",
                  "check": lambda t, u: f"@{u.lower()}" in t.lower()},
    "Reddit":    {"url": "https://www.reddit.com/user/{username}",
                  "check": lambda t, u: "reddit" in t.lower()},
    "GitHub":    {"url": "https://github.com/{username}",
                  "check": lambda t, u: f"https://github.com/{u}" in t or f'/{u}"' in t},
    "Telegram":  {"url": "https://t.me/{username}",
                  "check": lambda t, u: "tgme_username_link" in t or u in t},
    "LinkedIn":  {"url": "https://www.linkedin.com/in/{username}",
                  "check": lambda t, u: "linkedin" in t.lower()}
})

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; osint-ghost-root/2.1)"}


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def typing_effect(text, delay=0.05, color=Fore.GREEN):
    for char in text:
        sys.stdout.write(color + char + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def glitch_text(text, times=2):
    for _ in range(times):
        sys.stdout.write("\r" + Fore.RED + "".join(random.choice([c, "#", "%", "&", "@"]) for c in text))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write("\r" + Fore.GREEN + text + "\n")

def reverse_typing(text, delay=0.05):
    typing_effect(text, delay, Fore.RED)
    time.sleep(0.3)
    for _ in text:
        sys.stdout.write("\r" + Fore.RED + text + " " * 5)
        sys.stdout.flush()
        text = text[:-1]
        time.sleep(delay)
    print()


def intro_loading():
    clear_screen()
    typing_effect(">>> Selamat datang di Tools OSINT Ghost_Root", 0.03, Fore.RED)
    glitch_text("[SYSTEM INITIALIZING...]")
    time.sleep(0.2)
    typing_effect("✔ System Ready...", 0.03, Fore.GREEN)
    reverse_typing(">>> Welcome, Ghost Operator...")


from colorama import init, Fore, Style
init(autoreset=True)

def banner():
    ascii_art = Fore.RED + r"""
  ██████╗ ███████╗██╗███╗   ██╗████████╗
 ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
 ██║   ██║███████╗██║██╔██╗ ██║   ██║   
 ██║   ██║╚════██║██║██║╚██╗██║   ██║   
 ╚██████╔╝███████║██║██║ ╚████║   ██║   
  ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
""" + Style.RESET_ALL

    print(ascii_art)
    print(Fore.CYAN   + "########################################")
    print(Fore.CYAN   + "#              OSINT TOOLS              #")
    print(Fore.YELLOW + "#               Ghost Root              #")
    print(Fore.CYAN   + "########################################")

if __name__ == "_main_":
    banner()


def generate_usernames(name):
    base = name.strip().replace(" ", "")
    words = name.strip().split()
    base_lower = base.lower()
    combos = set()

    # Basic
    combos.add(base_lower)
    combos.add("".join(words).lower())
    combos.add("-".join(words).lower())
    combos.add(".".join(words).lower())

    # numeric suffixes
    for i in range(0, 20):
        combos.add(f"{base_lower}{i}")
    combos.add(base_lower + "123")
    combos.add(base_lower + "007")

    # prefixes & suffixes
    prefixes = ["real", "the", "official", "its", "mr", "ms", "iam"]
    suffixes = ["id", "ofc", "official", "real", "x", "id", "yt"]

    for p in prefixes:
        combos.add(f"{p}{base_lower}")
        combos.add(f"{p}_{base_lower}")

    for s in suffixes:
        combos.add(f"{base_lower}{s}")
        combos.add(f"{base_lower}_{s}")

    # reversed and leet-ish
    combos.add(base_lower[::-1])
    leet_map = str.maketrans({'o': '0', 'i': '1', 'e': '3', 'a': '4', 's': '5'})
    combos.add(base_lower.translate(leet_map))

    combos = {c for c in combos if len(c) >= 3}
    return sorted(combos)


def parse_input_name(raw_input):
    parts = [p.strip() for p in re.split(r"[,\s]+", raw_input) if p.strip()]
    name_parts, usernames = [], []
    for p in parts:
        if p.startswith("@"):
            usernames.append(p[1:])
        else:
            name_parts.append(p)
    return " ".join(name_parts), usernames


async def check_site(session, site, username, info):
    url = info["url"].format(username=username)
    try:
        async with session.get(url, headers=HEADERS, timeout=ClientTimeout(total=6)) as r:
            text = await r.text(errors="ignore")
            text_lower = text.lower() if isinstance(text, str) else ""

            exists = False
            try:
                exists = (r.status == 200) and info["check"](text, username)
            except Exception:
                exists = (r.status == 200) and (username.lower() in text_lower)

            if exists:
                inactive_keywords = ["not found", "doesn't exist", "404", "deactivated",
                                     "account suspended", "user not found", "profile unavailable",
                                     "banned", "removed", "page not found"]
                private_keywords = ["this account is private", "akun ini dikunci",
                                    "private account", "konten ini tidak tersedia",
                                    "this profile is private", "account private"]

                if any(k in text_lower for k in inactive_keywords):
                    status_flag = "inactive"
                elif any(k in text_lower for k in private_keywords):
                    status_flag = "private"
                else:
                    status_flag = "active"

                return {"site": site, "url": url, "found": True,
                        "status_account": status_flag, "username": username,
                        "status": r.status}

            return {"site": site, "url": url, "found": False,
                    "status_account": "not_found", "username": username,
                    "status": r.status}
    except Exception as exc:
        return {"site": site, "url": url, "found": False,
                "status_account": "error", "username": username,
                "status": None, "error": str(exc)}

async def scary_login_animation(stop_event):
    messages = [
        ">>> Initiating deep login sequence...",
        ">>> Bruteforcing hidden gateway...",
        ">>> Injecting ghost credentials...",
        "⚠ Multiple security alerts detected...",
        ">>> Bypassing intrusion detection system...",
        "✔ Ghost access granted - full system control"
    ]
    while not stop_event.is_set():
        for msg in messages:
            if stop_event.is_set():
                break
            glitch_text(msg)
            await asyncio.sleep(random.uniform(0.5, 1.0))


def hacker_progress_bar(total, prefix=">>> Executing scan"):
    bar_length = 40
    for i in range(total + 1):
        filled = int(bar_length * i // total) if total else bar_length
        bar = Fore.RED + "█" * filled + Fore.WHITE + "-" * (bar_length - filled)
        percent = f"{(i / total) * 100:3.0f}%" if total else "100%"
        sys.stdout.write(f"\r{prefix} |{bar}| {Fore.GREEN}{percent}{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.02 + random.uniform(0.005, 0.01))
    print()
    typing_effect("⚠ System anomaly detected...", 0.02, Fore.RED)
    time.sleep(0.3)
    typing_effect("✔ Progress bar completed - entering critical phase", 0.02, Fore.GREEN)


def print_grouped_report(results):
    found_by_site = defaultdict(list)
    for r in results:
        if r.get("found"):
            found_by_site[r["site"]].append((r["url"], r["username"], r.get("status_account", "unknown")))

    divider = "=" * 60
    print("\n" + divider)
    print("📊 HASIL SCANNING LENGKAP")
    print(divider)
    for site in SITES.keys():
        entries = found_by_site.get(site, [])
        if not entries:
            continue
        print(Fore.YELLOW + site + Style.RESET_ALL)
        for url, uname, status_flag in entries:
            if status_flag == "active":
                status = Fore.GREEN + "AKTIF"
            elif status_flag == "private":
                status = Fore.CYAN + "PRIVAT"
            elif status_flag == "inactive":
                status = Fore.RED + "NON-AKTIF"
            else:
                status = Fore.WHITE + status_flag.upper()
            print(f"   {Fore.GREEN}[✅]{Style.RESET_ALL} {url:<45} (username: {uname}) - {status}")
        print()
    print(divider)
    print("📌 RINGKASAN")
    print(divider)
    for site in SITES.keys():
        cnt = len(found_by_site.get(site, []))
        if cnt > 0:
            print(f"{site}: {cnt} akun")
    if not any(len(v) for v in found_by_site.values()):
        print("Tidak ada akun yang terdeteksi.")
    print()


def save_results(results, name):
    os.makedirs("results", exist_ok=True)
    safe_name = name.replace(" ", "_") if name else "target"
    filename = os.path.join("results", f"hasil_{safe_name}_{int(time.time())}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(Fore.GREEN + f"💾 Hasil lengkap tersimpan di: {Fore.CYAN}{filename}" + Style.RESET_ALL)


async def main():
    intro_loading()
    banner()

    raw = input(Fore.GREEN + "\nMasukkan nama Target : " + Style.RESET_ALL).strip()
    name, extra_usernames = parse_input_name(raw)

    print(f"\n{Fore.CYAN}Pilih mode scanning:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[1]{Style.RESET_ALL} Scan semua variasi dari nama")
    print(f"{Fore.YELLOW}[2]{Style.RESET_ALL} Hanya username langsung (@)")
    print(f"{Fore.YELLOW}[3]{Style.RESET_ALL} Gabungan nama + username (@)")
    choice = input(Fore.GREEN + ">> Pilihan (1/2/3): ").strip()

    if choice == "2":
        username_variants = extra_usernames
    elif choice == "3":
        username_variants = generate_usernames(name) + extra_usernames
    else:
        username_variants = generate_usernames(name)

    username_variants = sorted(set(username_variants))
    print(f"\n{Fore.RED}🔎 Total variasi dicek: {Fore.GREEN}{len(username_variants)}\n")

    results = []
    connector = aiohttp.TCPConnector(limit=100, ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [check_site(session, site, uname, info)
                 for uname in username_variants
                 for site, info in SITES.items()]

        stop_event = asyncio.Event()
        spin_task = asyncio.create_task(scary_login_animation(stop_event))

        hacker_progress_bar(100, prefix=">>> Scanning all platforms")

        for future in asyncio.as_completed(tasks):
            res = await future
            results.append(res)
            if res.get("found"):
                status = res.get("status_account", "unknown")
                print(f"\n{Fore.GREEN}[✅] {res['site']} → {res['url']} (username: {res['username']}) - {status.upper()}")

        stop_event.set()
        await spin_task

    save_results(results, name if name else raw)
    print_grouped_report(results)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n" + Fore.RED + "Dihentikan oleh pengguna." + Style.RESET_ALL)