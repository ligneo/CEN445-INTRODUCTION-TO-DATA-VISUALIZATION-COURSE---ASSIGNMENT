# Video Game Sales Visualization Dashboard

This project is an interactive data visualization dashboard developed using **Python** and **Streamlit**. It analyzes the `vgsales.csv` dataset to provide insights into global video game sales, trends across genres, publisher performance, and regional market differences.

## Dataset
- **Source**   The dataset used is [vgsales.csv](https://www.kaggle.com/datasets/gregorut/videogamesales?resource=download).
- **Description:** It contains data on video game sales greater than 10,000 copies.
- **Key Columns:** Rank, Name, Platform, Year, Genre, Publisher, NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales.
- **Preprocessing:** Rows with missing `Year` or `Publisher` information have been dropped to ensure data quality.


## Installation & Setup

- To run this project locally, follow these steps:

---

```bash
    git clone https://github.com/ligneo/CEN445-INTRODUCTION-TO-DATA-VISUALIZATION-COURSE---ASSIGNMENT.git
```

```bash
    pip install -r requirements.txt
```

```bash
    streamlit run app.py
```

## Project Structure & Contributions

The dashboard features 9 distinct visualizations created by the team members:

### Cenk
* **Scatter Plot:** Analysis of the correlation between NA and EU sales with marginal distribution histograms and trendlines.
* **Box Plot:** Distribution of sales across genres, focusing on the median values with a zoom feature.
* **Dynamic Treemap:** Hierarchical view of the market share (Publisher -> Genre -> Platform).

### **İlhan**
* **Stacked Area Chart:** Illustrated the sales evolution and market lifecycles of the Top 12 platforms over the years.
* **Sankey Diagram:** Visualized the multi-stage sales distribution from the Top 5 Publishers to specific Genres and Platforms.
* **Line Chart:** Tracked the annual global sales performance of specific publishers with interactive zooming features.

### **Hilmi**
* **Parallel Coordinates:** Compared regional sales profiles (NA, EU, JP, Other) across different game genres.
* **Interactive Heatmap (Choropleth):** A geographical visualization showing the regional footprint of the top-selling game for each year. It colors countries based on which region (Americas, Europe, Japan, Other) the year's hit game sold best in, highlighting global shifts in market dominance.
* **Bar Char:** Ranked the Top 20 best-selling games of all time.
