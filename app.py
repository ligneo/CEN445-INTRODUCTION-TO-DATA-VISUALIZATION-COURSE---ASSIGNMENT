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
# iteractive charts CENK   #  (2,4,9)
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
# CHARTS of Hilmi   # -----------------

with tabs[3]:
    st.header("1. Chart (Parallel Coordinates): Regional Sales Profiles of Genres")
    st.markdown("Compares the regional sales profiles of different **Genres**. You can use brushing on the axes to highlight games that fit a specific sales pattern.")

    # Prepared by: Hilmi
    #st.markdown("**Prepared by: Hilmi**")

    # Select only the relevant columns for the plot.
    df_parallel = df_filtered[['Genre', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].copy()
    
    # Create the Parallel Coordinates Plot using Plotly Express
    fig_par = px.parallel_coordinates(
        df_parallel,
        color="Genre", # Color by Genre
        labels={
            "NA_Sales": "North America (NA)",
            "EU_Sales": "Europe (EU)",
            "JP_Sales": "Japan (JP)",
            "Other_Sales": "Other Regions"
        },
        title="Regional Sales Profiles by Game Genre (Million Dollars)"
    )

    # Move legend to the top-right
    fig_par.update_layout(legend_orientation="h", legend_y=1.1, legend_x=0.5)

    st.plotly_chart(fig_par, use_container_width=True)

with tabs[4]:
    st.header("2. Chart (Stacked Area Chart): Genre Market Share Change Over Years")
    st.markdown("Shows how the total market share of different **Genres** has changed over the **Years** (As a percentage of Global Sales).")

    # Prepared by: Hilmi
    #st.markdown("**Prepared by: Hilmi**")

    # 1. Calculate total sales by Year and Genre
    sales_by_year_genre = df_filtered.groupby(['Year', 'Genre'])['Global_Sales'].sum().reset_index()

    # 2. Calculate total sales for each Year
    total_sales_by_year = sales_by_year_genre.groupby('Year')['Global_Sales'].transform('sum')

    # 3. Calculate Market Share (%)
    sales_by_year_genre['Market_Share'] = (sales_by_year_genre['Global_Sales'] / total_sales_by_year) * 100
    
    # Create the Stacked Area Chart
    fig_area = px.area(
        sales_by_year_genre,
        x='Year',
        y='Market_Share',
        color='Genre',
        title='Game Genre Market Share of Global Sales Over Years (%)',
        # Add necessary information for hover
        hover_data={
            'Market_Share': ':.2f', # Format percentage to 2 decimal places
            'Global_Sales': ':.2f',
            'Year': False
        },
        labels={'Market_Share': 'Market Share (%)', 'Year': 'Release Year', 'Genre': 'Game Genre'}
    )
    
    # Update axes and hover behavior
    fig_area.update_layout(
        yaxis_title='Market Share (%)',
        xaxis_title='Release Year',
        yaxis_tickformat='.0f',
        hovermode="x unified"
    )
    
    st.plotly_chart(fig_area, use_container_width=True)

with tabs[5]:
    st.header("3. Chart (Ranked Bar Chart): Top 20 Best-Selling Games of All Time")
    st.markdown("Shows the top 20 games by total global sales from the filtered dataset.")

    # Prepared by: Hilmi
    st.markdown("**Prepared by: Hilmi**")

    # Sort by Global_Sales and select the top 20
    df_top_20 = df_filtered.sort_values(by='Global_Sales', ascending=False).head(20)

    # Create the Ranked Bar Chart
    fig_bar_top = px.bar(
        df_top_20,
        y='Name', # Game Name (Y-axis)
        x='Global_Sales', # Global Sales (X-axis)
        orientation='h', # Horizontal bar chart
        color='Global_Sales', # Color by Sales value
        color_continuous_scale=px.colors.sequential.Plotly3,
        title='Top 20 Games by Global Sales (Million Dollars)',
        # Add Publisher, Platform, and Year to the tooltip (hover)
        hover_data=['Publisher', 'Platform', 'Year'],
        labels={'Global_Sales': 'Global Sales (Million Dollars)', 'Name': 'Game Name'}
    )
    
    # Reverse the Y-axis order to put the best-seller at the top
    fig_bar_top.update_layout(yaxis={'categoryorder':'total ascending'})

    st.plotly_chart(fig_bar_top, use_container_width=True)


# -----------------
# 3 CHARTS ---- MODIFY below  -------
# -----------------

with tabs[6]:
    st.header(" 4's Chart (e.g., Violin Plot)")
    st.warning("this will be modified ->  E.g., An advanced version of the box plot (Violin).")

with tabs[7]:
    st.header(" 5's Chart (e.g., Sunburst)")
    st.warning("this will be modified ->  E.g., A circular version of the treemap (Sunburst).")

with tabs[8]:
    st.header(" 6's Chart (e.g., Parallel Coordinates)")
    st.warning("this will be modified ->  E.g., Sales profile of genres by region (Parallel Coords).")
