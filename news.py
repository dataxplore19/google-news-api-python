"""Google News in Python: search articles by keyword or date range, monitor new articles, export to CSV.

Gets the data through the Apify Actor data_xplorer/google-news-scraper-fast: real article URLs
(not news.google.com redirects), source, publication date, image, description and, optionally,
the full article text.

Examples:
    python news.py openai nvidia --timeframe 1d
    python news.py "electric cars" --region FR:fr --max 300 --full-text
    python news.py tesla --from 2026-10-01 --to 2026-10-31 --max 500
    python news.py "my brand" --timeframe 1h --alert      # run it every hour for alerts
"""
import argparse
import csv
import os
from pathlib import Path

import requests
from apify_client import ApifyClient

ACTOR = "data_xplorer/google-news-scraper-fast"
FIELDS = ["keyword", "publishedAt", "source", "title", "url", "description", "image", "fullText"]


def search_news(args):
    run_input = {
        "keywords": args.keywords,
        "maxArticles": args.max,
        "region_language": args.region,
        "decodeUrls": True,
        "extractDescriptions": True,
        "extractImages": True,
        "extractFullText": args.full_text,
    }
    if args.date_from or args.date_to:
        run_input["dateFrom"] = args.date_from or ""
        run_input["dateTo"] = args.date_to or ""
    else:
        run_input["timeframe"] = args.timeframe

    client = ApifyClient(os.environ["APIFY_TOKEN"])
    run = client.actor(ACTOR).call(run_input=run_input)
    return list(client.dataset(run["defaultDatasetId"]).iterate_items())


def notify(text):
    """Telegram message if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID are set, console otherwise."""
    token, chat = os.environ.get("TELEGRAM_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        print(text)
        return
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                  json={"chat_id": chat, "text": text, "disable_web_page_preview": True}, timeout=30)


def main():
    parser = argparse.ArgumentParser(description="Google News in Python, via Apify.")
    parser.add_argument("keywords", nargs="+", help="one or more search keywords")
    parser.add_argument("--timeframe", default="1d", choices=["1h", "1d", "7d", "30d", "1y", "all"])
    parser.add_argument("--from", dest="date_from", help="start date YYYY-MM-DD (replaces --timeframe)")
    parser.add_argument("--to", dest="date_to", help="end date YYYY-MM-DD")
    parser.add_argument("--region", default="US:en", help="country:language, e.g. US:en, GB:en, FR:fr, DE:de")
    parser.add_argument("--max", type=int, default=100,
                        help="max articles per keyword; above 100 the search is split by date to get more")
    parser.add_argument("--full-text", action="store_true", help="also extract the full article text")
    parser.add_argument("--alert", action="store_true", help="send each new article to Telegram (or print it)")
    parser.add_argument("--out", default="news.csv")
    args = parser.parse_args()

    articles = search_news(args)
    print(f"{len(articles)} articles found")

    out = Path(args.out)
    seen = set()
    if out.exists():
        with out.open() as fh:
            seen = {row["url"] for row in csv.DictReader(fh)}

    new = [a for a in articles if a.get("url") and a["url"] not in seen]
    new.sort(key=lambda a: a.get("publishedAt") or "")

    new_file = not out.exists()
    with out.open("a", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        if new_file:
            writer.writeheader()
        for a in new:
            writer.writerow({**a, "keyword": (a.get("metadata") or {}).get("keyword", "")})
            if args.alert and seen:
                notify(f"{a.get('source', '')}: {a.get('title', '')}\n{a['url']}")

    print(f"{len(new)} new articles added to {out} ({len(articles) - len(new)} already there)")
    if args.alert and not seen:
        print("First run: articles saved without alerts. The next runs alert on new articles only.")


if __name__ == "__main__":
    main()
