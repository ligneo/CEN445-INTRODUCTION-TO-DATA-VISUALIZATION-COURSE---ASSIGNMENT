import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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
    "📈 Stacked Area (İlhan)",
    "🌊 Sankey (İlhan)", 
    "📉 Line Chart (İlhan)",
    "📊 Parallel Coordinates (Hilmi)", 
    "📈 Stacked Area (Hilmi)", 
    "🏆 Top 20 Games (Hilmi)"
]
tabs = st.tabs(tab_list)


# -----------------
# scatter plot,  box plot,  treemap Charts -  CENK
# -----------------

# Chart 1: Scatter Plot 
with tabs[0]:
    st.header("Chart 1: Regional Sales Correlation (Interactive Scatter)")
    st.markdown("Examine the relationship between North American (`NA_Sales`) and European (`EU_Sales`) sales. The marginal histograms on the sides show the distribution density of the data.")

    # colums for interactions
    c1, c2 = st.columns([1, 3])





    with c1:
        st.markdown("### ⚙️ Settings")
        # logarithmic scale
        log_scale = st.checkbox(
            "Logarithmic Scale", 
            value=False, 
            help="Use this to visualize small and large sales values clearly on the same chart."
        )
        
        # point sizing 
        size_metric = st.checkbox(
            "Size points by Global Sales", 
            value=True, 
            help="If checked, the size of the bubbles will indicate the total global sales success."
        )
        
        # trendline   
        ## ModuleNotFoundError
        show_trend = st.checkbox(
            "Show Trendline (OLS)", 
            value=False, 
            help="Adds a linear regression line to visualize the general correlation trend."
        )



    with c2:
        # Create Scatter Plot
        fig_scatter = px.scatter(
            df_filtered,  
            x='NA_Sales',
            y='EU_Sales',
            color='Genre',              # Color differentiation by Genre
            size='Global_Sales' if size_metric else None, # Bubble size logic
            hover_name='Name',          # Show Game Name on hover
            hover_data=['Platform', 'Year', 'Publisher'],
            title="NA Sales vs. EU Sales (with Marginal Distributions)",
            marginal_x="histogram",     # Top margin: Histogram
            marginal_y="histogram",     # Right margin: Histogram
            trendline="ols" if show_trend else None, # Optional trendline
            log_x=log_scale,            # Logarithmic axis settings
            log_y=log_scale,
            template="plotly_white",    # Clean background
            opacity=0.7                 # Transparency for overlapping points
        )
        
        # Styling adjustments
        fig_scatter.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=50, b=20),
            height=600
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)







