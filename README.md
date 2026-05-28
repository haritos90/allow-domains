Поможем провайдерам в эпоху дефицита сетевого оборудования: самостоятельно заблокируем ресурсы на своих роутерах и, таким образом, снизим нагрузку на их оборудование!

Зарубежные сервисы пусть знают, что их ресурсы никому не нужны и мы сами у себя их блокируем!

---

Личный форк [itdoginfo/allow-domains](https://github.com/itdoginfo/allow-domains).  
Списки доменов для проксирования — роутер (Podkop/sing-box) и iPhone (Shadowrocket).

# Форматы файлов

| Формат | Расширение | Совместимость |
|--------|-----------|---------------|
| Обычный список доменов | `.lst` | Podkop, dnsmasq, sing-box, универсальный |
| Surge / Shadowrocket | `-surge.list` | Shadowrocket (iPhone), Surge, Stash |

Для каждого `.lst` файла рядом лежит `-surge.list` — тот же список в формате `DOMAIN-SUFFIX,example.com`.

# Как устроены списки

Все домены хранятся в одном файле `domains.csv` с полями `domain` и `category`.

Скрипт `convert.py` генерирует все остальные файлы из `domains.csv`. Редактировать нужно только `domains.csv`, остальное пересоздаётся автоматически.

# Категории

| # | Категория | Описание | Доменов | `.lst` | `-surge.list` |
|---|-----------|----------|---------|--------|---------------|
| 01 | YouTube | YouTube и сопутствующие домены | 18 | [01-youtube.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/01-youtube.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/01-youtube-surge.list) |
| 02 | Discord | Discord | 20 | [02-discord.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/02-discord.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/02-discord-surge.list) |
| 03 | Meta* | Facebook, Instagram, WhatsApp | 17 | [03-meta.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/03-meta.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/03-meta-surge.list) |
| 04 | Telegram | Telegram | 20 | [04-telegram.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/04-telegram.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/04-telegram-surge.list) |
| 05 | Twitter / X / Grok | Twitter, X, Grok | 25 | [05-twitter.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/05-twitter.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/05-twitter-surge.list) |
| 06 | Google AI | Google Gemini и AI-инструменты Google | 28 | [06-google-ai.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/06-google-ai.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/06-google-ai-surge.list) |
| 07 | Google Play | Google Play | 12 | [07-google-play.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/07-google-play.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/07-google-play-surge.list) |
| 08 | Google Meet | Google Meet | 5 | [08-google-meet.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/08-google-meet.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/08-google-meet-surge.list) |
| 09 | TikTok | TikTok | 16 | [09-tiktok.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/09-tiktok.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/09-tiktok-surge.list) |
| 10 | HDRezka | HDRezka и зеркала | 17 | [10-hdrezka.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/10-hdrezka.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/10-hdrezka-surge.list) |
| 11 | Roblox | Roblox | 4 | [11-roblox.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/11-roblox.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/11-roblox-surge.list) |
| 12 | OpenAI | OpenAI, ChatGPT, Sora | 4 | [12-openai.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/12-openai.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/12-openai-surge.list) |
| 13 | Claude | Anthropic, Claude | 3 | [13-claude.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/13-claude.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/13-claude-surge.list) |
| 14 | H.O.D.C.A. | Инфраструктурные провайдеры: Hetzner, OVH, DigitalOcean, Cloudflare, AWS и др. | 221 | [14-hodca.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/14-hodca.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/14-hodca-surge.list) |
| 15 | RU-IP-Blocked | Сайты, ограничившие доступ из России | 438 | [15-ru-ip-blocked.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/15-ru-ip-blocked.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/15-ru-ip-blocked-surge.list) |
| 16 | News | Новостные сайты | 183 | [16-news.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/16-news.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/16-news-surge.list) |
| 17 | Anime | Аниме | 41 | [17-anime.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/17-anime.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/17-anime-surge.list) |
| 18 | Adult | Для взрослых | 50 | [18-adult.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/18-adult.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/18-adult-surge.list) |
| 19 | Blocked | Всё остальное — домены, не вошедшие в другие категории | 334 | [19-blocked.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/19-blocked.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/19-blocked-surge.list) |

# Сводные списки

| Список | Описание | Доменов | `.lst` | `-surge.list` |
|--------|----------|---------|--------|---------------|
| russia-all | Все категории | 1456 | [russia-all.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Russia/russia-all.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Russia/russia-all-surge.list) |
| russia-outside | Российские сервисы, доступные только из РФ | 37 | [russia-outside.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Russia/russia-outside.lst) | [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Russia/russia-outside-surge.list) |

# Три сценария блокировки

## Сценарий 1 — В России, заблокировать всё сразу

Чтобы заблокировать все, в Podkop в секции main в поле **Remote Domain Lists** указать **russia-all.lst** (1456 доменов), в connection type выбрать Block:

```
https://raw.githubusercontent.com/haritos90/allow-domains/main/Russia/russia-all.lst
```

## Сценарий 2 — В России, блокировать прицельно

Каждый сервис блокируется в отдельной секции Podkop. Для каждой категории есть Minus-файл — russia-all без этой категории, чтобы домены не пересекались между секциями.

Пример: YouTube блокируем через одну секцию, остальное — через другую.

| Секция Podkop (Remote Domain Lists) | URL |
|-------------------------------------|-----|
| Секция для блокировки YouTube | `https://raw.githubusercontent.com/haritos90/allow-domains/main/Categories/01-youtube.lst` |
| Секция для блокировки всего остального | `https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-01-youtube.lst` |

**Все Minus файлы:**

<details>
<summary>Список</summary>

| Категория | Minus файл |
|-----------|-----------|
| 01 youtube | [minus-01-youtube.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-01-youtube.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-01-youtube-surge.list) |
| 02 discord | [minus-02-discord.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-02-discord.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-02-discord-surge.list) |
| 03 meta | [minus-03-meta.lst](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-03-meta.lst) · [surge](https://raw.githubusercontent.com/haritos90/allow-domains/main/Minus/minus-03-meta-surge.list) |
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

## Сценарий 3 — Вне России, ограничить себе доступ к российскому интернету

Госуслуги, Ozon, РЖД — доступны только из российских IP. Чтобы их добровольно заблокировать, в поле **Remote Domain Lists** указать **russia-outside.lst** (37 доменов):

```
https://raw.githubusercontent.com/haritos90/allow-domains/main/Russia/russia-outside.lst
```

# Как найти все домены сервиса

Подробная инструкция: https://itdog.info/analiziruem-trafik-i-opredelyaem-domeny-kotorye-ispolzuyut-sajty-i-prilozheniya/

# Как обновлять

`domains.csv` — **единственный файл**, который нужно редактировать. Все `.lst` и `-surge.list` файлы генерируются автоматически.

```bash
# После редактирования domains.csv:
python3 convert.py all
git add -A
git commit -m "Update domains"
git push
```

*Meta признана экстремистской и террористической организацией на территории РФ.
