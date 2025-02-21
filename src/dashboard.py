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
            font-family: 'Arial', sans-serif;
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
        section[data-testid="stTable"] {
            background-color: #0e1117 !important;
            color: white !important;
            border-radius: 10px;
            padding: 10px;
        }
        div[data-testid="stDataFrame"] {
            background-color: #0e1117 !important;
            color: white !important;
            border-radius: 10px;
            padding: 10px;
        }
        
      
        .marquee {
            width: 100%;
            overflow: hidden;
            white-space: nowrap;
        }
        .marquee span {
            display: inline-block;
            padding-left: 100%;
            font-size: 36px; 
            color: #FF5733;
            animation: marquee 10s linear infinite;
        }
        @keyframes marquee {
            from {
                transform: translateX(0);
            }
            to {
                transform: translateX(-100%);
            }
        }
    </style>
            
    <div class="marquee">
        <span>Thorbjörn Persson Steive, Milou Sandén Lindroth, Irina Antipina</span>
    </div>

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
        return f"{value / 1_000_000_000:.1f}MD{suffix}"
    elif abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}MN{suffix}"
    elif abs(value) >= 1_000:
        return f"{value / 1_000:.1f}T{suffix}"
    return f"{value:.2f}{suffix}"

def layout():
    st.markdown("<h1>🚀 Crypto Live Dashboard</h1>", unsafe_allow_html=True)

    crypto_mapping = {"TRX": "TRON (TRX)", "S": "SONIC (S)"}
    crypto_display = list(crypto_mapping.values())

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_crypto = st.selectbox("Välj kryptovaluta", crypto_display)
        crypto_choice = [key for key, value in crypto_mapping.items() if value == selected_crypto][0]
    with col2:
        if crypto_choice == "TRX":
            st.image("src/tron.png", width=100)  
        else:
            st.image("src/sonic.png", width=100)

    with col3:    
        currency_choice = st.selectbox("Välj valuta", ["SEK", "NOK", "DKK", "EUR", "ISK"])

    if crypto_choice == "TRX":
        st.markdown("""
        **TRON (TRX)** lanserades 2017 av Justin Sun och bygger upp infrastrukturen för ett verkligt decentraliserat internet och dess höga genomströmning och skalbarhet gör den till en populär blockkedja för att bygga decentraliserade appar (dappar). TRX-token ansluter hela TRON-ekosystemet och har ett antal tillämpningar, bland annat för att få rösträtt och bandbredd.
        
        TRON (TRX) är en mycket nyare uppfinning än Bitcoin (BTC), men dess pris och värde har ändå haft en intressant historia. Om du vill veta mer om dess rörelser är du på rätt plats. Vi har sammanställt allt du behöver veta för att bättre förstå tidigare TRX-prisrörelser – och de faktorer som påverkar dem.
        """)
    elif crypto_choice == "S":
        st.markdown("""
        **Sonic (S)** – en ny kryptovaluta som precis har börjat sin resa, och ärligt talat, vi vet inte riktigt vad vi ska säga om den än. Kanske är detta den där mytomspunna myntet som ser ut som en gåta idag, men som imorgon är på allas läppar! Vem vet? Kanske är just **Sonic (S)** kryptovalutan som alla kommer att prata om om några år, och du kommer att kunna skryta om att du köpte den i rätt tid.
        
        Om du letar efter något nytt, utan alla vanliga löften och förutsägbara diagram, så kanske **Sonic (S)** är det du bör köpa för att testa din lycka. Kanske kommer den att bli den nya stjärnan på kryptomarknaden, eller kanske är det bara ännu ett experiment... Vem vet, om inte du?
        """)

    df = load_data(crypto_choice)

    if df.empty:
        st.warning(f"Ingen data tillgänglig för {selected_crypto} ännu. Vänta på uppdateringar...")
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

    with st.container():
        st.markdown(f"### 📋 Data Tabell för {selected_crypto} i {currency_choice}")
        st.dataframe(df[[f"price_{currency_choice.lower()}", 
                         f"volume_{currency_choice.lower()}", 
                         "volume_change_24h", 
                         "percent_change_24h"]], 
                     use_container_width=True)

    time.sleep(60)
    st.rerun()

if __name__ == "__main__":
    layout()
