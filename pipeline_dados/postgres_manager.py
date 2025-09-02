import pandas as pd
from sqlalchemy import create_engine, text


# Conexão com o banco de dados
def connect_to_postgres():
    engine = create_engine('postgresql://postgres-iot:12345@localhost:5432/database')
    return engine


# Criação da tabela
def create_table(engine):
    query = """
        CREATE TABLE IF NOT EXISTS iot_temp_log (
        id VARCHAR(100) PRIMARY KEY,
        room_id VARCHAR(100),
        noted_date TIMESTAMP,
        temperature FLOAT,
        location VARCHAR(10)
    );
    """
    with engine.begin() as conn:
        conn.execute(text(query))


def insert_row(engine, row):
    # Conversão do timestamp para o formato correto do PostgreSQL
    noted_date = pd.to_datetime(row['noted_date'], dayfirst=True).strftime('%Y-%m-%d %H:%M:%S')

    # Converte a temperatura para float
    temperature = float(str(row['temp']).replace(',', '.'))

    query = text("""
                 INSERT INTO iot_temp_log (id, room_id, noted_date,
                 temperature, location)
                 VALUES (:id, :room_id, :noted_date, :temperature, :location)
                 ON CONFLICT (id) DO NOTHING
                 """)

    # Dicionário com os dados formatados
    params = {
        'id': row['id'],
        'room_id': row['room_id/id'],
        'noted_date': noted_date,
        'temperature': temperature,
        'location': row['out/in']
    }

    with engine.begin() as conn:
        conn.execute(query, params)


def load_data_into_postgres():
    engine = connect_to_postgres()

    # Garantir que a tabela seja criada se necessário
    create_table(engine)

    # Ler o CSV e garantir que a coluna timestamp seja interpretada
    # corretamente
    data = pd.read_csv('csv/IOT-temp.csv')

    for _, row in data.iterrows():
        try:
            insert_row(engine, row)
        except Exception as e:
            print(f"Erro ao inserir {row['id']}: {e}")


if __name__ == "__main__":
    load_data_into_postgres()
