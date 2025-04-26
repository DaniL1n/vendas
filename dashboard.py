# python -m streamlit run app.py

# Importação das bibliotecas necessárias
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Título do dashboard
st.title("Dashboard de Funcionários")

# Caminho do arquivo CSV na mesma pasta
csv_file = 'Employee_Data.csv'

# Verifica se o arquivo CSV existe na mesma pasta
if os.path.exists(csv_file):
    # Lê o arquivo CSV em um DataFrame
    df = pd.read_csv(csv_file)

    # Exibe os dados carregados
    st.markdown("### Dados de Funcionários Carregados")
    st.dataframe(df.head())

    # Conversão da coluna "Date_of_Joining" para formato de data
    df['Date_of_Joining'] = pd.to_datetime(df['Date_of_Joining'], format='%Y-%m-%d')

    # Filtros de seleção
    st.sidebar.header("Filtros")
    selected_department = st.sidebar.multiselect(
        "Selecione o Departamento",
        options=df['Department'].unique(),
        default=df['Department'].unique()
    )
    selected_date_range = st.sidebar.date_input(
        "Selecione o Período de Admissão",
        [df['Date_of_Joining'].min(), df['Date_of_Joining'].max()]
    )

    # Filtragem dos dados com base na seleção do usuário
    filtered_df = df[
        (df['Department'].isin(selected_department)) &
        (df['Date_of_Joining'] >= pd.to_datetime(selected_date_range[0])) &
        (df['Date_of_Joining'] <= pd.to_datetime(selected_date_range[1]))
    ]

    # Exibe os dados filtrados
    st.markdown("### Dados Filtrados")
    st.dataframe(filtered_df)

    # Insights gerais
    st.markdown("## Insights Gerais")
    avg_performance = filtered_df['Performance_Score'].mean()
    avg_training_hours = filtered_df['Training_Hours'].mean()
    avg_salary = filtered_df['Salary'].mean()
    st.write(f"**Média da Performance:** {avg_performance:.2f}")
    st.write(f"**Média de Horas de Treinamento:** {avg_training_hours:.2f} horas")
    st.write(f"**Média Salarial:** R$ {avg_salary:,.2f}")

    # Gráfico de quantidade de funcionários por departamento
    st.markdown("### Funcionários por Departamento")
    employees_by_department = filtered_df['Department'].value_counts()
    st.bar_chart(employees_by_department)

    # Gráfico de performance média por departamento
    st.markdown("### Performance Média por Departamento")
    performance_by_department = filtered_df.groupby('Department')['Performance_Score'].mean().sort_values(ascending=False)
    st.bar_chart(performance_by_department)

    # Gráfico de evolução de admissões ao longo do tempo
    st.markdown("### Admissões ao Longo do Tempo")
    admissions_over_time = filtered_df.groupby('Date_of_Joining').size()
    st.line_chart(admissions_over_time)

    # Salário médio por departamento
    st.markdown("### Salário Médio por Departamento")
    salary_by_department = filtered_df.groupby('Department')['Salary'].mean().sort_values(ascending=False)
    st.bar_chart(salary_by_department)

    # Explicação do Streamlit
    st.markdown("## Sobre o Streamlit")
    st.write("""
    **Streamlit** é uma biblioteca de Python de código aberto que permite criar e compartilhar aplicativos de dados 
    interativos de forma fácil e rápida. Ela transforma scripts em uma interface de usuário web amigável e intuitiva 
    sem a necessidade de conhecimento em desenvolvimento web. Abaixo estão os principais conceitos utilizados neste exemplo:

    - `st.title()`: Adiciona um título ao seu aplicativo.
    - `st.markdown()`: Permite adicionar textos em formato Markdown.
    - `st.dataframe()`: Exibe um DataFrame do Pandas.
    - `st.sidebar`: Permite adicionar componentes de entrada e seleção na barra lateral do aplicativo.
    - `st.multiselect()`: Adiciona uma caixa de seleção múltipla.
    - `st.date_input()`: Adiciona um componente de seleção de data.
    - `st.bar_chart()`: Cria um gráfico de barras.
    - `st.line_chart()`: Cria um gráfico de linha.
    """)
else:
    st.write(f"Arquivo '{csv_file}' não encontrado. Por favor, coloque o arquivo na mesma pasta que este script.")
