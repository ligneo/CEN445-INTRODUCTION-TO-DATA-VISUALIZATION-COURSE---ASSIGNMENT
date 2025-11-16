import streamlit as st
import pandas as pd
import plotly.express as px


# page configuration
st.set_page_config(
    page_title="Video Game Sales Dashboard",
    page_icon="🎮",
    layout="wide"  # Use wide layout for graphs
)


# Data Loading and Preparation
@st.cache_data
def load_data():
    """
    Loads, cleans, and prepares the vgsales.csv dataset.
    
    Returns:
        pd.DataFrame: A cleaned DataFrame.
        None: If the file is not found.

    """
    try:
        df = pd.read_csv("vgsales.csv")
        
        df.dropna(subset=['Year', 'Publisher'], inplace=True)
        
        df['Year'] = df['Year'].astype(int)
        
        return df
    except FileNotFoundError:
        st.error("Error: 'vgsales.csv' not found. Please ensure the file is in the same directory as 'app.py'.")
        return None

df = load_data()

if df is None:
    st.stop()




# sidebar 
st.sidebar.header("Filter Options 🎮")


all_genres = df['Genre'].unique()

selected_genres = st.sidebar.multiselect(
    'Select Genre(s):',
    options=all_genres,
    default=all_genres[:5]  # Default to the first 5 genres
)


min_year = int(df['Year'].min())
max_year = int(df['Year'].max())


selected_year_range = st.sidebar.slider(
    'Select Year Range:',
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)  # Default to the full range
)


df_filtered = df[
    (df['Genre'].isin(selected_genres)) &
    (df['Year'] >= selected_year_range[0]) &
    (df['Year'] <= selected_year_range[1])
]

# sidebar-small-info
st.sidebar.info(f"{len(df_filtered)} games found based on selected filters.")


# Dashboard
st.title("Video Game Sales - Exploratory Dashboard")
st.write("This dashboard is for analyzing the `vgsales` dataset. Use the sidebar on the left to change filters.")

# laod 9 chart
tab_list = [
    "📈 Scatter (Cenk)", 
    "📊 Box Plot (Cenk)", 
    "🌳 Treemap (Cenk)",
    "Team 1: Bar Chart", 
    "Team 2: Histogram", 
    "Team 3: Heatmap",
    "Team 4: Violin", 
    "Team 5: Sunburst", 
    "Team 6: Parallel"
]
tabs = st.tabs(tab_list)


# -----------------
# iteractive charts CENK   #  (2,4,7)
# -----------------

# Chart 1: Scatter Plot
with tabs[0]:
    st.header("Chart 1: North America vs. Europe Sales (Scatter)")
    st.markdown("This chart shows the relationship between `NA_Sales` and `EU_Sales` for the selected genres and years. You can see the game name by hovering over the points.")
    
    # Create the interactive chart with Plotly Express
    fig_scatter = px.scatter(
        df_filtered,  
        x='NA_Sales',
        y='EU_Sales',
        color='Genre',  # Differentiate colors by genre
        hover_data=['Name', 'Platform', 'Year'],  # Show this info on hover
        title="NA Sales vs. EU Sales by Genre"
    )
    # display
    st.plotly_chart(fig_scatter, use_container_width=True)

# Chart 2: Box Plot
with tabs[1]:
    st.header("Chart 2: Global Sales Distribution by Genre (Box)")
    st.markdown("This chart compares the `Global_Sales` distribution (median, quartiles, outliers) of the selected genres.")
    
    fig_box = px.box(
        df_filtered, 
        x='Genre',
        y='Global_Sales',
        color='Genre',
        title="Global Sales Distribution by Genre"
    )
    st.plotly_chart(fig_box, use_container_width=True)

# Chart 3: Treemap
with tabs[2]:
    st.header("Chart 3: Publisher and Platform Market Share (Treemap)")
    st.markdown("This chart hierarchically shows which publisher and their platforms dominate the market, based on the **entire dataset** (unfiltered). You can drill down by clicking on a box.")
    
    # Note: A treemap is often more meaningful with unfiltered data to see the entire market.
    fig_tree = px.treemap(
        df,  
        path=[px.Constant("Entire Market"), 'Publisher', 'Genre', 'Platform'],  # Hierarchy
        values='Global_Sales',
        title="Market Share Hierarchy: Publisher -> Genre -> Platform"
    )
    fig_tree.update_traces(root_color="lightgrey")
    fig_tree.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(fig_tree, use_container_width=True)






# -----------------
# 6 CHARTS ---- MODIFY below  -------
# -----------------

with tabs[3]:
    st.header(" 1's Chart (e.g., Bar Chart)")
    st.warning("this will be modified ->  E.g., Top 10 selling publishers (Bar Chart).")
    # ----- MODIFY your spot ----
    # Example:
    # pub_sales = df_filtered.groupby('Publisher')['Global_Sales'].sum().nlargest(10).reset_index()
    # fig_bar = px.bar(pub_sales, x='Publisher', y='Global_Sales', title='Top 10 Publishers')
    # st.plotly_chart(fig_bar, use_container_width=True)

with tabs[4]:
    st.header(" 2's Chart (e.g., Histogram)")
    st.warning("this will be modified ->  E.g., Number of game releases per year (Histogram).")

with tabs[5]:
    st.header(" 3's Chart (e.g., Heatmap)")
    st.warning("this will be modified ->  E.g., Sales correlation between regions (Heatmap).")

with tabs[6]:
    st.header(" 4's Chart (e.g., Violin Plot)")
    st.warning("this will be modified ->  E.g., An advanced version of the box plot (Violin).")

with tabs[7]:
    st.header(" 5's Chart (e.g., Sunburst)")
    st.warning("this will be modified ->  E.g., A circular version of the treemap (Sunburst).")

with tabs[8]:
    st.header(" 6's Chart (e.g., Parallel Coordinates)")
    st.warning("this will be modified ->  E.g., Sales profile of genres by region (Parallel Coords).")
