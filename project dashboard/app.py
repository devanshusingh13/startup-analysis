import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='startup analysis')
df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
# data cleaning


def load_overall_details():
    st.title('Overall Analysis')
    # toatal invested amount
    total = round(df['amount'].sum())
    # max funding
    max_funding = df.groupby('startup')['amount'].max(
    ).sort_values(ascending=False).head(1).values[0]
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    # funded startup
    funded_startup = df['startup'].nunique()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Total', str(total) + 'Cr')
    with col2:
        st.metric('Max', str(max_funding) + 'Cr')
    with col3:
        st.metric('Avg', str(round(avg_funding)) + 'Cr')
    with col4:
        st.metric('Funded Startup', str(funded_startup))

    st.header('MoM graph')
    temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    temp_df['x_axis'] = temp_df['month'].astype(
        'str') + '-' + temp_df['year'].astype('str')

    fig4, ax4 = plt.subplots()
    ax4.plot(temp_df['x_axis'], temp_df['amount'])  # type: ignore
    st.pyplot(fig4)


def load_investor_details(investor):
    st.title(investor)
    # load last 5 investment
    last_5df = df[df['investors'].str.contains(investor)].head()[
        ['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investment')
    st.dataframe(last_5df)
    col1, col2 = st.columns(2)
    with col1:

        # biggest investment
        big_series = df[df['investors'].str.contains(investor)].groupby(
            'startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)  # type: ignore
        st.pyplot(fig)
    with col2:
        vertical_series = df[df['investors'].str.contains(
            investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index,  # type: ignore
                autopct="%0.01f%%")  # type: ignore
        st.pyplot(fig1)
    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')[
        'amount'].sum()
    st.subheader('YoY Investments')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index, year_series.values)  # type: ignore
    st.pyplot(fig2)


st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox(
    'Select One', ['Overall Analysis', 'StartUp', 'Investor'])
if option == 'Overall Analysis':
    btn3 = st.sidebar.button('Overall details')
    if btn3:
        load_overall_details()

elif option == 'Startup':
    st.sidebar.selectbox('Select Startup', sorted(
        df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')
else:
    selected_investor = st.sidebar.selectbox('Select Startup', sorted(
        set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)
