# Changelog

Updates to the [Google News Scraper](https://apify.com/data_xplorer/google-news-scraper-fast?fpr=6vi1cs) Actor used by this repository. Click **Watch > Custom > Releases** at the top of the page to be notified of new ones.

## Actor v3.2 (2026-11-18)

- Faster runs: a news site that answers slowly now gets 20 seconds at most, then the article is returned with what was found.
- More images: when an article page has no preview image tag, its main photo is used instead.
- No more timeouts: when a run is about to reach its time limit, it stops cleanly, keeps every article already saved and ends as succeeded.
- Cleaner `fullText`: promotional lines at the end of articles ("Learn more about...", "Join today") are removed.
- No change to the input or the output: nothing to update in your code.

## Actor v3.1 (2026-11-13)

- Full article text: set `extractFullText` (`--full-text` in the script) to get a `fullText` field with the body of each article.
- Custom date ranges: `dateFrom` and `dateTo` (`--from` / `--to`) search any period instead of a fixed timeframe.
- More than 100 articles per keyword: above 100, the search is split into smaller date windows and merged.
- No more duplicates on large runs: articles found through several windows are returned once.
