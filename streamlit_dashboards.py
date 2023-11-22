import pandas as pd
import plotly.express as px
import streamlit as st


@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io='supermarket_sales.xlsx',
        # engine='openpyxl',
        sheet_name='sales',
        # skiprows=3,
        # usecols='B:R',
        # nrows=1000,
    )
    df['hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour
    return df


df = get_data_from_excel()

# Side Bar
st.sidebar.header('Filtre os dados'.center(50))
city = st.sidebar.multiselect(
    'Selecione a cidade:',
    options=df['City'].unique(),
    default=df['City'].unique()
)

costumer_type = st.sidebar.multiselect(
    'Selecione o tipo de cliente:',
    options=df['Costumer_type'].unique(),
    default=df['Costumer_type'].unique()
)

gender = st.sidebar.multiselect(
    'Selecione o Género:',
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

df_selection = df.query(
    'City == @city & Costumer_type == @costumer_type & Gender == @gender'
)
st.dataframe(df_selection)

st.title('Vendas no Dashboard')
st.markdown('##')
total_sales = int(df_selection['Total'].sum())
star_rating = round(df_selection['Rating'].mean(), 1)
average_sale_by_transaction = round(df_selection['Total'].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader('Vendas Totais:')
    st.subheader(f'US MTN {total_sales:,}')
with middle_column:
    st.subheader('Classificação:')
    st.subheader(f'US MTN {star_rating:,}')
with right_column:
    st.subheader('Média das vendas:')
    st.subheader(f'US MTN {average_sale_by_transaction:,}')
st.markdown('---')
sales_by_product_line = (
    df_selection.groupby(by=['Product line']).sum()[['Total']].sort_values(by='Total'
                                                                           )
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x='Total',
    y=sales_by_product_line.index,
    orientation='h',
    title='<b>Vendas por linha de Produto</b>',
    color_discrete_sequence=['#0083B8'] * len(sales_by_product_line),
    template='plotly_white',
)

fig_product_sales.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False))
)

st.plotly_chart(fig_product_sales)

# sales by hour [Bar chart]
sales_by_hour = df_selection.groupby(by=['hour']).sum()[['Total']]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y='Total',
    title='<b> Vendas por horas </b>',
    color_discrete_sequence=['#0083B8'] * len(sales_by_hour),
    template='plotly_white',
)

st.plotly_chart(fig_hourly_sales)


