import streamlit as st
import requests

# ページの設定（スマホで見やすいようにワイドモード＆タイトル設定）
st.set_page_config(page_title="Remittance Calc", page_icon="💰", layout="centered")

# カスタムCSSで銀行の書類っぽく＆3,4,5番を強調
st.markdown("""
    <style>
    .report-box {
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 10px;
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
    }
    .highlight-box {
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        background-color: #fff3cd;
        border: 2px solid #ffc107;
    }
    .label-title {
        font-size: 0.9rem;
        font-weight: bold;
        color: #495057;
    }
    .label-sub {
        font-size: 0.7rem;
        color: #6c757d;
        margin-bottom: 5px;
    }
    .val-style {
        font-size: 1.2rem;
        font-weight: bold;
        text-align: right;
    }
    .val-highlight {
        font-size: 1.6rem;
        font-weight: bold;
        color: #bd2130;
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)

st.title("送金計算シミュレーター")
st.caption("For Bank Staff Reference")

# --- 為替レートの自動取得 ---
@st.cache_data(ttl=3600)  # 1時間キャッシュ
def get_current_rate():
    try:
        res = requests.get("https://open.er-api.com/v6/latest/JPY")
        data = res.json()
        return float(data["rates"]["THB"])
    except:
        return 0.23000

default_rate = get_current_rate()

# --- 入力エリア ---
st.subheader("入力項目")
total_thb = st.number_input("⑥ 合計・元金額 (Total THB)", min_value=0, value=100000, step=1000, format="%d")
rate = st.number_input("② 採用レート (Rate: 1 JPY = ? THB)", min_value=0.0, value=default_rate, format="%.5f")

# --- 計算ロジック ---
JAPAN_FEE_JPY = 5000
THAI_FEE_THB = 550

# 5. 日本手数料のバーツ換算
japan_fee_thb = round(JAPAN_FEE_JPY * rate)
# 3. 日本入金額（バーツ）
net_thb = total_thb - THAI_FEE_THB - japan_fee_thb
# 1. 日本入金額（円）
net_jpy = int(net_thb // rate) if net_thb > 0 and rate > 0 else 0

st.write("---")
st.subheader("銀行提出用（書類順）")

# １．日本入金額（円）
st.markdown(f"""
<div class="report-box">
    <div class="label-title">１．日本入金額 (JPY)</div>
    <div class="label-sub">Net JPY to Japan</div>
    <div class="val-style">{net_jpy:,} JPY</div>
</div>
""", unsafe_allow_html=True)

# ２．採用レート
st.markdown(f"""
<div class="report-box">
    <div class="label-title">２．採用レート (Rate)</div>
    <div class="label-sub">Applied Exchange Rate</div>
    <div class="val-style">{rate:.4f}</div>
</div>
""", unsafe_allow_html=True)

# ３．日本入金額（バーツ） ★強調
st.markdown(f"""
<div class="highlight-box">
    <div class="label-title" style="color: #533f03;">３．日本入金額 (THB) ★</div>
    <div class="label-sub">Net THB to Japan</div>
    <div class="val-highlight">{max(0, net_thb):,} THB</div>
</div>
""", unsafe_allow_html=True)

# ４．タイ手数料 ★強調
st.markdown(f"""
<div class="highlight-box">
    <div class="label-title" style="color: #533f03;">４．タイ側手数料 (THB) ★</div>
    <div class="label-sub">Thailand Fee</div>
    <div class="val-highlight">{THAI_FEE_THB:,} THB</div>
</div>
""", unsafe_allow_html=True)

# ５．日本手数料（バーツ換算） ★強調
st.markdown(f"""
<div class="highlight-box">
    <div class="label-title" style="color: #533f03;">５．日本側手数料 (THB) ★</div>
    <div class="label-sub">Japan Fee (5,000 JPY)</div>
    <div class="val-highlight">{japan_fee_thb:,} THB</div>
</div>
""", unsafe_allow_html=True)

# ６．合計・元金額
st.markdown(f"""
<div class="report-box" style="background-color: #e9ecef;">
    <div class="label-title">６．合計・元金額 (THB)</div>
    <div class="label-sub">Total Amount</div>
    <div class="val-style">{total_thb:,} THB</div>
</div>
""", unsafe_allow_html=True)
