import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import time
from constants import (
    POSTGRES_USER,
    POSTGRES_DBNAME,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
)
from charts import line_chart

connection_string = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"
engine = create_engine(connection_string)

st.markdown("""
    <style>
        body, [data-testid="stAppViewContainer"] {
            background-color: #0e1117;
            color: white;
        }
        h1, h2, h3 {
            font-family: 'Arial', sans-serif';
            color: #f39c12;
            text-align: center;
        }
        div.stSelectbox, div.stButton {
            background-color: #1f2630;
            color: white;
            border-radius: 10px;
        }
        .stMetric {
            background-color: #1f2630;
            border-radius: 10px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

def load_data(symbol):
    table = "trx" if symbol == "TRX" else "sonic"
    query = f"SELECT * FROM {table} WHERE symbol = '{symbol}' ORDER BY timestamp DESC LIMIT 100"
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.set_index("timestamp")
    return df

def format_number(value, suffix=""):
    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}B{suffix}"
    elif abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}M{suffix}"
    elif abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K{suffix}"
    return f"{value:.2f}{suffix}"

def layout():
    st.markdown("<h1>🚀 Crypto Live Dashboard</h1>", unsafe_allow_html=True)

    crypto_mapping = {"TRX": "TRON (TRX)", "S": "SONIC (S)"}
    crypto_display = list(crypto_mapping.values())

    col1, col2 = st.columns(2)
    with col1:
        selected_crypto = st.selectbox("Välj kryptovaluta", crypto_display)
        crypto_choice = [key for key, value in crypto_mapping.items() if value == selected_crypto][0]
    with col2:
        currency_choice = st.selectbox("Välj valuta", ["SEK", "NOK", "DKK", "EUR", "ISK"])

    df = load_data(crypto_choice)

    if df.empty:
        if crypto_choice == "S":
            st.warning("Ingen data tillgänglig för Sonic ännu. Se till att producer_s.py och consumer_s.py körs och vänta på att data ska börja strömma in.")
        else:
            st.warning("Ingen data tillgänglig ännu. Vänta på uppdateringar...")
        return

    latest = df.iloc[0]

    st.markdown("### 🔥 Marknadsdata")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(f"💰 Pris ({currency_choice})", f"{latest[f'price_{currency_choice.lower()}']:.2f} {currency_choice}")
    col2.metric("📉 Prisändring 24h", format_number(latest["percent_change_24h"], "%"), delta=latest["percent_change_24h"])
    col3.metric(f"📊 24h Volym ({currency_choice})", format_number(latest[f'volume_{currency_choice.lower()}']))
    col4.metric("📈 Volymändring 24h", format_number(latest["volume_change_24h"], "%"), delta=latest["volume_change_24h"])

    st.markdown(f"### 📈 {selected_crypto} Pris i {currency_choice}")
    fig_price = line_chart(df.index, df[f"price_{currency_choice.lower()}"], title="Pris över tid", xlabel="Tid", ylabel=f"Pris ({currency_choice})")
    st.pyplot(fig_price)

    st.markdown(f"### 📊 Handelsvolym för {selected_crypto} i {currency_choice}")
    fig_volume = line_chart(df.index, df[f"volume_{currency_choice.lower()}"], title="Volym över tid", xlabel="Tid", ylabel="Volym")
    st.pyplot(fig_volume)
    
    time.sleep(60)
    st.rerun()

if __name__ == "__main__":
    layout()
