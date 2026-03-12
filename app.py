# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import json

st.set_page_config(page_title="DataSense", page_icon="DS", layout="wide")

# Memory optimization
import gc
gc.enable()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');
html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
.stApp { background-color: #07070f; color: #e2e2f0; }
[data-testid="stSidebar"] { background-color: #0d0d1a; border-right: 1px solid #1e1e35; }
[data-testid="stSidebar"] * { color: #e2e2f0 !important; }
.stFileUploader { background: #0d0d1a !important; border: 1px dashed #2a2a4a !important; border-radius: 14px !important; }
hr { border-color: #1e1e35 !important; }
.hero { background: linear-gradient(135deg, #0d0d1a 0%, #12122a 100%); border: 1px solid #1e1e35; border-radius: 20px; padding: 36px 40px; margin-bottom: 28px; position: relative; overflow: hidden; }
.hero::before { content: ''; position: absolute; top: -60px; right: -60px; width: 220px; height: 220px; background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%); border-radius: 50%; }
.hero-title { font-size: 42px; font-weight: 800; letter-spacing: -1px; margin: 0 0 8px 0; line-height: 1; }
.hero-sub { font-size: 14px; color: #6b6b9a; font-family: 'JetBrains Mono'; }
.badge { display: inline-block; font-size: 10px; font-family: 'JetBrains Mono'; font-weight: 700; padding: 4px 12px; border-radius: 20px; letter-spacing: 1.5px; background: rgba(16,185,129,0.1); color: #10b981; border: 1px solid rgba(16,185,129,0.25); margin-bottom: 16px; }
.kpi { background: #0d0d1a; border: 1px solid #1e1e35; border-radius: 14px; padding: 18px 20px; border-top: 2px solid var(--accent); }
.kpi-label { font-size: 10px; font-family: 'JetBrains Mono'; color: #6b6b9a; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 8px; }
.kpi-value { font-size: 32px; font-weight: 800; color: #e2e2f0; line-height: 1; }
.kpi-sub { font-size: 11px; color: #6b6b9a; margin-top: 4px; font-family: 'JetBrains Mono'; }
.section-title { font-size: 10px; font-weight: 700; letter-spacing: 2.5px; text-transform: uppercase; color: #6366f1; padding: 6px 0 10px; border-bottom: 1px solid #1e1e35; margin: 28px 0 16px; }
.col-card { background: #0d0d1a; border: 1px solid #1e1e35; border-radius: 12px; padding: 14px 16px; }
.col-name { font-family: 'JetBrains Mono'; font-size: 12px; font-weight: 700; color: #a5b4fc; margin-bottom: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.tag { font-size: 9px; font-family: 'JetBrains Mono'; padding: 2px 8px; border-radius: 20px; font-weight: 700; letter-spacing: 0.5px; }
.bar-wrap { background: #07070f; border-radius: 3px; height: 3px; margin: 8px 0 5px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 3px; }
.col-meta { font-size: 10px; color: #6b6b9a; font-family: 'JetBrains Mono'; }
.insight-card { background: #0d0d1a; border: 1px solid #1e1e35; border-radius: 14px; padding: 20px 22px; }
.insight-title { font-size: 11px; font-family: 'JetBrains Mono'; color: #6366f1; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
.insight-body { font-size: 13px; color: #c4c4e0; line-height: 1.7; }
.story-box { background: linear-gradient(135deg, #0d0d1a, #12122a); border: 1px solid #2a2a4a; border-left: 3px solid #6366f1; border-radius: 16px; padding: 28px 32px; margin-bottom: 20px; }
.story-text { font-size: 18px; font-weight: 600; color: #e2e2f0; line-height: 1.7; }
.story-meta { font-size: 11px; font-family: 'JetBrains Mono'; color: #6b6b9a; margin-top: 12px; }
.pattern-card { background: #0d0d1a; border: 1px solid #1e1e35; border-radius: 14px; padding: 20px 22px; border-top: 2px solid var(--pc); }
.pattern-icon { font-size: 28px; margin-bottom: 10px; }
.pattern-title { font-size: 12px; font-family: 'JetBrains Mono'; text-transform: uppercase; letter-spacing: 1px; color: var(--pc); margin-bottom: 8px; }
.pattern-body { font-size: 13px; color: #c4c4e0; line-height: 1.7; }
.pattern-stat { font-size: 24px; font-weight: 800; color: var(--pc); margin: 6px 0; }
.risk-bar { height: 6px; border-radius: 3px; margin: 6px 0; }
.risk-card { background: #0d0d1a; border: 1px solid #1e1e35; border-radius: 10px; padding: 12px 14px; }
.risk-col { font-family: 'JetBrains Mono'; font-size: 11px; color: #a5b4fc; font-weight: 700; margin-bottom: 4px; }
.risk-label { font-size: 9px; font-family: 'JetBrains Mono'; text-transform: uppercase; letter-spacing: 1px; }
.question-item { display: flex; gap: 14px; padding: 14px 0; border-bottom: 1px solid #0f0f20; align-items: flex-start; }
.question-num { font-size: 11px; font-family: 'JetBrains Mono'; color: #6366f1; font-weight: 700; min-width: 24px; margin-top: 2px; }
.question-text { font-size: 14px; color: #e2e2f0; line-height: 1.6; font-weight: 600; }
.question-why { font-size: 12px; color: #6b6b9a; margin-top: 4px; font-family: 'JetBrains Mono'; }
.code-block { background: #0a0a18; border: 1px solid #1e1e35; border-left: 3px solid #6366f1; border-radius: 12px; padding: 20px 24px; font-family: 'JetBrains Mono'; font-size: 12px; color: #a5b4fc; line-height: 1.9; margin-bottom: 14px; white-space: pre-wrap; }
.code-title { font-size: 10px; color: #6b6b9a; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 8px; font-family: 'JetBrains Mono'; }
.store-table { width: 100%; border-collapse: collapse; font-family: 'JetBrains Mono'; font-size: 12px; }
.store-table th { color: #6b6b9a; text-align: left; padding: 8px 12px; border-bottom: 1px solid #1e1e35; font-size: 10px; letter-spacing: 1px; text-transform: uppercase; }
.store-table td { padding: 10px 12px; border-bottom: 1px solid #0f0f20; color: #c4c4e0; }
.store-table tr:hover td { background: #12122a; }
.verdict-box { background: linear-gradient(135deg, #0d0d1a, #12122a); border: 1px solid #1e1e35; border-radius: 16px; padding: 28px 32px; text-align: center; }
.issue-item { display: flex; align-items: flex-start; gap: 10px; padding: 10px 0; border-bottom: 1px solid #0f0f20; font-size: 13px; color: #c4c4e0; }
.issue-dot { width: 8px; height: 8px; border-radius: 50%; margin-top: 5px; flex-shrink: 0; }
.tool-btn { display: inline-block; cursor: pointer; padding: 8px 18px; border-radius: 8px; font-family: 'JetBrains Mono'; font-size: 12px; font-weight: 700; margin: 4px; border: 1px solid; transition: all 0.2s; }
.stButton > button { background: linear-gradient(135deg, #4f46e5, #7c3aed) !important; color: white !important; font-family: 'Syne' !important; font-weight: 700 !important; font-size: 15px !important; border: none !important; border-radius: 12px !important; padding: 14px 0 !important; width: 100% !important; }
.stRadio > div { gap: 8px !important; }
.stRadio label { background: #0d0d1a !important; border: 1px solid #1e1e35 !important; border-radius: 10px !important; padding: 8px 16px !important; font-family: 'JetBrains Mono' !important; font-size: 12px !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════

def detect_type(series):
    filled = series.dropna().astype(str).str.strip().replace('', pd.NA).dropna()
    if len(filled) == 0: return "empty"
    try:
        pd.to_numeric(filled.str.replace(r'[$,% ]', '', regex=True))
        return "numeric"
    except: pass
    try:
        pd.to_datetime(filled.iloc[:30], format="mixed", dayfirst=False)
        return "date"
    except: pass
    return "category" if filled.nunique() / len(filled) < 0.25 else "text"

TYPE_STYLE = {
    "numeric":  ("#00e5ff","rgba(0,229,255,0.08)","rgba(0,229,255,0.2)","NUM"),
    "date":     ("#10b981","rgba(16,185,129,0.08)","rgba(16,185,129,0.2)","DATE"),
    "category": ("#a78bfa","rgba(167,139,250,0.08)","rgba(167,139,250,0.2)","CAT"),
    "text":     ("#f59e0b","rgba(245,158,11,0.08)","rgba(245,158,11,0.2)","TEXT"),
    "empty":    ("#ef4444","rgba(239,68,68,0.08)","rgba(239,68,68,0.2)","EMPTY"),
}

def type_tag(t):
    c,bg,bd,lbl = TYPE_STYLE.get(t, TYPE_STYLE["text"])
    return f'<span class="tag" style="color:{c};background:{bg};border:1px solid {bd}">{lbl}</span>'

def bar_html(pct):
    color = "#10b981" if pct>90 else "#f59e0b" if pct>70 else "#ef4444"
    return f'<div class="bar-wrap"><div class="bar-fill" style="width:{pct}%;background:{color}"></div></div>'

def outlier_bounds(series):
    s = series.dropna()
    q1,q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3-q1
    return q1-1.5*iqr, q3+1.5*iqr

def quality_score(df):
    score = 100
    total = df.shape[0]*df.shape[1]
    missing_pct = df.isnull().sum().sum()/total*100
    score -= min(30, missing_pct*1.5)
    num_cols = df.select_dtypes(include='number').columns
    outlier_total = 0
    for col in num_cols:
        lo,hi = outlier_bounds(df[col])
        outlier_total += ((df[col]<lo)|(df[col]>hi)).sum()
    if len(df)>0: score -= min(20, (outlier_total/len(df))*5)
    score -= min(15, df.duplicated().sum()/len(df)*100*2)
    return max(0, round(score))

def detect_dataset_type(df):
    cols_lower = [c.lower() for c in df.columns]
    col_str = " ".join(cols_lower)
    if any(x in col_str for x in ['delivery','order','store','pickup','shipment','logistics']): return "operations"
    if any(x in col_str for x in ['revenue','sales','price','profit','cost','invoice','payment']): return "financial"
    if any(x in col_str for x in ['employee','salary','department','hire','hr','staff','headcount']): return "hr"
    if any(x in col_str for x in ['open','close','high','low','volume','stock','ticker']): return "financial_market"
    if any(x in col_str for x in ['patient','diagnosis','hospital','treatment','medical','drug']): return "healthcare"
    if any(x in col_str for x in ['student','grade','score','course','school','exam','gpa']): return "education"
    if any(x in col_str for x in ['customer','user','session','click','page','visit','retention']): return "product"
    return "general"


# ══════════════════════════════════════════════════════
# PATTERN DETECTION ENGINE
# ══════════════════════════════════════════════════════

def detect_patterns(df):
    patterns = []
    num_cols = df.select_dtypes(include='number').columns.tolist()
    date_cols = [c for c in df.columns if detect_type(df[c])=='date']
    cat_cols = [c for c in df.columns if detect_type(df[c])=='category']

    # 1. TREND DETECTION
    if date_cols and num_cols:
        try:
            df_t = df.copy()
            df_t['_date'] = pd.to_datetime(df_t[date_cols[0]], errors='coerce')
            df_t = df_t.dropna(subset=['_date']).sort_values('_date')
            col = num_cols[0]
            n = len(df_t)
            if n > 10:
                first_avg = df_t[col].iloc[:n//3].mean()
                last_avg = df_t[col].iloc[-n//3:].mean()
                change_pct = ((last_avg - first_avg) / abs(first_avg) * 100) if first_avg != 0 else 0
                if abs(change_pct) > 15:
                    direction = "upward" if change_pct > 0 else "downward"
                    color = "#10b981" if change_pct > 0 else "#ef4444"
                    patterns.append({
                        "title": f"{'Upward' if change_pct>0 else 'Downward'} Trend Detected",
                        "icon": "up" if change_pct>0 else "dn",
                        "color": color,
                        "stat": f"{'+' if change_pct>0 else ''}{change_pct:.1f}%",
                        "body": f"<b style='color:{color}'>{col}</b> shows a clear {direction} trend over time. The last third of your data averages <b>{last_avg:.1f}</b> vs <b>{first_avg:.1f}</b> at the start.",
                        "action": f"Use a Line Chart with {date_cols[0]} on X-axis to visualize this trend clearly."
                    })
        except: pass

    # 2. SEASONALITY / CYCLIC PATTERN
    if date_cols:
        try:
            df_s = df.copy()
            df_s['_date'] = pd.to_datetime(df_s[date_cols[0]], errors='coerce')
            df_s['_month'] = df_s['_date'].dt.month
            if num_cols and df_s['_month'].nunique() >= 3:
                col = num_cols[0]
                monthly = df_s.groupby('_month')[col].mean()
                peak_month = monthly.idxmax()
                low_month = monthly.idxmin()
                variance = (monthly.max() - monthly.min()) / monthly.mean() * 100
                months_map = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
                if variance > 20:
                    patterns.append({
                        "title": "Seasonal Pattern Found",
                        "icon": "sea",
                        "color": "#a78bfa",
                        "stat": f"{variance:.0f}% swing",
                        "body": f"<b style='color:#a78bfa'>{col}</b> peaks in <b>{months_map.get(peak_month,'?')}</b> and drops in <b>{months_map.get(low_month,'?')}</b>. Monthly variance is {variance:.0f}% — strong seasonal signal.",
                        "action": "Add a Month slicer to your dashboard and compare year-over-year."
                    })
        except: pass

    # 3. OUTLIER CLUSTER
    if num_cols:
        worst_col, worst_cnt, worst_pct = "", 0, 0
        for col in num_cols[:5]:
            lo,hi = outlier_bounds(df[col])
            cnt = int(((df[col]<lo)|(df[col]>hi)).sum())
            pct = cnt/len(df)*100
            if cnt > worst_cnt:
                worst_cnt,worst_col,worst_pct = cnt,col,pct
        if worst_cnt > 0 and worst_pct > 3:
            lo,hi = outlier_bounds(df[worst_col])
            patterns.append({
                "title": "Outlier Cluster Warning",
                "icon": "out",
                "color": "#ef4444",
                "stat": f"{worst_cnt:,} rows",
                "body": f"<b style='color:#ef4444'>{worst_col}</b> has <b>{worst_cnt:,} outliers ({worst_pct:.1f}%)</b> outside the normal range of <b>{lo:.1f} to {hi:.1f}</b>. These will skew every average and KPI you build.",
                "action": f"Filter: keep only rows where {worst_col} is between {lo:.0f} and {hi:.0f}."
            })

    # 4. MULTICOLLINEARITY
    if len(num_cols) >= 2:
        try:
            corr = df[num_cols[:6]].corr().abs()
            np.fill_diagonal(corr.values, 0)
            max_corr = corr.max().max()
            if max_corr > 0.85:
                idx = corr.stack().idxmax()
                patterns.append({
                    "title": "Multicollinearity Risk",
                    "icon": "cor",
                    "color": "#f59e0b",
                    "stat": f"r = {max_corr:.2f}",
                    "body": f"<b style='color:#f59e0b'>{idx[0]}</b> and <b style='color:#f59e0b'>{idx[1]}</b> are {max_corr*100:.0f}% correlated. Using both in the same regression or aggregation will produce misleading results — they measure the same underlying signal.",
                    "action": "Keep one as your primary metric. Create the other as a derived calculated column only when needed."
                })
        except: pass

    # 5. DATA SKEWNESS
    if num_cols:
        skewed = []
        for col in num_cols[:5]:
            s = df[col].dropna()
            if len(s) > 30:
                skewness = float(s.skew())
                if abs(skewness) > 1.5:
                    skewed.append((col, skewness))
        if skewed:
            col, skewness = max(skewed, key=lambda x: abs(x[1]))
            direction = "right (positive)" if skewness > 0 else "left (negative)"
            patterns.append({
                "title": "Skewed Distribution",
                "icon": "skw",
                "color": "#06b6d4",
                "stat": f"skew: {skewness:.2f}",
                "body": f"<b style='color:#06b6d4'>{col}</b> is heavily skewed {direction}. This means the <b>mean is misleading</b> — a few extreme values are pulling it away from the typical value. The median is more accurate here.",
                "action": "Use Median instead of Average in your KPI cards for this column."
            })

    # 6. GROWTH RATE
    if date_cols:
        try:
            df_g = df.copy()
            df_g['_date'] = pd.to_datetime(df_g[date_cols[0]], errors='coerce')
            df_g['_week'] = df_g['_date'].dt.isocalendar().week
            if num_cols:
                col = num_cols[0]
                weekly = df_g.groupby('_week')[col].mean()
                if len(weekly) >= 4:
                    growth = weekly.pct_change().mean() * 100
                    if abs(growth) > 2:
                        color = "#10b981" if growth > 0 else "#ef4444"
                        patterns.append({
                            "title": "Weekly Growth Rate",
                            "icon": "grw",
                            "color": color,
                            "stat": f"{'+' if growth>0 else ''}{growth:.1f}%/week",
                            "body": f"<b style='color:{color}'>{col}</b> is {'growing' if growth>0 else 'declining'} at <b>{abs(growth):.1f}% per week</b> on average. {'Positive momentum — capitalize on it.' if growth>0 else 'Negative trend — investigate root cause.'}",
                            "action": "Add a week-over-week % change column to track this KPI dynamically."
                        })
        except: pass

    return patterns


# ══════════════════════════════════════════════════════
# RISK SCORE ENGINE
# ══════════════════════════════════════════════════════

def calculate_risk(df):
    risk_data = []
    for col in df.columns:
        score = 0
        reasons = []
        series = df[col]
        filled = series.dropna()
        miss_pct = series.isnull().sum()/len(df)*100

        if miss_pct > 20: score += 40; reasons.append(f"{miss_pct:.0f}% missing")
        elif miss_pct > 5: score += 20; reasons.append(f"{miss_pct:.0f}% missing")
        elif miss_pct > 0: score += 5; reasons.append(f"{miss_pct:.1f}% missing")

        t = detect_type(series)
        if t == "numeric":
            try:
                lo,hi = outlier_bounds(pd.to_numeric(filled, errors='coerce').dropna())
                nums = pd.to_numeric(filled, errors='coerce').dropna()
                out_pct = ((nums<lo)|(nums>hi)).sum()/len(nums)*100
                if out_pct > 15: score += 35; reasons.append(f"{out_pct:.0f}% outliers")
                elif out_pct > 5: score += 20; reasons.append(f"{out_pct:.0f}% outliers")
                skewness = abs(float(nums.skew()))
                if skewness > 2: score += 15; reasons.append(f"high skew ({skewness:.1f})")
            except: pass
        elif t == "category":
            uniq = filled.nunique()
            if uniq == 1: score += 30; reasons.append("single value — no variation")
            dom_pct = filled.value_counts().iloc[0]/len(filled)*100 if len(filled)>0 else 0
            if dom_pct > 95: score += 20; reasons.append(f"dominated by one value ({dom_pct:.0f}%)")
        elif t == "text":
            score += 10; reasons.append("free text — hard to aggregate")

        if series.duplicated().sum()/len(df)*100 > 50: score += 10; reasons.append("high duplication")

        risk_level = "HIGH" if score >= 50 else "MEDIUM" if score >= 20 else "LOW"
        risk_color = "#ef4444" if risk_level=="HIGH" else "#f59e0b" if risk_level=="MEDIUM" else "#10b981"
        risk_data.append({"col": col, "score": min(100,score), "level": risk_level, "color": risk_color, "reasons": reasons, "type": t})

    return sorted(risk_data, key=lambda x: -x["score"])


# ══════════════════════════════════════════════════════
# DATA STORY ENGINE
# ══════════════════════════════════════════════════════

def generate_story(df, dataset_type, patterns, score):
    num_cols = df.select_dtypes(include='number').columns.tolist()
    cat_cols = [c for c in df.columns if detect_type(df[c])=='category']
    date_cols = [c for c in df.columns if detect_type(df[c])=='date']

    type_descriptions = {
        "operations": "operational performance dataset",
        "financial": "financial dataset",
        "financial_market": "market data dataset",
        "hr": "HR & workforce dataset",
        "healthcare": "healthcare dataset",
        "education": "educational dataset",
        "product": "product analytics dataset",
        "general": "dataset"
    }
    desc = type_descriptions.get(dataset_type, "dataset")

    parts = []
    parts.append(f"This is a <b style='color:#a5b4fc'>{df.shape[0]:,}-row {desc}</b> covering <b>{df.shape[1]} dimensions</b>")

    if date_cols:
        try:
            dates = pd.to_datetime(df[date_cols[0]], errors='coerce').dropna()
            span = (dates.max()-dates.min()).days
            if span > 0:
                parts.append(f"spanning <b style='color:#6366f1'>{span} days</b> of history")
        except: pass

    if cat_cols:
        best = cat_cols[0]
        n = df[best].nunique()
        top = df[best].value_counts().index[0]
        parts.append(f"across <b style='color:#a78bfa'>{n} {best.replace('_',' ').lower()} categories</b> — led by <b>{top}</b>")

    quality_desc = "in excellent condition" if score>=85 else "with moderate quality issues" if score>=65 else "with significant quality problems"
    parts.append(f"Data quality is <b style='color:{'#10b981' if score>=85 else '#f59e0b' if score>=65 else '#ef4444'}'>{quality_desc}</b> (score: {score}/100)")

    if patterns:
        p = patterns[0]
        parts.append(f"Key signal: <b style='color:{p['color']}'>{p['title']}</b> — {p['stat']}")

    story = ", ".join(parts[:3]) + ". " + ". ".join(parts[3:]) + "."
    return story


# ══════════════════════════════════════════════════════
# SUGGESTED QUESTIONS ENGINE
# ══════════════════════════════════════════════════════

def generate_questions(df, dataset_type, patterns):
    num_cols = df.select_dtypes(include='number').columns.tolist()
    cat_cols = [c for c in df.columns if detect_type(df[c])=='category']
    date_cols = [c for c in df.columns if detect_type(df[c])=='date']
    questions = []

    type_questions = {
        "operations": [
            ("What causes delivery delays?", f"Compare {num_cols[0] if num_cols else 'performance'} across different time periods and segments to find bottlenecks.", "Operational Efficiency"),
            ("Which locations/stores underperform?", f"Rank all {cat_cols[0] if cat_cols else 'groups'} by average performance metric to identify outliers.", "Performance Ranking"),
        ],
        "financial": [
            ("What drives revenue growth?", "Correlate revenue with time, product category, and region to find the strongest growth drivers.", "Revenue Analysis"),
            ("Where are we losing margin?", "Compare cost vs revenue across segments to find where profitability breaks down.", "Profitability"),
        ],
        "financial_market": [
            ("Is the asset trending or ranging?", "Analyze price movement over time with rolling averages to classify market regime.", "Trend Analysis"),
            ("What is the volatility profile?", "Compare standard deviation across different time periods to assess risk.", "Risk Assessment"),
        ],
        "hr": [
            ("What predicts employee retention?", "Correlate tenure with compensation, department, and performance scores.", "Retention Analysis"),
            ("Is there a pay equity issue?", "Compare compensation distributions across departments and seniority levels.", "Compensation Equity"),
        ],
        "product": [
            ("Where do users drop off?", "Analyze conversion rates across funnel stages and user segments.", "Funnel Analysis"),
            ("What drives user retention?", "Compare behavior patterns between retained and churned users.", "Retention"),
        ],
    }

    specific = type_questions.get(dataset_type, [])
    questions.extend(specific[:2])

    if date_cols:
        questions.append((
            f"How does performance change over time?",
            f"Plot {num_cols[0] if num_cols else 'key metrics'} by {date_cols[0]} and look for trends, seasonality, and anomalies.",
            "Time Analysis"
        ))

    if cat_cols and num_cols:
        questions.append((
            f"Which {cat_cols[0].replace('_',' ')} performs best?",
            f"Group by {cat_cols[0]} and calculate average {num_cols[0]} — rank from best to worst and investigate the gap.",
            "Segmentation"
        ))

    if len(num_cols) >= 2:
        questions.append((
            f"What is the relationship between {num_cols[0]} and {num_cols[1]}?",
            f"Build a scatter plot of {num_cols[0]} vs {num_cols[1]} — look for correlation, clusters, or unexpected patterns.",
            "Correlation"
        ))

    for p in patterns:
        if p.get("title") == "Multicollinearity Risk":
            questions.append((
                "Are we double-counting any metrics?",
                "Review highly correlated columns — using both in the same calculation inflates results artificially.",
                "Data Integrity"
            ))
            break

    return questions[:5]


# ══════════════════════════════════════════════════════
# CLEANING CODE GENERATOR
# ══════════════════════════════════════════════════════

def get_cleaning_code(df, tool, num_cols, null_cols):
    dupes = df.duplicated().sum()

    if tool == "Power BI":
        steps = []
        if dupes > 0:
            steps.append("// Remove duplicates\n= Table.Distinct(Source)")
        if null_cols:
            steps.append(f'// Replace nulls\n= Table.ReplaceValue(Source, null, 0, Replacer.ReplaceValue, {{"{null_cols[0]}"}})')
        if num_cols:
            lo, hi = outlier_bounds(df[num_cols[0]])
            steps.append(f'// Remove outliers in {num_cols[0]}\n= Table.SelectRows(Source, each [{num_cols[0]}] >= {lo:.0f} and [{num_cols[0]}] <= {hi:.0f})')
        steps.append('// Set column types\n= Table.TransformColumnTypes(Source, {{"date_col", type date}, {"id_col", type text}})')
        return steps, "Power Query (M Language)"

    elif tool == "Python":
        steps = []
        if dupes > 0:
            steps.append("# Remove duplicates\ndf = df.drop_duplicates()")
        if null_cols:
            steps.append(f'# Fill missing values\ndf["{null_cols[0]}"] = df["{null_cols[0]}"].fillna(0)')
        if num_cols:
            lo, hi = outlier_bounds(df[num_cols[0]])
            steps.append(f'# Remove outliers\ndf = df[(df["{num_cols[0]}"] >= {lo:.1f}) & (df["{num_cols[0]}"] <= {hi:.1f})]')
        steps.append("# Convert date column\n# df['date_col'] = pd.to_datetime(df['date_col'])")
        return steps, "Python (pandas)"

    elif tool == "SQL":
        steps = []
        if dupes > 0:
            steps.append("-- Remove duplicates\nSELECT DISTINCT * FROM your_table;")
        if null_cols:
            steps.append(f'-- Handle nulls\nSELECT COALESCE("{null_cols[0]}", 0) as "{null_cols[0]}"\nFROM your_table;')
        if num_cols:
            lo, hi = outlier_bounds(df[num_cols[0]])
            steps.append(f'-- Filter outliers\nSELECT * FROM your_table\nWHERE "{num_cols[0]}" BETWEEN {lo:.0f} AND {hi:.0f};')
        return steps, "SQL"

    elif tool == "Tableau":
        steps = []
        steps.append("// Tableau Prep — Remove duplicates\nUse the 'Clean' step > Remove Duplicates")
        if null_cols:
            steps.append(f'// Fill nulls in {null_cols[0]}\nCalculated Field: IFNULL([{null_cols[0]}], 0)')
        if num_cols:
            lo, hi = outlier_bounds(df[num_cols[0]])
            steps.append(f'// Filter outliers\nAdd Filter: [{num_cols[0]}] >= {lo:.0f} AND [{num_cols[0]}] <= {hi:.0f}')
        return steps, "Tableau Prep / Calculated Fields"

    elif tool == "Excel":
        steps = []
        if dupes > 0:
            steps.append("// Remove duplicates\nData tab > Remove Duplicates > Select all columns")
        if null_cols:
            steps.append(f'// Fill blanks in {null_cols[0]}\nCtrl+H > Find: (blank) > Replace with: 0\nOr use: =IF(ISBLANK(A1), 0, A1)')
        if num_cols:
            lo, hi = outlier_bounds(df[num_cols[0]])
            steps.append(f'// Filter outliers\n=AND({num_cols[0]}>{lo:.0f}, {num_cols[0]}<{hi:.0f})\nUse as helper column, then filter TRUE rows')
        return steps, "Excel (Power Query / Formulas)"

    return [], tool


def get_measures_code(df, tool, num_cols, cat_cols, missing_cols):
    if tool == "Power BI":
        measures = []
        if num_cols:
            measures.append((f"Average {num_cols[0]}", f"Avg {num_cols[0]} = \nAVERAGE(Data[{num_cols[0]}])"))
            measures.append(("Total Rows", "Total Rows = \nCOUNTROWS(Data)"))
        if missing_cols:
            mc = missing_cols[0]
            measures.append((f"Missing Rate — {mc}", f"Missing % = \nDIVIDE(\n    COUNTROWS(FILTER(Data, ISBLANK(Data[{mc}]))),\n    COUNTROWS(Data)\n) * 100"))
        if len(num_cols) >= 2:
            measures.append(("% Above Average", f"Pct Above Avg = \nDIVIDE(\n    COUNTROWS(FILTER(Data,\n        Data[{num_cols[0]}] > CALCULATE(AVERAGE(Data[{num_cols[0]}]), ALL(Data))\n    )),\n    COUNTROWS(Data)\n) * 100"))
        if cat_cols and num_cols:
            measures.append((f"Top {cat_cols[0]}", f"Top {cat_cols[0]} = \nCALCULATE(\n    MAX(Data[{cat_cols[0]}]),\n    TOPN(1,\n        VALUES(Data[{cat_cols[0]}]),\n        CALCULATE(AVERAGE(Data[{num_cols[0]}])), DESC\n    )\n)"))
        return measures

    elif tool == "Python":
        measures = []
        if num_cols:
            measures.append((f"Summary Stats", f"# Summary statistics\ndf['{num_cols[0]}'].describe()\n\n# Group by category\n" + (f"df.groupby('{cat_cols[0]}')['{num_cols[0]}'].mean()" if cat_cols else "")))
        if len(num_cols) >= 2:
            measures.append(("Correlation Matrix", f"# Correlation matrix\ndf[['{num_cols[0]}', '{num_cols[1]}']].corr()"))
        return measures

    elif tool == "SQL":
        measures = []
        if num_cols:
            measures.append(("Aggregation Query", f"SELECT\n    {('\"'+cat_cols[0]+'\",' if cat_cols else '')}\n    AVG(\"{num_cols[0]}\") as avg_{num_cols[0]},\n    COUNT(*) as total_rows,\n    MIN(\"{num_cols[0]}\") as min_val,\n    MAX(\"{num_cols[0]}\") as max_val\nFROM your_table\n{('GROUP BY \"'+cat_cols[0]+'\"' if cat_cols else '')};"))
        return measures

    elif tool == "Tableau":
        measures = []
        if num_cols:
            measures.append((f"Average {num_cols[0]}", f"// Calculated Field\nAVG([{num_cols[0]}])"))
            if cat_cols:
                measures.append(("% of Total", f"// % of total by category\nSUM([{num_cols[0]}]) / TOTAL(SUM([{num_cols[0]}]))"))
        return measures

    elif tool == "Excel":
        measures = []
        if num_cols:
            measures.append(("Average Formula", f"=AVERAGE({num_cols[0]}:{num_cols[0]})\n\n// Dynamic with criteria:\n=AVERAGEIF(category_col, \"value\", {num_cols[0]}:{num_cols[0]})"))
            if cat_cols:
                measures.append(("PivotTable Setup", f"// Recommended Pivot:\nRows: {cat_cols[0]}\nValues: Average of {num_cols[0]}\nFilter: Date column (if exists)"))
        return measures

    return []


# ══════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════

st.markdown("""
<div class="hero">
  <div class="badge">NO API KEY REQUIRED &nbsp;|&nbsp; FREE FOREVER &nbsp;|&nbsp; ANY TOOL</div>
  <div class="hero-title">Data<span style="color:#6366f1">Sense</span></div>
  <div class="hero-sub">Upload your dataset. Get deep analysis for any analytics tool.</div>
</div>
""", unsafe_allow_html=True)

# Tool selector
st.markdown('<div class="section-title">Your Analytics Tool</div>', unsafe_allow_html=True)
tool = st.radio("", ["Power BI", "Python", "SQL", "Tableau", "Excel"], horizontal=True, label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# Upload
uploaded = st.file_uploader("Upload CSV or Excel", type=["csv","xlsx","xls"], label_visibility="collapsed")

if not uploaded:
    st.markdown("""
    <div style="background:#0d0d1a;border:1.5px dashed #2a2a4a;border-radius:16px;padding:50px 20px;text-align:center;margin-top:10px">
      <div style="font-size:40px;margin-bottom:12px">+</div>
      <div style="font-size:16px;color:#6b6b9a">Drop your CSV or Excel file here</div>
      <div style="font-size:12px;color:#3a3a5a;font-family:monospace;margin-top:6px">Supports .csv, .xlsx, .xls</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Load
try:
    if uploaded.name.lower().endswith('.csv'):
        df = pd.read_csv(uploaded, encoding='utf-8', on_bad_lines='skip', nrows=50000)
    else:
        df = pd.read_excel(uploaded, nrows=50000)
    df = df.dropna(how='all')
    gc.collect()
except Exception as e:
    st.error(f"Error reading file: {e}")
    st.stop()

# Pre-compute
total_cells = df.shape[0]*df.shape[1]
missing_total = df.isnull().sum().sum()
missing_pct = round(missing_total/total_cells*100,1) if total_cells else 0
dupes = df.duplicated().sum()
score = quality_score(df)
score_color = "#10b981" if score>=80 else "#f59e0b" if score>=60 else "#ef4444"
num_cols = df.select_dtypes(include='number').columns.tolist()
cat_cols = [c for c in df.columns if detect_type(df[c])=='category']
date_cols = [c for c in df.columns if detect_type(df[c])=='date']
null_cols = [c for c in df.columns if df[c].isnull().any()]
missing_cols_list = [c for c in df.columns if df[c].isnull().sum()>0]
dataset_type = detect_dataset_type(df)
patterns = detect_patterns(df)
risk_data = calculate_risk(df)
story = generate_story(df, dataset_type, patterns, score)
questions = generate_questions(df, dataset_type, patterns)

# ── KPIs ─────────────────────────────────────────────
c1,c2,c3,c4 = st.columns(4)
kpis = [
    (c1,"Rows",f"{df.shape[0]:,}",f"{df.shape[1]} columns","#6366f1"),
    (c2,"Missing",f"{missing_pct}%",f"{missing_total:,} cells","#f59e0b" if missing_pct>5 else "#10b981"),
    (c3,"Duplicates",f"{dupes:,}",f"{dupes/len(df)*100:.1f}% of rows" if len(df) else "0%","#ef4444" if dupes>0 else "#10b981"),
    (c4,"Quality Score",f"{score}","out of 100",score_color),
]
for col,label,val,sub,accent in kpis:
    with col:
        st.markdown(f'<div class="kpi" style="--accent:{accent}"><div class="kpi-label">{label}</div><div class="kpi-value" style="color:{accent}">{val}</div><div class="kpi-sub">{sub}</div></div>', unsafe_allow_html=True)

# ── DATA STORY ────────────────────────────────────────
st.markdown('<div class="section-title">Data Story</div>', unsafe_allow_html=True)
dtype_badges = {"operations":"OPERATIONS","financial":"FINANCIAL","financial_market":"MARKET DATA","hr":"HR","healthcare":"HEALTHCARE","education":"EDUCATION","product":"PRODUCT","general":"GENERAL"}
st.markdown(f"""
<div class="story-box">
  <div style="margin-bottom:12px"><span class="badge">{dtype_badges.get(dataset_type,'DATA')}</span></div>
  <div class="story-text">{story}</div>
  <div class="story-meta">DataSense automatically detected dataset type and generated this summary</div>
</div>
""", unsafe_allow_html=True)

# ── PATTERN DETECTION ─────────────────────────────────
st.markdown('<div class="section-title">Pattern Detection</div>', unsafe_allow_html=True)
if patterns:
    icon_map = {"up":"up","dn":"dn","sea":"sea","out":"out","cor":"cor","skw":"skw","grw":"grw"}
    emoji_map = {"up":"trend_up","dn":"trend_dn","sea":"seasonal","out":"outlier","cor":"correlation","skw":"skewed","grw":"growth"}

    for i in range(0, len(patterns), 2):
        chunk = patterns[i:i+2]
        cols_p = st.columns(len(chunk))
        for j, p in enumerate(chunk):
            with cols_p[j]:
                st.markdown(f"""
                <div class="pattern-card" style="--pc:{p['color']}">
                  <div class="pattern-title">{p['title']}</div>
                  <div class="pattern-stat">{p['stat']}</div>
                  <div class="pattern-body">{p['body']}</div>
                  <div style="margin-top:12px;padding-top:10px;border-top:1px solid #1e1e35;font-size:11px;font-family:'JetBrains Mono';color:#6b6b9a">
                    <span style="color:{p['color']}">ACTION: </span>{p['action']}
                  </div>
                </div>""", unsafe_allow_html=True)
else:
    st.markdown('<div style="background:#0d0d1a;border:1px solid #1e1e35;border-radius:14px;padding:24px;color:#6b6b9a;font-family:JetBrains Mono;font-size:13px">No significant patterns detected. Dataset may be too small or too uniform for pattern analysis.</div>', unsafe_allow_html=True)

# ── COLUMN PROFILE ────────────────────────────────────
st.markdown('<div class="section-title">Column Profile</div>', unsafe_allow_html=True)
cols_list = list(df.columns)
for i in range(0, len(cols_list), 4):
    chunk = cols_list[i:i+4]
    grid = st.columns(4)
    for j, col_name in enumerate(chunk):
        s = df[col_name]
        filled = s.dropna()
        pct = round(len(filled)/len(df)*100) if len(df) else 0
        uniq = filled.nunique()
        t = detect_type(s)
        risk = next((r for r in risk_data if r['col']==col_name), None)
        risk_color = risk['color'] if risk else "#6b6b9a"
        risk_level = risk['level'] if risk else "LOW"
        extra = ""
        if t == "numeric":
            try:
                nums = pd.to_numeric(filled, errors='coerce').dropna()
                extra = f"avg: {nums.mean():.1f}"
            except: pass
        with grid[j]:
            st.markdown(f"""
            <div class="col-card">
              <div class="col-name" title="{col_name}">{col_name[:20]}{'...' if len(col_name)>20 else ''}</div>
              <div style="display:flex;justify-content:space-between;align-items:center;margin:4px 0 8px">
                {type_tag(t)}
                <span style="font-size:9px;font-family:'JetBrains Mono';color:{risk_color};font-weight:700">{risk_level}</span>
              </div>
              {bar_html(pct)}
              <div class="col-meta">{pct}% filled &nbsp;|&nbsp; {uniq} unique</div>
              {f'<div class="col-meta" style="margin-top:3px">{extra}</div>' if extra else ''}
            </div>""", unsafe_allow_html=True)

# ── RISK SCORE ────────────────────────────────────────
st.markdown('<div class="section-title">Column Risk Score</div>', unsafe_allow_html=True)
high_risk = [r for r in risk_data if r['level']=='HIGH']
med_risk = [r for r in risk_data if r['level']=='MEDIUM']
low_risk = [r for r in risk_data if r['level']=='LOW']

for section_data, label, color in [(high_risk,"HIGH RISK","#ef4444"),(med_risk,"MEDIUM RISK","#f59e0b"),(low_risk,"LOW RISK","#10b981")]:
    if section_data:
        st.markdown(f'<div style="font-size:10px;font-family:JetBrains Mono;color:{color};letter-spacing:2px;font-weight:700;margin:12px 0 8px">{label}</div>', unsafe_allow_html=True)
        for i in range(0, len(section_data), 4):
            chunk = section_data[i:i+4]
            grid = st.columns(4)
            for j, r in enumerate(chunk):
                with grid[j]:
                    reasons_html = " &nbsp;|&nbsp; ".join(r['reasons']) if r['reasons'] else "No issues found"
                    st.markdown(f"""
                    <div class="risk-card">
                      <div class="risk-col">{r['col'][:18]}{'...' if len(r['col'])>18 else ''}</div>
                      <div style="display:flex;align-items:center;gap:8px;margin:6px 0">
                        <div style="flex:1;background:#07070f;border-radius:3px;height:5px;overflow:hidden">
                          <div style="width:{r['score']}%;height:100%;background:{r['color']};border-radius:3px"></div>
                        </div>
                        <span style="font-size:11px;font-family:'JetBrains Mono';color:{r['color']};font-weight:700">{r['score']}</span>
                      </div>
                      <div style="font-size:10px;color:#6b6b9a;font-family:'JetBrains Mono';line-height:1.5">{reasons_html}</div>
                    </div>""", unsafe_allow_html=True)

# ── SMART INSIGHTS ─────────────────────────────────────
st.markdown('<div class="section-title">Smart Insights</div>', unsafe_allow_html=True)
insights = []
missing_by_col = df.isnull().sum()
missing_by_col = missing_by_col[missing_by_col>0].sort_values(ascending=False)
if len(missing_by_col)>0:
    top_miss = missing_by_col.index[0]
    top_miss_pct = round(missing_by_col.iloc[0]/len(df)*100,1)
    insights.append(("Missing Data Alert", f"<b style='color:#f59e0b'>{top_miss}</b> has the most missing values at <b style='color:#f59e0b'>{top_miss_pct}%</b>. This will create gaps in any time-series or aggregate analysis."))
else:
    insights.append(("Clean Dataset", "All columns are fully populated. Your dataset is clean and ready for analysis."))

if len(num_cols)>=2:
    try:
        corr = df[num_cols[:6]].corr().abs()
        np.fill_diagonal(corr.values, 0)
        max_c = corr.max().max()
        if max_c > 0.7:
            idx = corr.stack().idxmax()
            insights.append(("Strong Correlation", f"<b style='color:#00e5ff'>{idx[0]}</b> and <b style='color:#00e5ff'>{idx[1]}</b> are {max_c*100:.0f}% correlated (r={max_c:.2f}). Using both in the same model will cause double-counting."))
    except: pass

if dupes > 0:
    insights.append(("Duplicate Rows Found", f"<b style='color:#ef4444'>{dupes:,} duplicate rows</b> ({dupes/len(df)*100:.1f}%) detected. These inflate counts and distort aggregations."))

if num_cols:
    skewed_cols = []
    for col in num_cols[:5]:
        try:
            sk = abs(float(df[col].dropna().skew()))
            if sk > 1.5: skewed_cols.append((col, sk))
        except: pass
    if skewed_cols:
        col, sk = max(skewed_cols, key=lambda x: x[1])
        insights.append(("Skewed Distribution", f"<b style='color:#06b6d4'>{col}</b> is heavily skewed (skewness={sk:.1f}). The mean misrepresents the typical value — use <b>median</b> in KPI cards instead."))

cols_g = st.columns(2)
for i, (title, body) in enumerate(insights[:4]):
    with cols_g[i%2]:
        st.markdown(f'<div class="insight-card"><div class="insight-title">{title}</div><div class="insight-body">{body}</div></div>', unsafe_allow_html=True)

# ── GROUP COMPARISON ──────────────────────────────────
if cat_cols and num_cols and df[cat_cols[0]].nunique() <= 50:
    best_cat = cat_cols[0]
    best_num = num_cols[0]
    st.markdown(f'<div class="section-title">Group Comparison — {best_cat}</div>', unsafe_allow_html=True)
    grp = df.groupby(best_cat)[best_num].agg(['mean','count']).round(1).sort_values('mean')
    grp.columns = ['Average','Count']
    grp = grp.reset_index()
    total_grps = len(grp)
    rows_html = ""
    for idx_r, row in grp.iterrows():
        if idx_r==0: rank_html = '<span style="color:#10b981;font-weight:700">BEST</span>'
        elif idx_r==total_grps-1: rank_html = '<span style="color:#ef4444;font-weight:700">WORST</span>'
        else: rank_html = f'<span style="color:#6b6b9a">{idx_r+1}</span>'
        bar_w = int(row['Average']/grp['Average'].max()*140) if grp['Average'].max()>0 else 0
        bar_c = "#10b981" if idx_r<total_grps*0.33 else "#f59e0b" if idx_r<total_grps*0.66 else "#ef4444"
        rows_html += f'<tr><td>{rank_html}</td><td style="color:#e2e2f0;font-weight:600">{row[best_cat]}</td><td><div style="display:flex;align-items:center;gap:8px"><div style="width:{bar_w}px;height:5px;background:{bar_c};border-radius:3px"></div><span>{row["Average"]:.1f}</span></div></td><td style="color:#6b6b9a">{int(row["Count"]):,}</td></tr>'
    st.markdown(f'<table class="store-table"><thead><tr><th>#</th><th>{best_cat}</th><th>Avg {best_num}</th><th>Count</th></tr></thead><tbody>{rows_html}</tbody></table>', unsafe_allow_html=True)

# ── CRITICAL ISSUES ───────────────────────────────────
st.markdown('<div class="section-title">Critical Issues to Fix</div>', unsafe_allow_html=True)
issues = []
for col in df.columns:
    pct = df[col].isnull().sum()/len(df)*100
    if pct>10: issues.append(("#ef4444", f"<b>{col}</b> — {pct:.1f}% missing. High impact on analysis accuracy."))
    elif pct>0: issues.append(("#f59e0b", f"<b>{col}</b> — {pct:.1f}% missing. Replace with 0, median, or mode."))
for col in num_cols[:5]:
    lo,hi = outlier_bounds(df[col])
    cnt = int(((df[col]<lo)|(df[col]>hi)).sum())
    if cnt/len(df)>0.1: issues.append(("#ef4444", f"<b>{col}</b> — {cnt:,} outliers ({cnt/len(df)*100:.1f}%). Filter to range {lo:.0f}–{hi:.0f}."))
if dupes>0: issues.append(("#ef4444", f"<b>{dupes:,} duplicate rows</b> — remove before any aggregation."))
if not issues: issues.append(("#10b981", "No critical issues found. Dataset is clean and ready."))
issues_html = "".join([f'<div class="issue-item"><div class="issue-dot" style="background:{c}"></div><div>{t}</div></div>' for c,t in issues[:6]])
st.markdown(f'<div style="background:#0d0d1a;border:1px solid #1e1e35;border-radius:14px;padding:20px 24px">{issues_html}</div>', unsafe_allow_html=True)

# ── CLEANING CODE ─────────────────────────────────────
cleaning_steps, lang_label = get_cleaning_code(df, tool, num_cols, null_cols)
st.markdown(f'<div class="section-title">Cleaning Steps — {lang_label}</div>', unsafe_allow_html=True)
for step in cleaning_steps:
    st.markdown(f'<div class="code-block">{step}</div>', unsafe_allow_html=True)

# ── MEASURES / FORMULAS ───────────────────────────────
measures = get_measures_code(df, tool, num_cols, cat_cols, missing_cols_list)
if measures:
    tool_labels = {"Power BI":"DAX Measures","Python":"Python Snippets","SQL":"SQL Queries","Tableau":"Calculated Fields","Excel":"Excel Formulas"}
    st.markdown(f'<div class="section-title">{tool_labels.get(tool,"Formulas")}</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    for i,(title,code) in enumerate(measures[:4]):
        with (col1 if i%2==0 else col2):
            st.markdown(f'<div class="code-title">{title}</div><div class="code-block">{code}</div>', unsafe_allow_html=True)

# ── SUGGESTED QUESTIONS ───────────────────────────────
st.markdown('<div class="section-title">5 Questions Worth Answering</div>', unsafe_allow_html=True)
q_html = ""
for i,(q,why,category) in enumerate(questions):
    q_html += f'<div class="question-item"><div class="question-num">0{i+1}</div><div><div class="question-text">{q}</div><div class="question-why">{why}</div></div></div>'
st.markdown(f'<div style="background:#0d0d1a;border:1px solid #1e1e35;border-radius:14px;padding:20px 24px">{q_html}</div>', unsafe_allow_html=True)

# ── CUSTOMER SEGMENTATION ─────────────────────────────
repeat_col = next((c for c in df.columns if any(x in c.lower() for x in ['order_count','purchase','visit','user_count'])), None)
if repeat_col and detect_type(df[repeat_col])=='numeric':
    st.markdown(f'<div class="section-title">Customer Segmentation — {repeat_col}</div>', unsafe_allow_html=True)
    df['_seg'] = df[repeat_col].apply(lambda x: 'New' if x==1 else ('Loyal' if x>=5 else 'Returning'))
    seg = df['_seg'].value_counts()
    seg_cols = st.columns(3)
    seg_colors = {'New':'#6366f1','Returning':'#10b981','Loyal':'#f59e0b'}
    for i,(sn,cnt) in enumerate(seg.items()):
        color = seg_colors.get(sn,'#6b6b9a')
        with seg_cols[i%3]:
            st.markdown(f'<div class="kpi" style="--accent:{color}"><div class="kpi-label">{sn} Customers</div><div class="kpi-value" style="color:{color}">{cnt:,}</div><div class="kpi-sub">{round(cnt/len(df)*100,1)}% of total</div></div>', unsafe_allow_html=True)
    df.drop(columns=['_seg'], inplace=True)

# ── FINAL VERDICT ─────────────────────────────────────
st.markdown('<div class="section-title">Final Verdict</div>', unsafe_allow_html=True)
verdict = "READY" if score>=80 else "NEEDS WORK" if score>=60 else "CRITICAL"
verdict_color = "#10b981" if score>=80 else "#f59e0b" if score>=60 else "#ef4444"
verdict_msg = ("Clean dataset. Minimal prep needed before analysis." if score>=80 else "Fix the issues above before building dashboards." if score>=60 else "Critical quality issues. Resolve all problems first.")

tool_visuals = {
    "Power BI": ["KPI Card","Line Chart","Bar Chart","Scatter Plot","Matrix"],
    "Python": ["plt.plot()","sns.barplot()","sns.scatterplot()","df.corr() heatmap","px.histogram()"],
    "SQL": ["GROUP BY query","Window function","CTE analysis","Subquery filter","JOIN analysis"],
    "Tableau": ["KPI Summary","Trend Line","Bar in Bar","Scatter Plot","Heat Map"],
    "Excel": ["PivotTable","Line Chart","Bar Chart","Scatter Plot","Conditional Formatting"],
}
visuals = tool_visuals.get(tool, ["KPI Card","Line Chart","Bar Chart","Scatter Plot","Matrix"])
rec_html = "".join([f'<div style="padding:8px 0;border-bottom:1px solid #1e1e35;font-family:JetBrains Mono;font-size:13px;color:#c4c4e0"><span style="color:{verdict_color};margin-right:10px">0{i+1}</span>{v}</div>' for i,v in enumerate(visuals)])

col1,col2 = st.columns([1,2])
with col1:
    st.markdown(f"""
    <div class="verdict-box">
      <div style="font-size:72px;font-weight:800;line-height:1;color:{verdict_color}">{score}</div>
      <div style="font-size:12px;font-family:'JetBrains Mono';color:#6b6b9a;margin-top:6px">Quality Score</div>
      <div style="font-size:20px;font-weight:800;color:{verdict_color};margin-top:10px">{verdict}</div>
      <div style="font-size:12px;color:#6b6b9a;margin-top:8px;font-family:'JetBrains Mono';line-height:1.6">{verdict_msg}</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div style="background:#0d0d1a;border:1px solid #1e1e35;border-radius:16px;padding:24px 28px">
      <div class="section-title" style="margin-top:0">Recommended {tool} Visuals</div>
      {rec_html}
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
