#!/usr/bin/env python3
"""
Утилита для управления списками доменов и подсетей.

Источник правды: domains.csv (domain, category)
IP-подсети: Subnets/IPv4/ и Subnets/IPv6/ (генерируются get-subnets.py)

Команды:
  python convert.py build    — пересобрать все файлы из domains.csv
  python convert.py surge    — пересоздать *-surge.list файлы для Shadowrocket
  python convert.py minus    — пересоздать Minus/ файлы для сплит-тоннелей
  python convert.py subnets  — пересоздать Minus/ subnet-файлы (нужен Subnets/)
  python convert.py singbox  — пересоздать sing-box/ rule-set (.json + .srs)
  python convert.py all      — выполнить все (рекомендуется)
"""

import csv, ipaddress, os, sys, glob, json, shutil, subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOMAINS_CSV = os.path.join(BASE_DIR, "domains.csv")

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
    ("blocked",         "Categories/19-blocked"),
    ("russia-outside",  "Russia/russia-outside"),
]
CATEGORY_PATH = {slug: path for slug, path in CATEGORIES}

# Категории, не входящие в russia-all и Minus-файлы
RUSSIA_ALL_EXCLUDE = {"russia-outside"}

# Категории, для которых генерируются subnet minus-файлы (slug, prefix, has_v6)
SUBNET_CATEGORIES = [
    ("discord",     "02-discord",     False),
    ("meta",        "03-meta",        True),
    ("telegram",    "04-telegram",    True),
    ("twitter",     "05-twitter",     True),
    ("google-meet", "08-google-meet", False),
    ("hodca",       "14-hodca",       True),
    ("zscaler",     "20-zscaler",     True),
]

# Каталог sing-box rule-set (исходники .json + скомпилированные .srs)
SINGBOX_DIR = "sing-box"


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

    all_domains = [r["domain"] for r in rows if r["category"] not in RUSSIA_ALL_EXCLUDE]
    write_lst(os.path.join(BASE_DIR, "Russia", "russia-all"), all_domains)
    print(f"[build] Russia/russia-all.lst: {len(all_domains)}")


def _is_ip_cidr(s):
    try:
        ipaddress.ip_network(s, strict=False)
        return True
    except ValueError:
        return False


