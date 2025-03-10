# streaming_crypto_group_7
Group project - building a streaming data platform with Kafka to stream cryptocurrency data

Kryptokollen – Real-Time Cryptocurrency Dashboard 🚀
Kryptokollen är ett realtidsbaserat system för att samla in, bearbeta och visualisera kryptovalutadata. Systemet hämtar data från CoinMarketCap API, hanterar datastreams via Kafka, lagrar information i PostgreSQL, och visualiserar pris- och volymutveckling i en Streamlit-dashboard.

📌 Teknologier: Python, Apache Kafka, PostgreSQL, Streamlit, Docker
📌 Funktioner:
✅ Realtidsinsamling av kryptovalutadata (TRX, SONIC)
✅ Skalbar arkitektur med Kafka för strömmande data
✅ Interaktiv dashboard med grafer och nyckelindikatorer
✅ Stöd för flera valutor (SEK, NOK, DKK, EUR, ISK)

🚀 Hur man kör projektet:
1️⃣ Klona repot: git clone <repo-url>
2️⃣ Starta miljön: docker-compose up --build
3️⃣ Kör alla tjänster: python run_all.py
4️⃣ Öppna dashboarden i webbläsaren
