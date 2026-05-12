import streamlit as st
import pandas as pd
import json
import re
import requests
import os
from datetime import datetime

# ====================== Session State ======================
if "aliyun_df" not in st.session_state:
    st.session_state.aliyun_df = None
if "ollama_df" not in st.session_state:
    st.session_state.ollama_df = None

# ====================== Page Config ======================
st.set_page_config(
    page_title="LogSentry AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================== Custom CSS ======================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main > div {
        padding: 2rem 3rem;
        max-width: 1400px;
        margin: 0 auto;
    }

    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #0d2137 100%);
        padding: 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: "";
        position: absolute;
        top: -50%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(56,189,248,0.1) 0%, transparent 70%);
        border-radius: 50%;
    }

    .main-header h1 {
        color: #f0f9ff;
        font-weight: 700;
        font-size: 2.2rem;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .main-header p {
        color: #94a3b8;
        margin: 0.5rem 0 0 0;
        font-size: 1.05rem;
        font-weight: 300;
    }

    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1;
    }

    .metric-label {
        font-size: 0.875rem;
        color: #64748b;
        margin-top: 0.5rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1e293b;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(59,130,246,0.3);
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(59,130,246,0.4);
    }

    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    .footer {
        text-align: center;
        padding: 2rem;
        color: #94a3b8;
        font-size: 0.875rem;
        margin-top: 3rem;
        border-top: 1px solid #e2e8f0;
    }

    .info-box {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }

    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
        margin: 2rem 0;
    }

    /* Streamlit chart text - red color */
    [data-testid="stChart"] text {
        fill: #dc2626 !important;
        font-family: 'Inter', sans-serif !important;
    }

    [data-testid="stChart"] .vega-embed svg text {
        fill: #dc2626 !important;
    }
</style>
""", unsafe_allow_html=True)

# ====================== Sidebar ======================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 2rem 0;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🛡️</div>
        <h2 style="color: #f8fafc; font-weight: 700; margin: 0; font-size: 1.5rem;">LogSentry AI</h2>
        <p style="color: #94a3b8; margin: 0.5rem 0 0 0; font-size: 0.875rem;">Intelligent Log Security Analysis</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: #334155; margin: 1rem 0;'>", unsafe_allow_html=True)

    st.markdown(
        "<p style='color: #94a3b8; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem;'>Model Configuration</p>",
        unsafe_allow_html=True)

    model_type = st.radio(
        "Select Model",
        ["Alibaba Cloud Tongyi Qianwen", "Local Ollama"],
        index=1,
        label_visibility="collapsed"
    )

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    if model_type == "Alibaba Cloud Tongyi Qianwen":
        api_key = st.text_input(
            "API Key",
            type="password",
            placeholder="sk-xxxxxxxx",
            help="Your Alibaba Cloud API key starting with sk-"
        )
    else:
        ollama_model = st.selectbox(
            "Local Model",
            ["qwen2.5:3b"],
            index=0
        )
        ollama_url = st.text_input(
            "Ollama Endpoint",
            "http://127.0.0.1:11434/api/generate",
            help="Ollama API endpoint URL"
        )

    st.markdown("<hr style='border-color: #334155; margin: 1.5rem 0;'>", unsafe_allow_html=True)

    st.markdown(
        "<p style='color: #94a3b8; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem;'>Feature Toggles</p>",
        unsafe_allow_html=True)

    enable_ip = st.checkbox("IP Intelligence Lookup", value=True)
    enable_waf = st.checkbox("WAF Rule Generation", value=True)

    st.markdown("<div style='position: fixed; bottom: 2rem; left: 2rem; right: 2rem;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: rgba(30,58,95,0.5); border-radius: 10px; padding: 1rem; text-align: center;">
        <p style="color: #64748b; font-size: 0.75rem; margin: 0;">LogSentry AI v2.0</p>
        <p style="color: #475569; font-size: 0.7rem; margin: 0.25rem 0 0 0;">Powered by AI Security Engine</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ====================== Log Parser ======================
def parse_log(line):
    pattern = r'(\S+) \S+ \S+ \[(.*?)\] "(.*?)" (\d+)'
    m = re.match(pattern, line)
    if m:
        ip = m.group(1)
        time_str = m.group(2)
        request = m.group(3)
        url = request.split()[1] if len(request.split()) > 1 else request
        return {
            "time": time_str,
            "ip": ip,
            "url": url,
            "raw": line.strip()
        }
    else:
        return {
            "time": "-",
            "ip": "-",
            "url": line[:100],
            "raw": line.strip()
        }


# ====================== Security Rules ======================
def security_rule_check(url):
    url_lower = url.lower()
    if "../etc/passwd" in url_lower or "../shadow" in url_lower or "..%2f" in url_lower or "/?page=.." in url_lower:
        return {"is_attack": True, "attack_type": "Path Traversal", "confidence": 95, "severity": "high",
                "action": "Block"}
    elif "<script" in url_lower or "alert(" in url_lower:
        return {"is_attack": True, "attack_type": "XSS Cross-Site Scripting", "confidence": 95, "severity": "high",
                "action": "Block"}
    elif "cmd=whoami" in url_lower or "exec=" in url_lower or "system(" in url_lower:
        return {"is_attack": True, "attack_type": "Command Execution", "confidence": 95, "severity": "high",
                "action": "Block"}
    elif "union select" in url_lower or "id=1'" in url_lower or "select *" in url_lower:
        return {"is_attack": True, "attack_type": "SQL Injection", "confidence": 95, "severity": "high",
                "action": "Block"}
    else:
        return None


# ====================== Alibaba Cloud Analysis ======================
def analyze_aliyun(log, api_key):
    prompt = f"""You are a professional Web security log analyst. Analyze the access behavior and output strictly in JSON format without any extra explanatory text.
