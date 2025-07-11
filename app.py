import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Sonu Screener", layout="wide")
st.title("📊 F&O Screener (5-min Candle Logic)")

with open("fnolist.txt") as f:
    fno_stocks = [line.strip() for line in f if line.strip()]

bullish = []
bearish = []

for symbol in fno_stocks:
    try:
        data = yf.download(symbol, interval="5m", period="1d")
        prev_data = yf.download(symbol, period="2d")
        prev_high = prev_data.iloc[-2]["High"]
        prev_low = prev_data.iloc[-2]["Low"]
        live_price = data.iloc[-1]["Close"]

        first = data.iloc[0]
        second = data.iloc[1]

        # Bullish Condition
        if first["Close"] > first["Open"] and second["Close"] < second["Open"] and live_price > prev_high:
            bullish.append({"Stock": symbol, "Price": live_price})

        # Bearish Condition
        if first["Close"] < first["Open"] and second["Close"] > second["Open"] and live_price < prev_low:
            bearish.append({"Stock": symbol, "Price": live_price})
    except:
        pass

st.subheader("🟩 Bullish Setup")
st.dataframe(pd.DataFrame(bullish))

st.subheader("🟥 Bearish Setup")
st.dataframe(pd.DataFrame(bearish))