# Chart 2: Box Plot 
### bug : genre selection? 
### outliners scatter the image  \ log scale or fixed scale selection
# Chart 2: Box Plot (Fixed: Focused View by Default)
with tabs[1]:
    st.header("Chart 2: Sales Distribution Analytics")
    st.markdown("Compare the sales distributions. By default, the view is **focused** on the main cluster of games to make the boxes visible.")

    # Layout: Sol tarafta Satış Tipi, Sağ tarafta Görünüm Modu (Zoom)
    c1, c2 = st.columns([2, 2])
    
    with c1:
        # Interaction: Select Sales Metric
        y_axis_option = st.radio(
            "Select Sales Metric:",
            ['Global_Sales', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'],
            horizontal=True,
            format_func=lambda x: x.replace('_', ' ')
        )
    
    with c2:
        # Interaction: View Mode (Zoom vs Full)
        # Senin istediğin "Default olarak zoomlu gelsin" mantığı burada
        view_mode = st.radio(
            "Y-Axis Scale Mode:",
            ["Focused", "Full Range (All Outliers)"],
            index=0,  # Index 0 seçili gelir (Focused) -> Kutular net gözükür
            horizontal=True,
            help="Focused mode clips extreme outliers to show the box distribution clearly."
        )
    
    # Custom Color Palette
    color_discrete_map = px.colors.qualitative.Bold

    fig_box = px.box(
        df_filtered, 
        x='Genre',
        y=y_axis_option,
        color='Genre',
        points="outliers", 
        notched=True,       
        title=f"{y_axis_option.replace('_', ' ')} Distribution by Genre",
        color_discrete_sequence=color_discrete_map
    )
    
    # Eksen Ayarlaması (Zoom Mantığı)
    if view_mode == "Focused":  # 0-5 
        #fig_box.update_yaxes(range=[0, 25])
        fig_box.update_yaxes(range=[0, 2])
    else:
        # Otomatik bırakıyoruz, en yüksek değere (82M) kadar uzuyor.
        fig_box.update_yaxes(autorange=True)

    fig_box.update_layout(
        xaxis_title="Game Genre",
        yaxis_title=f"{y_axis_option} (Million $)",
        legend_title_text="Genre List",
        height=600
    )
    
    st.plotly_chart(fig_box, use_container_width=True)




## Chart 3: Treemap 
# (Dynamic Hierarchy)
with tabs[2]:
    st.header("Chart 3: Market Hierarchy Explorer (Dynamic Treemap)")
    st.markdown("Who dominates the market? Explore the data from different angles by dynamically changing the hierarchy order.")

    col_tree1, col_tree2 = st.columns([1, 3])

    with col_tree1:
        st.info("💡 Tip: By changing the hierarchy order, you can answer questions like 'Which Publisher is strong in which Genre?' or 'Which Publisher dominates which Platform?'.")
        
        #dynamic hierarchy selection, interaction
        default_path = ['Publisher', 'Genre', 'Platform']
        path_options = ['Publisher', 'Genre', 'Platform', 'Year']
        
        selected_path = st.multiselect(
            "Select Hierarchy Order (Top -> Down):",
            options=path_options,
            default=default_path
        )
        
        #if empty
        if not selected_path:
            selected_path = default_path

        #coloring metric, interaction
        color_metric = st.selectbox(
            "Color Boxes By:",
            options=['Global_Sales', 'Year'],
            format_func=lambda x: "Total Sales (Heatmap)" if x == 'Global_Sales' else "Release Year (New vs Old)"
        )

    with col_tree2:
        # Treemaps are often more meaningful with the full dataset context, 
        # but here we use df_filtered to respect user's global filters.
        
        fig_tree = px.treemap(
            df_filtered,
            path=[px.Constant("All Games")] + selected_path,
            values='Global_Sales',
            color=color_metric, 
            # Red-Blue for Years, Viridis (Green-Purple) for Sales magnitude
            color_continuous_scale='RdBu_r' if color_metric == 'Year' else 'Viridis', 
            title=f"Market Hierarchy by {' > '.join(selected_path)}"
        )
        
        fig_tree.update_traces(
            root_color="lightgrey",
            hovertemplate='<b>%{label}</b><br>Sales: %{value:.2f}M$<br>%{parent}'
        )
        fig_tree.update_layout(margin=dict(t=50, l=0, r=0, b=0))
        
        st.plotly_chart(fig_tree, use_container_width=True)



#  --------------------


# -----------------
# CHARTS of Hilmi   # -----------------

with tabs[6]:
    st.header("Parallel Coordinates (Hilmi): Regional Sales Profiles of Genres")
    st.markdown("Compares the regional sales profiles of different **Genres**. You can use brushing on the axes to highlight games that fit a specific sales pattern.")

    # Prepared by: Hilmi
    st.markdown("**Prepared by: Hilmi**")

    # Select only the relevant columns for the plot.
    df_parallel = df_filtered[['Genre', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].copy()
    
    # Genre'yi sayısal bir ID'ye dönüştür (color parametresi için sayısal değer gerekli)
    genre_map = {genre: idx for idx, genre in enumerate(df_parallel['Genre'].unique())}
    df_parallel['Genre_ID'] = df_parallel['Genre'].map(genre_map)
    
    # Create the Parallel Coordinates Plot using Plotly Express
    # dimensions'da sadece sayısal kolonları kullan, color için Genre_ID kullan
    fig_par = px.parallel_coordinates(
        df_parallel,
        dimensions=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'],
        color="Genre_ID", # Color by Genre ID (sayısal değer)
        color_continuous_scale=px.colors.qualitative.Set3,
        labels={
            "NA_Sales": "North America (NA)",
            "EU_Sales": "Europe (EU)",
            "JP_Sales": "Japan (JP)",
            "Other_Sales": "Other Regions"
        },
        title="Regional Sales Profiles by Game Genre (Million Dollars)"
    )
    
    # Colorbar'ı gizle çünkü Genre_ID sayısal, Genre isimlerini gösteremeyiz
    fig_par.update_layout(
        coloraxis_showscale=False
    )
    
    # Genre bilgisini göstermek için bir bilgi notu ekle
    st.info("💡 Grafikteki renkler farklı oyun türlerini (Genre) temsil eder. Her tür için farklı bir renk kullanılmıştır.")

    st.plotly_chart(fig_par, use_container_width=True)

with tabs[7]:
    st.header("Stacked Area Chart (Hilmi): Genre Market Share Change Over Years")
    st.markdown("Shows how the total market share of different **Genres** has changed over the **Years** (As a percentage of Global Sales).")

    # Prepared by: Hilmi
    st.markdown("**Prepared by: Hilmi**")

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

with tabs[3]:
    st.header("Stacked Area Chart: Platform Popularity Over Years")
    st.markdown("This chart shows the sales trends of the top 12 platforms by total sales over the years in a stacked format. It visualizes the rise and fall of platforms (for example, PS2 being replaced by PS3).")
    
    # Veri hazırlığı - NaN değerleri temizle
    df_clean = df_filtered.dropna(subset=['Year', 'Global_Sales', 'Platform']).copy()
    df_clean['Year'] = df_clean['Year'].astype(int)
    
    # Grafik karmaşık olmasın diye EN ÇOK SATAN 12 PLATFORMU alıyoruz
    top_platforms = df_clean.groupby('Platform')['Global_Sales'].sum().nlargest(12).index
    df_chart = df_clean[df_clean['Platform'].isin(top_platforms)].copy()
    
    # Platform x Year, Global_Sales toplamı
    df_chart = df_chart.groupby(['Platform', 'Year'])['Global_Sales'].sum().reset_index()
    
    # Platformları çıkış yılına göre sıralayalım (Eskiden yeniye akış için)
    platform_order = df_chart.groupby('Platform')['Year'].min().sort_values().index
    
    # Tüm platform-yıl kombinasyonlarını oluştur (eksik olanları 0 ile doldur)
    # Bu, 2000'den önceki verilerin doğru gösterilmesi için önemli
    min_year = int(df_chart['Year'].min())
    max_year = int(df_chart['Year'].max())
    all_years = list(range(min_year, max_year + 1))
    all_platforms = list(df_chart['Platform'].unique())
    
    # Tüm kombinasyonları oluştur (pandas MultiIndex kullanarak)
    multi_index = pd.MultiIndex.from_product([all_platforms, all_years], names=['Platform', 'Year'])
    all_combinations = pd.DataFrame(index=multi_index).reset_index()
    
    # Mevcut verilerle birleştir ve eksik olanları 0 ile doldur
    df_chart = all_combinations.merge(df_chart, on=['Platform', 'Year'], how='left')
    df_chart['Global_Sales'] = df_chart['Global_Sales'].fillna(0)
    
    # Veri tiplerini düzelt
    df_chart['Year'] = df_chart['Year'].astype(int)
    df_chart['Global_Sales'] = df_chart['Global_Sales'].astype(float)
    
    # Yıla göre sırala (her platform için)
    df_chart = df_chart.sort_values(['Platform', 'Year']).reset_index(drop=True)
    
    # STACKED AREA CHART (YIĞILMIŞ ALAN GRAFİĞİ)
    fig_stacked = px.area(
        df_chart,
        x="Year",
        y="Global_Sales",
        color="Platform",
        category_orders={"Platform": list(platform_order)},  # Sıralı renklendirme
        title="Platform Market Share Over Years (Stacked)",
        template="plotly_dark",
        height=600  # Tek parça olduğu için aşırı yüksekliğe gerek yok
    )
    
    # Fine-tuning
    fig_stacked.update_layout(
        xaxis_title="Year",
        yaxis_title="Total Global Sales (Million)",
        legend_title="Platforms",
        hovermode='x unified'  # Mouse'un X eksenindeki konumuna göre o yılın tüm platform verilerini göster
    )
    
    # Hover'ın mouse'un grafikteki yerine göre o yılın verilerini göstermesi için trace'leri güncelle
    for trace in fig_stacked.data:
        trace.update(
            hovertemplate='<b>%{fullData.name}</b><br>' +
                          'Year: %{x}<br>' +
                          'Sales: %{y:.2f}M$<br>' +
                          '<extra></extra>',
            fill='tonexty',  # Stacked area için fill ayarı
            line=dict(width=0)  # Çizgi kalınlığını 0 yap, sadece alan hover'ı tetiklesin
        )
    
    st.plotly_chart(fig_stacked, use_container_width=True)

with tabs[4]:
    st.header("Sankey Diagram: Publisher → Genre → Platform Sales Flow")
    st.markdown("This chart shows a flow diagram of how the sales of the top 5 publishers flow to different game genres (Genre) and then to different platforms (Platform). Select a genre to highlight only its flows.")
    
    # En büyük 5 yayıncıyı bul (Global_Sales toplamına göre - filtrelenmiş veriden)
    top_publishers = df_filtered.groupby('Publisher')['Global_Sales'].sum().nlargest(5).index.tolist()
    df_sankey = df_filtered[df_filtered['Publisher'].isin(top_publishers)].copy()
    
    # Publisher -> Genre -> Platform akışını hesapla
    # Kaynak: Publisher, Hedef 1: Genre, Hedef 2: Platform
    # İki aşamalı akış: Publisher->Genre ve Genre->Platform
    
    # 1. Publisher -> Genre akışı
    pub_genre = df_sankey.groupby(['Publisher', 'Genre'])['Global_Sales'].sum().reset_index()
    pub_genre.columns = ['Source', 'Target', 'Value']
    
    # 2. Genre -> Platform akışı (aynı publisher'lar için)
    genre_platform = df_sankey.groupby(['Genre', 'Platform'])['Global_Sales'].sum().reset_index()
    genre_platform.columns = ['Source', 'Target', 'Value']
    
    # Tüm node'ları topla (unique değerler)
    all_nodes = set()
    all_nodes.update(pub_genre['Source'].unique())
    all_nodes.update(pub_genre['Target'].unique())
    all_nodes.update(genre_platform['Source'].unique())
    all_nodes.update(genre_platform['Target'].unique())
    
    # Node listesi oluştur
    node_list = sorted(list(all_nodes))
    node_dict = {node: idx for idx, node in enumerate(node_list)}
    
    # Node tiplerini belirle (Publisher, Genre, Platform)
    publisher_nodes = set(pub_genre['Source'].unique())
    genre_nodes = set(pub_genre['Target'].unique())
    platform_nodes = set(genre_platform['Target'].unique())
    
    # Genre seçimi için dropdown
    all_genres_list = sorted(list(genre_nodes))
    selected_genre = st.selectbox(
        "Select a Genre to Highlight:",
        options=['All'] + all_genres_list,
        index=0,
        key='sankey_genre_selector'
    )
    
    # Renk paletleri
    publisher_colors = px.colors.qualitative.Set1[:len(publisher_nodes)]
    genre_colors = px.colors.qualitative.Pastel[:len(genre_nodes)]
    platform_colors = px.colors.qualitative.Set3[:len(platform_nodes)]
    
    # Node renklerini atama (orijinal renkler)
    publisher_color_map = {pub: publisher_colors[i % len(publisher_colors)] 
                          for i, pub in enumerate(sorted(publisher_nodes))}
    genre_color_map = {genre: genre_colors[i % len(genre_colors)] 
                      for i, genre in enumerate(sorted(genre_nodes))}
    platform_color_map = {platform: platform_colors[i % len(platform_colors)] 
                         for i, platform in enumerate(sorted(platform_nodes))}
    
    # Seçilen genre'ye göre renkleri belirle
    node_colors = []
    highlighted_nodes = set()
    
    if selected_genre == 'All':
        # Tüm node'lar renkli
        for node in node_list:
            if node in publisher_color_map:
                node_colors.append(publisher_color_map[node])
            elif node in genre_color_map:
                node_colors.append(genre_color_map[node])
            elif node in platform_color_map:
                node_colors.append(platform_color_map[node])
            else:
                node_colors.append('#d3d3d3')
        highlighted_nodes = set(node_list)
    else:
        # Sadece seçilen genre ve onunla bağlantılı node'lar renkli
        highlighted_nodes.add(selected_genre)
        
        # Seçilen genre'ye bağlı publisher'ları bul
        connected_publishers = set(pub_genre[pub_genre['Target'] == selected_genre]['Source'].unique())
        highlighted_nodes.update(connected_publishers)
        
        # Seçilen genre'ye bağlı platform'ları bul
        connected_platforms = set(genre_platform[genre_platform['Source'] == selected_genre]['Target'].unique())
        highlighted_nodes.update(connected_platforms)
        
        # Node renklerini atama (highlighted olanlar renkli, diğerleri gri)
        for node in node_list:
            if node in highlighted_nodes:
                if node in publisher_color_map:
                    node_colors.append(publisher_color_map[node])
                elif node in genre_color_map:
                    node_colors.append(genre_color_map[node])
                elif node in platform_color_map:
                    node_colors.append(platform_color_map[node])
                else:
                    node_colors.append('#d3d3d3')
            else:
                node_colors.append('#d3d3d3')  # Gri
    
    # Link'leri oluştur ve renklerini belirle
    links = []
    link_colors = []
    
    # Hex rengi rgba'ya çeviren yardımcı fonksiyon
    def hex_to_rgba(hex_color, alpha=0.6):
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f'rgba({r},{g},{b},{alpha})'
    
    # Publisher -> Genre link'leri
    for _, row in pub_genre.iterrows():
        source_idx = node_dict[row['Source']]
        target_idx = node_dict[row['Target']]
        links.append({
            'source': source_idx,
            'target': target_idx,
            'value': row['Value']
        })
        # Link rengi: eğer her iki node da highlighted ise renkli, değilse gri
        if row['Source'] in highlighted_nodes and row['Target'] in highlighted_nodes:
            source_color = node_colors[source_idx]
            if source_color.startswith('#'):
                link_colors.append(hex_to_rgba(source_color, 0.5))
            else:
                link_colors.append(source_color)
        else:
            link_colors.append('rgba(128,128,128,0.3)')  # Gri ve şeffaf
    
    # Genre -> Platform link'leri
    for _, row in genre_platform.iterrows():
        source_idx = node_dict[row['Source']]
        target_idx = node_dict[row['Target']]
        links.append({
            'source': source_idx,
            'target': target_idx,
            'value': row['Value']
        })
        # Link rengi: eğer her iki node da highlighted ise renkli, değilse gri
        if row['Source'] in highlighted_nodes and row['Target'] in highlighted_nodes:
            source_color = node_colors[source_idx]
            if source_color.startswith('#'):
                link_colors.append(hex_to_rgba(source_color, 0.5))
            else:
                link_colors.append(source_color)
        else:
            link_colors.append('rgba(128,128,128,0.3)')  # Gri ve şeffaf
    
    # Sankey diagram oluştur
    fig_sankey = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="white", width=1.5),
            label=node_list,
            color=node_colors
        ),
        link=dict(
            source=[link['source'] for link in links],
            target=[link['target'] for link in links],
            value=[link['value'] for link in links],
            color=link_colors,
            hovertemplate='%{source.label} → %{target.label}<br>Sales: %{value:.2f}M$<extra></extra>'
        )
    )])
    
    fig_sankey.update_layout(
        title_text="Top 5 Publishers Sales Flow: Publisher → Genre → Platform",
        font_size=10,
        height=800
    )
    
    st.plotly_chart(fig_sankey, use_container_width=True)