IP: {log['ip']}
URL: {log['url']}

Identify type: Normal Request, SQL Injection, XSS Cross-Site Scripting, Path Traversal, Command Execution.
Required output fields:
is_attack: boolean
attack_type: attack type/Normal
confidence: integer 0-100
severity: low/high
action: Ignore/Block

Strictly follow this format:
{{
    "is_attack":false,
    "attack_type":"Normal",
    "confidence":0,
    "severity":"low",
    "action":"Ignore"
}}
"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "qwen-turbo",
        "input": {"messages": [{"role": "user", "content": prompt}]}
    }
    try:
        resp = requests.post(
            "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
            headers=headers,
            json=data,
            timeout=15
        )
        res = resp.json()
        content = res["output"]["text"]
        js_match = re.search(r"\{.*\}", content, re.DOTALL)
        if js_match:
            return json.loads(js_match.group())
        return {"is_attack": False, "attack_type": "Parse Failed", "confidence": 0, "severity": "low",
                "action": "Ignore"}
    except Exception as e:
        return {"is_attack": False, "attack_type": "API Error", "confidence": 0, "severity": "low",
                "action": str(e)[:20]}


# ====================== Local Ollama Analysis ======================
def analyze_ollama(log, model, api_url):
    rule_result = security_rule_check(log["url"])
    if rule_result is not None:
        return rule_result

    prompt = f"""You are a Web security log detection assistant. Output only JSON, no extra text.
IP: {log['ip']}
URL: {log['url']}

Determine if this is an attack: Normal Request, SQL Injection, XSS, Path Traversal, Command Execution.
Fixed output format:
{{"is_attack":false,"attack_type":"Normal","confidence":0,"severity":"low","action":"Ignore"}}
"""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.0, "num_ctx": 512}
    }
    try:
        r = requests.post(api_url, json=payload, timeout=20)
        res = r.json()
        js = re.search(r"\{.*\}", res.get("response", ""), re.DOTALL)
        return json.loads(js.group()) if js else {"is_attack": False, "attack_type": "Parse Failed", "confidence": 0,
                                                  "severity": "low", "action": "Ignore"}
    except:
        return {"is_attack": False, "attack_type": "Ollama Connection Error", "confidence": 0, "severity": "low",
                "action": "Check Local Service"}


# ====================== IP & WAF Functions ======================
def get_ip_info(ip):
    return {"country": "Local", "region": "-", "city": "-", "isp": "-"}


def gen_waf_rule(attack_type):
    rules = {
        "SQL Injection": 'SecRule REQUEST_URI "@rx union|select" "id:1001,deny,status:403,msg:SQL Injection"',
        "XSS Cross-Site Scripting": 'SecRule REQUEST_URI "@rx <script" "id:1002,deny,status:403,msg:XSS"',
        "Command Execution": 'SecRule REQUEST_URI "@rx whoami|cmd" "id:1003,deny,status:403,msg:Command Execution"',
        "Path Traversal": 'SecRule REQUEST_URI "@rx ../" "id:1004,deny,status:403,msg:Path Traversal"'
    }
    return rules.get(attack_type, "# No matching WAF rule")


# ====================== Main Header ======================
st.markdown("""
<div class="main-header">
    <h1>🛡️ LogSentry AI</h1>
    <p>Intelligent Web Log Security Analysis & Threat Detection Platform</p>
</div>
""", unsafe_allow_html=True)

# ====================== Upload Section ======================
st.markdown('<div class="section-header">📤 Upload Log File</div>', unsafe_allow_html=True)

uploaded = st.file_uploader(
    "Drop your log file here or click to browse",
    type=['log', 'txt'],
    help="Supported formats: .log, .txt"
)

