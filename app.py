# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import gc

st.set_page_config(page_title="DataSense", page_icon="DS", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=JetBrains+Mono:wght@400;700&display=swap');
html,body,[class*="css"]{font-family:'Syne',sans-serif;}
.stApp{background:#07070f;color:#e2e2f0;}
[data-testid="stSidebar"]{background:#0d0d1a;border-right:1px solid #1e1e35;}
.hero{background:linear-gradient(135deg,#0d0d1a,#12122a);border:1px solid #1e1e35;border-radius:20px;padding:32px 36px;margin-bottom:24px;}
.badge{display:inline-block;font-size:10px;font-family:'JetBrains Mono';font-weight:700;padding:4px 12px;border-radius:20px;letter-spacing:1.5px;background:rgba(16,185,129,0.1);color:#10b981;border:1px solid rgba(16,185,129,0.25);margin-bottom:14px;}
.kpi{background:#0d0d1a;border:1px solid #1e1e35;border-radius:14px;padding:16px 18px;border-top:2px solid var(--a);}
.kpi-l{font-size:10px;font-family:'JetBrains Mono';color:#6b6b9a;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:6px;}
.kpi-v{font-size:28px;font-weight:800;line-height:1;}
.kpi-s{font-size:11px;color:#6b6b9a;margin-top:4px;font-family:'JetBrains Mono';}
.sec{font-size:10px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:#6366f1;padding:6px 0 10px;border-bottom:1px solid #1e1e35;margin:24px 0 14px;}
.card{background:#0d0d1a;border:1px solid #1e1e35;border-radius:12px;padding:14px 16px;}
.tag{font-size:9px;font-family:'JetBrains Mono';padding:2px 8px;border-radius:20px;font-weight:700;}
.bw{background:#07070f;border-radius:3px;height:3px;margin:8px 0 5px;overflow:hidden;}
.bf{height:100%;border-radius:3px;}
.cm{font-size:10px;color:#6b6b9a;font-family:'JetBrains Mono';}
.cn{font-family:'JetBrains Mono';font-size:12px;font-weight:700;color:#a5b4fc;margin-bottom:6px;}
.pc{background:#0d0d1a;border:1px solid #1e1e35;border-radius:14px;padding:18px 20px;border-top:2px solid var(--c);}
.pt{font-size:11px;font-family:'JetBrains Mono';text-transform:uppercase;letter-spacing:1px;color:var(--c);margin-bottom:6px;}
.ps{font-size:22px;font-weight:800;color:var(--c);margin:4px 0;}
.pb{font-size:13px;color:#c4c4e0;line-height:1.6;}
.pa{margin-top:10px;padding-top:8px;border-top:1px solid #1e1e35;font-size:11px;font-family:'JetBrains Mono';color:#6b6b9a;}
.cb{background:#0a0a18;border:1px solid #1e1e35;border-left:3px solid #6366f1;border-radius:10px;padding:16px 20px;font-family:'JetBrains Mono';font-size:12px;color:#a5b4fc;line-height:1.8;margin-bottom:12px;white-space:pre-wrap;}
.ct{font-size:10px;color:#6b6b9a;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:6px;font-family:'JetBrains Mono';}
.qi{display:flex;gap:12px;padding:12px 0;border-bottom:1px solid #0f0f20;}
.qn{font-size:11px;font-family:'JetBrains Mono';color:#6366f1;font-weight:700;min-width:22px;}
.qt{font-size:13px;color:#e2e2f0;font-weight:600;line-height:1.5;}
.qw{font-size:11px;color:#6b6b9a;margin-top:3px;font-family:'JetBrains Mono';}
.ii{display:flex;align-items:flex-start;gap:10px;padding:10px 0;border-bottom:1px solid #0f0f20;font-size:13px;color:#c4c4e0;}
.id{width:8px;height:8px;border-radius:50%;margin-top:5px;flex-shrink:0;}
.stButton>button{background:linear-gradient(135deg,#4f46e5,#7c3aed)!important;color:white!important;font-family:'Syne'!important;font-weight:700!important;border:none!important;border-radius:12px!important;padding:12px 0!important;width:100%!important;}
.stRadio label{background:#0d0d1a!important;border:1px solid #1e1e35!important;border-radius:10px!important;padding:7px 14px!important;font-family:'JetBrains Mono'!important;font-size:12px!important;}
</style>
""", unsafe_allow_html=True)

# ── HELPERS ──────────────────────────────────────────
@st.cache_data(max_entries=3)
def load_data(file_bytes, fname):
    import io
    if fname.endswith('.csv'):
        df = pd.read_csv(io.BytesIO(file_bytes), on_bad_lines='skip', nrows=30000)
    else:
        df = pd.read_excel(io.BytesIO(file_bytes), nrows=30000)
    return df.dropna(how='all')

def detect_type(series):
    filled = series.dropna().astype(str).str.strip()
    filled = filled[filled != '']
    if len(filled) == 0: return "empty"
    try:
        pd.to_numeric(filled.str.replace(r'[$,% ]','',regex=True))
        return "numeric"
    except: pass
    try:
        pd.to_datetime(filled.iloc[:20], format="mixed", dayfirst=False)
        return "date"
    except: pass
    return "category" if filled.nunique()/len(filled) < 0.25 else "text"

TS = {
    "numeric": ("#00e5ff","rgba(0,229,255,0.08)","rgba(0,229,255,0.2)","NUM"),
    "date":    ("#10b981","rgba(16,185,129,0.08)","rgba(16,185,129,0.2)","DATE"),
    "category":("#a78bfa","rgba(167,139,250,0.08)","rgba(167,139,250,0.2)","CAT"),
    "text":    ("#f59e0b","rgba(245,158,11,0.08)","rgba(245,158,11,0.2)","TEXT"),
    "empty":   ("#ef4444","rgba(239,68,68,0.08)","rgba(239,68,68,0.2)","EMPTY"),
}
def ttag(t):
    c,bg,bd,l = TS.get(t,TS["text"])
    return f'<span class="tag" style="color:{c};background:{bg};border:1px solid {bd}">{l}</span>'

def obounds(s):
    q1,q3 = s.quantile(0.25),s.quantile(0.75)
    iqr = q3-q1
    return q1-1.5*iqr, q3+1.5*iqr

def qscore(df, num_cols):
    score = 100
    total = df.shape[0]*df.shape[1]
    if total == 0: return 0
    mp = df.isnull().sum().sum()/total*100
    score -= min(30, mp*1.5)
    ot = sum(((df[c]<obounds(df[c])[0])|(df[c]>obounds(df[c])[1])).sum() for c in num_cols[:4])
    if len(df)>0: score -= min(20,(ot/len(df))*5)
    score -= min(15, df.duplicated().sum()/len(df)*100*2)
    return max(0,round(score))

def dtype(df):
    cs = " ".join(df.columns.str.lower())
    if any(x in cs for x in ['delivery','order','store','logistics']): return "operations"
    if any(x in cs for x in ['revenue','sales','profit','invoice']): return "financial"
    if any(x in cs for x in ['open','close','high','low','volume','stock']): return "market"
    if any(x in cs for x in ['employee','salary','department','hire']): return "hr"
    if any(x in cs for x in ['patient','hospital','medical']): return "healthcare"
    if any(x in cs for x in ['customer','user','session','click']): return "product"
    return "general"

def patterns(df, num_cols, date_cols, cat_cols):
    pts = []
    # Trend
    if date_cols and num_cols:
        try:
            dt = df.copy()[[date_cols[0], num_cols[0]]]
            dt['_d'] = pd.to_datetime(dt[date_cols[0]], errors='coerce', format="mixed")
            dt = dt.dropna().sort_values('_d')
            n = len(dt)
            if n > 20:
                f = dt[num_cols[0]].iloc[:n//3].mean()
                l = dt[num_cols[0]].iloc[-n//3:].mean()
                ch = ((l-f)/abs(f)*100) if f!=0 else 0
                if abs(ch)>10:
                    c = "#10b981" if ch>0 else "#ef4444"
                    pts.append({"t":f"{'Up' if ch>0 else 'Down'}ward Trend","c":c,"s":f"{'+' if ch>0 else ''}{ch:.1f}%","b":f"<b style='color:{c}'>{num_cols[0]}</b> {'grew' if ch>0 else 'declined'} {abs(ch):.1f}% from start to end of dataset.","a":f"Use Line Chart with {date_cols[0]} on X-axis."})
        except: pass
    # Outliers
    if num_cols:
        wc,wn,wp = "",0,0
        for col in num_cols[:4]:
            try:
                lo,hi = obounds(df[col].dropna())
                n = int(((df[col]<lo)|(df[col]>hi)).sum())
                p = n/len(df)*100
                if n>wn: wc,wn,wp = col,n,p
            except: pass
        if wn>0 and wp>5:
            lo,hi = obounds(df[wc].dropna())
            pts.append({"t":"Outlier Cluster","c":"#ef4444","s":f"{wn:,} rows","b":f"<b style='color:#ef4444'>{wc}</b> has {wn:,} outliers ({wp:.1f}%). Normal range: {lo:.0f}–{hi:.0f}.","a":f"Filter rows outside {lo:.0f}–{hi:.0f} in cleaning step."})
    # Correlation
    if len(num_cols)>=2:
        try:
            cr = df[num_cols[:5]].corr().abs()
            np.fill_diagonal(cr.values,0)
            mx = cr.max().max()
            if mx>0.85:
                idx = cr.stack().idxmax()
                pts.append({"t":"Multicollinearity","c":"#f59e0b","s":f"r={mx:.2f}","b":f"<b style='color:#f59e0b'>{idx[0]}</b> and <b style='color:#f59e0b'>{idx[1]}</b> are {mx*100:.0f}% correlated. Using both causes double-counting.","a":"Keep one as primary metric, derive the other only when needed."})
        except: pass
    # Skew
    if num_cols:
        sk = [(c,abs(float(df[c].dropna().skew()))) for c in num_cols[:4] if len(df[c].dropna())>30]
        if sk:
            c,s = max(sk,key=lambda x:x[1])
            if s>1.5:
                pts.append({"t":"Skewed Distribution","c":"#06b6d4","s":f"skew:{s:.1f}","b":f"<b style='color:#06b6d4'>{c}</b> is heavily skewed. Mean is misleading — median is more accurate.","a":"Use Median instead of Average in KPI cards."})
    return pts[:4]

def questions(ds_type, num_cols, cat_cols, date_cols):
    qs = {
        "operations":[("What causes delivery delays?","Compare performance across time and location segments.","Operations"),("Which locations underperform?","Rank all groups by average metric to find outliers.","Performance")],
        "financial":[("What drives revenue growth?","Correlate revenue with time and category.","Revenue"),("Where is margin lost?","Compare cost vs revenue across segments.","Profitability")],
        "market":[("Is the asset trending?","Analyze price with rolling averages.","Trend"),("What is volatility?","Compare std deviation across periods.","Risk")],
        "hr":[("What predicts retention?","Correlate tenure with compensation.","Retention"),("Is there pay equity?","Compare pay across departments.","Equity")],
        "product":[("Where do users drop off?","Analyze conversion across funnel stages.","Funnel"),("What drives retention?","Compare retained vs churned users.","Retention")],
    }
    res = qs.get(ds_type,[("What are the key trends?","Analyze changes over time.","Trend"),("Which segment performs best?","Compare groups by key metric.","Segmentation")])
    if date_cols: res.append((f"How does performance change over time?",f"Plot {num_cols[0] if num_cols else 'metrics'} by {date_cols[0]}.","Time"))
    if cat_cols and num_cols: res.append((f"Which {cat_cols[0]} performs best?",f"Rank {cat_cols[0]} by avg {num_cols[0]}.","Segmentation"))
    if len(num_cols)>=2: res.append((f"Relationship between {num_cols[0]} and {num_cols[1]}?","Build scatter plot and look for patterns.","Correlation"))
    return res[:5]

def cleaning_code(df, tool, num_cols, null_cols):
    d = df.duplicated().sum()
    steps = []
    if tool=="Power BI":
        if d>0: steps.append(f"// Remove duplicates\n= Table.Distinct(Source)")
        if null_cols: steps.append(f'// Replace nulls\n= Table.ReplaceValue(Source, null, 0,\n  Replacer.ReplaceValue, {{"{null_cols[0]}"}})')
        if num_cols:
            lo,hi = obounds(df[num_cols[0]].dropna())
            steps.append(f'// Remove outliers\n= Table.SelectRows(Source,\n  each [{num_cols[0]}] >= {lo:.0f}\n  and [{num_cols[0]}] <= {hi:.0f})')
        return steps,"Power Query"
    elif tool=="Python":
        if d>0: steps.append("# Remove duplicates\ndf = df.drop_duplicates()")
        if null_cols: steps.append(f'# Fill nulls\ndf["{null_cols[0]}"] = df["{null_cols[0]}"].fillna(0)')
        if num_cols:
            lo,hi = obounds(df[num_cols[0]].dropna())
            steps.append(f'# Remove outliers\ndf = df[(df["{num_cols[0]}"] >= {lo:.1f})\n      & (df["{num_cols[0]}"] <= {hi:.1f})]')
        return steps,"Python (pandas)"
    elif tool=="SQL":
        if d>0: steps.append("-- Remove duplicates\nSELECT DISTINCT * FROM your_table;")
        if null_cols: steps.append(f'-- Handle nulls\nSELECT COALESCE("{null_cols[0]}", 0)\nFROM your_table;')
        if num_cols:
            lo,hi = obounds(df[num_cols[0]].dropna())
            steps.append(f'-- Filter outliers\nSELECT * FROM your_table\nWHERE "{num_cols[0]}" BETWEEN {lo:.0f} AND {hi:.0f};')
        return steps,"SQL"
    elif tool=="Tableau":
        steps.append("// Remove duplicates\nTableau Prep > Clean > Remove Duplicates")
        if null_cols: steps.append(f'// Fill nulls\nCalculated Field:\nIFNULL([{null_cols[0]}], 0)')
        if num_cols:
            lo,hi = obounds(df[num_cols[0]].dropna())
            steps.append(f'// Filter outliers\n[{num_cols[0]}] >= {lo:.0f}\nAND [{num_cols[0]}] <= {hi:.0f}')
        return steps,"Tableau Prep"
    else:
        steps.append("// Remove duplicates\nData > Remove Duplicates")
        if null_cols: steps.append(f'// Fill blanks\n=IF(ISBLANK(A1),0,A1)')
        if num_cols:
            lo,hi = obounds(df[num_cols[0]].dropna())
            steps.append(f'// Filter outliers\n=AND({num_cols[0]}>{lo:.0f},{num_cols[0]}<{hi:.0f})')
        return steps,"Excel"

def measures_code(tool, num_cols, cat_cols, null_cols):
    ms = []
    if tool=="Power BI":
        if num_cols: ms.append((f"Avg {num_cols[0]}",f"Avg {num_cols[0]} =\nAVERAGE(Data[{num_cols[0]}])"))
        ms.append(("Total Rows","Total Rows =\nCOUNTROWS(Data)"))
        if null_cols: ms.append((f"Missing %",f"Missing % =\nDIVIDE(\n  COUNTROWS(FILTER(Data,\n    ISBLANK(Data[{null_cols[0]}]))),\n  COUNTROWS(Data)\n)*100"))
        if len(num_cols)>=1: ms.append(("% Above Avg",f"Pct Above Avg =\nDIVIDE(\n  COUNTROWS(FILTER(Data,\n    Data[{num_cols[0]}]>CALCULATE(\n      AVERAGE(Data[{num_cols[0]}]),ALL(Data)))),\n  COUNTROWS(Data)\n)*100"))
    elif tool=="Python":
        if num_cols: ms.append(("Summary",f"df['{num_cols[0]}'].describe()"))
        if cat_cols and num_cols: ms.append(("Group By",f"df.groupby('{cat_cols[0]}')['{num_cols[0]}'].mean()"))
        if len(num_cols)>=2: ms.append(("Correlation",f"df[['{num_cols[0]}','{num_cols[1]}']].corr()"))
    elif tool=="SQL":
        if num_cols:
            g = f'"{cat_cols[0]}",' if cat_cols else ''
            ms.append(("Aggregation",f"SELECT {g}\n  AVG(\"{num_cols[0]}\") as avg,\n  COUNT(*) as total\nFROM your_table\n{('GROUP BY \"'+cat_cols[0]+'\"') if cat_cols else ''};"))
    elif tool=="Tableau":
        if num_cols: ms.append((f"Avg {num_cols[0]}",f"AVG([{num_cols[0]}])"))
        if cat_cols and num_cols: ms.append(("% of Total",f"SUM([{num_cols[0]}])/\nTOTAL(SUM([{num_cols[0]}]))"))
    else:
        if num_cols: ms.append(("Average",f"=AVERAGE({num_cols[0]}:{num_cols[0]})"))
        if cat_cols and num_cols: ms.append(("AVERAGEIF",f"=AVERAGEIF({cat_cols[0]}:{cat_cols[0]},\n\"value\",{num_cols[0]}:{num_cols[0]})"))
    return ms[:4]

# ── HEADER ───────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="badge">NO API KEY &nbsp;|&nbsp; FREE &nbsp;|&nbsp; ANY TOOL</div>
  <div style="font-size:38px;font-weight:800;letter-spacing:-1px">Data<span style="color:#6366f1">Sense</span></div>
  <div style="font-size:13px;color:#6b6b9a;font-family:'JetBrains Mono';margin-top:6px">Upload your dataset. Deep analysis for any analytics tool.</div>
</div>
""", unsafe_allow_html=True)

tool = st.radio("", ["Power BI","Python","SQL","Tableau","Excel"], horizontal=True, label_visibility="collapsed")
st.markdown("<br>", unsafe_allow_html=True)
uploaded = st.file_uploader("Upload", type=["csv","xlsx","xls"], label_visibility="collapsed")

if not uploaded:
    st.markdown('<div style="background:#0d0d1a;border:1.5px dashed #2a2a4a;border-radius:14px;padding:40px;text-align:center;color:#6b6b9a;font-family:JetBrains Mono">Drop CSV or Excel file here</div>', unsafe_allow_html=True)
    st.stop()

try:
    df = load_data(uploaded.read(), uploaded.name)
    gc.collect()
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

num_cols = df.select_dtypes(include='number').columns.tolist()
cat_cols = [c for c in df.columns if detect_type(df[c])=='category']
date_cols = [c for c in df.columns if detect_type(df[c])=='date']
null_cols = [c for c in df.columns if df[c].isnull().any()]
miss_total = df.isnull().sum().sum()
miss_pct = round(miss_total/(df.shape[0]*df.shape[1])*100,1) if df.shape[0]*df.shape[1]>0 else 0
dupes = df.duplicated().sum()
score = qscore(df, num_cols)
sc = "#10b981" if score>=80 else "#f59e0b" if score>=60 else "#ef4444"
ds_type = dtype(df)

# KPIs
c1,c2,c3,c4 = st.columns(4)
for col,l,v,s,a in [(c1,"Rows",f"{df.shape[0]:,}",f"{df.shape[1]} cols","#6366f1"),(c2,"Missing",f"{miss_pct}%",f"{miss_total:,} cells","#f59e0b" if miss_pct>5 else "#10b981"),(c3,"Dupes",f"{dupes:,}",f"{dupes/len(df)*100:.1f}%","#ef4444" if dupes>0 else "#10b981"),(c4,"Quality",f"{score}","/100",sc)]:
    with col:
        st.markdown(f'<div class="kpi" style="--a:{a}"><div class="kpi-l">{l}</div><div class="kpi-v" style="color:{a}">{v}</div><div class="kpi-s">{s}</div></div>', unsafe_allow_html=True)

# Data Story
type_map = {"operations":"OPERATIONS","financial":"FINANCIAL","market":"MARKET DATA","hr":"HR","healthcare":"HEALTHCARE","product":"PRODUCT","general":"GENERAL"}
st.markdown('<div class="sec">Data Story</div>', unsafe_allow_html=True)
story_parts = [f"<b style='color:#a5b4fc'>{df.shape[0]:,}-row {type_map.get(ds_type,'DATA').lower()} dataset</b> with {df.shape[1]} dimensions"]
if date_cols:
    try:
        ds = pd.to_datetime(df[date_cols[0]], errors='coerce', format="mixed").dropna()
        span = (ds.max()-ds.min()).days
        if span>0: story_parts.append(f"covering <b style='color:#6366f1'>{span} days</b>")
    except: pass
if cat_cols: story_parts.append(f"across <b style='color:#a78bfa'>{df[cat_cols[0]].nunique()} {cat_cols[0].replace('_',' ')} categories</b>")
quality_txt = "in excellent condition" if score>=85 else "with moderate quality issues" if score>=65 else "with quality problems"
story_parts.append(f"Data is <b style='color:{sc}'>{quality_txt}</b> ({score}/100)")
st.markdown(f'<div style="background:#0d0d1a;border:1px solid #1e1e35;border-left:3px solid #6366f1;border-radius:14px;padding:24px 28px"><span class="badge">{type_map.get(ds_type,"DATA")}</span><div style="font-size:17px;font-weight:600;color:#e2e2f0;line-height:1.8">{" — ".join(story_parts)}.</div></div>', unsafe_allow_html=True)

# Patterns
pts = patterns(df, num_cols, date_cols, cat_cols)
gc.collect()
st.markdown('<div class="sec">Pattern Detection</div>', unsafe_allow_html=True)
if pts:
    for i in range(0,len(pts),2):
        chunk = pts[i:i+2]
        g = st.columns(len(chunk))
        for j,p in enumerate(chunk):
            with g[j]:
                st.markdown(f'<div class="pc" style="--c:{p["c"]}"><div class="pt">{p["t"]}</div><div class="ps">{p["s"]}</div><div class="pb">{p["b"]}</div><div class="pa"><span style="color:{p["c"]}">ACTION: </span>{p["a"]}</div></div>', unsafe_allow_html=True)
else:
    st.markdown('<div style="background:#0d0d1a;border:1px solid #1e1e35;border-radius:12px;padding:20px;color:#6b6b9a;font-family:JetBrains Mono;font-size:13px">No significant patterns detected.</div>', unsafe_allow_html=True)

# Column Profile
st.markdown('<div class="sec">Column Profile</div>', unsafe_allow_html=True)
cl = list(df.columns)
for i in range(0,len(cl),4):
    chunk = cl[i:i+4]
    g = st.columns(4)
    for j,cn in enumerate(chunk):
        s = df[cn]
        filled = s.dropna()
        pct = round(len(filled)/len(df)*100) if len(df) else 0
        uniq = filled.nunique()
        t = detect_type(s)
        c_bar = "#10b981" if pct>90 else "#f59e0b" if pct>70 else "#ef4444"
        extra = ""
        if t=="numeric":
            try:
                n = pd.to_numeric(filled,errors='coerce').dropna()
                extra = f"avg: {n.mean():.1f}"
            except: pass
        with g[j]:
            st.markdown(f'<div class="card"><div class="cn" title="{cn}">{cn[:18]}{"..." if len(cn)>18 else ""}</div><div style="margin:4px 0 8px">{ttag(t)}</div><div class="bw"><div class="bf" style="width:{pct}%;background:{c_bar}"></div></div><div class="cm">{pct}% filled | {uniq} unique{(" | "+extra) if extra else ""}</div></div>', unsafe_allow_html=True)

# Issues
st.markdown('<div class="sec">Critical Issues</div>', unsafe_allow_html=True)
iss = []
for c in df.columns:
    p = df[c].isnull().sum()/len(df)*100
    if p>10: iss.append(("#ef4444",f"<b>{c}</b> — {p:.1f}% missing. High impact."))
    elif p>0: iss.append(("#f59e0b",f"<b>{c}</b> — {p:.1f}% missing. Replace with 0 or median."))
for c in num_cols[:4]:
    try:
        lo,hi = obounds(df[c].dropna())
        n = int(((df[c]<lo)|(df[c]>hi)).sum())
        if n/len(df)>0.1: iss.append(("#ef4444",f"<b>{c}</b> — {n:,} outliers ({n/len(df)*100:.1f}%). Filter to {lo:.0f}–{hi:.0f}."))
    except: pass
if dupes>0: iss.append(("#ef4444",f"<b>{dupes:,} duplicate rows</b> — remove before aggregation."))
if not iss: iss.append(("#10b981","No critical issues. Dataset is clean."))
st.markdown('<div style="background:#0d0d1a;border:1px solid #1e1e35;border-radius:12px;padding:16px 20px">'+"".join([f'<div class="ii"><div class="id" style="background:{c}"></div><div>{t}</div></div>' for c,t in iss[:6]])+'</div>', unsafe_allow_html=True)

# Cleaning
steps,lang = cleaning_code(df, tool, num_cols, null_cols)
st.markdown(f'<div class="sec">Cleaning Steps — {lang}</div>', unsafe_allow_html=True)
for s in steps:
    st.markdown(f'<div class="cb">{s}</div>', unsafe_allow_html=True)

# Measures
ms = measures_code(tool, num_cols, cat_cols, null_cols)
tlabels = {"Power BI":"DAX Measures","Python":"Python","SQL":"SQL Queries","Tableau":"Calculated Fields","Excel":"Excel Formulas"}
st.markdown(f'<div class="sec">{tlabels.get(tool,"Formulas")}</div>', unsafe_allow_html=True)
g1,g2 = st.columns(2)
for i,(title,code) in enumerate(ms):
    with (g1 if i%2==0 else g2):
        st.markdown(f'<div class="ct">{title}</div><div class="cb">{code}</div>', unsafe_allow_html=True)

# Questions
qs = questions(ds_type, num_cols, cat_cols, date_cols)
st.markdown('<div class="sec">5 Questions Worth Answering</div>', unsafe_allow_html=True)
st.markdown('<div style="background:#0d0d1a;border:1px solid #1e1e35;border-radius:12px;padding:16px 20px">'+"".join([f'<div class="qi"><div class="qn">0{i+1}</div><div><div class="qt">{q}</div><div class="qw">{w}</div></div></div>' for i,(q,w,_) in enumerate(qs)])+'</div>', unsafe_allow_html=True)

# Verdict
st.markdown('<div class="sec">Final Verdict</div>', unsafe_allow_html=True)
verdict = "READY" if score>=80 else "NEEDS WORK" if score>=60 else "CRITICAL"
vmsg = "Clean and ready for analysis." if score>=80 else "Fix issues above before building dashboards." if score>=60 else "Critical issues — resolve before proceeding."
tvis = {"Power BI":["KPI Card","Line Chart","Bar Chart","Scatter Plot","Matrix"],"Python":["plt.plot()","sns.barplot()","df.corr() heatmap","px.histogram()","sns.scatterplot()"],"SQL":["GROUP BY","Window Functions","CTEs","Subqueries","JOINs"],"Tableau":["KPI Summary","Trend Line","Bar Chart","Scatter Plot","Heat Map"],"Excel":["PivotTable","Line Chart","Bar Chart","Scatter Plot","Conditional Format"]}
vis = tvis.get(tool,["KPI Card","Line Chart","Bar Chart","Scatter Plot","Matrix"])
c1,c2 = st.columns([1,2])
with c1:
    st.markdown(f'<div style="background:#0d0d1a;border:1px solid #1e1e35;border-radius:14px;padding:24px;text-align:center"><div style="font-size:64px;font-weight:800;color:{sc}">{score}</div><div style="font-size:11px;font-family:JetBrains Mono;color:#6b6b9a">Quality Score</div><div style="font-size:18px;font-weight:800;color:{sc};margin:8px 0">{verdict}</div><div style="font-size:12px;color:#6b6b9a;font-family:JetBrains Mono">{vmsg}</div></div>', unsafe_allow_html=True)
with c2:
    rh = "".join([f'<div style="padding:8px 0;border-bottom:1px solid #1e1e35;font-family:JetBrains Mono;font-size:13px;color:#c4c4e0"><span style="color:{sc};margin-right:10px">0{i+1}</span>{v}</div>' for i,v in enumerate(vis)])
    st.markdown(f'<div style="background:#0d0d1a;border:1px solid #1e1e35;border-radius:14px;padding:20px 24px"><div class="sec" style="margin-top:0">Recommended {tool} Visuals</div>{rh}</div>', unsafe_allow_html=True)

gc.collect()
st.markdown("<br>", unsafe_allow_html=True)