with tabs[5]:
    st.header("Line Chart: Sales Trend Over Years")
    st.markdown("This chart shows the trend of total global/regional game sales over the years. You can change the displayed metric (Global/NA/EU/JP Sales) using the dropdown menu, and perform dragging or zooming on the chart.")
    
    # Dropdown menu for sales type selection
    sales_type = st.selectbox(
        "Select Sales Type:",
        options=['Global_Sales', 'NA_Sales', 'EU_Sales', 'JP_Sales'],
        index=0,
        format_func=lambda x: {
            'Global_Sales': 'Global Sales',
            'NA_Sales': 'NA Sales (North America)',
            'EU_Sales': 'EU Sales (Europe)',
            'JP_Sales': 'JP Sales (Japan)'
        }[x]
    )
    
    # Yıllara göre toplam satış hesapla (filtrelenmiş veriden)
    yearly_sales = df_filtered.groupby('Year')[sales_type].sum().reset_index()
    yearly_sales = yearly_sales.sort_values('Year')
    
    # Create line chart
    fig_line = px.line(
        yearly_sales,
        x='Year',
        y=sales_type,
        title=f'{sales_type.replace("_", " ")} Trend Over Years',
        labels={
            'Year': 'Year',
            sales_type: f'{sales_type.replace("_", " ")} (Million $)'
        },
        markers=True
    )
    
    # Interactive features: zoom, pan, drag
    fig_line.update_layout(
        xaxis_title="Year",
        yaxis_title=f"{sales_type.replace('_', ' ')} (Million $)",
        hovermode='x unified',
        xaxis=dict(
            rangeslider=dict(visible=True),  # Range slider at the bottom
            type="linear"
        ),
        dragmode='zoom'  # Default zoom mode
    )
    
    # Update hover template
    fig_line.update_traces(
        hovertemplate='Year: %{x}<br>Sales: %{y:.2f}M$<extra></extra>'
    )
    
    st.plotly_chart(fig_line, use_container_width=True)

