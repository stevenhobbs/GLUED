# %% Libraries
import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
import seaborn as sns

try:
    from IPython.display import display
except ImportError:

    def display(x):
        print(x)


# %% PART 1) Load Data
DATA_PATH = Path(__file__).resolve().parents[1] / "data"
FIGURE_PATH = Path(__file__).resolve().parents[1] / "figures"
FIGURE_PATH.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(DATA_PATH / "enrollments.csv")
# %% Inspect Data
print(("HEAD"))
display(df.head())

print("\nTAIL")
display(df.tail())

print("\nINFO")
# Fix lat/long issue for parquet export
df["latitude"] = pd.to_numeric(df["latitude"].astype(str).str.strip(), errors="coerce")
df["longitude"] = pd.to_numeric(df["longitude"].astype(str).str.strip(), errors="coerce")

df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
# df['year'] = pd.to_datetime(df['year'])
# df['year'] = df['year'].dt.year
df.info()


print(f"\nUnique countries: {df['country'].nunique()}")
print(f"\nUnique regions: {df['region'].nunique()}")

# %% PART 2) EXPLORE 1991 SOVIET UNION COLLAPSE
# %% Get list of Soviet and stable western referrence countries
all_countries = df["country"].unique()
soviet_countries = [
    "russian federation",
    "ukraine",
    "belarus",
    "kazakhstan",
    "uzbekistan",
    "georgia",
    "azerbaijan",
    "armenia",
    "turkmenistan",
    "tajikistan",
    "kyrgyz republic",
    "moldova",
    "lithuania",
    "latvia",
    "estonia",
]
western_countries = ["united states", "france", "united kingdom", "poland", "germany"]

# Check spelling & inclusion
for c in soviet_countries + western_countries:
    if c in all_countries:
        print(f"{c} : Yes")
    else:
        print(f"{c} : No")

# Find krygystan spelling
for c in all_countries:
    if c.startswith("ky"):
        print(f"krygyzstan spelling: {c}")

# Check for other representations of Russia
all_country_codes = df["countrycode"].unique()
russia_codes = ["RU", "RUS"]
soviet_codes = ["SU", "SUN", 810, "SUHH"]
for c in russia_codes + soviet_codes:
    if c in all_country_codes:
        print(f"{c} : Yes")
    else:
        print(f"{c} : No")

# %% Group dfs by country and year to aggregate enrollment and calc percent change
all_grouped = df.groupby(["country", "year"], as_index=False)
all_grouped_enroll = (
    all_grouped["students5_estimated"]
    .sum()
    .rename(columns={"students5_estimated": "total_enrollment"})
    .sort_values(["country", "year"])
)

all_grouped_enroll["percent_change"] = (
    all_grouped_enroll.groupby("country")["total_enrollment"]
    .pct_change()
    .mul(100)
    .round()
)
print("\nAll Countries")
display(all_grouped_enroll.head())

soviet_grouped_enroll = all_grouped_enroll[
    all_grouped_enroll["country"].isin(soviet_countries)
]
print("\n Soviet Countries")
display(soviet_grouped_enroll.head())

western_grouped_enroll = all_grouped_enroll[
    all_grouped_enroll["country"].isin(western_countries)
]
print("\n Western Countries")
display(western_grouped_enroll.head())
# %% Plot Enrollment & Percent Change in Soviet Countries (all years)
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(12, 10))

# Total enrollment
sns.lineplot(
    data=soviet_grouped_enroll, x="year", y="total_enrollment", hue="country", ax=ax1
)
ax1.axvline(1991, linestyle="--")  # Soviet Union collapse
ax1.text(
    x=1991 + 0.5,
    y=soviet_grouped_enroll["total_enrollment"].max() * 0.9,
    s="Soviet Union Collapse",
    rotation=90,
    va="top",
    ha="left",
)
ax1.set_title("Total Enrollment in Soviet Universities by Country over all years")
handles, labels = ax1.get_legend_handles_labels()
ax1.get_legend().remove()

