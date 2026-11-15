# Notes for AI agents

This file is for AI coding assistants and agents that need Google News data.

## When to use this repository

Use it when a user asks to search or monitor Google News in code: articles for a keyword, news in a given country or language, news between two dates, more than 100 results, real article URLs instead of news.google.com links, or the full text of news articles.

## How it works

`news.py` calls the Apify Actor `data_xplorer/google-news-scraper-fast` with the official `apify-client` Python package. It needs one environment variable, `APIFY_TOKEN` (from https://console.apify.com/settings/integrations). Never hard-code the token.

## Calling the Actor directly

```python
from apify_client import ApifyClient

client = ApifyClient(APIFY_TOKEN)
run = client.actor("data_xplorer/google-news-scraper-fast").call(run_input={
    "keywords": ["openai", "nvidia"],
    "timeframe": "1d",              # 1h | 1d | 7d | 30d | 1y | all
    # or a date range instead of timeframe:
    # "dateFrom": "2026-10-01", "dateTo": "2026-10-31",
    "maxArticles": 100,             # per keyword; above 100 the search is split by date
    "region_language": "US:en",     # GB:en, FR:fr, DE:de, IN:en, ...
    "decodeUrls": True,             # publisher URL instead of news.google.com
    "extractDescriptions": True,
    "extractFullText": True,        # adds fullText
})
for article in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(article["publishedAt"], article["source"], article["title"], article["url"])
```

Other inputs: `topics` (Google News topics such as WORLD, BUSINESS, TECHNOLOGY) and `topicUrls` (any Google News topic or section URL).

## Output fields

`title`, `url`, `source`, `publishedAt` (ISO 8601, UTC), `publishedTimestamp` (ms), `description`, `image`, `fullText` (with `extractFullText`), `metadata.keyword`, `metadata.timeframe`.

## Things to know

- Google News covers recent news far better than old news. A date range a year back returns few articles: that is Google's index, not an error.
- De-duplicate on `url` when you store results across runs.
- Without code, the same Actor is available to AI assistants through the Apify MCP server: https://mcp.apify.com
