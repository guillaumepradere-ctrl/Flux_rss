import re
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

## INIT ##
URL = "https://entreprises.selectra.info/energie/gaz/marche-de-gros"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

html = requests.get(URL, headers=headers).text

## GET CHART HEADER TITLE
soup = BeautifulSoup(html, "html.parser")
chart_titles = {}
for el in soup.find_all(id=re.compile(r"^js-chart")):
    heading = el.find_previous(["h2", "h3"])
    if heading:
        chart_titles[el["id"]] = heading.get_text(strip=True)


pattern = re.compile(
    r'window\.chartDataLine\["([^"]+)"\]\s*=\s*(\{.*?\});',
    re.DOTALL,
)

dfs = []

## ITER SUR CHARTS
for match in pattern.finditer(html):
    chart_id = match.group(1)
    raw_json = match.group(2)

    try:
        chart = json.loads(raw_json)
    except json.JSONDecodeError:
        print(f"[WARN] Impossible de parser le JSON pour {chart_id}")
        continue

    labels = chart["data"].get("labels", [])
    datasets = chart["data"].get("datasets", [])
    title = chart_titles.get(chart_id) or chart.get("datasetsTitle", chart_id)

    series = {}
    for ds in datasets:
        n = len(ds["data"])
        idx = labels[:n] if n <= len(labels) else labels + [f"extra_{i}" for i in range(n - len(labels))]
        series[ds["label"]] = pd.Series(ds["data"], index=idx)
    df = pd.DataFrame(series)
    df.index.name = "date"

    dfs.append((title, chart_id, df))
    print(f"\n=== {title} ({chart_id}) ===")
    print(df.to_string())

print(f"\n{len(dfs)} tableau(x) récupéré(s) : {[t for t, _, _ in dfs]}")
