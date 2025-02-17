from quixstreams import Application
from quixstreams.sinks.community.postgresql import PostgreSQLSink
from constants import (
    POSTGRES_USER,
    POSTGRES_DBNAME,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
)


def extract_coin_data(message):
    return {
        "coin": message["name"],
        "symbol": message["symbol"],
        "price_sek": message["prices"]["SEK"],
        "price_nok": message["prices"]["NOK"],
        "price_dkk": message["prices"]["DKK"],
        "price_eur": message["prices"]["EUR"],
        "timestamp": message["timestamp"]
    }


def create_postgres_sink():
    sink = PostgreSQLSink(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DBNAME,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        table_name="trx",
        schema_auto_update=True,
    )

    return sink


def main():
    app = Application(
        broker_address="localhost:9092",
        consumer_group="coin_group",
        auto_offset_reset="earliest",
    )

    messages_topic = app.topic(name="messages", value_deserializer="json")

    sdf = app.dataframe(topic=messages_topic)

    sdf = sdf.apply(extract_coin_data)

    sdf.update(lambda coin_data: print(coin_data))

    postgres_sink = create_postgres_sink()

    sdf.sink(postgres_sink)
    app.run()


if __name__ == "__main__":
    main()