def to_surge(lst_file, out_file):
    entries = []
    with open(lst_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                entries.append(line)
    if not entries:
        return 0
    with open(out_file, "w", encoding="utf-8") as f:
        for e in entries:
            if e.startswith("."):
                e = e[1:]
            if _is_ip_cidr(e):
                net = ipaddress.ip_network(e, strict=False)
                tag = "IP-CIDR6" if net.version == 6 else "IP-CIDR"
                f.write(f"{tag},{e}\n")
            else:
                f.write(f"DOMAIN-SUFFIX,{e}\n")
    return len(entries)


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
    all_domains = set(r["domain"] for r in rows if r["category"] not in RUSSIA_ALL_EXCLUDE)
    by_cat = {}
    for r in rows:
        if r["category"] not in RUSSIA_ALL_EXCLUDE:
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


def _read_subnet_lst(path):
    if not os.path.exists(path):
        return set()
    entries = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                entries.add(line)
    return entries


def generate_subnet_minus():
    subnets_dir = os.path.join(BASE_DIR, "Subnets")
    if not os.path.isdir(subnets_dir):
        print("[subnet-minus] Subnets/ не найден — сначала запустите get-subnets.py")
        return

    minus_dir = os.path.join(BASE_DIR, "Minus")
    os.makedirs(minus_dir, exist_ok=True)

    for version, v_suffix in [("IPv4", "v4"), ("IPv6", "v6")]:
        ver_dir = os.path.join(subnets_dir, version)
        if not os.path.isdir(ver_dir):
            continue

        all_entries = set()
        for _, prefix, has_v6 in SUBNET_CATEGORIES:
            if version == "IPv6" and not has_v6:
                continue
            all_entries |= _read_subnet_lst(os.path.join(ver_dir, f"{prefix}.lst"))

        if not all_entries:
            continue

        for _, prefix, has_v6 in SUBNET_CATEGORIES:
            if version == "IPv6" and not has_v6:
                continue
            cat_entries = _read_subnet_lst(os.path.join(ver_dir, f"{prefix}.lst"))
            if not cat_entries:
                continue
            remainder = all_entries - cat_entries
            out_path = os.path.join(minus_dir, f"minus-{prefix}-{v_suffix}")
            write_lst(out_path, remainder)
            print(f"[subnet-minus] Minus/minus-{prefix}-{v_suffix}.lst: {len(remainder)}")


def _singbox_rules(entries):
    """Разбить записи на domain_suffix / ip_cidr и собрать правила sing-box."""
    domains, ips = [], []
    for e in entries:
        e = e.strip()
        if not e or e.startswith("#"):
            continue
        if e.startswith("."):
            e = e[1:]
        (ips if _is_ip_cidr(e) else domains).append(e)
    rules = []
    if domains:
        rules.append({"domain_suffix": sorted(set(domains))})
    if ips:
        # v4 численно, затем v6 — детерминированно и читаемо
        def _ip_key(c):
            net = ipaddress.ip_network(c, strict=False)
            return (net.version, int(net.network_address), net.prefixlen)
        rules.append({"ip_cidr": sorted(set(ips), key=_ip_key)})
    return rules


def _write_singbox_json(name, entries):
    """Записать sing-box/<name>.json (schema version 1). Вернуть путь либо None."""
    rules = _singbox_rules(entries)
    if not rules:
        return None
    sb_dir = os.path.join(BASE_DIR, SINGBOX_DIR)
    os.makedirs(sb_dir, exist_ok=True)
    path = os.path.join(sb_dir, name + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"version": 1, "rules": rules}, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return path


def _compile_singbox(json_paths):
    """Скомпилировать .srs рядом с каждым .json, если в PATH есть sing-box."""
    sb = shutil.which("sing-box")
    if not sb:
        print("[singbox] sing-box не найден в PATH — .srs пропущены (JSON готов); "
              "установите sing-box для компиляции .srs")
        return
    for jp in json_paths:
        srs = os.path.splitext(jp)[0] + ".srs"
        subprocess.run([sb, "rule-set", "compile", "--output", srs, jp], check=True)
    print(f"[singbox] Скомпилировано .srs: {len(json_paths)}")


def generate_singbox():
    rows = read_csv()
    by_cat = {}
    for r in rows:
        by_cat.setdefault(r["category"], []).append(r["domain"])

    written = []
    # доменные rule-set по категориям
    for slug, _ in CATEGORIES:
        p = _write_singbox_json(slug, by_cat.get(slug, []))
        if p:
            written.append(p)

    # сводный список всех доменов (кроме russia-outside)
    all_domains = [r["domain"] for r in rows if r["category"] not in RUSSIA_ALL_EXCLUDE]
    p = _write_singbox_json("russia-all", all_domains)
    if p:
        written.append(p)

    # IP rule-set по категориям (IPv4 + IPv6 в одном ip_cidr)
    subnets_dir = os.path.join(BASE_DIR, "Subnets")
    if os.path.isdir(subnets_dir):
        for slug, prefix, has_v6 in SUBNET_CATEGORIES:
            cidrs = _read_subnet_lst(os.path.join(subnets_dir, "IPv4", f"{prefix}.lst"))
            if has_v6:
                cidrs |= _read_subnet_lst(os.path.join(subnets_dir, "IPv6", f"{prefix}.lst"))
            p = _write_singbox_json(f"{slug}-ip", cidrs)
            if p:
                written.append(p)
        # сводный IP rule-set (все подсети, v4 + v6)
        all_ip = _read_subnet_lst(os.path.join(subnets_dir, "IPv4", "all.lst")) \
               | _read_subnet_lst(os.path.join(subnets_dir, "IPv6", "all.lst"))
        p = _write_singbox_json("subnets-ip", all_ip)
        if p:
            written.append(p)

    print(f"[singbox] JSON rule-set: {len(written)}")
    _compile_singbox(written)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd == "build":
        build()
    elif cmd == "surge":
        generate_surge()
    elif cmd == "minus":
        generate_minus()
    elif cmd == "subnets":
        generate_subnet_minus()
    elif cmd == "singbox":
        generate_singbox()
    elif cmd == "all":
        build(); print()
        generate_minus(); print()
        generate_subnet_minus(); print()
        generate_surge(); print()
        generate_singbox()
    else:
        print(__doc__)
