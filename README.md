- streamlit
- pandas
- https://plotly.com/python/plotly-express/

# Requirements
pip install statsmodels, streamlit, pandas, plotly


# How to run 

```
streamlit run app.py
```


---

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
* **Interactive Scatter Plot:** Analysis of the correlation between NA and EU sales with marginal distribution histograms and trendlines.
* **Box Plot (Deep Zoom):** Distribution of sales across genres, focusing on the median values with a zoom feature.
* **Dynamic Treemap:** Hierarchical view of the market share (Publisher -> Genre -> Platform).

### **İlhan**
* **Stacked Area Chart:** Platform popularity trends over the years.
* **Sankey Diagram:** Flow of sales from Top 5 Publishers to Genres and Platforms.
* **Line Chart:** Global and regional sales trends over time with interactive zooming.

### **Hilmi**
* **Parallel Coordinates:** Comparing regional sales profiles across different genres.
* **Stacked Area Chart (Market Share):** Evolution of Genre market shares (percentage) over the years.
* **Top 20 Games:** A ranked horizontal bar chart of the best-selling games of all time.
