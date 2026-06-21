#!/usr/bin/env python3
"""
Утилита для получения IP-подсетей сервисов из официальных источников.

Генерирует Subnets/IPv4/ и Subnets/IPv6/.
Запускать отдельно при обновлении IP-диапазонов (требует интернет).

Использование:
  python3 get-subnets.py
"""

import ipaddress
import json
import os
import sys
import time

try:
    import requests
except ImportError:
    print("Нужен пакет requests: pip install requests")
    sys.exit(1)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HEADERS = {"User-Agent": "allow-domains/1.0"}
TIMEOUT = 30


def collapse(nets):
    return list(ipaddress.collapse_addresses(nets))


def write_subnet_file(path, nets):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for n in sorted(nets, key=lambda x: (x.version, int(x.network_address))):
            f.write(str(n) + "\n")


def fetch_ripe_prefixes(asns):
    """Получить анонсированные префиксы для списка ASN через RIPE Statistics API."""
    v4, v6 = [], []
    for asn in asns:
        url = f"https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS{asn}"
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        for p in r.json()["data"]["prefixes"]:
            try:
                net = ipaddress.ip_network(p["prefix"], strict=False)
                (v4 if net.version == 4 else v6).append(net)
            except ValueError:
                pass
        time.sleep(0.3)
    return v4, v6


def fetch_telegram():
    v4, v6 = [], []
    r = requests.get(
        "https://core.telegram.org/resources/cidr.txt",
        headers=HEADERS, timeout=TIMEOUT,
    )
    r.raise_for_status()
    for line in r.text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            net = ipaddress.ip_network(line, strict=False)
            (v4 if net.version == 4 else v6).append(net)
        except ValueError:
            pass
    ripe_v4, ripe_v6 = fetch_ripe_prefixes([44907, 59930, 62014, 62041, 211157])
    return collapse(v4 + ripe_v4), collapse(v6 + ripe_v6)


def fetch_discord():
    v4 = []
    url = "https://iplist.opencck.org/?format=text&data=cidr4&site=discord.gg&site=discord.media"
    r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    for line in r.text.splitlines():
        line = line.strip()
        if line:
            try:
                v4.append(ipaddress.ip_network(line, strict=False))
            except ValueError:
                pass
    v4.append(ipaddress.ip_network("104.16.0.0/12"))
    return collapse(v4), []


def fetch_meta():
    v4, v6 = fetch_ripe_prefixes([32934, 63293, 54115, 149642])
    return collapse(v4), collapse(v6)


def fetch_twitter():
    v4, v6 = fetch_ripe_prefixes([13414])
    return collapse(v4), collapse(v6)


def fetch_google_meet():
    v4_raw = [
        "74.125.0.0/16",
        "64.233.160.0/19",
        "66.102.0.0/20",
        "66.249.80.0/20",
        "72.14.192.0/18",
        "108.177.8.0/21",
        "173.194.0.0/16",
        "209.85.128.0/17",
        "216.58.192.0/19",
        "216.239.32.0/19",
    ]
    return [ipaddress.ip_network(x) for x in v4_raw], []


def fetch_hodca():
    """Cloudflare + CloudFront (AWS) + DigitalOcean + Hetzner + OVH."""
    v4, v6 = [], []

    for ver, lst in [("v4", v4), ("v6", v6)]:
        r = requests.get(
            f"https://www.cloudflare.com/ips-{ver}",
            headers=HEADERS, timeout=TIMEOUT,
        )
        r.raise_for_status()
        for line in r.text.splitlines():
            line = line.strip()
            if line:
                try:
                    lst.append(ipaddress.ip_network(line, strict=False))
                except ValueError:
                    pass

    r = requests.get(
        "https://ip-ranges.amazonaws.com/ip-ranges.json",
        headers=HEADERS, timeout=TIMEOUT,
    )
    r.raise_for_status()
    data = r.json()
    for p in data.get("prefixes", []):
        if p.get("service") == "CLOUDFRONT":
            try:
                v4.append(ipaddress.ip_network(p["ip_prefix"], strict=False))
            except ValueError:
                pass
    for p in data.get("ipv6_prefixes", []):
        if p.get("service") == "CLOUDFRONT":
            try:
                v6.append(ipaddress.ip_network(p["ipv6_prefix"], strict=False))
            except ValueError:
                pass

    ripe_v4, ripe_v6 = fetch_ripe_prefixes([14061, 24940, 16276])  # DO, Hetzner, OVH
    return collapse(v4 + ripe_v4), collapse(v6 + ripe_v6)


