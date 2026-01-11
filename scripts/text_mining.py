"""Text-mining utilities for central bank communication.
"""

import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.bankofengland.co.uk"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; academic-research/1.0)",
}

MONTHS = [
    "january", "february", "march", "april",
    "may", "june", "july", "august",
    "september", "october", "november", "december",
]


def build_mpsm_url(year, month_name):
    """Build the URL for a given year and month name."""
    month_slug = month_name.lower()
    return f"{BASE_URL}/monetary-policy-summary-and-minutes/{year}/{month_slug}-{year}"


def fetch_html(url, headers=None, timeout=20):
    """Fetch a page and return its HTML text or None on error/404."""
    if headers is None:
        headers = HEADERS
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return resp.text
    except requests.exceptions.RequestException:
        return None


def extract_minutes_from_soup(soup):
    """Extract title, date and main text content from an MPC minutes page."""
    title_el = soup.find("h1")
    title = title_el.get_text(strip=True) if title_el else ""

    date_el = soup.find("time")
    date_text = date_el.get_text(strip=True) if date_el else ""

    main = (
        soup.select_one("[role='main']")
        or soup.select_one(".article-body")
        or soup.select_one(".content")
        or soup.body
    )

    for tag in main.find_all(["nav", "aside", "footer", "script", "style"]):
        tag.decompose()

    text = main.get_text(separator="\n", strip=True)

    return {
        "title": title,
        "date": date_text,
        "text": text,
    }


def scrape_boe_mpc_minutes(start_year, end_year, months=None, sleep_sec=1.0):
    """Scrape Bank of England MPC minutes into a pandas DataFrame.

    Parameters

    start_year : int
        First year to scrape (inclusive).
    end_year : int
        Last year to scrape (inclusive).
    months : list[str] or None
        List of month names (e.g. ["january", "february"]).
        If None, all 12 months are used.
    sleep_sec : float
        Delay between requests to be polite to the server.
    """
    if months is None:
        months = MONTHS

    rows = []

    for year in range(start_year, end_year + 1):
        for month in months:
            url = build_mpsm_url(year, month)
            html = fetch_html(url)
            if html is None:
                continue

            soup = BeautifulSoup(html, "lxml")
            info = extract_minutes_from_soup(soup)
            info.update({
                "year": year,
                "month": month,
                "url": url,
            })
            rows.append(info)

            time.sleep(sleep_sec)

    df = pd.DataFrame(rows)
    if not df.empty:
        df["text"] = df["text"].str.replace(r"\s+", " ", regex=True).str.strip()

    return df
