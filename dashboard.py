# python -m streamlit run app.py

# Importação das bibliotecas necessárias
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Título do dashboard
st.title("📊 Dashboard de Vendas de Produtos")

# Caminho do arquivo CSV na mesma pasta
csv_file = 'Product_Sales_Data.csv'

# Verifica se o arquivo CSV existe na mesma pasta
if os.path.exists(csv_file):
    # Lê o arquivo CSV em um DataFrame
    df = pd.read_csv(csv_file)

    # Exibe os dados carregados
    st.markdown("### 📄 Dados de Vendas Carregados")
    st.dataframe(df.head())

    # Conversão da coluna "Date_Sold" para formato de data
    df['Date_Sold'] = pd.to_datetime(df['Date_Sold'], format='%Y-%m-%d')

    # Filtros de seleção na barra lateral
    st.sidebar.header("Filtros")
    selected_category = st.sidebar.multiselect("Selecione a Categoria", options=df['Category'].unique(), default=df['Category'].unique())
    selected_product = st.sidebar.multiselect("Selecione o Produto", options=df['Product_Name'].unique(), default=df['Product_Name'].unique())
    selected_date_range = st.sidebar.date_input("Selecione o Período", [df['Date_Sold'].min(), df['Date_Sold'].max()])

    # Filtragem dos dados com base na seleção do usuário
    filtered_df = df[(df['Category'].isin(selected_category)) & 
                     (df['Product_Name'].isin(selected_product)) &
                     (df['Date_Sold'] >= pd.to_datetime(selected_date_range[0])) & 
                     (df['Date_Sold'] <= pd.to_datetime(selected_date_range[1]))]

    # Exibe os dados filtrados
    st.markdown("### 📄 Dados Filtrados")
    st.dataframe(filtered_df)

    # Insights gerais em colunas
    st.markdown("## 📈 Insights Gerais")
    col1, col2 = st.columns(2)

    total_sales = filtered_df['Total_Sales'].sum()
    total_quantity = filtered_df['Quantity_Sold'].sum()

    col1.metric(label="💰 Total de Vendas", value=f"R$ {total_sales:,.2f}")
    col2.metric(label="📦 Total de Unidades Vendidas", value=f"{total_quantity}")

    # Gráfico de Vendas por Produto
    st.markdown("### 🛒 Vendas por Produto")
    sales_by_product = filtered_df.groupby('Product_Name')['Total_Sales'].sum().sort_values(ascending=False).reset_index()
    fig_product = px.bar(sales_by_product, x='Product_Name', y='Total_Sales', color='Total_Sales', 
                         color_continuous_scale='Blues', title="Vendas Totais por Produto")
    st.plotly_chart(fig_product)

    # Gráfico de Vendas por Categoria
    st.markdown("### 🗂️ Vendas por Categoria")
    sales_by_category = filtered_df.groupby('Category')['Total_Sales'].sum().sort_values(ascending=False).reset_index()
    fig_category = px.bar(sales_by_category, x='Category', y='Total_Sales', color='Total_Sales', 
                          color_continuous_scale='Greens', title="Vendas Totais por Categoria")
    st.plotly_chart(fig_category)

    # Evolução das Vendas ao Longo do Tempo
    st.markdown("### 📅 Evolução das Vendas ao Longo do Tempo")
    sales_over_time = filtered_df.groupby('Date_Sold')['Total_Sales'].sum().reset_index()
    fig_time = px.line(sales_over_time, x='Date_Sold', y='Total_Sales', markers=True, title="Total de Vendas ao Longo do Tempo")
    st.plotly_chart(fig_time)

    # Preço Médio por Categoria
    st.markdown("### 💲 Preço Médio por Categoria")
    avg_price_by_category = filtered_df.groupby('Category')['Price'].mean().sort_values(ascending=False).reset_index()
    fig_avg_price = px.bar(avg_price_by_category, x='Category', y='Price', color='Price',
                           color_continuous_scale='Oranges', title="Preço Médio por Categoria")
    st.plotly_chart(fig_avg_price)

    # Explicação do Streamlit
    st.markdown("## ℹ️ Sobre o Streamlit")
    st.write("""
    **Streamlit** é uma biblioteca de Python de código aberto que facilita a criação de dashboards e aplicações de dados 
    de maneira rápida e interativa. Este app utiliza:

    - `st.title()`, `st.markdown()`, `st.dataframe()`, `st.sidebar` para layout e filtros
    - `st.metric()` para KPIs
    - `plotly.express` para gráficos interativos
    """)
else:
    st.error(f"Arquivo '{csv_file}' não encontrado. Por favor, coloque o arquivo na mesma pasta que este script.")
