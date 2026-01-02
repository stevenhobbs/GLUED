# %% Libraries
import pandas as pd
import polars as pl
import numpy as np
import pymer4
from pymer4.models import lmer
from pathlib import Path

# %% Load & clean data
DATA_PATH = Path(__file__).parents[1] / 'output'
FILE_PATH = DATA_PATH / 'lmm_input.parquet'

df = pd.read_parquet(FILE_PATH)

features = ["students5_estimated", "gdp", "year", "region", "country"]

regions = [
    "North America",
    "East Asia and Pacific",
    "Europe and Central Asia",
    "Latin America and Caribbean",
    "Middle East and North Africa",
    "South Asia",
    "Sub-Saharan Africa",
]

df_pl = (
    pl.from_pandas(df)
    .drop_nulls(features)
    .with_columns(
        pl.col('region').cast(pl.Categorical).cast(pl.Enum(regions)),
        gdp_z = (pl.col("gdp") - pl.col('gdp').mean()) / pl.col('gdp').std(),
        year_c = pl.col('year') - pl.col('year').mean(),
    )
)

display(df_pl.head())

# %% Baseline Linear Mixed Model
model_A= lmer("students5_estimated ~ gdp_z + region + year_c + (1 | country)", data=df_pl)
model_A.fit()

# %% Linear Mixed Model with gdp:region interaction 
model_B = lmer("students5_estimated ~ gdp_z * region + year_c + (1 | country)", data=df_pl)
model_B.fit()

# %% Baseline model
model_A.summary()


# %% Model with interaaction 
model_B.summary()

# df_pl_clean['region'].unique()
print("The referrence region is North America")

# %% PART 3 CONCLUSIONS
# The relationship between GDP and enrollment is not well represented by a single parameter (slope). A 
# linear mixed model with country random intercept strongly indicates the relationship differs by region. Adding
# an interaction effect between GDP and region greatly improves the model fit (delta AIC = 345).
#
# With North America as the referrence region, GDP has highly signficiant negative influence on enrollments, where a one 
# standard deviation increase in GDP associates with 973.905 fewer enrollments, while holding year constant (p < .001).
# In other regions, the relationship can be positive, such as Europe and Central Asia, where a one standard deviation
# increase in GDP predicts 7941.013 (-973.905 + 8914.918) more enrollments  (p < .001).

# %% NEXT STEPS
# 1.Check assumptions (residuals), leverage, outliers and update data/model as needed
# 2. Explore year*region interaction
# 3. Explore splines to test if relationship changes before/after 1991 Soviet collapse. 
# 4. Explore a tree-based model with more flexibility and compare with baseline linear model