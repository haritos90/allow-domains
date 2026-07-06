# Списки доменов для блокировки

Поможем провайдерам в эпоху дефицита сетевого оборудования: самостоятельно заблокируем ресурсы на своих роутерах и, таким образом, снизим нагрузку на их оборудование!

Зарубежные сервисы пусть знают, что их ресурсы никому не нужны и мы сами у себя их блокируем!

Проект основан на [itdoginfo/allow-domains](https://github.com/itdoginfo/allow-domains). В оригинале нельзя распределить сервисы по разным секциям Podkop — здесь это реализовано через Minus-файлы либо вручную собирая группы из непересакающихся доменов.  
Списки сделаны для роутеров под OpenWRT (Podkop/sing-box) и iPhone (Shadowrocket).

---

## Legal Notice

This software is intended for development, testing, and research purposes only.

The author does not provide any guarantees regarding:

- availability of network access
- compatibility with specific services
- compliance with any external restrictions

Users are solely responsible for how they use this software and must comply with applicable laws.

## Usage Restrictions

This software is not intended to be used for bypassing access restrictions or violating applicable laws. The author does not support or encourage such use.

---

## Status

Alpha software — not intended for production use. The author sells nothing: not the app, access, configurations, subscriptions, or support; anything given is a voluntary donation.

---

# Форматы файлов

| Формат | Расширение | Совместимость |
|--------|-----------|---------------|
| Домены / подсети | `.lst` | Podkop, dnsmasq, sing-box, универсальный |
| Surge / Shadowrocket | `-surge.list` | Shadowrocket (iPhone), Surge, Stash |

Для каждого `.lst` файла рядом лежит `-surge.list` — тот же список в формате `DOMAIN-SUFFIX,example.com` (домены) или `IP-CIDR,x.x.x.x/y` / `IP-CIDR6,x::/y` (подсети).

# Как устроены списки

Списки состоят из групп доменов и связанных с ними подсетей.

Все домены хранятся в `domains.csv`. Скрипт `convert.py` генерирует из него все `.lst` и `-surge.list` файлы, включая Minus-файлы.

Не все сервисы можно полностью заблокировать по доменам, некоторые обращаются к своим серверам напрямую по фиксированным IP, минуя DNS. Для таких сервисов одних доменов недостаточно: нужно дополнительно блокировать трафик по IP через поле **Remote Subnet Lists** в Podkop. Скрипт `get-subnets.py` получает актуальные IP-диапазоны из официальных источников (RIPE, Cloudflare, Telegram) и создает списки подсетей.

У 6 доменных категорий есть соответствующие списки IP-подсетей; для них предусмотрены и доменные, и subnet Minus-файлы — чтобы при разбивке по секциям Podkop домены и IP-диапазоны оставались согласованными.

Отдельно есть категория **Zscaler** — только IP-подсети, без доменов. Zscaler Client Connector (ZIA-туннель и ZPA) гонит трафик на IP узлов/брокеров, а реальные домены спрятаны внутри TLS/DTLS-туннеля — поэтому ловить его можно только по IP-диапазонам. Для неё есть subnet Minus-файлы.

Для категорий, к которым нет списков подсетей, блокировка возможна просто по доменному имени.

# Категории

| # | Категория | Описание | Домены | IPv4 | IPv6 |
|---|-----------|----------|--------|------|------|
| 01 | YouTube | YouTube и сопутствующие домены | 18 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/01-youtube.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/01-youtube-surge.list) | — | — |
| 02 | Discord | Discord | 25 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/02-discord.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/02-discord-surge.list) | 8 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv4/02-discord.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv4/02-discord-surge.list) | — |
| 03 | Meta* | Facebook, Instagram, WhatsApp | 17 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/03-meta.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/03-meta-surge.list) | 68 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv4/03-meta.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv4/03-meta-surge.list) | 42 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv6/03-meta.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv6/03-meta-surge.list) |
| 04 | Telegram | Telegram | 20 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/04-telegram.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/04-telegram-surge.list) | 8 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv4/04-telegram.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv4/04-telegram-surge.list) | 4 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv6/04-telegram.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv6/04-telegram-surge.list) |
| 05 | Twitter / X / Grok | Twitter, X, Grok | 25 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/05-twitter.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/05-twitter-surge.list) | 13 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv4/05-twitter.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv4/05-twitter-surge.list) | 3 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv6/05-twitter.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv6/05-twitter-surge.list) |
| 06 | Google AI | Google Gemini и AI-инструменты Google | 28 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/06-google-ai.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/06-google-ai-surge.list) | — | — |
| 07 | Google Play | Google Play | 12 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/07-google-play.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/07-google-play-surge.list) | — | — |
| 08 | Google Meet | Google Meet | 5 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/08-google-meet.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/08-google-meet-surge.list) | 10 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv4/08-google-meet.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv4/08-google-meet-surge.list) | — |
| 09 | TikTok | TikTok | 16 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/09-tiktok.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/09-tiktok-surge.list) | — | — |
| 10 | HDRezka | HDRezka и зеркала | 17 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/10-hdrezka.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/10-hdrezka-surge.list) | — | — |
| 11 | Roblox | Roblox | 4 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/11-roblox.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/11-roblox-surge.list) | — | — |
| 12 | OpenAI | OpenAI, ChatGPT, Sora | 4 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/12-openai.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/12-openai-surge.list) | — | — |
| 13 | Claude | Anthropic, Claude | 3 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/13-claude.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/13-claude-surge.list) | — | — |
| 14 | H.O.D.C.A. | Инфраструктурные провайдеры: Hetzner, OVH, DigitalOcean, Cloudflare, AWS и др. | 221 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/14-hodca.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/14-hodca-surge.list) | 990 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv4/14-hodca.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv4/14-hodca-surge.list) | 60 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv6/14-hodca.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv6/14-hodca-surge.list) |
| 15 | RU-IP-Blocked | Сайты, ограничившие доступ из России | 438 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/15-ru-ip-blocked.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/15-ru-ip-blocked-surge.list) | — | — |
| 16 | News | Новостные сайты | 183 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/16-news.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/16-news-surge.list) | — | — |
| 17 | Anime | Аниме | 41 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/17-anime.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/17-anime-surge.list) | — | — |
| 18 | Adult | Для взрослых | 50 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/18-adult.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/18-adult-surge.list) | — | — |
| 19 | Blocked | Всё остальное — домены, не вошедшие в другие категории | 334 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/19-blocked.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/19-blocked-surge.list) | — | — |
| 20 | Zscaler | Zscaler Client Connector (ZIA/ZPA) — узлы и брокеры, только по IP | — | 50 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv4/20-zscaler.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv4/20-zscaler-surge.list) | 54 · [lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv6/20-zscaler.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv6/20-zscaler-surge.list) |

