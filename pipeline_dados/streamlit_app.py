import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Conexão com o banco de dados
engine = create_engine('postgresql://postgres-iot:12345@localhost:5432/database')


# Função para carregar dados de uma view
def load_data(view_name):
    return pd.read_sql(f"SELECT * FROM {view_name}", engine)


# Função principal do Streamlit
def main():
    # Título do dashboard
    st.title('Dashboard de Temperaturas IoT')

    st.header('Tabela de Leituras de Temperaturas (Dados Brutos)')
    df = load_data('iot_temp_log')
    st.dataframe(df)

    st.markdown("---")

    # Gráfico 1: Média de temperatura por local (In / Out)
    st.header('Média de Temperatura por Local')
    df_avg_temp = load_data('avg_temp_por_local')
    fig1 = px.bar(
        df_avg_temp,
        x='location',
        y='avg_temp',
        color='location',
        color_discrete_sequence=px.colors.qualitative.Set2,
        text='avg_temp'
    )
    fig1.update_layout(showlegend=True)
    st.plotly_chart(fig1)

    # Gráfico 2: Contagem de leituras por hora
    st.header('Leituras por Hora do Dia')
    df_leituras_hora = load_data('leituras_por_hora')
    fig2 = px.line(df_leituras_hora, x='hora', y='contagem')
    st.plotly_chart(fig2)

    # Gráfico 3: Temperaturas máximas e mínimas por dia
    st.header('Temperaturas Máximas e Mínimas por Dia')
    df_temp_max_min = load_data('temp_max_min_por_dia')
    fig3 = px.line(df_temp_max_min, x='data', y=['temp_max', 'temp_min'])
    st.plotly_chart(fig3)


if __name__ == '__main__':
    main()