def fetch_zscaler():
    """Собственные IP-диапазоны Zscaler (hub + CENR по всем облакам).

    Покрывают и ZEN-узлы (ZIA), и ZPA-брокеры на инфраструктуре Zscaler.
    Источник: config.zscaler.com (hubs/cidr/recommended + cenr).
    """
    v4, v6 = [], []
    clouds = [
        "zscaler.net", "zscalerone.net", "zscalertwo.net", "zscalerthree.net",
        "zscloud.net", "zscalerten.net", "zscalerbeta.net",
    ]

    def add(prefix):
        try:
            net = ipaddress.ip_network(prefix, strict=False)
            (v4 if net.version == 4 else v6).append(net)
        except ValueError:
            pass

    for cloud in clouds:
        # агрегированные hub-диапазоны (recommended)
        r = requests.get(
            f"https://config.zscaler.com/api/{cloud}/hubs/cidr/json/recommended",
            headers=HEADERS, timeout=TIMEOUT,
        )
        r.raise_for_status()
        for p in r.json().get("hubPrefixes", []):
            add(p)

        # детальные диапазоны узлов (Cloud Enforcement Node Ranges)
        r = requests.get(
            f"https://config.zscaler.com/api/{cloud}/cenr/json",
            headers=HEADERS, timeout=TIMEOUT,
        )
        r.raise_for_status()
        for conts in r.json().values():
            if not isinstance(conts, dict):
                continue
            for cities in conts.values():
                if not isinstance(cities, dict):
                    continue
                for entries in cities.values():
                    if not isinstance(entries, list):
                        continue
                    for e in entries:
                        if isinstance(e, dict) and e.get("range"):
                            add(e["range"])
        time.sleep(0.3)

    return collapse(v4), collapse(v6)


# (fetch_func, has_v6)
BUILDERS = {
    "02-discord":     (fetch_discord,     False),
    "03-meta":        (fetch_meta,        True),
    "04-telegram":    (fetch_telegram,    True),
    "05-twitter":     (fetch_twitter,     True),
    "08-google-meet": (fetch_google_meet, False),
    "14-hodca":       (fetch_hodca,       True),
    "20-zscaler":     (fetch_zscaler,     True),
}


def main():
    all_v4, all_v6 = [], []

    for slug, (func, has_v6) in BUILDERS.items():
        print(f"[subnets] {slug}...", end=" ", flush=True)
        try:
            v4, v6 = func()
        except Exception as e:
            print(f"ОШИБКА: {e}")
            sys.exit(1)

        path_v4 = os.path.join(BASE_DIR, "Subnets", "IPv4", f"{slug}.lst")
        write_subnet_file(path_v4, v4)
        all_v4.extend(v4)
        msg = f"IPv4: {len(v4)}"

        if has_v6 and v6:
            path_v6 = os.path.join(BASE_DIR, "Subnets", "IPv6", f"{slug}.lst")
            write_subnet_file(path_v6, v6)
            all_v6.extend(v6)
            msg += f", IPv6: {len(v6)}"

        print(msg)

    all_v4_c = collapse(all_v4)
    write_subnet_file(os.path.join(BASE_DIR, "Subnets", "IPv4", "all.lst"), all_v4_c)
    print(f"[subnets] Subnets/IPv4/all.lst: {len(all_v4_c)}")

    if all_v6:
        all_v6_c = collapse(all_v6)
        write_subnet_file(os.path.join(BASE_DIR, "Subnets", "IPv6", "all.lst"), all_v6_c)
        print(f"[subnets] Subnets/IPv6/all.lst: {len(all_v6_c)}")

    print("[subnets] Готово")


if __name__ == "__main__":
    main()