# Сводные списки

| Список | Описание | Записей | `.lst` | `-surge.list` |
|--------|----------|---------|--------|---------------|
| Все домены | Все 19 категорий | 1461 | [russia-all.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Russia/russia-all.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Russia/russia-all-surge.list) |
| Все подсети IPv4 | Discord, Meta*, Telegram, Twitter, Google Meet, H.O.D.C.A., Zscaler | 1143 | [all.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv4/all.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv4/all-surge.list) |
| Все подсети IPv6 | Meta*, Telegram, Twitter, H.O.D.C.A., Zscaler | 163 | [all.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv6/all.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv6/all-surge.list) |
| russia-outside | Российские сервисы, доступные только из РФ | 41 | [russia-outside.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Russia/russia-outside.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Russia/russia-outside-surge.list) |

# Три сценария блокировки

## Сценарий 1 — В России, заблокировать всё сразу

Чтобы заблокировать всё, в Podkop в секции main в поле **Remote Domain Lists** указать **russia-all.lst** (1456 доменов), в connection type выбрать Block:

```
https://raw.githubusercontent.com/haritos90/allow-domains/main/Russia/russia-all.lst
```

Также указать в поле **Remote Subnet Lists** (для сервисов с фиксированными IP):

```
https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv4/all.lst
```
```
https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv6/all.lst
```

## Сценарий 2 — В России, блокировать раздельно

Когда на определенный сервис нужна отдельная секции Podkop. Важно: для сервисов с IP-подсетями нужно настраивать оба поля — **Remote Domain Lists** и **Remote Subnet Lists**. Если указать только домены, трафик приложения, которое использует фиксированные IP, обойдёт правило.

**Пример: Telegram блокируется отдельно, всё остальное — через вторую секцию.**

Секция для блокировки Telegram, указать 3 списка:

| Поле Podkop | URL |
|-------------|-----|
| Remote Domain Lists | `https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/04-telegram.lst` |
| Remote Subnet Lists | `https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv4/04-telegram.lst` |
| Remote Subnet Lists | `https://raw.githubusercontent.com/haritos90/allow-domains/main/Subnets/IPv6/04-telegram.lst` |

Секция для блокировки всего остального, указать 3 Minus-файла:

| Поле Podkop | URL |
|-------------|-----|
| Remote Domain Lists | `https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-04-telegram.lst` |
| Remote Subnet Lists | `https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-04-telegram-v4.lst` |
| Remote Subnet Lists | `https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-04-telegram-v6.lst` |

Minus-файлы обеспечивают согласованность: домены и IP-диапазоны в обеих секциях не пересекаются и вместе полностью покрывают весь список.

**Все Minus-файлы:**

<details>
<summary>Домены</summary>

