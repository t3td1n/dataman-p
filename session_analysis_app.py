import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Session End Reason Analysis", layout="wide")
st.title("📊 Session End Reason Analysis")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = [col.strip() for col in df.columns]

    # Rename columns if necessary
    if '' in df.columns:
        df = df.drop(columns=[''])

    # Convert Generate Time to datetime
    df['Generate Time'] = pd.to_datetime(df['Generate Time'], errors='coerce')
    df = df.dropna(subset=['Generate Time'])

    # Trend of session end reasons over time
    trend_data = df.groupby([pd.Grouper(key='Generate Time', freq='5min'), 'Session End Reason'])['Count'].sum().reset_index()
    fig_trend = px.line(trend_data, x='Generate Time', y='Count', color='Session End Reason',
                        title='Trend of Session End Reasons Over Time',
                        labels={'Generate Time': 'Time', 'Count': 'Session Count'})
    st.plotly_chart(fig_trend, use_container_width=True)

    # Distribution of session end reasons
    distribution_data = df.groupby('Session End Reason')['Count'].sum().reset_index()
    fig_distribution = px.bar(distribution_data, x='Session End Reason', y='Count',
                              title='Distribution of Session End Reasons',
                              labels={'Session End Reason': 'Session End Reason', 'Count': 'Total Count'})
    st.plotly_chart(fig_distribution, use_container_width=True)
else:
    st.info("Please upload a CSV file to begin analysis.")