# Percent Change
sns.lineplot(
    data=soviet_grouped_enroll, x="year", y="percent_change", hue="country", ax=ax2
)
ax2.axvline(1991, linestyle="--")  # Soviet Union collapse
ax2.text(
    x=1991 + 0.5,
    y=soviet_grouped_enroll["percent_change"].max() * 0.9,
    s="Soviet Union Collapse",
    rotation=90,
    va="top",
    ha="left",
)
ax2.set_ylabel("% Change over 5-year interval")
ax2.set_title(
    "Percent Change in Enrollment in Soviet Universities by Country over all years"
)
ax2.get_legend().remove()

fig.legend(handles, labels, title="Country", loc="center left", bbox_to_anchor=(1, 0.5))
plt.subplots_adjust(right=0.95)
plt.savefig(
    FIGURE_PATH / "soviet_enrollment_percent_change_all_years.png",
    dpi=300,
    bbox_inches="tight",
)
plt.show()
plt.close(fig)


# %% Plot Enrollment & Percent Change in Soviet Countries (1980 - 2000)
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(12, 10))

soviet_20yr_mask = soviet_grouped_enroll["year"].between(1980, 2000)

# Total enrollment
sns.lineplot(
    data=soviet_grouped_enroll[soviet_20yr_mask],
    x="year",
    y="total_enrollment",
    hue="country",
    ax=ax1,
)
ax1.axvline(1991, linestyle="--")  # Soviet Union collapse
ax1.text(
    x=1991 + 0.5,
    y=soviet_grouped_enroll[soviet_20yr_mask]["total_enrollment"].max() * 0.9,
    s="Soviet Union Collapse",
    rotation=90,
    va="top",
    ha="left",
)
ax1.set_title("Total Enrollment in Soviet Universities by Country (1980 - 2000)")
handles, labels = ax1.get_legend_handles_labels()
ax1.get_legend().remove()

# Percent Change
sns.lineplot(
    data=soviet_grouped_enroll[soviet_20yr_mask],
    x="year",
    y="percent_change",
    hue="country",
    ax=ax2,
)
ax2.axvline(1991, linestyle="--")  # Soviet Union collapse
ax2.text(
    x=1991 + 0.5,
    y=soviet_grouped_enroll[soviet_20yr_mask]["percent_change"].max() * 0.9,
    s="Soviet Union Collapse",
    rotation=90,
    va="top",
    ha="left",
)
ax2.set_ylabel("% Change over 5-year interval")
ax2.set_title(
    "Percent Change in Enrollment in Soviet Universities by Country (1980 - 2000)"
)
ax2.get_legend().remove()

fig.legend(handles, labels, title="Country", loc="center left", bbox_to_anchor=(1, 0.5))
plt.subplots_adjust(right=0.95)
plt.savefig(
    FIGURE_PATH / "soviet_enrollment_percent_change_1980_2000.png",
    dpi=300,
    bbox_inches="tight",
)
plt.show()
plt.close(fig)

"""
Fix axis labels if time. Show only 5 year intervals on x.
"""


# %% Plot Percent Change in Western Countries (1980 - 2000)
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(12, 10))

western_20yr_mask = western_grouped_enroll["year"].between(1980, 2000)

# Total enrollment
sns.lineplot(
    data=western_grouped_enroll[western_20yr_mask],
    x="year",
    y="total_enrollment",
    hue="country",
    ax=ax1,
)
ax1.axvline(1991, linestyle="--")  # Soviet Union collapse
ax1.text(
    x=1991 + 0.5,
    y=western_grouped_enroll[western_20yr_mask]["total_enrollment"].max() * 0.9,
    s="Soviet Union Collapse",
    rotation=90,
    va="top",
    ha="left",
)
ax1.set_title("Total Enrollment in Western Universities by Country (1980 - 2000)")
handles, labels = ax1.get_legend_handles_labels()
ax1.get_legend().remove()

# Percent Change
sns.lineplot(
    data=western_grouped_enroll[western_20yr_mask],
    x="year",
    y="percent_change",
    hue="country",
    ax=ax2,
)
ax2.axvline(1991, linestyle="--")  # Soviet Union collapse
ax2.text(
    x=1991 + 0.5,
    y=western_grouped_enroll[western_20yr_mask]["percent_change"].max() * 0.9,
    s="Soviet Union Collapse",
    rotation=90,
    va="top",
    ha="left",
)
ax2.set_ylabel("% Change over 5-year interval")
ax2.set_title(
    "Percent Change in Enrollment in Western Universities by Country (1980 - 2000)"
)
ax2.get_legend().remove()

