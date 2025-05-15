import asyncio
import httpx
import pandas as pd

# Constants
INDICATORS = ["NY.GDP.MKTP.CD", "SP.POP.TOTL"]
START_YEAR = 2020
END_YEAR = 2024


async def fetch_all_countries():
    url = "http://api.worldbank.org/v2/country"
    params = {"format": "json", "per_page": 300}  # Enough to get all countries
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        result = r.json()

    countries = []
    for c in result[1]:
        if c.get("region", {}).get("value", "") != "Aggregates":
            countries.append(
                {
                    "id": c["id"],
                    "iso2code": c.get("iso2Code", ""),
                    "name": c.get("name", ""),
                    "region_name": c.get("region", {}).get("value", ""),
                    "capital_city": c.get("capitalCity", ""),
                }
            )
    return countries


async def fetch_indicator_metadata(indicator_code):
    url = f"http://api.worldbank.org/v2/indicator/{indicator_code}?format=json"
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url)
        r.raise_for_status()
        data = r.json()
    if len(data) > 1 and data[1]:
        meta = data[1][0]
        return {
            "id": meta.get("id"),
            "name": meta.get("name"),
            "source": meta.get("source", {}).get("value", ""),
            "unit": meta.get("unit", ""),
            "topics": [t["value"] for t in meta.get("topics", [])],
        }
    return None


async def fetch_indicator_data(country_id, indicator_code, start_year, end_year):
    url = f"http://api.worldbank.org/v2/country/{country_id}/indicator/{indicator_code}"
    params = {
        "format": "json",
        "date": f"{start_year}:{end_year}",
        "per_page": 1000,
    }
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        data = r.json()

    results = []
    if len(data) > 1 and data[1]:
        for entry in data[1]:
            year = entry.get("date")
            value = entry.get("value")
            if value is not None:
                results.append(
                    {
                        "country_iso3code": country_id,
                        "year": int(year),
                        "indicator_code": indicator_code,
                        "indicator_value": value,
                    }
                )
    return results


async def main_etl():
    print("Fetching countries...")
    countries = await fetch_all_countries()
    df_countries = pd.DataFrame(countries)
    df_countries.to_csv(".data/raw_countries.csv", index=False)
    print(f"Saved raw_countries.csv with {len(df_countries)} countries")

    print("Fetching indicator metadata...")
    metadata_list = []
    for ind in INDICATORS:
        meta = await fetch_indicator_metadata(ind)
        if meta:
            metadata_list.append(meta)
    df_meta = pd.DataFrame(metadata_list)
    df_meta.to_csv(".data/indicator_metadata.csv", index=False)
    print("Saved indicator_metadata.csv")

    print("Fetching indicator data for all countries and indicators...")
    all_data = []
    for country in countries:
        for ind in INDICATORS:
            data_points = await fetch_indicator_data(
                country["id"], ind, START_YEAR, END_YEAR
            )
            all_data.extend(data_points)

    df_data = pd.DataFrame(all_data)
    df_data.to_csv(".data/raw_indicators.csv", index=False)
    print(f"Saved raw_indicators.csv with {len(df_data)} data points")


if __name__ == "__main__":
    asyncio.run(main_etl())
