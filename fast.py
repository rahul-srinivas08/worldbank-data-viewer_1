from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, List
import pandas as pd

from fastapi.staticfiles import StaticFiles



app = FastAPI(title="Country & Region Data Viewer")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load data
df_countries = pd.read_csv("data/raw_countries.csv")
df_indicators = pd.read_csv("data/raw_indicators.csv")

merged_df = df_indicators.merge(
    df_countries, left_on="country_iso3code", right_on="id", how="left"
)

country_names = sorted(df_countries["name"].dropna().astype(str).unique())
iso_codes = sorted(df_countries["iso2code"].dropna().astype(str).unique())
capital_cities = sorted(df_countries["capital_city"].dropna().astype(str).unique())
region_names = sorted(df_countries["region_name"].dropna().astype(str).unique())

dropdown_options = (
    [{"label": f"Country: {c}", "value": c} for c in country_names]
    + [{"label": f"ISO Code: {c}", "value": c} for c in iso_codes]
    + [{"label": f"Capital City: {c}", "value": c} for c in capital_cities]
)

region_options = [
    {"label": region.strip(), "value": region.strip()} for region in region_names
]


@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "options": dropdown_options,
            "regions": region_options,
            "result": None,
            "selected": [],
            "selected_regions": [],
            "region_data": None,
            "error": None,
            "chart_data": None,
        },
    )


@app.post("/", response_class=HTMLResponse)
async def handle_search(
    request: Request,
    selected_values: Optional[List[str]] = Form(None),
    selected_regions: Optional[List[str]] = Form(None),
):
    selected_lower = [val.lower() for val in selected_values] if selected_values else []

    filtered_countries = (
        df_countries[
            df_countries.apply(
                lambda row: (
                    str(row["name"]).lower() in selected_lower
                    or str(row["iso2code"]).lower() in selected_lower
                    or str(row["capital_city"]).lower() in selected_lower
                ),
                axis=1,
            )
        ]
        if selected_lower
        else pd.DataFrame()
    )

    country_results = []
    if not filtered_countries.empty:
        for _, country in filtered_countries.iterrows():
            country_code = country["id"]
            data = merged_df[merged_df["country_iso3code"] == country_code]

            gdp = data[data["indicator_code"] == "NY.GDP.MKTP.CD"]
            pop = data[data["indicator_code"] == "SP.POP.TOTL"]

            country_results.append(
                {
                    "country": country["name"],
                    "region": country["region_name"],
                    "capital": country["capital_city"],
                    "gdp": [
                        {
                            "year": int(row["year"]),
                            "value": float(row["indicator_value"]),
                        }
                        for _, row in gdp.iterrows()
                    ],
                    "population": [
                        {
                            "year": int(row["year"]),
                            "value": int(row["indicator_value"]),
                        }
                        for _, row in pop.iterrows()
                    ],
                }
            )

    region_results = []
    if selected_regions:
        for region in selected_regions:
            region_countries = df_countries[
                df_countries["region_name"].str.strip() == region.strip()
            ]
            region_codes = region_countries["id"].unique()

            region_data = merged_df[merged_df["country_iso3code"].isin(region_codes)]

            for indicator in ["NY.GDP.MKTP.CD", "SP.POP.TOTL"]:
                indicator_data = region_data[region_data["indicator_code"] == indicator]
                grouped = (
                    indicator_data.groupby("year")["indicator_value"]
                    .sum()
                    .reset_index()
                )

                region_results.append(
                    {
                        "region": region,
                        "indicator": (
                            "GDP" if indicator == "NY.GDP.MKTP.CD" else "Population"
                        ),
                        "data": [
                            {
                                "year": int(row["year"]),
                                "value": float(row["indicator_value"]),
                            }
                            for _, row in grouped.iterrows()
                        ],
                    }
                )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "options": dropdown_options,
            "regions": region_options,
            "result": country_results if not filtered_countries.empty else None,
            "selected": selected_values or [],
            "selected_regions": selected_regions or [],
            "region_data": region_results if region_results else None,
            "chart_data": country_results if country_results else None,
            "error": None if country_results or region_results else "No data found.",
        },
    )