| Категория | Minus файл |
|-----------|-----------|
| 01 youtube | [minus-01-youtube.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-01-youtube.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-01-youtube-surge.list) |
| 02 discord | [minus-02-discord.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-02-discord.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-02-discord-surge.list) |
| 03 meta* | [minus-03-meta.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-03-meta.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-03-meta-surge.list) |
| 04 telegram | [minus-04-telegram.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-04-telegram.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-04-telegram-surge.list) |
| 05 twitter | [minus-05-twitter.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-05-twitter.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-05-twitter-surge.list) |
| 06 google-ai | [minus-06-google-ai.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-06-google-ai.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-06-google-ai-surge.list) |
| 07 google-play | [minus-07-google-play.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-07-google-play.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-07-google-play-surge.list) |
| 08 google-meet | [minus-08-google-meet.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-08-google-meet.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-08-google-meet-surge.list) |
| 09 tiktok | [minus-09-tiktok.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-09-tiktok.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-09-tiktok-surge.list) |
| 10 hdrezka | [minus-10-hdrezka.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-10-hdrezka.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-10-hdrezka-surge.list) |
| 11 roblox | [minus-11-roblox.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-11-roblox.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-11-roblox-surge.list) |
| 12 openai | [minus-12-openai.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-12-openai.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-12-openai-surge.list) |
| 13 claude | [minus-13-claude.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-13-claude.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-13-claude-surge.list) |
| 14 hodca | [minus-14-hodca.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-14-hodca.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-14-hodca-surge.list) |
| 15 ru-ip-blocked | [minus-15-ru-ip-blocked.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-15-ru-ip-blocked.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-15-ru-ip-blocked-surge.list) |
| 16 news | [minus-16-news.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-16-news.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-16-news-surge.list) |
| 17 anime | [minus-17-anime.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-17-anime.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-17-anime-surge.list) |
| 18 adult | [minus-18-adult.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-18-adult.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-18-adult-surge.list) |
| 19 blocked | [minus-19-blocked.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-19-blocked.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-19-blocked-surge.list) |

</details>

<details>
<summary>Подсети (IPv4 / IPv6)</summary>

| Категория | IPv4 Minus | IPv6 Minus |
|-----------|-----------|-----------|
| 02 discord | [minus-02-discord-v4.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-02-discord-v4.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-02-discord-v4-surge.list) | — |
| 03 meta* | [minus-03-meta-v4.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-03-meta-v4.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-03-meta-v4-surge.list) | [minus-03-meta-v6.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-03-meta-v6.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-03-meta-v6-surge.list) |
| 04 telegram | [minus-04-telegram-v4.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-04-telegram-v4.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-04-telegram-v4-surge.list) | [minus-04-telegram-v6.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-04-telegram-v6.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-04-telegram-v6-surge.list) |
| 05 twitter | [minus-05-twitter-v4.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-05-twitter-v4.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-05-twitter-v4-surge.list) | [minus-05-twitter-v6.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-05-twitter-v6.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-05-twitter-v6-surge.list) |
| 08 google-meet | [minus-08-google-meet-v4.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-08-google-meet-v4.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-08-google-meet-v4-surge.list) | — |
| 14 hodca | [minus-14-hodca-v4.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-14-hodca-v4.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-14-hodca-v4-surge.list) | [minus-14-hodca-v6.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-14-hodca-v6.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-14-hodca-v6-surge.list) |
| 20 zscaler | [minus-20-zscaler-v4.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-20-zscaler-v4.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-20-zscaler-v4-surge.list) | [minus-20-zscaler-v6.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-20-zscaler-v6.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-20-zscaler-v6-surge.list) |

</details>

## Сценарий 3 — Вне России, ограничить себе доступ к российскому интернету

Госуслуги, Ozon, РЖД — доступны только из российских IP. Чтобы их добровольно заблокировать, в поле **Remote Domain Lists** указать **russia-outside.lst** (37 доменов):

```
https://raw.githubusercontent.com/haritos90/allow-domains/main/Russia/russia-outside.lst
```

# Как найти все домены сервиса

Подробная инструкция: https://itdog.info/analiziruem-trafik-i-opredelyaem-domeny-kotorye-ispolzuyut-sajty-i-prilozheniya/

# Как обновлять

`domains.csv` — **единственный файл**, который нужно редактировать: все 19 категорий и `russia-outside`. Все `.lst` и `-surge.list` файлы генерируются автоматически.

```bash
# Обновить IP-диапазоны (требует интернет, ~30 сек):
python3 get-subnets.py

# После редактирования domains.csv или обновления подсетей:
python3 convert.py all
git add -A
git commit -m "feat: add domains"   # сообщения — по Conventional Commits (feat/fix/chore/docs)
git push
```

# Сравнение списков доменов с upstream

Проект основан на [itdoginfo/allow-domains](https://github.com/itdoginfo/allow-domains). Последняя проверка — коммит `8d45624` (2026-07-06): перенесены 53 новых домена. Чтобы посмотреть, какие домены добавили в апстрим с тех пор:

```bash
# Подключить апстрим как второй источник (один раз):
git remote add upstream https://github.com/itdoginfo/allow-domains.git

# Проверка:
git fetch upstream
git diff 8d45624..upstream/main -- 'Categories/*.lst' 'Services/*.lst'
```

Нужные домены из вывода переносятся вручную в `domains.csv`. После переноса обновить хеш `8d45624` на актуальный (`git rev-parse --short upstream/main`), чтобы следующее сравнение начиналось с новой точки.

*Meta признана экстремистской и террористической организацией на территории РФ.
