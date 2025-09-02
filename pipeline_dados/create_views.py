from sqlalchemy import create_engine, text

# Conexão com o banco de dados
engine = create_engine('postgresql://postgres-iot:12345@localhost:5432/database')


def create_views():
    with engine.begin() as conn:
        # Média de temperatura por local (In / Out)
        conn.execute(text("""
            CREATE OR REPLACE VIEW avg_temp_por_local AS
            SELECT location, AVG(temperature) AS avg_temp
            FROM iot_temp_log
            GROUP BY location;
        """))

        # Contagem de leituras por hora
        conn.execute(text("""
            CREATE OR REPLACE VIEW leituras_por_hora AS
            SELECT EXTRACT(HOUR FROM noted_date) AS hora, COUNT(*) AS contagem
            FROM iot_temp_log
            GROUP BY EXTRACT(HOUR FROM noted_date)
            ORDER BY hora;
        """))

        # Temperatura máxima e mínima por dia
        conn.execute(text("""
            CREATE OR REPLACE VIEW temp_max_min_por_dia AS
            SELECT DATE(noted_date) AS data,
                   MAX(temperature) AS temp_max,
                   MIN(temperature) AS temp_min
            FROM iot_temp_log
            GROUP BY DATE(noted_date)
            ORDER BY data;
        """))

    print("Views criadas com sucesso!")


if __name__ == "__main__":
    create_views()
