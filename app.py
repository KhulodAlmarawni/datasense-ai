# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import gc

st.set_page_config(page_title="DataSense", page_icon="DS", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');
*{box-sizing:border-box;}
html,body,[class*="css"]{font-family:'Syne',sans-serif;}
.stApp{background:#07070f;color:#e2e2f0;}
/* Hide streamlit default elements */
#MainMenu,footer,header{visibility:hidden;}
[data-testid="stSidebar"]{background:#0d0d1a;border-right:1px solid #1e1e35;}
/* Remove ALL default streamlit widget borders/backgrounds */
.stRadio>div{gap:0 !important;background:transparent !important;border:none !important;padding:0 !important;}
.stRadio>div>div{background:transparent !important;}
[data-testid="stFileUploader"]{background:transparent !important;border:none !important;padding:0 !important;}
[data-testid="stFileUploader"]>div{background:transparent !important;border:none !important;}
[data-testid="stFileUploader"]{background:#0a0a18 !important;border:1.5px dashed #1e1e35 !important;border-radius:16px !important;padding:8px 16px !important;}
[data-testid="stFileUploader"]:hover{border-color:#6366f1 !important;}
[data-testid="stFileUploaderDropzone"]{background:transparent !important;border:none !important;}
[data-testid="stFileUploaderDropzone"] *{color:#4a4a6a !important;}
[data-testid="stFileUploaderDropzone"] button{background:rgba(99,102,241,0.1) !important;border:1px solid #6366f1 !important;color:#a5b4fc !important;border-radius:8px !important;}
/* Hero */
.hero{background:linear-gradient(135deg,#0a0a18 0%,#0f0f22 50%,#0a0a18 100%);border:1px solid #1a1a30;border-radius:24px;padding:40px 44px;margin-bottom:32px;position:relative;overflow:hidden;}
.hero::after{content:'';position:absolute;top:-80px;right:-80px;width:300px;height:300px;background:radial-gradient(circle,rgba(99,102,241,0.08) 0%,transparent 70%);border-radius:50%;pointer-events:none;}
.badge{display:inline-flex;align-items:center;gap:6px;font-size:10px;font-family:'JetBrains Mono';font-weight:700;padding:5px 14px;border-radius:20px;letter-spacing:1.5px;background:rgba(16,185,129,0.08);color:#10b981;border:1px solid rgba(16,185,129,0.2);margin-bottom:18px;}
.badge::before{content:'';width:5px;height:5px;border-radius:50%;background:#10b981;animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.3;}}
/* Hide radio label box completely */
div[data-testid="stRadio"] > label {display:none !important;}
div[data-testid="stRadio"] > div {background:transparent !important;border:none !important;padding:0 !important;gap:8px !important;}
.tool-label{font-size:11px;font-family:'JetBrains Mono';color:#4a4a6a;text-transform:uppercase;letter-spacing:2px;margin-bottom:10px;}
.stRadio label{background:transparent !important;border:1px solid #1e1e35 !important;border-radius:8px !important;padding:7px 16px !important;font-family:'JetBrains Mono' !important;font-size:11px !important;color:#6b6b9a !important;transition:all 0.15s !important;cursor:pointer !important;}
.stRadio label:hover{border-color:#6366f1 !important;color:#a5b4fc !important;}
[data-baseweb="radio"] input:checked+div+div label,
.stRadio [aria-checked="true"] label{background:rgba(99,102,241,0.1) !important;border-color:#6366f1 !important;color:#a5b4fc !important;}
/* Upload zone — clean, no inner box */
.upload-zone{border:1.5px dashed #1e1e35;border-radius:16px;padding:36px 24px;text-align:center;background:linear-gradient(135deg,#0a0a18,#0d0d1a);transition:border-color 0.2s;margin-top:8px;cursor:pointer;}
.upload-zone:hover{border-color:#6366f1;}
.upload-icon{font-size:32px;margin-bottom:10px;opacity:0.6;}
.upload-title{font-size:15px;font-weight:700;color:#e2e2f0;margin-bottom:4px;}
.upload-sub{font-size:11px;color:#4a4a6a;font-family:'JetBrains Mono';}
/* KPI */
.kpi{background:#0a0a18;border:1px solid #1a1a30;border-radius:16px;padding:18px 20px;border-top:2px solid var(--a);position:relative;overflow:hidden;}
.kpi::after{content:'';position:absolute;bottom:-20px;right:-20px;width:80px;height:80px;background:radial-gradient(circle,var(--a) 0%,transparent 70%);opacity:0.06;border-radius:50%;}
.kpi-l{font-size:9px;font-family:'JetBrains Mono';color:#4a4a6a;text-transform:uppercase;letter-spacing:2px;margin-bottom:8px;}
.kpi-v{font-size:30px;font-weight:800;line-height:1;letter-spacing:-1px;}
.kpi-s{font-size:10px;color:#4a4a6a;margin-top:5px;font-family:'JetBrains Mono';}
/* Section headers */
.sec{font-size:9px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#3a3a5a;padding:6px 0 12px;border-bottom:1px solid #0f0f20;margin:28px 0 16px;display:flex;align-items:center;gap:8px;}
.sec::before{content:'';width:3px;height:12px;background:#6366f1;border-radius:2px;display:inline-block;}
/* Cards */
.card{background:#0a0a18;border:1px solid #1a1a30;border-radius:14px;padding:16px 18px;}
.tag{font-size:8px;font-family:'JetBrains Mono';padding:3px 9px;border-radius:20px;font-weight:700;letter-spacing:0.5px;}
.bw{background:#07070f;border-radius:3px;height:2px;margin:8px 0 6px;overflow:hidden;}
.bf{height:100%;border-radius:3px;}
.cm{font-size:10px;color:#4a4a6a;font-family:'JetBrains Mono';}
.cn{font-family:'JetBrains Mono';font-size:11px;font-weight:700;color:#8b8bcc;margin-bottom:8px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
/* Pattern cards */
.pc{background:#0a0a18;border:1px solid #1a1a30;border-radius:16px;padding:20px 22px;border-left:3px solid var(--c);}
.pt{font-size:9px;font-family:'JetBrains Mono';text-transform:uppercase;letter-spacing:1.5px;color:var(--c);margin-bottom:8px;opacity:0.9;}
.ps{font-size:26px;font-weight:800;color:var(--c);margin:4px 0 10px;letter-spacing:-1px;}
.pb{font-size:13px;color:#a0a0c0;line-height:1.7;}
.pa{margin-top:12px;padding-top:10px;border-top:1px solid #0f0f20;font-size:10px;font-family:'JetBrains Mono';color:#4a4a6a;line-height:1.6;}
/* Code blocks */
.cb{background:#050510;border:1px solid #1a1a30;border-radius:12px;padding:18px 22px;font-family:'JetBrains Mono';font-size:11px;color:#8b8bcc;line-height:2;margin-bottom:14px;white-space:pre-wrap;position:relative;}
.ct{font-size:9px;color:#3a3a5a;text-transform:uppercase;letter-spacing:2px;margin-bottom:8px;font-family:'JetBrains Mono';}
/* Questions */
.qi{display:flex;gap:14px;padding:14px 0;border-bottom:1px solid #0a0a18;align-items:flex-start;}
.qn{font-size:10px;font-family:'JetBrains Mono';color:#6366f1;font-weight:700;min-width:20px;margin-top:3px;}
.qt{font-size:13px;color:#e2e2f0;font-weight:700;line-height:1.5;margin-bottom:3px;}
.qw{font-size:11px;color:#4a4a6a;font-family:'JetBrains Mono';line-height:1.5;}
/* Issues */
.ii{display:flex;align-items:flex-start;gap:12px;padding:12px 0;border-bottom:1px solid #0a0a18;font-size:13px;color:#a0a0c0;line-height:1.6;}
.idot{width:6px;height:6px;border-radius:50%;margin-top:6px;flex-shrink:0;}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# SMART COLUMN CLASSIFIER
# ══════════════════════════════════════════════════════

def classify_column(col_name, series):
    """Classify column into: id, metric, group, time, location, flag, useless"""
    name = col_name.lower().replace('_',' ').replace('-',' ')
    filled = series.dropna()
    if len(filled) == 0: return "empty"

    # Useless — single value
    if filled.nunique() <= 1:
        return "useless"

    # Location detection — before anything else
    loc_keywords = ['lat','lon','lng','latitude','longitude','coordinate','geo']
    if any(k in name for k in loc_keywords):
        return "location"

    # ID detection — name ends with id/key/code OR high cardinality number
    id_suffixes = ['_id', ' id', '_key', ' key', '_uuid', '_hash', '_ref', '_code', '_no', '_num']
    is_id_name = any(name == k.strip() or name.endswith(k) for k in id_suffixes)
    is_high_card = filled.nunique() / len(filled) > 0.6 if len(filled) > 0 else False
    if is_id_name and is_high_card:
        return "id"

    # Time detection — ONLY if column contains date-like strings (not pure numbers)
    filled_str = filled.astype(str).str.strip()
    has_date_pattern = filled_str.str.match(r'\d{4}-\d{2}|\d{2}/\d{2}|\d{4}/\d{2}').any()
    if has_date_pattern:
        try:
            pd.to_datetime(filled_str.iloc[:20], format="mixed", dayfirst=False)
            return "time"
        except: pass

    # Numeric columns
    try:
        nums = pd.to_numeric(filled, errors='coerce').dropna()
        if len(nums) / max(len(filled), 1) > 0.85:

            # Hour grouper — small range 0-23
            if 'hour' in name and nums.max() <= 23 and nums.min() >= 0:
                return "time_num"

            # Month grouper
            if 'month' in name and nums.max() <= 12 and nums.min() >= 1:
                return "time_num"

            # Year grouper — few unique values
            if 'year' in name and nums.nunique() <= 15:
                return "time_num"

            # Binary flag
            if nums.nunique() == 2 and set(nums.unique()).issubset({0, 1}):
                return "flag"

            # Group-like numeric — very few unique values relative to total
            if nums.nunique() <= 20 and nums.nunique() / len(nums) < 0.005:
                return "group_num"

            # True metric — continuous numeric with real variance
            return "metric"

    except: pass

    # Categorical group
    if filled.nunique() <= 50:
        return "group"

    return "text"


def get_real_metrics(df):
    """Return only true metric columns — no IDs, no locations, no useless"""
    metrics = []
    for col in df.columns:
        role = classify_column(col, df[col])
        if role == "metric":
            metrics.append(col)
    return metrics

def get_groups(df):
    """Return good grouping columns"""
    groups = []
    for col in df.columns:
        role = classify_column(col, df[col])
        if role in ("group", "group_num", "time_num"):
            groups.append(col)
    return groups

def get_time_cols(df):
    """Return time columns"""
    times = []
    for col in df.columns:
        role = classify_column(col, df[col])
        if role in ("time", "time_num"):
            times.append(col)
    return times

def get_useless(df):
    """Return useless columns"""
    return [col for col in df.columns if classify_column(col, df[col]) in ("useless", "id")]


# ══════════════════════════════════════════════════════
# SMART OUTLIER BOUNDS (never negative for physical values)
# ══════════════════════════════════════════════════════

def smart_bounds(col_name, series):
    """Calculate outlier bounds with domain logic"""
    s = series.dropna()
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    lo = q1 - 1.5 * iqr
    hi = q3 + 1.5 * iqr

    name = col_name.lower()
    # Physical values that can't be negative
    non_negative = ['time','seconds','minutes','hours','price','cost','amount','cents','fee',
                    'distance','count','total','items','skus','rate','score','age','weight']
    if any(k in name for k in non_negative):
        lo = max(0, lo)

    return round(lo, 1), round(hi, 1)


# ══════════════════════════════════════════════════════
# SMART MISSING VALUE ADVICE
# ══════════════════════════════════════════════════════

def missing_advice(col_name, series, df):
    """Give smart advice for missing values based on column context"""
    name = col_name.lower()
    miss_pct = series.isnull().sum() / len(df) * 100
    filled = series.dropna()

    # Helper: safe median for numeric
    def safe_median(s):
        try:
            m = pd.to_numeric(s, errors='coerce').median()
            return None if pd.isna(m) else m
        except: return None

    # Helper: most frequent value
    def top_val(s):
        try:
            top = s.mode()
            return f'"{top.iloc[0]}"' if len(top) > 0 else "most frequent value"
        except: return "most frequent value"

    # Financial/reward — missing = zero
    if any(k in name for k in ['cashback','bonus','reward','promo']):
        return "Missing likely means no cashback. Safe to replace with 0."

    # Location — don't replace with 0
    if any(k in name for k in ['lat','lon','lng','latitude','longitude']):
        return f"Missing location data ({miss_pct:.1f}%). Exclude these rows from geographic analysis — do NOT replace with 0."

    # Numeric time/duration columns
    if any(k in name for k in ['time','seconds','minutes','duration']):
        med = safe_median(series)
        if med is not None:
            return f"Replace with median ({med:.1f}) — more robust than mean for time data."

    # Price/amount/cost
    if any(k in name for k in ['price','amount','cents','fee','cost']):
        med = safe_median(series)
        if med is not None:
            return f"Replace with 0 if absence means no charge, or median ({med:.1f}) if it's a recording gap."

    # Text/categorical columns — use mode
    med = safe_median(series)
    if med is None:
        tv = top_val(filled)
        return f"Text column — replace with most frequent value ({tv}) or remove rows."

    # Numeric default
    return f"Replace with median ({med:.1f}) or remove rows if critical field."


# ══════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════

@st.cache_data(max_entries=3)
def load_data(file_bytes, fname):
    import io
    if fname.lower().endswith('.csv'):
        df = pd.read_csv(io.BytesIO(file_bytes), on_bad_lines='skip', nrows=30000)
    else:
        df = pd.read_excel(io.BytesIO(file_bytes), nrows=30000)
    return df.dropna(how='all')

TS = {
    "metric":   ("#00e5ff","rgba(0,229,255,0.08)","rgba(0,229,255,0.2)","METRIC"),
    "time":     ("#10b981","rgba(16,185,129,0.08)","rgba(16,185,129,0.2)","TIME"),
    "time_num": ("#10b981","rgba(16,185,129,0.08)","rgba(16,185,129,0.2)","TIME"),
    "group":    ("#a78bfa","rgba(167,139,250,0.08)","rgba(167,139,250,0.2)","GROUP"),
    "group_num":("#a78bfa","rgba(167,139,250,0.08)","rgba(167,139,250,0.2)","GROUP"),
    "id":       ("#6b6b9a","rgba(107,107,154,0.08)","rgba(107,107,154,0.2)","ID"),
    "location": ("#f59e0b","rgba(245,158,11,0.08)","rgba(245,158,11,0.2)","GEO"),
    "flag":     ("#ec4899","rgba(236,72,153,0.08)","rgba(236,72,153,0.2)","FLAG"),
    "useless":  ("#ef4444","rgba(239,68,68,0.08)","rgba(239,68,68,0.2)","USELESS"),
    "text":     ("#f59e0b","rgba(245,158,11,0.08)","rgba(245,158,11,0.2)","TEXT"),
}
def ttag(t):
    c,bg,bd,l = TS.get(t, ("#6b6b9a","rgba(107,107,154,0.08)","rgba(107,107,154,0.2)","?"))
    return f'<span class="tag" style="color:{c};background:{bg};border:1px solid {bd}">{l}</span>'

def qscore(df, metrics):
    score = 100
    total = df.shape[0] * df.shape[1]
    if total == 0: return 0
    mp = df.isnull().sum().sum() / total * 100
    score -= min(30, mp * 1.5)
    for col in metrics[:4]:
        try:
            lo, hi = smart_bounds(col, df[col])
            ot = ((df[col] < lo) | (df[col] > hi)).sum()
            score -= min(5, (ot / len(df)) * 3)
        except: pass
    score -= min(15, df.duplicated().sum() / len(df) * 100 * 2)
    return max(0, round(score))

def detect_dataset_type(df):
    cs = " ".join(df.columns.str.lower())
    if any(x in cs for x in ['delivery','order','store','logistics','picking']): return "operations"
    if any(x in cs for x in ['revenue','sales','profit','invoice','payment']): return "financial"
    if any(x in cs for x in ['open','close','high','low','volume','stock']): return "market"
    if any(x in cs for x in ['employee','salary','department','hire','headcount']): return "hr"
    if any(x in cs for x in ['patient','hospital','medical','diagnosis']): return "healthcare"
    if any(x in cs for x in ['customer','user','session','click','retention']): return "product"
    return "general"


# ══════════════════════════════════════════════════════
# PATTERN DETECTION (uses real metrics only)
# ══════════════════════════════════════════════════════

def detect_patterns(df, metrics, time_cols, groups):
    pts = []

    # Trend on real metrics
    if time_cols and metrics:
        try:
            col = metrics[0]
            dt = df[[time_cols[0], col]].copy()
            dt['_d'] = pd.to_datetime(dt[time_cols[0]], errors='coerce', format="mixed")
            dt = dt.dropna().sort_values('_d')
            n = len(dt)
            if n > 20:
                f = dt[col].iloc[:n//3].mean()
                l = dt[col].iloc[-n//3:].mean()
                ch = ((l-f)/abs(f)*100) if f!=0 else 0
                if abs(ch) > 10:
                    c = "#10b981" if ch > 0 else "#ef4444"
                    pts.append({"t":f"{'Up' if ch>0 else 'Down'}ward Trend","c":c,"s":f"{'+' if ch>0 else ''}{ch:.1f}%","b":f"<b style='color:{c}'>{col}</b> {'grew' if ch>0 else 'declined'} {abs(ch):.1f}% over the dataset period.","a":f"Use Line Chart: {time_cols[0]} on X-axis, {col} on Y-axis."})
        except: pass

    # Outliers on real metrics only
    if metrics:
        wc, wn, wp = "", 0, 0
        for col in metrics[:4]:
            try:
                lo, hi = smart_bounds(col, df[col])
                n = int(((df[col] < lo) | (df[col] > hi)).sum())
                p = n / len(df) * 100
                if n > wn: wc, wn, wp = col, n, p
            except: pass
        if wn > 0 and wp > 5:
            lo, hi = smart_bounds(wc, df[wc])
            pts.append({"t":"Outlier Cluster","c":"#ef4444","s":f"{wn:,} rows","b":f"<b style='color:#ef4444'>{wc}</b> has {wn:,} outliers ({wp:.1f}%). Valid range: {lo}–{hi}.","a":f"Filter: keep rows where {wc} is between {lo} and {hi}."})

    # Correlation between real metrics
    if len(metrics) >= 2:
        try:
            cr = df[metrics[:5]].corr().abs()
            np.fill_diagonal(cr.values, 0)
            mx = cr.max().max()
            if mx > 0.85:
                idx = cr.stack().idxmax()
                pts.append({"t":"Multicollinearity","c":"#f59e0b","s":f"r={mx:.2f}","b":f"<b style='color:#f59e0b'>{idx[0]}</b> and <b style='color:#f59e0b'>{idx[1]}</b> are {mx*100:.0f}% correlated. Using both causes double-counting.","a":"Keep one as primary metric. Derive the other only when needed."})
        except: pass

    # Skewness on real metrics
    if metrics:
        sk = []
        for col in metrics[:4]:
            try:
                s = abs(float(df[col].dropna().skew()))
                if s > 1.5: sk.append((col, s))
            except: pass
        if sk:
            col, s = max(sk, key=lambda x: x[1])
            pts.append({"t":"Skewed Distribution","c":"#06b6d4","s":f"skew:{s:.1f}","b":f"<b style='color:#06b6d4'>{col}</b> is heavily skewed (skewness={s:.1f}). Mean is misleading here.","a":f"Use Median instead of Average for {col} in KPI cards."})

    # Useless columns warning
    useless = get_useless(df)
    if useless:
        pts.append({"t":"Low-Value Columns","c":"#6b6b9a","s":f"{len(useless)} cols","b":f"Columns <b style='color:#6b6b9a'>{', '.join(useless[:4])}</b> are IDs or single-value — they add no analytical value.","a":"Remove these columns before building your dashboard."})

    return pts[:4]


# ══════════════════════════════════════════════════════
# QUESTIONS (uses real metrics + groups)
# ══════════════════════════════════════════════════════

def generate_questions(ds_type, metrics, groups, time_cols):
    m0 = metrics[0] if metrics else "key metric"
    m1 = metrics[1] if len(metrics) > 1 else (metrics[0] if metrics else "metric 2")
    g0 = groups[0] if groups else "segment"
    t0 = time_cols[0] if time_cols else "date"

    all_qs = {
        "operations": [
            ("What causes delivery delays?", f"Compare {m0} across {g0} and time periods — find the bottleneck.", "Operations"),
            ("Which locations underperform?", f"Rank all {g0} by average {m0} — investigate the bottom 20%.", "Performance"),
            (f"What is the peak hour for orders?", f"Group by hour and plot {m0} — find when demand spikes.", "Time"),
            (f"Is there a {g0} with consistently high {m0}?", f"Compare {g0} distribution — look for consistently high or low performers.", "Segmentation"),
            (f"Does {m0} correlate with {m1}?", f"Scatter plot {m0} vs {m1} — a strong correlation means one drives the other.", "Correlation"),
        ],
        "financial": [
            ("What drives revenue growth?", f"Correlate {m0} with time and {g0}.", "Revenue"),
            ("Where is margin lost?", f"Compare cost vs revenue across {g0}.", "Profitability"),
            (f"Which {g0} is most profitable?", f"Group by {g0}, rank by {m0} highest to lowest.", "Segmentation"),
            (f"Is {m0} trending up or down?", f"Plot {m0} over {t0} — add a trend line.", "Trend"),
            (f"Does {m0} correlate with {m1}?", f"Scatter plot {m0} vs {m1} to find the relationship.", "Correlation"),
        ],
        "hr": [
            ("What predicts retention?", f"Correlate tenure with {m0}.", "Retention"),
            ("Is there pay equity?", f"Compare {m0} across {g0}.", "Equity"),
            (f"Which {g0} has the highest {m0}?", f"Rank {g0} by avg {m0}.", "Segmentation"),
            (f"How has {m0} changed over time?", f"Plot {m0} by {t0}.", "Trend"),
            (f"Does {m0} affect {m1}?", f"Scatter {m0} vs {m1}.", "Correlation"),
        ],
        "product": [
            ("Where do users drop off?", "Analyze conversion rates across funnel stages.", "Funnel"),
            ("What drives retention?", "Compare retained vs churned user behavior.", "Retention"),
            (f"Which {g0} has the best engagement?", f"Rank {g0} by avg {m0}.", "Segmentation"),
            (f"How does {m0} change over time?", f"Plot {m0} by {t0}.", "Trend"),
            (f"Does {m0} correlate with {m1}?", f"Scatter {m0} vs {m1}.", "Correlation"),
        ],
    }

    default = [
        (f"What are the trends in {m0}?", f"Plot {m0} over {t0} — identify peaks and drops.", "Trend"),
        (f"Which {g0} performs best?", f"Group by {g0}, rank by avg {m0}.", "Segmentation"),
        (f"Are there outliers in {m0}?", f"Box plot {m0} — flag values outside normal range.", "Quality"),
        (f"Does {m0} correlate with {m1}?", f"Scatter {m0} vs {m1} — look for patterns.", "Correlation"),
        (f"What is the distribution of {m0}?", f"Histogram of {m0} — check if mean equals median.", "Distribution"),
    ]

    return all_qs.get(ds_type, default)[:5]




# ══════════════════════════════════════════════════════
# CLEANING CODE (uses real metrics + smart bounds)
# ══════════════════════════════════════════════════════

def cleaning_code(df, tool, metrics, null_cols):
    d = df.duplicated().sum()
    steps = []

    # Get first real null metric
    null_metrics = [c for c in null_cols if classify_column(c, df[c]) == "metric"]
    null_col = null_metrics[0] if null_metrics else (null_cols[0] if null_cols else None)

    if tool == "Power BI":
        if d > 0: steps.append("// Remove duplicates\n= Table.Distinct(Source)")
        if null_col:
            advice = missing_advice(null_col, df[null_col], df)
            steps.append(f'// {advice}\n= Table.ReplaceValue(Source, null, 0,\n  Replacer.ReplaceValue, {{"{null_col}"}})')
        if metrics:
            lo, hi = smart_bounds(metrics[0], df[metrics[0]])
            steps.append(f'// Remove outliers in {metrics[0]}\n= Table.SelectRows(Source,\n  each [{metrics[0]}] >= {lo}\n  and [{metrics[0]}] <= {hi})')
        steps.append('// Set column types\n= Table.TransformColumnTypes(Source,\n  {{"date_col", type date},\n   {"id_col", type text}})')
        return steps, "Power Query"

    elif tool == "Python":
        if d > 0: steps.append("# Remove duplicates\ndf = df.drop_duplicates()")
        if null_col:
            advice = missing_advice(null_col, df[null_col], df)
            fill_val = 0 if 'cashback' in null_col.lower() or 'discount' in null_col.lower() else f'df["{null_col}"].median()'
            steps.append(f'# {advice}\ndf["{null_col}"] = df["{null_col}"].fillna({fill_val})')
        if metrics:
            lo, hi = smart_bounds(metrics[0], df[metrics[0]])
            steps.append(f'# Remove outliers in {metrics[0]}\ndf = df[\n  (df["{metrics[0]}"] >= {lo}) &\n  (df["{metrics[0]}"] <= {hi})\n]')
        return steps, "Python (pandas)"

    elif tool == "SQL":
        if d > 0: steps.append("-- Remove duplicates\nSELECT DISTINCT * FROM your_table;")
        if null_col:
            advice = missing_advice(null_col, df[null_col], df)
            steps.append(f'-- {advice}\nSELECT COALESCE("{null_col}", 0)\nFROM your_table;')
        if metrics:
            lo, hi = smart_bounds(metrics[0], df[metrics[0]])
            steps.append(f'-- Filter outliers in {metrics[0]}\nSELECT * FROM your_table\nWHERE "{metrics[0]}" BETWEEN {lo} AND {hi};')
        return steps, "SQL"

    elif tool == "Tableau":
        steps.append("// Remove duplicates\nTableau Prep > Clean > Remove Duplicates")
        if null_col:
            advice = missing_advice(null_col, df[null_col], df)
            steps.append(f'// {advice}\nCalculated Field:\nIFNULL([{null_col}], 0)')
        if metrics:
            lo, hi = smart_bounds(metrics[0], df[metrics[0]])
            steps.append(f'// Filter outliers in {metrics[0]}\n[{metrics[0]}] >= {lo}\nAND [{metrics[0]}] <= {hi}')
        return steps, "Tableau Prep"

    else:  # Excel
        steps.append("// Remove duplicates\nData > Remove Duplicates")
        if null_col:
            advice = missing_advice(null_col, df[null_col], df)
            steps.append(f'// {advice}\n=IF(ISBLANK(A1), 0, A1)')
        if metrics:
            lo, hi = smart_bounds(metrics[0], df[metrics[0]])
            steps.append(f'// Filter outliers in {metrics[0]}\n=AND({metrics[0]}>{lo}, {metrics[0]}<{hi})')
        return steps, "Excel"


# ══════════════════════════════════════════════════════
# MEASURES (uses real metrics + groups only)
# ══════════════════════════════════════════════════════

def get_measures(tool, metrics, groups, time_cols):
    ms = []
    m = metrics[0] if metrics else None
    g = groups[0] if groups else None
    m2 = metrics[1] if len(metrics) > 1 else None

    if tool == "Power BI":
        if m: ms.append((f"Avg {m}", f"Avg {m} =\nAVERAGE(Data[{m}])"))
        if m: ms.append((f"Median {m}", f"Median {m} =\nMEDIANX(Data, Data[{m}])"))
        if m and g: ms.append((f"Top {g} by {m}", f"Top {g} =\nCALCULATE(\n  MAX(Data[{g}]),\n  TOPN(1, VALUES(Data[{g}]),\n  CALCULATE(AVERAGE(Data[{m}])),DESC)\n)"))
        if m: ms.append(("% Above Average", f"Pct Above Avg =\nDIVIDE(\n  COUNTROWS(FILTER(Data,\n    Data[{m}] > CALCULATE(\n      AVERAGE(Data[{m}]),ALL(Data)))),\n  COUNTROWS(Data)\n)*100"))

    elif tool == "Python":
        if m: ms.append(("Summary Stats", f"df['{m}'].describe()\n# Key: mean vs median gap\nprint('Mean:', df['{m}'].mean().round(1))\nprint('Median:', df['{m}'].median().round(1))"))
        if m and g: ms.append(("Group Analysis", f"df.groupby('{g}')['{m}'].agg(\n  ['mean','median','count']\n).sort_values('mean', ascending=False)"))
        if m and m2: ms.append(("Correlation", f"df[['{m}','{m2}']].corr()\n# Scatter plot:\nimport matplotlib.pyplot as plt\nplt.scatter(df['{m}'], df['{m2}'])\nplt.show()"))

    elif tool == "SQL":
        if m and g:
            ms.append(("Performance by Group", f"SELECT\n  \"{g}\",\n  AVG(\"{m}\") as avg_{m.split('_')[0]},\n  PERCENTILE_CONT(0.5)\n    WITHIN GROUP (ORDER BY \"{m}\")\n    as median_{m.split('_')[0]},\n  COUNT(*) as total\nFROM your_table\nGROUP BY \"{g}\"\nORDER BY avg_{m.split('_')[0]} DESC;"))
        if m: ms.append(("Outlier Detection", f"SELECT * FROM your_table\nWHERE \"{m}\" > (\n  SELECT AVG(\"{m}\") + 2*STDDEV(\"{m}\")\n  FROM your_table\n);"))

    elif tool == "Tableau":
        if m: ms.append((f"Avg {m}", f"AVG([{m}])"))
        if m: ms.append((f"Median {m}", f"MEDIAN([{m}])"))
        if m and g: ms.append(("% of Total", f"SUM([{m}]) /\nTOTAL(SUM([{m}]))"))
        if m and time_cols: ms.append(("YoY Change", f"(SUM([{m}]) - LOOKUP(SUM([{m}]),-1))\n/ ABS(LOOKUP(SUM([{m}]),-1))"))

    else:  # Excel
        if m: ms.append(("Average", f"=AVERAGE({m}:{m})"))
        if m: ms.append(("Median", f"=MEDIAN({m}:{m})"))
        if m and g: ms.append(("AVERAGEIF", f"=AVERAGEIF(\n  {g}:{g},\"value\",\n  {m}:{m})"))
        if m: ms.append(("Above Average Count", f"=COUNTIF({m}:{m},\n  \">\"&AVERAGE({m}:{m}))"))

    return ms[:4]


# ══════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style="padding:4px 0 16px">
      <div style="font-size:22px;font-weight:800;letter-spacing:-0.5px">Data<span style="color:#6366f1">Sense</span></div>
      <div style="font-size:9px;font-family:'JetBrains Mono';color:#3a3a5a;letter-spacing:2px;margin-top:2px">DATASET ANALYZER</div>
    </div>
    <div style="height:1px;background:#1a1a30;margin-bottom:20px"></div>
    <div style="font-size:9px;font-family:'JetBrains Mono';color:#3a3a5a;text-transform:uppercase;letter-spacing:2px;margin-bottom:12px">Analytics Tool</div>
    """, unsafe_allow_html=True)
    tool = st.radio("Analytics Tool", ["Power BI", "Python", "SQL", "Tableau", "Excel"], label_visibility="collapsed")
    st.markdown("""
    <div style="height:1px;background:#1a1a30;margin:20px 0 16px"></div>
    <div style="font-size:9px;font-family:'JetBrains Mono';color:#3a3a5a;text-transform:uppercase;letter-spacing:2px;margin-bottom:8px">Upload Dataset</div>
    <div style="font-size:11px;color:#4a4a6a;font-family:'JetBrains Mono';margin-bottom:10px;line-height:1.7">CSV or Excel — up to 30,000 rows</div>
    """, unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload", type=["csv","xlsx","xls"], label_visibility="collapsed")
    if uploaded:
        st.markdown(f'<div style="margin-top:8px;padding:8px 12px;background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.2);border-radius:8px;font-size:10px;font-family:JetBrains Mono;color:#10b981">uploaded: {uploaded.name}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# MAIN AREA
# ══════════════════════════════════════════════════════

st.markdown("""
<div class="hero">
  <div class="badge">NO API KEY &nbsp;&nbsp;FREE &nbsp;&nbsp;ANY TOOL</div>
  <div style="font-size:44px;font-weight:800;letter-spacing:-2px;line-height:1;margin-bottom:10px">Data<span style="color:#6366f1">Sense</span></div>
  <div style="font-size:13px;color:#3a3a5a;font-family:'JetBrains Mono'">Instant deep analysis for any analytics tool — no setup required</div>
</div>
""", unsafe_allow_html=True)

if not uploaded:
    st.markdown("""
    <div style="display:flex;align-items:center;justify-content:center;height:50vh;flex-direction:column;gap:14px">
      <div style="font-size:13px;font-family:'JetBrains Mono';color:#3a3a5a;text-align:center;line-height:2">
        Upload your dataset from the sidebar to begin
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

try:
    df = load_data(uploaded.read(), uploaded.name)
    gc.collect()
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

# Smart column classification
metrics = get_real_metrics(df)
groups = get_groups(df)
time_cols = get_time_cols(df)
useless_cols = get_useless(df)
null_cols = [c for c in df.columns if df[c].isnull().any()]
miss_total = df.isnull().sum().sum()
miss_pct = round(miss_total / (df.shape[0]*df.shape[1]) * 100, 1) if df.shape[0]*df.shape[1] > 0 else 0
dupes = df.duplicated().sum()
score = qscore(df, metrics)
sc = "#10b981" if score>=80 else "#f59e0b" if score>=60 else "#ef4444"
ds_type = detect_dataset_type(df)

# ── KPIs ─────────────────────────────────────────────
c1,c2,c3,c4 = st.columns(4)
for col,l,v,s,a in [
    (c1,"Rows",f"{df.shape[0]:,}",f"{df.shape[1]} columns","#6366f1"),
    (c2,"Missing",f"{miss_pct}%",f"{miss_total:,} cells","#f59e0b" if miss_pct>5 else "#10b981"),
    (c3,"Duplicates",f"{dupes:,}",f"{dupes/len(df)*100:.1f}% of rows","#ef4444" if dupes>0 else "#10b981"),
    (c4,"Quality",f"{score}","/100",sc)
]:
    with col:
        st.markdown(f'<div class="kpi" style="--a:{a}"><div class="kpi-l">{l}</div><div class="kpi-v" style="color:{a}">{v}</div><div class="kpi-s">{s}</div></div>', unsafe_allow_html=True)

# ── DATA STORY ────────────────────────────────────────
type_map = {"operations":"OPERATIONS","financial":"FINANCIAL","market":"MARKET DATA","hr":"HR","healthcare":"HEALTHCARE","product":"PRODUCT","general":"GENERAL"}
st.markdown('<div class="sec">Data Story</div>', unsafe_allow_html=True)
parts = [f"<b style='color:#a5b4fc'>{df.shape[0]:,}-row {type_map.get(ds_type,'').lower()} dataset</b> with {df.shape[1]} columns"]
if time_cols:
    try:
        ds = pd.to_datetime(df[time_cols[0]], errors='coerce', format="mixed").dropna()
        span = (ds.max()-ds.min()).days
        if span > 0: parts.append(f"spanning <b style='color:#6366f1'>{span} days</b>")
    except: pass
if groups: parts.append(f"across <b style='color:#a78bfa'>{df[groups[0]].nunique()} {groups[0].replace('_',' ')} groups</b>")
if metrics: parts.append(f"key metrics: <b style='color:#00e5ff'>{', '.join(metrics[:3])}</b>")
if useless_cols: parts.append(f"<b style='color:#6b6b9a'>{len(useless_cols)} ID/useless columns</b> flagged for removal")
quality_txt = "excellent condition" if score>=85 else "moderate quality" if score>=65 else "quality issues"
parts.append(f"Data quality: <b style='color:{sc}'>{quality_txt}</b> ({score}/100)")
st.markdown(f'<div style="background:#0d0d1a;border:1px solid #1e1e35;border-left:3px solid #6366f1;border-radius:14px;padding:24px 28px"><span class="badge">{type_map.get(ds_type,"DATA")}</span><div style="font-size:16px;font-weight:600;color:#e2e2f0;line-height:1.9">{" — ".join(parts)}.</div></div>', unsafe_allow_html=True)

# ── PATTERN DETECTION ─────────────────────────────────
pts = detect_patterns(df, metrics, time_cols, groups)
gc.collect()
st.markdown('<div class="sec">Pattern Detection</div>', unsafe_allow_html=True)
if pts:
    for i in range(0, len(pts), 2):
        chunk = pts[i:i+2]
        g = st.columns(len(chunk))
        for j, p in enumerate(chunk):
            with g[j]:
                st.markdown(f'<div class="pc" style="--c:{p["c"]}"><div class="pt">{p["t"]}</div><div class="ps">{p["s"]}</div><div class="pb">{p["b"]}</div><div class="pa"><span style="color:{p["c"]}">ACTION: </span>{p["a"]}</div></div>', unsafe_allow_html=True)
else:
    st.markdown('<div style="background:#0d0d1a;border:1px solid #1e1e35;border-radius:12px;padding:20px;color:#6b6b9a;font-family:JetBrains Mono;font-size:13px">No significant patterns detected.</div>', unsafe_allow_html=True)

# ── COLUMN PROFILE ────────────────────────────────────
st.markdown('<div class="sec">Column Profile</div>', unsafe_allow_html=True)
for i in range(0, len(df.columns), 4):
    chunk = list(df.columns)[i:i+4]
    g = st.columns(4)
    for j, cn in enumerate(chunk):
        s = df[cn]
        filled = s.dropna()
        pct = round(len(filled)/len(df)*100) if len(df) else 0
        uniq = filled.nunique()
        role = classify_column(cn, s)
        c_bar = "#10b981" if pct>90 else "#f59e0b" if pct>70 else "#ef4444"
        extra = ""
        if role == "metric":
            try:
                n = pd.to_numeric(filled, errors='coerce').dropna()
                extra = f"avg:{n.mean():.1f} | med:{n.median():.1f}"
            except: pass
        elif role == "id":
            extra = "not useful for analysis"
        elif role == "useless":
            extra = "single value — remove"
        with g[j]:
            st.markdown(f'<div class="card"><div class="cn" title="{cn}">{cn[:18]}{"..." if len(cn)>18 else ""}</div><div style="margin:4px 0 8px">{ttag(role)}</div><div class="bw"><div class="bf" style="width:{pct}%;background:{c_bar}"></div></div><div class="cm">{pct}% filled | {uniq} unique{(" | "+extra) if extra else ""}</div></div>', unsafe_allow_html=True)

# ── CRITICAL ISSUES ───────────────────────────────────
st.markdown('<div class="sec">Critical Issues</div>', unsafe_allow_html=True)
iss = []
for c in null_cols:
    p = df[c].isnull().sum()/len(df)*100
    advice = missing_advice(c, df[c], df)
    color = "#ef4444" if p > 10 else "#f59e0b"
    iss.append((color, f"<b>{c}</b> — {p:.1f}% missing. {advice}"))
for c in metrics[:4]:
    try:
        lo, hi = smart_bounds(c, df[c])
        n = int(((df[c] < lo) | (df[c] > hi)).sum())
        if n/len(df) > 0.05:
            iss.append(("#ef4444", f"<b>{c}</b> — {n:,} outliers ({n/len(df)*100:.1f}%). Valid range: {lo}–{hi}."))
    except: pass
if dupes > 0: iss.append(("#ef4444", f"<b>{dupes:,} duplicate rows</b> — remove before aggregation."))
if useless_cols: iss.append(("#6b6b9a", f"<b>Low-value columns:</b> {', '.join(useless_cols[:5])} — consider removing."))
if not iss: iss.append(("#10b981", "No critical issues found. Dataset is clean and ready."))
st.markdown('<div style="background:#0d0d1a;border:1px solid #1e1e35;border-radius:12px;padding:16px 20px">' + "".join([f'<div class="ii"><div class="idot" style="background:{c}"></div><div>{t}</div></div>' for c,t in iss[:7]]) + '</div>', unsafe_allow_html=True)

# ── CLEANING STEPS ────────────────────────────────────
steps, lang = cleaning_code(df, tool, metrics, null_cols)
st.markdown(f'<div class="sec">Cleaning Steps — {lang}</div>', unsafe_allow_html=True)
for s in steps:
    st.markdown(f'<div class="cb">{s}</div>', unsafe_allow_html=True)

# ── MEASURES ─────────────────────────────────────────
ms = get_measures(tool, metrics, groups, time_cols)
tlabels = {"Power BI":"DAX Measures","Python":"Python Snippets","SQL":"SQL Queries","Tableau":"Calculated Fields","Excel":"Excel Formulas"}
st.markdown(f'<div class="sec">{tlabels.get(tool,"Formulas")}</div>', unsafe_allow_html=True)
g1, g2 = st.columns(2)
for i,(title,code) in enumerate(ms):
    with (g1 if i%2==0 else g2):
        st.markdown(f'<div class="ct">{title}</div><div class="cb">{code}</div>', unsafe_allow_html=True)

# ── QUESTIONS ─────────────────────────────────────────
qs = generate_questions(ds_type, metrics, groups, time_cols)
st.markdown('<div class="sec">5 Questions Worth Answering</div>', unsafe_allow_html=True)
st.markdown('<div style="background:#0d0d1a;border:1px solid #1e1e35;border-radius:12px;padding:16px 20px">' + "".join([f'<div class="qi"><div class="qn">0{i+1}</div><div><div class="qt">{q}</div><div class="qw">{w}</div></div></div>' for i,(q,w,_) in enumerate(qs)]) + '</div>', unsafe_allow_html=True)

# ── GROUP COMPARISON ──────────────────────────────────
if groups and metrics and df[groups[0]].nunique() <= 50:
    g_col, m_col = groups[0], metrics[0]
    st.markdown(f'<div class="sec">Group Comparison — {g_col} by {m_col}</div>', unsafe_allow_html=True)
    grp = df.groupby(g_col)[m_col].agg(['mean','median','count']).round(1).sort_values('mean')
    grp.columns = ['Mean','Median','Count']
    grp = grp.reset_index()
    total_g = len(grp)
    rows_html = ""
    for idx_r, row in grp.iterrows():
        if idx_r==0: rank = '<span style="color:#10b981;font-weight:700;font-family:JetBrains Mono;font-size:11px">BEST</span>'
        elif idx_r==total_g-1: rank = '<span style="color:#ef4444;font-weight:700;font-family:JetBrains Mono;font-size:11px">WORST</span>'
        else: rank = f'<span style="color:#6b6b9a;font-size:11px;font-family:JetBrains Mono">{idx_r+1}</span>'
        bw = int(row['Mean']/grp['Mean'].max()*120) if grp['Mean'].max()>0 else 0
        bc = "#10b981" if idx_r<total_g*0.33 else "#f59e0b" if idx_r<total_g*0.66 else "#ef4444"
        rows_html += f'<tr><td style="padding:8px 12px">{rank}</td><td style="padding:8px 12px;color:#e2e2f0;font-weight:600;font-family:JetBrains Mono;font-size:12px">{row[g_col]}</td><td style="padding:8px 12px"><div style="display:flex;align-items:center;gap:8px"><div style="width:{bw}px;height:5px;background:{bc};border-radius:3px"></div><span style="color:#e2e2f0;font-family:JetBrains Mono;font-size:12px">{row["Mean"]:.1f}</span></div></td><td style="padding:8px 12px;color:#6b6b9a;font-family:JetBrains Mono;font-size:12px">{row["Median"]:.1f}</td><td style="padding:8px 12px;color:#6b6b9a;font-family:JetBrains Mono;font-size:12px">{int(row["Count"]):,}</td></tr>'
    st.markdown(f'<table style="width:100%;border-collapse:collapse;background:#0d0d1a;border:1px solid #1e1e35;border-radius:12px;overflow:hidden"><thead><tr style="border-bottom:1px solid #1e1e35"><th style="padding:8px 12px;color:#6b6b9a;text-align:left;font-size:10px;font-family:JetBrains Mono;letter-spacing:1px;text-transform:uppercase">#</th><th style="padding:8px 12px;color:#6b6b9a;text-align:left;font-size:10px;font-family:JetBrains Mono;letter-spacing:1px;text-transform:uppercase">{g_col}</th><th style="padding:8px 12px;color:#6b6b9a;text-align:left;font-size:10px;font-family:JetBrains Mono;letter-spacing:1px;text-transform:uppercase">Mean</th><th style="padding:8px 12px;color:#6b6b9a;text-align:left;font-size:10px;font-family:JetBrains Mono;letter-spacing:1px;text-transform:uppercase">Median</th><th style="padding:8px 12px;color:#6b6b9a;text-align:left;font-size:10px;font-family:JetBrains Mono;letter-spacing:1px;text-transform:uppercase">Count</th></tr></thead><tbody>{rows_html}</tbody></table>', unsafe_allow_html=True)

# ── FINAL VERDICT ─────────────────────────────────────
st.markdown('<div class="sec">Final Verdict</div>', unsafe_allow_html=True)
verdict = "READY" if score>=80 else "NEEDS WORK" if score>=60 else "CRITICAL"
vmsg = "Clean and ready for analysis." if score>=80 else "Fix issues above before building dashboards." if score>=60 else "Critical issues — resolve before proceeding."
tvis = {"Power BI":["KPI Card","Line Chart","Bar Chart","Scatter Plot","Matrix"],"Python":["plt.plot()","sns.barplot()","df.corr() heatmap","px.histogram()","sns.scatterplot()"],"SQL":["GROUP BY","Window Functions","CTEs","Subqueries","JOINs"],"Tableau":["KPI Summary","Trend Line","Bar Chart","Scatter Plot","Heat Map"],"Excel":["PivotTable","Line Chart","Bar Chart","Scatter Plot","Conditional Format"]}
vis = tvis.get(tool, ["KPI Card","Line Chart","Bar Chart","Scatter Plot","Matrix"])
c1, c2 = st.columns([1,2])
with c1:
    st.markdown(f'<div style="background:#0d0d1a;border:1px solid #1e1e35;border-radius:14px;padding:24px;text-align:center"><div style="font-size:64px;font-weight:800;color:{sc}">{score}</div><div style="font-size:11px;font-family:JetBrains Mono;color:#6b6b9a">Quality Score</div><div style="font-size:18px;font-weight:800;color:{sc};margin:8px 0">{verdict}</div><div style="font-size:12px;color:#6b6b9a;font-family:JetBrains Mono">{vmsg}</div></div>', unsafe_allow_html=True)
with c2:
    rh = "".join([f'<div style="padding:8px 0;border-bottom:1px solid #1e1e35;font-family:JetBrains Mono;font-size:13px;color:#c4c4e0"><span style="color:{sc};margin-right:10px">0{i+1}</span>{v}</div>' for i,v in enumerate(vis)])
    st.markdown(f'<div style="background:#0d0d1a;border:1px solid #1e1e35;border-radius:14px;padding:20px 24px"><div class="sec" style="margin-top:0">Recommended {tool} Visuals</div>{rh}</div>', unsafe_allow_html=True)

gc.collect()
st.markdown("<br>", unsafe_allow_html=True)
