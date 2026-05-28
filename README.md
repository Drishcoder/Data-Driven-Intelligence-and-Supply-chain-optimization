# 🎯 Data-Driven Intelligence & Supply Chain Optimization

Advanced analytics platform combining **RFM (Recency, Frequency, Monetary) analysis** and **machine learning** to intelligently segment customers and optimize supply chain strategies.

## 📋 Overview

This project leverages customer purchase behavior data to identify high-value customers, at-risk customers, and growth opportunities. Using K-means clustering on RFM metrics, we segment customers into four distinct groups, enabling targeted retention strategies and inventory optimization.

---

## ✨ Key Features

- **RFM Customer Segmentation**: Analyzes customer behavior based on Recency, Frequency, and Monetary value
- **Machine Learning Clustering**: K-means algorithm with data scaling and log transformation for optimal segmentation
- **Interactive Dashboard**: Real-time Streamlit dashboard for data visualization and analysis
- **Customer Intelligence**: Identify Champions, At-Risk, Potential Loyalists, and Hibernating customers
- **Supply Chain Insights**: Data-driven recommendations for inventory and demand forecasting
- **Actionable Metrics**: Metrics and insights for customer retention and lifetime value optimization

---

## 🛠️ Technology Stack

| Technology | Purpose |
|-----------|---------|
| **Python 3.x** | Core programming language |
| **Pandas** | Data manipulation and analysis |
| **NumPy** | Numerical computations |
| **Scikit-learn** | Machine learning (K-means clustering, StandardScaler) |
| **Streamlit** | Interactive web dashboard |
| **Plotly** | Interactive visualizations |
| **Matplotlib & Seaborn** | Statistical plotting |

---

## 📁 Project Structure

```
Data-Driven-Intelligence-and-Supply-chain-optimization/
├── README.md                  # Project documentation
├── online_retail.csv          # Dataset (customer transactions)
├── offproject.ipynb           # Jupyter notebook with analysis
├── streamlit_app.py           # Interactive dashboard application
└── [Additional analysis files]
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip or conda package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Data-Driven-Intelligence-and-Supply-chain-optimization.git
   cd Data-Driven-Intelligence-and-Supply-chain-optimization
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install pandas numpy scikit-learn streamlit plotly matplotlib seaborn
   ```

---

## 💡 Usage

### Running the Interactive Dashboard
```bash
streamlit run streamlit_app.py
```
Access the dashboard at `http://localhost:8501` in your web browser.

### Running the Analysis Notebook
Open `offproject.ipynb` in Jupyter Notebook or Jupyter Lab to explore the detailed analysis and methodology.

---

## 📊 Customer Segments Explained

| Segment | Description | Characteristics | Strategy |
|---------|-------------|-----------------|----------|
| **Champions** | Best customers | High recency, frequency, and monetary value | Reward loyalty, personalized offers |
| **At Risk** | Used to be good, now inactive | Low recency, high monetary value | Win-back campaigns, special discounts |
| **Potential Loyalists** | Recent buyers with decent value | Good recency and frequency | Nurture with engagement, cross-sell |
| **Hibernating** | Inactive long ago | Low recency, low frequency/monetary | Re-engagement campaigns, surveys |

---

## 🔄 Data Processing Pipeline

1. **Data Cleaning**
   - Remove null values (CustomerID, Description)
   - Filter out cancelled orders (negative quantities)
   - Remove invalid prices and invoices

2. **RFM Calculation**
   - **Recency**: Days since last purchase
   - **Frequency**: Number of transactions
   - **Monetary**: Total spending amount

3. **Feature Scaling**
   - Log transformation (to handle skewed distributions)
   - StandardScaler normalization

4. **Clustering**
   - K-means with k=4 clusters
   - Random state=42 for reproducibility
   - K-means++ initialization

---

## 📈 Dashboard Features

- **Segment Overview**: Customer distribution across segments
- **RFM Metrics**: Interactive visualizations of Recency, Frequency, Monetary values
- **Filtering**: Multi-select options to analyze specific customer segments
- **Custom Styling**: Professional UI with gradient cards and styled components
- **Real-time Analytics**: Performance metrics and KPIs

---

## 🎯 Business Applications

- ✅ **Customer Retention**: Identify and retain at-risk customers
- ✅ **Personalized Marketing**: Tailor campaigns to segment behavior
- ✅ **Inventory Optimization**: Align stock with customer demand patterns
- ✅ **Revenue Growth**: Focus resources on high-value customer segments
- ✅ **Lifetime Value Prediction**: Forecast customer worth and growth potential

---

## 📝 Analysis Methodology

- **Clustering Algorithm**: K-means (unsupervised learning)
- **Feature Engineering**: RFM metrics as primary features
- **Scaling**: Logarithmic transformation + StandardScaler
- **Optimization**: K-means++ initialization with 50 iterations
- **Validation**: Cluster analysis and business interpretation

---

## 🔮 Future Enhancements

- [ ] Implement cohort analysis for temporal trends
- [ ] Add predictive models for churn prediction
- [ ] Integrate real-time data pipelines
- [ ] Implement automated alert systems for at-risk customers
- [ ] Develop recommendation engine for product cross-sell
- [ ] Add export functionality for reports and dashboards
- [ ] Implement A/B testing framework for retention strategies

---

## 📊 Key Metrics & KPIs

- Customer Lifetime Value (CLV)
- Churn Rate by Segment
- Average Order Value (AOV)
- Customer Acquisition Cost (CAC)
- Repeat Purchase Rate
- Segment Size and Distribution

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📧 Contact & Support

For questions or suggestions, please reach out via GitHub Issues or contact the maintainer directly.

---

## 🙏 Acknowledgments

- Dataset: Online Retail Dataset
- Libraries: pandas, scikit-learn, Streamlit, Plotly
- Methodology: RFM Analysis + K-means Clustering
