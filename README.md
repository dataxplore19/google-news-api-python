# Google News API for Python

Search Google News in Python and save the results to CSV: articles for any keyword, country and language, or a custom date range, with the real article URL, source, publication date, image, description and the full article text. You can also run it on a schedule and get a Telegram alert for each new article.

Google has no official Google News API, and the Google News RSS feed stops at about 100 items and only gives `news.google.com` redirect links. This script gets the data through the [Google News Scraper](https://apify.com/data_xplorer/google-news-scraper-fast) Actor on Apify, which decodes the links to the original article, splits the search by date to go past 100 results, and can extract the article text.

> Click **Watch > Custom > Releases** at the top of this page to be notified when the Actor gets new features. See the [changelog](CHANGELOG.md).

## What you can do

| Task | Command |
| --- | --- |
| Latest news for keywords | `python news.py openai nvidia --timeframe 1d` |
| News in another country and language | `python news.py "voiture électrique" --region FR:fr` |
| More than 100 articles for one keyword | `python news.py tesla --timeframe 30d --max 500` |
| Articles between two dates | `python news.py tesla --from 2026-10-01 --to 2026-10-31` |
| Full article text, for analysis or an LLM | `python news.py openai --full-text` |
| Alert for each new article (brand monitoring) | `python news.py "your brand" --timeframe 1h --alert` |

## Quick start

You need Python 3.9+ and an [Apify](https://apify.com) account (the free plan includes monthly credits).

```bash
git clone https://github.com/dataxplore19/google-news-api-python.git
cd google-news-api-python
pip install -r requirements.txt
export APIFY_TOKEN="your_apify_token"
python news.py openai --timeframe 1d --max 10 --full-text
```

Console:

```
10 articles found
10 new articles added to news.csv (0 already there)
```

`news.csv`:

```csv
keyword,publishedAt,source,title,url,description,image,fullText
openai,2026-11-14T19:16:38+00:00,The Decoder,OpenAI reassigns robotics researchers to other teams...,https://the-decoder.com/openai-reassigns-robotics-researchers-to-other-teams/,...,...,...
openai,2026-11-15T00:28:37+00:00,Mashable,OpenAI launches ChatGPT Wallet...,https://mashable.com/tech/openai-launches-chatgpt-wallet,...,...,...
```

## Options

- `keywords`: one or more search terms. Google News operators work inside a keyword (`"exact phrase"`, `site:reuters.com`, `-excluded`).
- `--timeframe`: `1h`, `1d` (default), `7d`, `30d`, `1y` or `all`.
- `--from` / `--to`: a date range (`YYYY-MM-DD`, both days included) instead of `--timeframe`. Google's date filter is approximate, so a few articles can be dated a day outside the range: filter on `publishedAt` if you need exact bounds. Google News indexes recent news much better than old news: expect around 100 articles per day for a popular keyword over the last weeks, far fewer for dates a year back.
- `--region`: country and language, such as `US:en`, `GB:en`, `IN:en`, `FR:fr`, `DE:de`, `ES:es`, `BR:pt-419`, `JP:ja`. 84 region and language pairs are supported.
- `--max`: maximum articles per keyword (default 100). Above 100, the Actor splits the period into smaller date windows and merges the results without duplicates.
- `--full-text`: adds the full text of each article (`fullText`).
- `--alert`: sends each new article to Telegram (or prints it). The first run only fills `news.csv`; the next runs alert on what is new.

Telegram alerts need two environment variables:

```bash
export TELEGRAM_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"
```

## Data returned for each article

| Field | Content |
| --- | --- |
| `title` | Headline |
| `url` | Original article URL (decoded, not a news.google.com link) |
| `source` | Publisher name |
| `publishedAt` | Publication date, ISO 8601 in UTC |
| `description` | Article summary |
| `image` | Main image URL |
| `fullText` | Full article text, with `--full-text` |

Results append to `news.csv` and are de-duplicated by URL, so you can run the script as often as you like.

## Run it on a schedule

Brand monitoring with cron, every hour:

```bash
0 * * * * cd /path/to/google-news-api-python && APIFY_TOKEN=your_apify_token /usr/bin/python3 news.py "your brand" --timeframe 1h --alert
```

## Use the data in pandas or with an LLM

```python
import pandas as pd

df = pd.read_csv("news.csv", parse_dates=["publishedAt"])
print(df.groupby("source").size().sort_values(ascending=False).head(10))

# Feed the full texts to a summarizer, a sentiment model or an LLM
texts = df["fullText"].dropna().tolist()
```


## Other languages

Prefer JavaScript? The same tool for Node.js: [google-news-api-node](https://github.com/dataxplore19/google-news-api-node).

## FAQ

### Is there an official Google News API?

No. Google deprecated its Google News Search API in 2011 and later turned it off. The options are the RSS feed (limited to about 100 items, with redirect links), paid news APIs with their own sources, or a scraper that reads Google News itself, like the one used here.

### How do I get more than 100 results from Google News?

Use `--max` above 100 with a timeframe of a week or more, or a date range. The Actor runs one search per smaller date window and merges the results.

### How do I get the real article URL instead of the news.google.com link?

The script turns on `decodeUrls`, so `url` is always the publisher's own URL.

### Can I get the full text of the articles?

Yes, with `--full-text`. The text is read from the publisher's page. A few paywalled sites only give the first paragraphs.

### Can I search news by topic instead of keyword?

Yes. The Actor also accepts Google News topics (World, Business, Technology...) and topic URLs. See the [Actor's input page](https://apify.com/data_xplorer/google-news-scraper-fast/input-schema).

### Can an AI agent use it?

Yes. See [AGENTS.md](AGENTS.md). The Actor is also available to AI assistants through the [Apify MCP server](https://mcp.apify.com).

## Disclosure

I am the author of the Google News Scraper Actor used by this script.

## License

MIT