fig.legend(handles, labels, title="Country", loc="center left", bbox_to_anchor=(1, 0.5))
plt.subplots_adjust(right=0.95)
plt.savefig(
    FIGURE_PATH / "western_enrollment_percent_change_1980_2000.png",
    dpi=300,
    bbox_inches="tight",
)
plt.show()
plt.close(fig)

# Fix axis labels if time. Show only 5 year intervals on x.


# %% Did 1990 - 1995 enrollment growth rate differ in Soviet countries compared to referrence countries (or all countries)?
sns.histplot(all_grouped_enroll["percent_change"], binrange=(-100, 200))
plt.title("World distribution of enrollment percent change from previous 5-year mark")
plt.xlabel("Percent Change in Enrollment (5-year interval)")
plt.savefig(
    FIGURE_PATH / "world_enrollment_percent_change_histogram.png",
    dpi=300,
    bbox_inches="tight",
)
plt.show()
plt.close(fig)

# %% Percentiile Rank in 1995 percent_change by country and empirical tail probability
all_grouped_1995 = all_grouped_enroll.loc[all_grouped_enroll["year"] == 1995].copy()

all_grouped_1995["percentile"] = (
    all_grouped_1995["percent_change"].rank(method="average", pct=True).round(3)
)

# 2-sided empirical probability
all_grouped_1995["prob_empirical"] = 2 * np.minimum(
    all_grouped_1995["percentile"], 1 - all_grouped_1995["percentile"]
).round(3)
# display(all_grouped_1995.head())


soviet_grouped_1995 = all_grouped_1995[
    all_grouped_1995["country"].isin(soviet_countries)
].copy()
# display(soviet_grouped_1995)

display(
    soviet_grouped_1995.drop(["year", "total_enrollment"], axis=1).sort_values(
        "prob_empirical"
    )
)

# %% PART 2 CONCLUSIONS
# Although the percent change in enrollment from 1990 to 1995 was positive for all
# soviet countries, no changes were unusually large or small relative to the world
# population. While a better test might be to evaluate the soviet group as a whole
# (maybe using ranks or medians) as opposed to evaluating probabilities of individual
# soviet countries, I don't see strong enough evidence to continue down this path
# (and given the timebox constraint). 
# However, the 1991 collapse may have impacted enrollments on a shorter or longer 
# time scale than is detectable in this analysis, and which may be obscured by
# the interpolation/extrapolation used to fill-in missing enrollment data.


# %% PART 3)
# %% Load GDP data
gdp = pd.read_csv(DATA_PATH / "Countries GDP 1960-2020.csv")

# %% Inspect GDP Data
print("Head")
display(gdp.head())

print("\nTail")
display(gdp.tail())

print("\nInfo")
print(gdp.info())

# %% Melt gdp data
gdp_long = gdp.melt(id_vars = ['Country Name', 'Country Code'], var_name = 'year', value_name='gdp')
# gdp_long['year'] = pd.to_datetime(gdp_long['year'] ,format="%Y")
gdp_long['year'] = pd.to_numeric(gdp_long['year'], errors='coerce').astype('int64')

# %% Merge df (enrollment data) and gdp_long 
df_m = df.merge(gdp_long, how='left', left_on=['countrycode', 'year'], right_on=['Country Code','year'])

display(df_m.head())
display(df_m.tail())

print("\Enrollments info")
print(df.info())

print("\nMerged data info")
print(df_m.info())


# %% Save merged df for import by GLUED_LMM.py
OUTPUT_PATH = Path(__file__).parents[1] / "output"
Path.mkdir(OUTPUT_PATH, exist_ok=True)
FILE_PATH = OUTPUT_PATH / 'lmm_input.parquet'
df_m.to_parquet(FILE_PATH, index=False)
print(f"Merged output written to {FILE_PATH}")


# %%
