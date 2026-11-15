# Changelog

Updates to the [Google News Scraper](https://apify.com/data_xplorer/google-news-scraper-fast) Actor used by this repository. Click **Watch > Custom > Releases** at the top of the page to be notified of new ones.

## Actor v3.1 (2026-11-13)

- Full article text: set `extractFullText` (`--full-text` in the script) to get a `fullText` field with the body of each article.
- Custom date ranges: `dateFrom` and `dateTo` (`--from` / `--to`) search any period instead of a fixed timeframe.
- More than 100 articles per keyword: above 100, the search is split into smaller date windows and merged.
- No more duplicates on large runs: articles found through several windows are returned once.
