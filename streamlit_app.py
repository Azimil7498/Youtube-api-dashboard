import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="YouTube Data Analysis", layout="wide")

# Load Data
try:
    full_df = pd.read_csv("youtube_video_data.csv")
except FileNotFoundError:
    st.error("CSV file not found. Please upload 'youtube_video_data.csv' to the app directory.")
    st.stop()

# Rename columns to match expected names
rename_map = {
    'Video Title': 'title',
    'Channel': 'channel_title',
    'Views': 'views',
    'Likes': 'likes',
    'Comments': 'comment_count'
}
full_df.rename(columns=rename_map, inplace=True)

# Check required columns
required_columns = {'channel_title', 'views', 'likes', 'comment_count', 'title'}
if not required_columns.issubset(full_df.columns):
    st.error(f"CSV must contain these columns: {', '.join(required_columns)}")
    st.stop()

# Page Title
st.title("📊 YouTube Dataset Analysis Dashboard")
st.write("Welcome to your visual data adventure, powered by Python + Streamlit 🚀")

# Sidebar Filters
st.sidebar.title("🔍 Filters")
channels = st.sidebar.multiselect("Select Channels", full_df['channel_title'].unique())
if channels:
    full_df = full_df[full_df['channel_title'].isin(channels)]

# 🔥 Top 10 Videos by Views
st.subheader("🔥 Top 10 Videos by Views")
top_views = full_df.sort_values('views', ascending=False).head(10)
fig1, ax1 = plt.subplots(figsize=(12,6))
sns.barplot(data=top_views, x='title', y='views', ax=ax1, palette="coolwarm")
plt.xticks(rotation=45, ha='right')
st.pyplot(fig1)

# 💖 Likes vs Views
st.subheader("💖 Likes vs Views")
fig2, ax2 = plt.subplots(figsize=(10,6))
sns.scatterplot(data=full_df, x='views', y='likes', hue='channel_title', ax=ax2)
st.pyplot(fig2)

# 💬 Comments vs Views
st.subheader("💬 Comments vs Views")
fig3, ax3 = plt.subplots(figsize=(10,6))
sns.scatterplot(data=full_df, x='views', y='comment_count', hue='channel_title', ax=ax3)
st.pyplot(fig3)
# KPIs Section
total_views = full_df['views'].sum()
total_likes = full_df['likes'].sum()
total_comments = full_df['comment_count'].sum()
avg_views = full_df['views'].mean()

st.markdown("### 📌 Key Performance Indicators (KPIs)")
col1, col2, col3, col4 = st.columns(4)
col1.metric("📺 Total Views", f"{total_views:,}")
col2.metric("❤️ Total Likes", f"{total_likes:,}")
col3.metric("💬 Total Comments", f"{total_comments:,}")
col4.metric("📊 Avg Views per Video", f"{avg_views:,.0f}")
