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
#MainMenu,footer,header{visibility:hidden;}
[data-testid="stSidebar"]{background:#0d0d1a;border-right:1px solid #1e1e35;}
.stRadio>div{gap:0!important;background:transparent!important;border:none!important;padding:0!important;}
.stRadio>div>div{background:transparent!important;}
div[data-testid="stRadio"]>label{display:none!important;}
div[data-testid="stRadio"]>div{background:transparent!important;border:none!important;padding:0!important;gap:8px!important;}
.stRadio label{background:transparent!important;border:1px solid #1e1e35!important;border-radius:8px!important;padding:7px 16px!important;font-family:'JetBrains Mono'!important;font-size:11px!important;color:#6b6b9a!important;transition:all 0.15s!important;cursor:pointer!important;}
.stRadio label:hover{border-color:#6366f1!important;color:#a5b4fc!important;}
[data-testid="stFileUploader"]{background:#0a0a18!important;border:1.5px dashed #1e1e35!important;border-radius:16px!important;padding:8px 16px!important;}
[data-testid="stFileUploader"]:hover{border-color:#6366f1!important;}
[data-testid="stFileUploaderDropzone"]{background:transparent!important;border:none!important;}
[data-testid="stFileUploaderDropzone"] *{color:#4a4a6a!important;}
[data-testid="stFileUploaderDropzone"] button{background:rgba(99,102,241,0.1)!important;border:1px solid #6366f1!important;color:#a5b4fc!important;border-radius:8px!important;}
.hero{background:linear-gradient(135deg,#0a0a18 0%,#0f0f22 50%,#0a0a18 100%);border:1px solid #1a1a30;border-radius:24px;padding:40px 44px;margin-bottom:32px;position:relative;overflow:hidden;}
.hero::after{content:'';position:absolute;top:-80px;right:-80px;width:300px;height:300px;background:radial-gradient(circle,rgba(99,102,241,0.08) 0%,transparent 70%);border-radius:50%;pointer-events:none;}
.badge{display:inline-flex;align-items:center;gap:6px;font-size:10px;font-family:'JetBrains Mono';font-weight:700;padding:5px 14px;border-radius:20px;letter-spacing:1.5px;background:rgba(16,185,129,0.08);color:#10b981;border:1px solid rgba(16,185,129,0.2);margin-bottom:18px;}
.badge::before{content:'';width:5px;height:5px;border-radius:50%;background:#10b981;animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.3;}}
.kpi{background:#0a0a18;border:1px solid #1a1a30;border-radius:16px;padding:18px 20px;border-top:2px solid var(--a);position:relative;overflow:hidden;}
.kpi::after{content:'';position:absolute;bottom:-20px;right:-20px;width:80px;height:80px;background:radial-gradient(circle,var(--a) 0%,transparent 70%);opacity:0.06;border-radius:50%;}
.kpi-l{font-size:9px;font-family:'JetBrains Mono';color:#4a4a6a;text-transform:uppercase;letter-spacing:2px;margin-bottom:8px;}
.kpi-v{font-size:30px;font-weight:800;line-height:1;letter-spacing:-1px;}
.kpi-s{font-size:10px;color:#4a4a6a;margin-top:5px;font-family:'JetBrains Mono';}
.sec{font-size:9px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#3a3a5a;padding:6px 0 12px;border-bottom:1px solid #0f0f20;margin:28px 0 16px;display:flex;align-items:center;gap:8px;}
.sec::before{content:'';width:3px;height:12px;background:#6366f1;border-radius:2px;display:inline-block;}
.card{background:#0a0a18;border:1px solid #1a1a30;border-radius:14px;padding:16px 18px;}
.tag{font-size:8px;font-family:'JetBrains Mono';padding:3px 9px;border-radius:20px;font-weight:700;letter-spacing:0.5px;}
.bw{background:#07070f;border-radius:3px;height:2px;margin:8px 0 6px;overflow:hidden;}
.bf{height:100%;border-radius:3px;}
.cm{font-size:10px;color:#4a4a6a;font-family:'JetBrains Mono';}
.cn{font-family:'JetBrains Mono';font-size:11px;font-weight:700;color:#8b8bcc;margin-bottom:8px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.pc{background:#0a0a18;border:1px solid #1a1a30;border-radius:16px;padding:20px 22px;border-left:3px solid var(--c);}
.pt{font-size:9px;font-family:'JetBrains Mono';text-transform:uppercase;letter-spacing:1.5px;color:var(--c);margin-bottom:8px;opacity:0.9;}
.ps{font-size:26px;font-weight:800;color:var(--c);margin:4px 0 10px;letter-spacing:-1px;}
.pb{font-size:13px;color:#a0a0c0;line-height:1.7;}
.pa{margin-top:12px;padding-top:10px;border-top:1px solid #0f0f20;font-size:10px;font-family:'JetBrains Mono';color:#4a4a6a;line-height:1.6;}
.cb{background:#050510;border:1px solid #1a1a30;border-radius:12px;padding:18px 22px;font-family:'JetBrains Mono';font-size:11px;color:#8b8bcc;line-height:2;margin-bottom:14px;white-space:pre-wrap;}
.ct{font-size:9px;color:#3a3a5a;text-transform:uppercase;letter-spacing:2px;margin-bottom:8px;font-family:'JetBrains Mono';}
.qi{display:flex;gap:14px;padding:14px 0;border-bottom:1px solid #0a0a18;align-items:flex-start;}
.qn{font-size:10px;font-family:'JetBrains Mono';color:#6366f1;font-weight:700;min-width:20px;margin-top:3px;}
.qt{font-size:13px;color:#e2e2f0;font-weight:700;line-height:1.5;margin-bottom:3px;}
.qw{font-size:11px;color:#4a4a6a;font-family:'JetBrains Mono';line-height:1.5;}
.ii{display:flex;align-items:flex-start;gap:12px;padding:12px 0;border-bottom:1px solid #0a0a18;font-size:13px;color:#a0a0c0;line-height:1.6;}
.idot{width:6px;height:6px;border-radius:50%;margin-top:6px;flex-shrink:0;}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# SMART COLUMN CLASSIFIER
# ══════════════════════════════════════════════════════

def classify_column(col_name, series):
    name = col_name.lower().replace('_',' ').replace('-',' ').strip()
    filled = series.dropna()
    if len(filled) == 0: return "empty"
    if filled.nunique() <= 1: return "useless"

    # Location — highest priority before numeric check
    if any(k in name for k in ['lat','lon','lng','latitude','longitude','coordinate','geo']):
        return "location"

    # ID — name pattern + high cardinality
    # Covers: user_id, order_id, store_id (low card = group), award_id (low card = group_num)
    id_endings = ['_id',' id','_key',' key','_uuid','_hash','_ref']
    is_id_name = any(name.endswith(e.strip()) for e in id_endings)
    cardinality_ratio = filled.nunique() / len(filled)
    if is_id_name and cardinality_ratio > 0.5:
        return "id"

    # Time — only strings with date patterns, never pure numbers
    sample = filled.astype(str).str.strip()
    has_date = sample.str.match(r'^\d{4}[-/]\d{2}|^\d{2}[-/]\d{2}[-/]\d{4}').any()
    if has_date:
        try:
            pd.to_datetime(sample.iloc[:30], format="mixed", dayfirst=False)
            return "time"
        except: pass

    # Numeric analysis
    try:
        nums = pd.to_numeric(filled, errors='coerce').dropna()
        numeric_ratio = len(nums) / max(len(filled), 1)
        if numeric_ratio > 0.85:
            uniq = nums.nunique()
            n = len(nums)

            # Hour of day — 0 to 23
            if 'hour' in name and nums.max() <= 23 and nums.min() >= 0:
                return "time_num"
            # Month — 1 to 12
            if 'month' in name and nums.max() <= 12 and nums.min() >= 1:
                return "time_num"
            # Year — few unique values
            if 'year' in name and uniq <= 20:
                return "time_num"
            # Day of week — 1 to 7
            if 'day' in name and nums.max() <= 7 and nums.min() >= 1:
                return "time_num"

            # Binary flag
            if uniq == 2 and set(nums.unique()).issubset({0, 1}):
                return "flag"

            # Group-like numeric: very few unique relative to count
            # e.g. delivery_fee_cents with 5 values, missing_skus_count with 5
            if uniq <= 25 and uniq / n < 0.003:
                return "group_num"

            # True metric
            return "metric"
    except: pass

    # Categorical group
    if filled.nunique() <= 100:
        return "group"

    return "text"


def safe_num(series):
    """Safely convert series to numeric"""
    try:
        return pd.to_numeric(series, errors='coerce').dropna()
    except:
        return pd.Series([], dtype=float)

def safe_median(series):
    """Return median or None"""
    try:
        m = pd.to_numeric(series, errors='coerce').median()
        return None if pd.isna(m) else float(m)
    except:
        return None

def top_value(series):
    """Return most frequent value as string"""
    try:
        top = series.dropna().mode()
        return f'"{top.iloc[0]}"' if len(top) > 0 else "most frequent value"
    except:
        return "most frequent value"

def get_real_metrics(df):
    return [c for c in df.columns if classify_column(c, df[c]) == "metric"]

def get_groups(df):
    return [c for c in df.columns if classify_column(c, df[c]) in ("group","group_num","time_num")]

def get_time_cols(df):
    return [c for c in df.columns if classify_column(c, df[c]) in ("time","time_num")]

def get_useless(df):
    return [c for c in df.columns if classify_column(c, df[c]) in ("useless","id")]


# ══════════════════════════════════════════════════════
# SMART BOUNDS — domain-aware, never negative for physical values
# ══════════════════════════════════════════════════════

NON_NEGATIVE_KEYWORDS = [
    'time','second','minute','hour','duration',
    'price','cost','amount','cent','fee','budget','revenue','sales','profit','spend','income',
    'distance','count','total','item','sku','quantity','size','area','weight','age','score','rate'
]

def smart_bounds(col_name, series):
    nums = safe_num(series)
    if len(nums) < 4:
        return 0, float(nums.max()) if len(nums) > 0 else 0
    q1, q3 = nums.quantile(0.25), nums.quantile(0.75)
    iqr = q3 - q1
    lo = q1 - 1.5 * iqr
    hi = q3 + 1.5 * iqr
    name = col_name.lower()
    if any(k in name for k in NON_NEGATIVE_KEYWORDS):
        lo = max(0.0, lo)
    return round(lo, 1), round(hi, 1)


# ══════════════════════════════════════════════════════
# SMART MISSING VALUE ADVICE
# ══════════════════════════════════════════════════════

def missing_advice(col_name, series, df):
    name = col_name.lower()
    miss_pct = series.isnull().sum() / len(df) * 100
    med = safe_median(series)

    # Reward/cashback — absence means zero
    if any(k in name for k in ['cashback','bonus','reward','promo','incentive']):
        return "Absence likely means no reward. Safe to replace with 0."

    # Discount — could be zero or missing data
    if any(k in name for k in ['discount','coupon']):
        return f"Replace with 0 if no discount was applied, or median ({med:.0f}) if it's a data gap." if med else "Replace with 0 if no discount was applied."

    # Location — never replace with 0
    if any(k in name for k in ['lat','lon','lng','latitude','longitude']):
        return f"Missing location ({miss_pct:.1f}%). Exclude these rows from geographic analysis — do NOT replace with 0."

    # Numeric time/duration
    if any(k in name for k in ['time','second','minute','duration']) and med is not None:
        return f"Replace with median ({med:.1f}) — more robust than mean for skewed time data."

    # Price/financial
    if any(k in name for k in ['price','amount','cent','fee','cost','budget','revenue']) and med is not None:
        return f"Replace with 0 if absence = no charge, or median ({med:,.0f}) if it's a recording gap."

    # Text/categorical — use mode
    if med is None:
        tv = top_value(series)
        return f"Categorical column — replace with most frequent value ({tv}) or remove rows."

    # Numeric default
    return f"Replace with median ({med:,.1f}) or remove rows if this is a critical field."


# ══════════════════════════════════════════════════════
# DATA LOADER
# ══════════════════════════════════════════════════════

@st.cache_data(max_entries=3)
def load_data(file_bytes, fname):
    import io
    try:
        if fname.lower().endswith('.csv'):
            df = pd.read_csv(io.BytesIO(file_bytes), on_bad_lines='skip', nrows=30000)
        else:
            df = pd.read_excel(io.BytesIO(file_bytes), nrows=30000)
        return df.dropna(how='all')
    except Exception as e:
        raise e


# ══════════════════════════════════════════════════════
# COLUMN TAG STYLES
# ══════════════════════════════════════════════════════

TS = {
    "metric":    ("#00e5ff","rgba(0,229,255,0.08)","rgba(0,229,255,0.2)","METRIC"),
    "time":      ("#10b981","rgba(16,185,129,0.08)","rgba(16,185,129,0.2)","TIME"),
    "time_num":  ("#10b981","rgba(16,185,129,0.08)","rgba(16,185,129,0.2)","TIME"),
    "group":     ("#a78bfa","rgba(167,139,250,0.08)","rgba(167,139,250,0.2)","GROUP"),
    "group_num": ("#a78bfa","rgba(167,139,250,0.08)","rgba(167,139,250,0.2)","GROUP"),
    "id":        ("#6b6b9a","rgba(107,107,154,0.08)","rgba(107,107,154,0.2)","ID"),
    "location":  ("#f59e0b","rgba(245,158,11,0.08)","rgba(245,158,11,0.2)","GEO"),
    "flag":      ("#ec4899","rgba(236,72,153,0.08)","rgba(236,72,153,0.2)","FLAG"),
    "useless":   ("#ef4444","rgba(239,68,68,0.08)","rgba(239,68,68,0.2)","USELESS"),
    "text":      ("#f59e0b","rgba(245,158,11,0.08)","rgba(245,158,11,0.2)","TEXT"),
    "empty":     ("#6b6b9a","rgba(107,107,154,0.08)","rgba(107,107,154,0.2)","EMPTY"),
}

def ttag(t):
    c,bg,bd,l = TS.get(t, ("#6b6b9a","rgba(107,107,154,0.08)","rgba(107,107,154,0.2)","?"))
    return f'<span class="tag" style="color:{c};background:{bg};border:1px solid {bd}">{l}</span>'


# ══════════════════════════════════════════════════════
# QUALITY SCORE
# ══════════════════════════════════════════════════════

def quality_score(df, metrics):
    score = 100
    total = df.shape[0] * df.shape[1]
    if total == 0: return 0
    # Missing penalty
    mp = df.isnull().sum().sum() / total * 100
    score -= min(30, mp * 1.5)
    # Outlier penalty on real metrics only
    for col in metrics[:4]:
        try:
            lo, hi = smart_bounds(col, df[col])
            ot = ((df[col] < lo) | (df[col] > hi)).sum()
            score -= min(5, (ot / len(df)) * 3)
        except: pass
    # Duplicate penalty
    score -= min(15, df.duplicated().sum() / len(df) * 100 * 2)
    return max(0, round(score))


# ══════════════════════════════════════════════════════
# DATASET TYPE DETECTOR
# ══════════════════════════════════════════════════════

def detect_type(df):
    cs = " ".join(df.columns.str.lower())
    if any(x in cs for x in ['delivery','order','store','logistics','picking','shipment']): return "operations"
    if any(x in cs for x in ['revenue','sales','profit','invoice','payment','transaction']): return "financial"
    if any(x in cs for x in ['open','close','high','low','volume','stock','ticker']): return "market"
    if any(x in cs for x in ['employee','salary','department','hire','headcount','staff']): return "hr"
    if any(x in cs for x in ['patient','hospital','medical','diagnosis','treatment']): return "healthcare"
    if any(x in cs for x in ['customer','user','session','click','retention','churn']): return "product"
    if any(x in cs for x in ['project','budget_project','sector','region']): return "projects"
    return "general"


# ══════════════════════════════════════════════════════
# PATTERN DETECTION
# ══════════════════════════════════════════════════════

def detect_patterns(df, metrics, time_cols, groups):
    pts = []

    # 1. Trend — on first real metric over first time column
    if time_cols and metrics:
        try:
            col = metrics[0]
            tcol = time_cols[0]
            dt = df[[tcol, col]].copy()
            dt['_d'] = pd.to_datetime(dt[tcol], errors='coerce', format="mixed")
            dt = dt.dropna(subset=['_d', col]).sort_values('_d')
            n = len(dt)
            if n > 30:
                first = dt[col].iloc[:n//3].mean()
                last  = dt[col].iloc[-n//3:].mean()
                ch = ((last - first) / abs(first) * 100) if first != 0 else 0
                if abs(ch) > 10:
                    c = "#10b981" if ch > 0 else "#ef4444"
                    pts.append({"t":f"{'Up' if ch>0 else 'Down'}ward Trend","c":c,
                        "s":f"{'+' if ch>0 else ''}{ch:.1f}%",
                        "b":f"<b style='color:{c}'>{col}</b> {'grew' if ch>0 else 'declined'} {abs(ch):.1f}% from start to end of the dataset.",
                        "a":f"Build a Line Chart with {tcol} on X-axis and {col} on Y-axis."})
        except: pass

    # 2. Outliers — worst metric by outlier count
    if metrics:
        worst_col, worst_n, worst_p = "", 0, 0
        for col in metrics[:5]:
            try:
                lo, hi = smart_bounds(col, df[col])
                n = int(((df[col] < lo) | (df[col] > hi)).sum())
                p = n / len(df) * 100
                if n > worst_n: worst_col, worst_n, worst_p = col, n, p
            except: pass
        if worst_n > 0 and worst_p > 5:
            lo, hi = smart_bounds(worst_col, df[worst_col])
            pts.append({"t":"Outlier Cluster","c":"#ef4444",
                "s":f"{worst_n:,} rows",
                "b":f"<b style='color:#ef4444'>{worst_col}</b> has {worst_n:,} outliers ({worst_p:.1f}%). Valid range is {lo:,}–{hi:,}.",
                "a":f"Filter: keep only rows where {worst_col} is between {lo:,} and {hi:,}."})

    # 3. Multicollinearity — between real metrics only
    if len(metrics) >= 2:
        try:
            sub = df[metrics[:6]].apply(pd.to_numeric, errors='coerce')
            cr = sub.corr().abs()
            np.fill_diagonal(cr.values, 0)
            mx = cr.max().max()
            if mx > 0.85:
                idx = cr.stack().idxmax()
                pts.append({"t":"Multicollinearity Warning","c":"#f59e0b",
                    "s":f"r = {mx:.2f}",
                    "b":f"<b style='color:#f59e0b'>{idx[0]}</b> and <b style='color:#f59e0b'>{idx[1]}</b> are {mx*100:.0f}% correlated. Using both in the same calculation will double-count the same signal.",
                    "a":"Keep one as your primary metric. Create the other as a derived measure only when needed."})
        except: pass

    # 4. Skewness — worst metric
    if metrics:
        sk_list = []
        for col in metrics[:5]:
            try:
                s = abs(float(df[col].dropna().skew()))
                if s > 1.5: sk_list.append((col, s))
            except: pass
        if sk_list:
            col, s = max(sk_list, key=lambda x: x[1])
            med = safe_median(df[col])
            mean_val = safe_num(df[col]).mean()
            gap = abs(mean_val - med) / abs(med) * 100 if med and med != 0 else 0
            pts.append({"t":"Skewed Distribution","c":"#06b6d4",
                "s":f"skew: {s:.1f}",
                "b":f"<b style='color:#06b6d4'>{col}</b> is heavily skewed. Mean ({mean_val:,.0f}) vs Median ({med:,.0f}) — a {gap:.0f}% gap. The mean is misleading here.",
                "a":f"Use Median instead of Average for {col} in all KPI cards."})

    # 5. Low-value columns
    useless = get_useless(df)
    if useless:
        pts.append({"t":"Low-Value Columns","c":"#6b6b9a",
            "s":f"{len(useless)} cols",
            "b":f"<b style='color:#6b6b9a'>{', '.join(useless[:5])}</b> — these are IDs or single-value columns. They add zero analytical value to any dashboard.",
            "a":"Remove these columns before building your model or dashboard."})

    return pts[:4]


# ══════════════════════════════════════════════════════
# QUESTIONS — always 5, always with real column names
# ══════════════════════════════════════════════════════

def generate_questions(ds_type, metrics, groups, time_cols):
    # Safe fallbacks — never "key metric"
    m0 = metrics[0] if metrics else None
    m1 = metrics[1] if len(metrics) > 1 else (metrics[0] if metrics else None)
    g0 = groups[0] if groups else None
    t0 = time_cols[0] if time_cols else None

    # If no metrics found at all, skip analysis questions
    if not m0:
        return [
            ("No numeric metrics detected", "The dataset may be entirely categorical. Try cleaning and re-uploading.", "Info"),
            ("Check column types", "Make sure numeric columns are not stored as text strings.", "Info"),
            ("Consider adding a numeric column", "Metrics like count, amount, or score enable quantitative analysis.", "Info"),
            ("Review data format", "Dates should follow YYYY-MM-DD format for best detection.", "Info"),
            ("Re-upload after cleaning", "Fix formatting issues and re-upload to get full analysis.", "Info"),
        ]

    type_qs = {
        "operations": [
            (f"What causes delays in {m0}?",
             f"Compare {m0} across {g0 or 'segments'} and time periods — find the bottleneck.", "Operations"),
            (f"Which {g0 or 'group'} underperforms?",
             f"Rank all {g0 or 'groups'} by average {m0} — investigate the bottom 20%.", "Performance"),
            (f"When does {m0} peak?",
             f"Group by hour/day and plot {m0} — identify when volume or delay is highest.", "Time"),
            (f"Is there a {g0 or 'segment'} with consistently high {m0}?",
             f"Box plot {m0} per {g0 or 'group'} — look for consistently high or low performers.", "Segmentation"),
            (f"Does {m0} drive {m1}?",
             f"Scatter plot {m0} vs {m1} — a strong correlation means one causes the other.", "Correlation"),
        ],
        "financial": [
            (f"What drives {m0} growth?",
             f"Plot {m0} over {t0 or 'time'} and correlate with {g0 or 'category'}.", "Revenue"),
            (f"Where is {m0} lost?",
             f"Compare {m0} across {g0 or 'segments'} — find the lowest performers.", "Profitability"),
            (f"Which {g0 or 'segment'} has the highest {m0}?",
             f"Group by {g0 or 'category'}, rank by {m0} highest to lowest.", "Segmentation"),
            (f"Is {m0} trending up or down?",
             f"Plot {m0} over {t0 or 'time'} — add a trend line to confirm direction.", "Trend"),
            (f"Does {m0} correlate with {m1}?",
             f"Scatter {m0} vs {m1} — find the relationship strength.", "Correlation"),
        ],
        "projects": [
            (f"Which sector has the highest {m0}?",
             f"Group by {g0 or 'sector'}, rank by total {m0} — find the biggest spender.", "Segmentation"),
            (f"What is the {m0} distribution by region?",
             f"Compare {m0} across regions — identify geographic concentration.", "Geography"),
            (f"Are there outlier projects in {m0}?",
             f"Box plot {m0} — identify abnormally large or small projects.", "Quality"),
            (f"What is the completion rate by {g0 or 'type'}?",
             f"Count completed vs ongoing by {g0 or 'category'} — find delays.", "Status"),
            (f"Does {m0} correlate with {m1}?",
             f"Scatter {m0} vs {m1} — check if bigger budgets mean more projects.", "Correlation"),
        ],
        "hr": [
            (f"What predicts {m0}?",
             f"Correlate {m0} with {g0 or 'department'} and tenure.", "Retention"),
            (f"Is there equity in {m0} across {g0 or 'groups'}?",
             f"Compare {m0} distribution across {g0 or 'departments'}.", "Equity"),
            (f"Which {g0 or 'department'} has the highest {m0}?",
             f"Rank {g0 or 'departments'} by avg {m0}.", "Segmentation"),
            (f"How has {m0} changed over time?",
             f"Plot {m0} by {t0 or 'period'}.", "Trend"),
            (f"Does {m0} affect {m1}?",
             f"Scatter {m0} vs {m1} — look for a pattern.", "Correlation"),
        ],
        "product": [
            ("Where do users drop off?",
             "Analyze conversion rates across funnel stages.", "Funnel"),
            (f"Which {g0 or 'segment'} has the best engagement?",
             f"Rank {g0 or 'segments'} by avg {m0}.", "Segmentation"),
            (f"How does {m0} change over time?",
             f"Plot {m0} by {t0 or 'date'}.", "Trend"),
            (f"Does {m0} drive {m1}?",
             f"Scatter {m0} vs {m1} — look for correlation.", "Correlation"),
            (f"What is the {m0} distribution?",
             f"Histogram of {m0} — check for skewness.", "Distribution"),
        ],
    }

    default = [
        (f"What are the trends in {m0}?",
         f"Plot {m0} over {t0 or 'time'} — identify peaks, drops, and patterns.", "Trend"),
        (f"Which {g0 or 'segment'} performs best in {m0}?",
         f"Group by {g0 or 'category'}, rank by avg {m0} — identify top and bottom.", "Segmentation"),
        (f"Are there outliers in {m0}?",
         f"Box plot {m0} — flag values that fall outside the normal range.", "Quality"),
        (f"Does {m0} correlate with {m1}?",
         f"Scatter {m0} vs {m1} — look for patterns or clusters.", "Correlation"),
        (f"What is the distribution of {m0}?",
         f"Histogram of {m0} — check if mean equals median. If not, use median.", "Distribution"),
    ]

    return type_qs.get(ds_type, default)[:5]


# ══════════════════════════════════════════════════════
# CLEANING CODE
# ══════════════════════════════════════════════════════

def cleaning_code(df, tool, metrics, null_cols):
    dupes = df.duplicated().sum()
    steps = []

    # Pick best null column to show — prefer metric, then any
    null_metric_cols = [c for c in null_cols if classify_column(c, df[c]) == "metric"]
    null_col = null_metric_cols[0] if null_metric_cols else (null_cols[0] if null_cols else None)

    # Pick first metric for outlier example
    m = metrics[0] if metrics else None
    lo, hi = (smart_bounds(m, df[m]) if m else (0, 0))

    adv = missing_advice(null_col, df[null_col], df) if null_col else None
    fill_val_py = "0" if null_col and any(k in null_col.lower() for k in ['cashback','bonus','reward','promo','discount']) else (f'df["{null_col}"].median()' if null_col else "0")

    if tool == "Power BI":
        if dupes > 0:
            steps.append("// Step 1: Remove duplicates\n= Table.Distinct(Source)")
        if null_col and adv:
            steps.append(f'// Step 2: {adv}\n= Table.ReplaceValue(Source, null, 0,\n  Replacer.ReplaceValue, {{"{null_col}"}})')
        if m:
            steps.append(f'// Step 3: Remove outliers in {m}\n= Table.SelectRows(Source,\n  each [{m}] >= {lo}\n  and [{m}] <= {hi})')
        steps.append('// Step 4: Set correct column types\n= Table.TransformColumnTypes(Source,\n  {{"your_date_col", type date},\n   {"your_id_col", type text}})')
        return steps, "Power Query (M)"

    elif tool == "Python":
        if dupes > 0:
            steps.append("# Step 1: Remove duplicates\ndf = df.drop_duplicates().reset_index(drop=True)")
        if null_col and adv:
            steps.append(f'# Step 2: {adv}\ndf["{null_col}"] = df["{null_col}"].fillna({fill_val_py})')
        if m:
            steps.append(f'# Step 3: Remove outliers in {m}\ndf = df[\n  (df["{m}"] >= {lo}) &\n  (df["{m}"] <= {hi})\n].reset_index(drop=True)')
        steps.append("# Step 4: Convert date columns\n# df['your_date_col'] = pd.to_datetime(df['your_date_col'])")
        return steps, "Python (pandas)"

    elif tool == "SQL":
        if dupes > 0:
            steps.append("-- Step 1: Remove duplicates\nSELECT DISTINCT * FROM your_table;")
        if null_col and adv:
            steps.append(f'-- Step 2: {adv}\nSELECT\n  COALESCE("{null_col}", 0) AS "{null_col}"\nFROM your_table;')
        if m:
            steps.append(f'-- Step 3: Filter outliers in {m}\nSELECT * FROM your_table\nWHERE "{m}" BETWEEN {lo} AND {hi};')
        return steps, "SQL"

    elif tool == "Tableau":
        if dupes > 0:
            steps.append("// Step 1: Remove duplicates\nTableau Prep > Clean Step > Remove Duplicates")
        if null_col and adv:
            steps.append(f'// Step 2: {adv}\nCalculated Field:\nIFNULL([{null_col}], 0)')
        if m:
            steps.append(f'// Step 3: Filter outliers in {m}\n[{m}] >= {lo}\nAND [{m}] <= {hi}')
        return steps, "Tableau Prep"

    else:  # Excel
        if dupes > 0:
            steps.append("// Step 1: Remove duplicates\nData tab > Remove Duplicates > Select all columns > OK")
        if null_col and adv:
            steps.append(f'// Step 2: {adv}\n=IF(ISBLANK(A2), 0, A2)\nOr: Home > Find & Select > Go To Special > Blanks > Fill 0')
        if m:
            steps.append(f'// Step 3: Filter outliers in {m}\n=AND({m}>={lo},{m}<={hi})\nAdd as helper column, filter TRUE rows only')
        return steps, "Excel"


# ══════════════════════════════════════════════════════
# MEASURES / FORMULAS
# ══════════════════════════════════════════════════════

def get_measures(tool, metrics, groups, time_cols):
    ms = []
    m  = metrics[0] if metrics else None
    m2 = metrics[1] if len(metrics) > 1 else None
    g  = groups[0]  if groups  else None
    t  = time_cols[0] if time_cols else None

    if not m: return []

    if tool == "Power BI":
        ms.append((f"Avg {m}", f"Avg {m} =\nAVERAGE(Data[{m}])"))
        ms.append((f"Median {m}", f"Median {m} =\nMEDIANX(Data, Data[{m}])"))
        if g:
            ms.append((f"Top {g} by {m}",
                f"Top {g} =\nCALCULATE(\n  MAX(Data[{g}]),\n  TOPN(1,\n    VALUES(Data[{g}]),\n    CALCULATE(AVERAGE(Data[{m}])),\n    DESC\n  )\n)"))
        ms.append(("% Above Average",
            f"Pct Above Avg =\nDIVIDE(\n  COUNTROWS(FILTER(Data,\n    Data[{m}] > CALCULATE(\n      AVERAGE(Data[{m}]),\n      ALL(Data)))),\n  COUNTROWS(Data)\n) * 100"))

    elif tool == "Python":
        ms.append(("Summary Stats",
            f"# Distribution summary\ndf['{m}'].describe()\nprint('Mean:  ', df['{m}'].mean().round(1))\nprint('Median:', df['{m}'].median().round(1))"))
        if g:
            ms.append(("Group Analysis",
                f"df.groupby('{g}')['{m}'].agg(\n  ['mean','median','count']\n).sort_values('mean', ascending=False)"))
        if m2:
            ms.append(("Correlation",
                f"import matplotlib.pyplot as plt\nplt.scatter(df['{m}'], df['{m2}'], alpha=0.3)\nplt.xlabel('{m}')\nplt.ylabel('{m2}')\nplt.title('Correlation')\nplt.show()"))

    elif tool == "SQL":
        if g:
            ms.append(("Performance by Group",
                f'SELECT\n  "{g}",\n  ROUND(AVG("{m}"),1) as avg_{m.split("_")[0]},\n  COUNT(*) as total_rows\nFROM your_table\nGROUP BY "{g}"\nORDER BY avg_{m.split("_")[0]} DESC;'))
        ms.append(("Outlier Query",
            f'SELECT * FROM your_table\nWHERE "{m}" > (\n  SELECT AVG("{m}") + 2 * STDDEV("{m}")\n  FROM your_table\n);'))

    elif tool == "Tableau":
        ms.append((f"Avg {m}", f"AVG([{m}])"))
        ms.append((f"Median {m}", f"MEDIAN([{m}])"))
        if g:
            ms.append(("% of Total", f"SUM([{m}]) /\nTOTAL(SUM([{m}]))"))
        if t:
            ms.append(("Period-over-Period",
                f"(SUM([{m}]) - LOOKUP(SUM([{m}]), -1))\n/ ABS(LOOKUP(SUM([{m}]), -1))"))

    else:  # Excel
        ms.append(("Average", f"=AVERAGE({m}:{m})"))
        ms.append(("Median", f"=MEDIAN({m}:{m})"))
        if g:
            ms.append(("AVERAGEIF by Group",
                f'=AVERAGEIF({g}:{g},"GroupValue",{m}:{m})'))
        ms.append(("Count Above Average",
            f'=COUNTIF({m}:{m},">"&AVERAGE({m}:{m}))'))

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
    tool = st.radio("Analytics Tool", ["Power BI","Python","SQL","Tableau","Excel"], label_visibility="collapsed")
    st.markdown("""
    <div style="height:1px;background:#1a1a30;margin:20px 0 16px"></div>
    <div style="font-size:9px;font-family:'JetBrains Mono';color:#3a3a5a;text-transform:uppercase;letter-spacing:2px;margin-bottom:8px">Upload Dataset</div>
    <div style="font-size:11px;color:#4a4a6a;font-family:'JetBrains Mono';margin-bottom:10px;line-height:1.7">CSV or Excel — up to 30,000 rows</div>
    """, unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload", type=["csv","xlsx","xls"], label_visibility="collapsed")
    if uploaded:
        st.markdown(f'<div style="margin-top:8px;padding:8px 12px;background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.2);border-radius:8px;font-size:10px;font-family:JetBrains Mono;color:#10b981">✓ {uploaded.name}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# MAIN
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
      <div style="font-size:13px;font-family:'JetBrains Mono';color:#3a3a5a;text-align:center;line-height:2.2">
        Upload your dataset from the sidebar to begin
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

try:
    df = load_data(uploaded.read(), uploaded.name)
    gc.collect()
except Exception as e:
    st.error(f"Could not read file: {e}")
    st.stop()

# ── CLASSIFY ──────────────────────────────────────────
metrics   = get_real_metrics(df)
groups    = get_groups(df)
time_cols = get_time_cols(df)
useless_cols = get_useless(df)
null_cols = [c for c in df.columns if df[c].isnull().any()]
miss_total = df.isnull().sum().sum()
miss_pct   = round(miss_total / max(df.shape[0]*df.shape[1], 1) * 100, 1)
dupes      = df.duplicated().sum()
score      = quality_score(df, metrics)
sc         = "#10b981" if score>=80 else "#f59e0b" if score>=60 else "#ef4444"
ds_type    = detect_type(df)
TYPE_MAP   = {"operations":"OPERATIONS","financial":"FINANCIAL","market":"MARKET DATA",
              "hr":"HR","healthcare":"HEALTHCARE","product":"PRODUCT","projects":"PROJECTS","general":"GENERAL"}

# ── KPIs ──────────────────────────────────────────────
c1,c2,c3,c4 = st.columns(4)
for col,l,v,s,a in [
    (c1,"Rows",   f"{df.shape[0]:,}", f"{df.shape[1]} columns","#6366f1"),
    (c2,"Missing",f"{miss_pct}%",     f"{miss_total:,} cells","#f59e0b" if miss_pct>5 else "#10b981"),
    (c3,"Duplicates",f"{dupes:,}",    f"{dupes/len(df)*100:.1f}% of rows","#ef4444" if dupes>0 else "#10b981"),
    (c4,"Quality",f"{score}",         "/100", sc)
]:
    with col:
        st.markdown(f'<div class="kpi" style="--a:{a}"><div class="kpi-l">{l}</div><div class="kpi-v" style="color:{a}">{v}</div><div class="kpi-s">{s}</div></div>', unsafe_allow_html=True)

# ── DATA STORY ────────────────────────────────────────
st.markdown('<div class="sec">Data Story</div>', unsafe_allow_html=True)
parts = [f"<b style='color:#a5b4fc'>{df.shape[0]:,}-row {TYPE_MAP.get(ds_type,'').lower()} dataset</b> with {df.shape[1]} columns"]
if time_cols:
    try:
        ds = pd.to_datetime(df[time_cols[0]], errors='coerce', format="mixed").dropna()
        span = (ds.max()-ds.min()).days
        if span > 0: parts.append(f"spanning <b style='color:#6366f1'>{span} days</b>")
    except: pass
if groups:
    parts.append(f"across <b style='color:#a78bfa'>{df[groups[0]].nunique()} {groups[0].replace('_',' ')} groups</b>")
if metrics:
    parts.append(f"key metrics: <b style='color:#00e5ff'>{', '.join(metrics[:3])}</b>")
if useless_cols:
    parts.append(f"<b style='color:#6b6b9a'>{len(useless_cols)} ID/useless columns</b> flagged for removal")
qt = "excellent condition" if score>=85 else "moderate quality" if score>=65 else "quality issues"
parts.append(f"Data quality: <b style='color:{sc}'>{qt}</b> ({score}/100)")
st.markdown(f'<div style="background:#0d0d1a;border:1px solid #1e1e35;border-left:3px solid #6366f1;border-radius:14px;padding:24px 28px"><span class="badge">{TYPE_MAP.get(ds_type,"DATA")}</span><div style="font-size:16px;font-weight:600;color:#e2e2f0;line-height:1.9">{" — ".join(parts)}.</div></div>', unsafe_allow_html=True)

# ── PATTERNS ──────────────────────────────────────────
pts = detect_patterns(df, metrics, time_cols, groups)
gc.collect()
st.markdown('<div class="sec">Pattern Detection</div>', unsafe_allow_html=True)
if pts:
    for i in range(0, len(pts), 2):
        chunk = pts[i:i+2]
        g = st.columns(len(chunk))
        for j,p in enumerate(chunk):
            with g[j]:
                st.markdown(f'<div class="pc" style="--c:{p["c"]}"><div class="pt">{p["t"]}</div><div class="ps">{p["s"]}</div><div class="pb">{p["b"]}</div><div class="pa"><span style="color:{p["c"]}">ACTION: </span>{p["a"]}</div></div>', unsafe_allow_html=True)
else:
    st.markdown('<div style="background:#0d0d1a;border:1px solid #1e1e35;border-radius:12px;padding:20px;color:#6b6b9a;font-family:JetBrains Mono;font-size:13px">No significant patterns detected in this dataset.</div>', unsafe_allow_html=True)

# ── COLUMN PROFILE ────────────────────────────────────
st.markdown('<div class="sec">Column Profile</div>', unsafe_allow_html=True)
for i in range(0, len(df.columns), 4):
    chunk = list(df.columns)[i:i+4]
    g = st.columns(4)
    for j,cn in enumerate(chunk):
        s = df[cn]
        filled = s.dropna()
        pct  = round(len(filled)/len(df)*100) if len(df) else 0
        uniq = filled.nunique()
        role = classify_column(cn, s)
        cb   = "#10b981" if pct>90 else "#f59e0b" if pct>70 else "#ef4444"
        extra = ""
        if role == "metric":
            try:
                n = safe_num(filled)
                extra = f"avg:{n.mean():,.1f} | med:{n.median():,.1f}"
            except: pass
        elif role == "id":      extra = "identifier — not for analysis"
        elif role == "useless": extra = "single value — remove"
        elif role == "location":extra = f"geo coordinates"
        with g[j]:
            st.markdown(f'<div class="card"><div class="cn" title="{cn}">{cn[:18]}{"..." if len(cn)>18 else ""}</div><div style="margin:4px 0 8px">{ttag(role)}</div><div class="bw"><div class="bf" style="width:{pct}%;background:{cb}"></div></div><div class="cm">{pct}% filled | {uniq} unique{(" | "+extra) if extra else ""}</div></div>', unsafe_allow_html=True)

# ── CRITICAL ISSUES ───────────────────────────────────
st.markdown('<div class="sec">Critical Issues</div>', unsafe_allow_html=True)
iss = []
for c in null_cols:
    p = df[c].isnull().sum()/len(df)*100
    adv = missing_advice(c, df[c], df)
    color = "#ef4444" if p > 15 else "#f59e0b"
    iss.append((color, f"<b>{c}</b> — {p:.1f}% missing. {adv}"))
for c in metrics[:5]:
    try:
        lo, hi = smart_bounds(c, df[c])
        n = int(((df[c] < lo) | (df[c] > hi)).sum())
        if n/len(df) > 0.05:
            iss.append(("#ef4444", f"<b>{c}</b> — {n:,} outliers ({n/len(df)*100:.1f}%). Valid range: {lo:,}–{hi:,}."))
    except: pass
if dupes > 0:
    iss.append(("#ef4444", f"<b>{dupes:,} duplicate rows</b> — remove before any aggregation."))
if useless_cols:
    iss.append(("#6b6b9a", f"<b>Low-value columns:</b> {', '.join(useless_cols[:5])} — consider removing from your model."))
if not iss:
    iss.append(("#10b981", "No critical issues found. Dataset is clean and ready for analysis."))
st.markdown('<div style="background:#0d0d1a;border:1px solid #1e1e35;border-radius:12px;padding:16px 20px">'+"".join([f'<div class="ii"><div class="idot" style="background:{c}"></div><div>{t}</div></div>' for c,t in iss[:8]])+'</div>', unsafe_allow_html=True)

# ── CLEANING STEPS ────────────────────────────────────
steps, lang = cleaning_code(df, tool, metrics, null_cols)
st.markdown(f'<div class="sec">Cleaning Steps — {lang}</div>', unsafe_allow_html=True)
for s in steps:
    st.markdown(f'<div class="cb">{s}</div>', unsafe_allow_html=True)

# ── MEASURES ──────────────────────────────────────────
ms = get_measures(tool, metrics, groups, time_cols)
tlabels = {"Power BI":"DAX Measures","Python":"Python Snippets","SQL":"SQL Queries","Tableau":"Calculated Fields","Excel":"Excel Formulas"}
st.markdown(f'<div class="sec">{tlabels.get(tool,"Formulas")}</div>', unsafe_allow_html=True)
if ms:
    g1,g2 = st.columns(2)
    for i,(title,code) in enumerate(ms):
        with (g1 if i%2==0 else g2):
            st.markdown(f'<div class="ct">{title}</div><div class="cb">{code}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div style="background:#0d0d1a;border:1px solid #1e1e35;border-radius:12px;padding:20px;color:#6b6b9a;font-family:JetBrains Mono;font-size:13px">No numeric metrics found for formula generation.</div>', unsafe_allow_html=True)

# ── QUESTIONS ─────────────────────────────────────────
qs = generate_questions(ds_type, metrics, groups, time_cols)
st.markdown('<div class="sec">5 Questions Worth Answering</div>', unsafe_allow_html=True)
st.markdown('<div style="background:#0d0d1a;border:1px solid #1e1e35;border-radius:12px;padding:16px 20px">'+"".join([f'<div class="qi"><div class="qn">0{i+1}</div><div><div class="qt">{q}</div><div class="qw">{w}</div></div></div>' for i,(q,w,_) in enumerate(qs)])+'</div>', unsafe_allow_html=True)

# ── GROUP COMPARISON ──────────────────────────────────
if groups and metrics:
    g_col = groups[0]
    m_col = metrics[0]
    n_unique = df[g_col].nunique()
    if 2 <= n_unique <= 50:
        st.markdown(f'<div class="sec">Group Comparison — {g_col} by {m_col}</div>', unsafe_allow_html=True)
        try:
            grp = df.groupby(g_col)[m_col].agg(['mean','median','count']).round(1).sort_values('mean')
            grp.columns = ['Mean','Median','Count']
            grp = grp.reset_index()
            total_g = len(grp)
            rows_html = ""
            max_mean = grp['Mean'].max()
            for idx_r, row in grp.iterrows():
                if idx_r == 0:        rank = '<span style="color:#10b981;font-weight:700;font-family:JetBrains Mono;font-size:10px">BEST</span>'
                elif idx_r == total_g-1: rank = '<span style="color:#ef4444;font-weight:700;font-family:JetBrains Mono;font-size:10px">WORST</span>'
                else:                 rank = f'<span style="color:#6b6b9a;font-size:10px;font-family:JetBrains Mono">{idx_r+1}</span>'
                bw  = int(row['Mean']/max_mean*100) if max_mean > 0 else 0
                bc  = "#10b981" if idx_r < total_g*0.33 else "#f59e0b" if idx_r < total_g*0.66 else "#ef4444"
                mv  = f"{row['Mean']:,.1f}"
                mdv = f"{row['Median']:,.1f}"
                rows_html += f'<tr><td style="padding:8px 12px">{rank}</td><td style="padding:8px 12px;color:#e2e2f0;font-weight:600;font-family:JetBrains Mono;font-size:11px">{row[g_col]}</td><td style="padding:8px 12px"><div style="display:flex;align-items:center;gap:8px"><div style="width:{bw}px;height:4px;background:{bc};border-radius:3px;min-width:2px"></div><span style="color:#e2e2f0;font-family:JetBrains Mono;font-size:11px">{mv}</span></div></td><td style="padding:8px 12px;color:#6b6b9a;font-family:JetBrains Mono;font-size:11px">{mdv}</td><td style="padding:8px 12px;color:#6b6b9a;font-family:JetBrains Mono;font-size:11px">{int(row["Count"]):,}</td></tr>'
            st.markdown(f'<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;background:#0d0d1a;border:1px solid #1e1e35;border-radius:12px;overflow:hidden"><thead><tr style="border-bottom:1px solid #1e1e35"><th style="padding:8px 12px;color:#3a3a5a;text-align:left;font-size:9px;font-family:JetBrains Mono;letter-spacing:1.5px;text-transform:uppercase">#</th><th style="padding:8px 12px;color:#3a3a5a;text-align:left;font-size:9px;font-family:JetBrains Mono;letter-spacing:1.5px;text-transform:uppercase">{g_col}</th><th style="padding:8px 12px;color:#3a3a5a;text-align:left;font-size:9px;font-family:JetBrains Mono;letter-spacing:1.5px;text-transform:uppercase">Mean</th><th style="padding:8px 12px;color:#3a3a5a;text-align:left;font-size:9px;font-family:JetBrains Mono;letter-spacing:1.5px;text-transform:uppercase">Median</th><th style="padding:8px 12px;color:#3a3a5a;text-align:left;font-size:9px;font-family:JetBrains Mono;letter-spacing:1.5px;text-transform:uppercase">Count</th></tr></thead><tbody>{rows_html}</tbody></table></div>', unsafe_allow_html=True)
        except: pass

# ── FINAL VERDICT ─────────────────────────────────────
st.markdown('<div class="sec">Final Verdict</div>', unsafe_allow_html=True)
verdict = "READY" if score>=80 else "NEEDS WORK" if score>=60 else "CRITICAL"
vmsg    = "Clean and ready for analysis." if score>=80 else "Fix the issues above before building dashboards." if score>=60 else "Critical quality issues — resolve before proceeding."
TVIS = {
    "Power BI": ["KPI Card","Line Chart","Bar Chart","Scatter Plot","Matrix Table"],
    "Python":   ["plt.plot() — trends","sns.barplot() — groups","sns.scatterplot() — correlation","px.histogram() — distribution","df.corr() heatmap — multicollinearity"],
    "SQL":      ["GROUP BY aggregation","Window functions (RANK, LAG)","CTEs for step-by-step logic","Subqueries for filtering","JOIN for combining tables"],
    "Tableau":  ["KPI Summary card","Trend Line chart","Bar in Bar chart","Scatter Plot","Heat Map"],
    "Excel":    ["PivotTable by group","Line Chart for trends","Scatter chart","Histogram","Conditional Formatting"],
}
vis = TVIS.get(tool, TVIS["Power BI"])
c1,c2 = st.columns([1,2])
with c1:
    st.markdown(f'<div style="background:#0d0d1a;border:1px solid #1e1e35;border-radius:14px;padding:24px;text-align:center"><div style="font-size:64px;font-weight:800;color:{sc};letter-spacing:-3px">{score}</div><div style="font-size:10px;font-family:JetBrains Mono;color:#3a3a5a;text-transform:uppercase;letter-spacing:2px;margin:6px 0">Quality Score</div><div style="font-size:18px;font-weight:800;color:{sc};margin:10px 0 8px">{verdict}</div><div style="font-size:11px;color:#4a4a6a;font-family:JetBrains Mono;line-height:1.7">{vmsg}</div></div>', unsafe_allow_html=True)
with c2:
    rh = "".join([f'<div style="padding:10px 0;border-bottom:1px solid #0f0f20;font-family:JetBrains Mono;font-size:12px;color:#c4c4e0;display:flex;gap:12px;align-items:center"><span style="color:{sc};font-weight:700;min-width:24px">0{i+1}</span>{v}</div>' for i,v in enumerate(vis)])
    st.markdown(f'<div style="background:#0d0d1a;border:1px solid #1e1e35;border-radius:14px;padding:20px 24px"><div class="sec" style="margin-top:0">Recommended {tool} Visuals</div>{rh}</div>', unsafe_allow_html=True)

gc.collect()
st.markdown("<br>", unsafe_allow_html=True)