with tabs[8]:
    st.header("Top 20 Games (Hilmi): Best-Selling Games of All Time")
    st.markdown("Shows the top 20 games by total global sales from the filtered dataset.")

    # Prepared by: Hilmi
    st.markdown("**Prepared by: Hilmi**")

    # Sort by Global_Sales and select the top 20
    df_top_20 = df_filtered.sort_values(by='Global_Sales', ascending=False).head(20)
    
    # Oyun isimlerini satış sırasına göre listele (en yüksekten en düşüğe)
    # Bu sıralama Y eksenindeki sıralamayı belirleyecek
    name_order = df_top_20['Name'].tolist()

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
        labels={'Global_Sales': 'Global Sales (Million Dollars)', 'Name': 'Game Name'},
        category_orders={'Name': name_order}  # Oyun isimlerini satış sırasına göre sırala
    )
    
    # Y-axis order: en yüksek satış en üstte (horizontal bar'da descending = en üstte en yüksek)
    fig_bar_top.update_layout(
        yaxis={
            'categoryorder': 'array',
            'categoryarray': name_order,
            'tickmode': 'linear'  # Tüm tick'leri göster
        },
        height=max(600, len(df_top_20) * 30)  # Her oyun için yeterli yükseklik
    )

    st.plotly_chart(fig_bar_top, use_container_width=True)
