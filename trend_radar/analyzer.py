from pytrends.request import TrendReq
import pandas as pd

def analyze_trends(keyword):

    pytrends = TrendReq(hl='en-US', tz=360)

    pytrends.build_payload([keyword])

    data = pytrends.interest_over_time()

    if data.empty:
        return pd.DataFrame()

    data = data.reset_index()

    data.rename(
        columns={
            keyword: "trend_score"
        },
        inplace=True
    )

    return data[["date", "trend_score"]]


def get_top_trend(df):

    top = df.sort_values(
        "trend_score",
        ascending=False
    ).iloc[0]

    return {
        "keyword": "Selected Keyword",
        "trend_score": top["trend_score"]
    }