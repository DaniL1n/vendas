# python -m streamlit run app.py

# Importação das bibliotecas necessárias
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título do dashboard
st.title("📊 Dashboard de Vendas de Produtos")

# Caminho do arquivo CSV (assumimos que está na mesma pasta)
csv_file = 'sales_data.csv'

try:
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
    filtered_df = df[
        (df['Category'].isin(selected_category)) &
        (df['Product_Name'].isin(selected_product)) &
        (df['Date_Sold'] >= pd.to_datetime(selected_date_range[0])) &
        (df['Date_Sold'] <= pd.to_datetime(selected_date_range[1]))
    ]

    # Exibe os dados filtrados
    st.markdown("### 📄 Dados Filtrados")
    st.dataframe(filtered_df)

    # Insights gerais
    st.markdown("## 📈 Insights Gerais")
    col1, col2 = st.columns(2)

    total_sales = filtered_df['Total_Sales'].sum()
    total_quantity = filtered_df['Quantity_Sold'].sum()

    col1.metric(label="💰 Total de Vendas", value=f"R$ {total_sales:,.2f}")
    col2.metric(label="📦 Total de Unidades Vendidas", value=f"{total_quantity}")

    # Gráfico de Vendas por Produto
    st.markdown("### 🛒 Vendas por Produto")
    sales_by_product = filtered_df.groupby('Product_Name')['Total_Sales'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 5))
    sales_by_product.plot(kind='bar', ax=ax)
    ax.set_ylabel("Total de Vendas (R$)")
    ax.set_xlabel("Produto")
    ax.set_title("Vendas Totais por Produto")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    # Gráfico de Vendas por Categoria
    st.markdown("### 🗂️ Vendas por Categoria")
    sales_by_category = filtered_df.groupby('Category')['Total_Sales'].sum().sort_values(ascending=False)
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sales_by_category.plot(kind='bar', color='green', ax=ax2)
    ax2.set_ylabel("Total de Vendas (R$)")
    ax2.set_xlabel("Categoria")
    ax2.set_title("Vendas Totais por Categoria")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig2)

    # Evolução das Vendas ao Longo do Tempo
    st.markdown("### 📅 Evolução das Vendas ao Longo do Tempo")
    sales_over_time = filtered_df.groupby('Date_Sold')['Total_Sales'].sum()
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sales_over_time.plot(ax=ax3)
    ax3.set_ylabel("Total de Vendas (R$)")
    ax3.set_xlabel("Data")
    ax3.set_title("Total de Vendas ao Longo do Tempo")
    plt.xticks(rotation=45)
    st.pyplot(fig3)

    # Preço Médio por Categoria
    st.markdown("### 💲 Preço Médio por Categoria")
    avg_price_by_category = filtered_df.groupby('Category')['Price'].mean().sort_values(ascending=False)
    fig4, ax4 = plt.subplots(figsize=(8, 4))
    avg_price_by_category.plot(kind='bar', color='orange', ax=ax4)
    ax4.set_ylabel("Preço Médio (R$)")
    ax4.set_xlabel("Categoria")
    ax4.set_title("Preço Médio por Categoria")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig4)

except FileNotFoundError:
    st.error(f"❌ Arquivo '{csv_file}' não encontrado. Por favor, coloque o arquivo na mesma pasta que este script.")