if uploaded:
    content = uploaded.read().decode('utf-8', errors='ignore')
    lines = [l.strip() for l in content.splitlines() if l.strip()]

    st.markdown(f"""
    <div class="info-box">
        <span style="font-weight: 600; color: #1e40af;">&#10003; File Loaded Successfully</span>
        <span style="color: #475569;"> — Detected <strong>{len(lines)}</strong> log entries ready for analysis</span>
    </div>
    """, unsafe_allow_html=True)

    col_btn, _ = st.columns([1, 4])
    with col_btn:
        analyze_btn = st.button("🚀 Start AI Analysis", type="primary", use_container_width=True)

    if analyze_btn:
        if model_type == "Alibaba Cloud Tongyi Qianwen" and not api_key:
            st.error("⚠️ Please enter your Alibaba Cloud API Key")
            st.stop()

        progress_container = st.container()
        with progress_container:
            progress = st.progress(0)
            status = st.empty()

        results = []

        for i, line in enumerate(lines):
            status.markdown(f"""
            <div style="display: flex; align-items: center; gap: 0.75rem; color: #64748b; font-size: 0.9rem;">
                <span>&#128260;</span>
                <span>Analyzing entry <strong>{i + 1}</strong> of <strong>{len(lines)}</strong>...</span>
            </div>
            """, unsafe_allow_html=True)

            log = parse_log(line)
            if model_type == "Alibaba Cloud Tongyi Qianwen":
                ai_result = analyze_aliyun(log, api_key)
            else:
                ai_result = analyze_ollama(log, ollama_model, ollama_url)

            ai_result.setdefault("is_attack", False)
            ai_result.setdefault("attack_type", "Normal")
            ai_result.setdefault("confidence", 0)
            ai_result.setdefault("severity", "low")
            ai_result.setdefault("action", "Ignore")

            if enable_ip and ai_result["is_attack"]:
                ai_result.update(get_ip_info(log["ip"]))
            if enable_waf and ai_result["is_attack"]:
                ai_result["waf_rule"] = gen_waf_rule(ai_result["attack_type"])

            results.append({**log, **ai_result})
            progress.progress((i + 1) / len(lines))

        status.empty()
        progress.empty()

        df = pd.DataFrame(results)

        if model_type == "Alibaba Cloud Tongyi Qianwen":
            st.session_state.aliyun_df = df.copy()
        else:
            st.session_state.ollama_df = df.copy()

        st.success("✅ Analysis Complete! Results are displayed below.")

# ====================== Results Section ======================
st.markdown('<div class="section-header">📊 Analysis Results</div>', unsafe_allow_html=True)

show_cols = ["time", "ip", "url", "is_attack", "attack_type", "confidence", "severity", "action"]

df = None
if model_type == "Alibaba Cloud Tongyi Qianwen" and st.session_state.aliyun_df is not None:
    df = st.session_state.aliyun_df
elif model_type == "Local Ollama" and st.session_state.ollama_df is not None:
    df = st.session_state.ollama_df

if df is not None:
    attack_df = df[df["is_attack"] == True]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(df):,}</div>
            <div class="metric-label">Total Logs</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #dc2626;">{len(attack_df):,}</div>
            <div class="metric-label">Threats Detected</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #ea580c;">{len(df[df['severity'] == 'high']):,}</div>
            <div class="metric-label">High Severity</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        safety_rate = round((1 - len(attack_df) / len(df)) * 100, 1) if len(df) > 0 else 100
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #16a34a;">{safety_rate}%</div>
            <div class="metric-label">Safety Rate</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    st.markdown(
        '<div style="background: white; border-radius: 12px; padding: 1rem; border: 1px solid #e2e8f0; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">',
        unsafe_allow_html=True)
    st.dataframe(
        df[show_cols],
        use_container_width=True,
        height=450,
        hide_index=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if len(attack_df) > 0:
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">📈 Threat Distribution</div>', unsafe_allow_html=True)

        chart_col1, chart_col2 = st.columns([2, 1])

        with chart_col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)

            threat_counts = attack_df["attack_type"].value_counts().reset_index()
            threat_counts.columns = ["Threat Type", "Count"]

            st.bar_chart(
                threat_counts,
                x="Count",
                y="Threat Type",
                horizontal=True,
                color="Count",
                width="stretch",
                height=350
            )
            st.markdown('</div>', unsafe_allow_html=True)

        with chart_col2:
            threat_summary = attack_df["attack_type"].value_counts()
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown("<p style='font-weight: 600; color: #1e293b; margin-bottom: 1rem;'>Threat Summary</p>",
                        unsafe_allow_html=True)
            for threat, count in threat_summary.items():
                percentage = round(count / len(attack_df) * 100, 1)
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid #f1f5f9;">
                    <span style="color: #475569; font-size: 0.9rem;">{threat}</span>
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <div style="background: #e2e8f0; height: 6px; width: 60px; border-radius: 3px; overflow: hidden;">
                            <div style="background: linear-gradient(90deg, #3b82f6, #06b6d4); height: 100%; width: {percentage}%;"></div>
                        </div>
                        <span style="color: #1e293b; font-weight: 600; font-size: 0.875rem;">{count}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    export_col1, export_col2 = st.columns([1, 4])
    with export_col1:
        st.download_button(
            "📥 Export Report",
            df.to_csv(index=False).encode("utf-8"),
            "security_analysis_report.csv",
            mime="text/csv",
            use_container_width=True
        )

# ====================== Footer ======================
st.markdown("""
<div class="footer">
    <p>&#128274; LogSentry AI — Advanced Web Security Log Analysis Platform</p>
    <p style="font-size: 0.75rem; margin-top: 0.5rem;">Built with Streamlit · AI-Powered Threat Detection</p>
</div>
""", unsafe_allow_html=True)