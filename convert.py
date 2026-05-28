#!/usr/bin/env python3
"""
Утилита для управления списками доменов.

Источник правды: domains.csv (domain, category)

Команды:
  python convert.py build   — пересобрать все файлы из domains.csv
  python convert.py surge   — пересоздать *-surge.list файлы для Shadowrocket
  python convert.py minus   — пересоздать Minus/ файлы для сплит-тоннелей
  python convert.py all     — выполнить все три (рекомендуется)
"""

import csv, os, sys, glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOMAINS_CSV = os.path.join(BASE_DIR, "domains.csv")

# Порядок категорий (определяет нумерацию и порядок в README)
CATEGORIES = [
    ("youtube",      "Categories/01-youtube"),
    ("discord",      "Categories/02-discord"),
    ("meta",         "Categories/03-meta"),
    ("telegram",     "Categories/04-telegram"),
    ("twitter",      "Categories/05-twitter"),
    ("google-ai",    "Categories/06-google-ai"),
    ("google-play",  "Categories/07-google-play"),
    ("google-meet",  "Categories/08-google-meet"),
    ("tiktok",       "Categories/09-tiktok"),
    ("hdrezka",      "Categories/10-hdrezka"),
    ("roblox",       "Categories/11-roblox"),
    ("openai",       "Categories/12-openai"),
    ("claude",       "Categories/13-claude"),
    ("hodca",        "Categories/14-hodca"),
    ("ru-ip-blocked","Categories/15-ru-ip-blocked"),
    ("news",         "Categories/16-news"),
    ("anime",        "Categories/17-anime"),
    ("adult",        "Categories/18-adult"),
    ("blocked",      "Categories/19-blocked"),
]
CATEGORY_PATH = {slug: path for slug, path in CATEGORIES}


def read_csv():
    with open(DOMAINS_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_lst(path, domains):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + ".lst", "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(domains)) + "\n")


def build():
    rows = read_csv()
    by_cat = {}
    for r in rows:
        by_cat.setdefault(r["category"], []).append(r["domain"])

    for slug, path in CATEGORIES:
        domains = by_cat.get(slug, [])
        if not domains:
            continue
        full = os.path.join(BASE_DIR, path)
        write_lst(full, domains)
        print(f"[build] {path}.lst: {len(domains)}")

    all_domains = [r["domain"] for r in rows]
    write_lst(os.path.join(BASE_DIR, "Russia", "russia-all"), all_domains)
    print(f"[build] Russia/russia-all.lst: {len(all_domains)}")


def to_surge(lst_file, out_file):
    domains = []
    with open(lst_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                domains.append(line)
    if not domains:
        return 0
    with open(out_file, "w", encoding="utf-8") as f:
        for d in domains:
            if d.startswith("."):
                d = d[1:]
            if d[0].isdigit() or "/" in d:
                f.write(f"IP-CIDR,{d}\n")
            else:
                f.write(f"DOMAIN-SUFFIX,{d}\n")
    return len(domains)


def generate_surge():
    skip = ["dnsmasq", "kvas", "mikrotik", "clashx", "outside-raw", "inside-raw"]
    lst_files = sorted(glob.glob(os.path.join(BASE_DIR, "**", "*.lst"), recursive=True))
    n = 0
    for lst in lst_files:
        if any(p in lst for p in skip) or "-surge" in lst:
            continue
        out = lst.replace(".lst", "-surge.list")
        count = to_surge(lst, out)
        print(f"[surge] {os.path.relpath(lst, BASE_DIR)} ({count})")
        n += 1
    print(f"[surge] Готово: {n} файлов")


def generate_minus():
    rows = read_csv()
    all_domains = set(r["domain"] for r in rows)
    by_cat = {}
    for r in rows:
        by_cat.setdefault(r["category"], set()).add(r["domain"])

    minus_dir = os.path.join(BASE_DIR, "Minus")
    os.makedirs(minus_dir, exist_ok=True)

    for i, (slug, _) in enumerate(CATEGORIES, 1):
        if slug not in by_cat:
            continue
        remainder = all_domains - by_cat[slug]
        num = f"{i:02d}"
        path = os.path.join(minus_dir, f"minus-{num}-{slug}")
        write_lst(path, remainder)
        print(f"[minus] Minus/minus-{num}-{slug}.lst: {len(remainder)}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd == "build":
        build()
    elif cmd == "surge":
        generate_surge()
    elif cmd == "minus":
        generate_minus()
    elif cmd == "all":
        build(); print()
        generate_minus(); print()
        generate_surge()
    else:
        print(__doc__)
