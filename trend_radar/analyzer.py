from pytrends.request import TrendReq
import pandas as pd


# ==========================================================
# GOOGLE TRENDS SETTINGS
# ==========================================================

TREND_LANGUAGE = "en-US"
TREND_TIMEZONE = 360


# ==========================================================
# ANALYZE TRENDS
# ==========================================================

def analyze_trends(keyword):

    keyword = keyword.strip()

    if not keyword:
        return pd.DataFrame()

    pytrends = TrendReq(
        hl=TREND_LANGUAGE,
        tz=TREND_TIMEZONE
    )

    pytrends.build_payload(
        [keyword],
        timeframe="today 12-m",
        geo=""
    )

    data = pytrends.interest_over_time()

    if data.empty:
        return pd.DataFrame()

    data = data.reset_index()

    # ------------------------------------------------------
    # RENAME TREND COLUMN
    # ------------------------------------------------------

    if keyword in data.columns:

        data.rename(
            columns={
                keyword: "trend_score"
            },
            inplace=True
        )

    # ------------------------------------------------------
    # REMOVE PARTIAL DATA COLUMN
    # ------------------------------------------------------

    if "isPartial" in data.columns:

        data.drop(
            columns=["isPartial"],
            inplace=True
        )

    # ------------------------------------------------------
    # CLEAN DATA
    # ------------------------------------------------------

    data["trend_score"] = pd.to_numeric(
        data["trend_score"],
        errors="coerce"
    )

    data.dropna(
        subset=["trend_score"],
        inplace=True
    )

    return data[
        [
            "date",
            "trend_score"
        ]
    ]


# ==========================================================
# TREND SUMMARY
# ==========================================================

def get_trend_summary(df):

    if df is None or df.empty:

        return {
            "average": 0,
            "peak": 0,
            "lowest": 0,
            "current": 0,
            "change_percent": 0,
            "status": "⚪ No Data"
        }

    scores = pd.to_numeric(
        df["trend_score"],
        errors="coerce"
    ).dropna()

    if scores.empty:

        return {
            "average": 0,
            "peak": 0,
            "lowest": 0,
            "current": 0,
            "change_percent": 0,
            "status": "⚪ No Data"
        }

    # ------------------------------------------------------
    # CORE METRICS
    # ------------------------------------------------------

    average = float(
        scores.mean()
    )

    peak = float(
        scores.max()
    )

    lowest = float(
        scores.min()
    )

    current = float(
        scores.iloc[-1]
    )

    # ------------------------------------------------------
    # CHANGE
    # ------------------------------------------------------

    if len(scores) >= 2:

        previous = float(
            scores.iloc[-2]
        )

        if previous != 0:

            change_percent = (
                (current - previous)
                / previous
            ) * 100

        else:

            change_percent = 0

    else:

        change_percent = 0

    # ------------------------------------------------------
    # STATUS
    # ------------------------------------------------------

    if change_percent >= 10:

        status = "🚀 Rising"

    elif change_percent >= 3:

        status = "📈 Growing"

    elif change_percent <= -10:

        status = "📉 Declining"

    elif change_percent <= -3:

        status = "⚠️ Weakening"

    else:

        status = "➡️ Stable"

    return {

        "average": round(
            average,
            2
        ),

        "peak": round(
            peak,
            2
        ),

        "lowest": round(
            lowest,
            2
        ),

        "current": round(
            current,
            2
        ),

        "change_percent": round(
            change_percent,
            2
        ),

        "status": status
    }


# ==========================================================
# TREND OPPORTUNITY SCORE
# ==========================================================

def calculate_trend_score(summary):

    average = summary.get(
        "average",
        0
    )

    current = summary.get(
        "current",
        0
    )

    change_percent = summary.get(
        "change_percent",
        0
    )

    # ------------------------------------------------------
    # BASE SCORE
    # ------------------------------------------------------

    base_score = average

    # ------------------------------------------------------
    # CURRENT MOMENTUM
    # ------------------------------------------------------

    momentum_bonus = 0

    if change_percent > 0:

        momentum_bonus = min(
            change_percent * 0.5,
            20
        )

    else:

        momentum_bonus = max(
            change_percent * 0.25,
            -20
        )

    # ------------------------------------------------------
    # CURRENT TREND STRENGTH
    # ------------------------------------------------------

    current_bonus = (
        current * 0.15
    )

    score = (
        base_score
        + momentum_bonus
        + current_bonus
    )

    score = max(
        0,
        min(
            score,
            100
        )
    )

    return round(
        score,
        2
    )


# ==========================================================
# OPPORTUNITY LABEL
# ==========================================================

def get_opportunity_label(score):

    if score >= 80:

        return "🔥 Excellent Opportunity"

    elif score >= 65:

        return "🚀 High Opportunity"

    elif score >= 50:

        return "🟢 Good Opportunity"

    elif score >= 35:

        return "🟡 Moderate Opportunity"

    else:

        return "🔴 Low Opportunity"