# Sephora Beauty Analytics
## Data Warehouse and Customer Engagement Intelligence for Skincare Products

**Tools:** Python (Pandas, TextBlob, Matplotlib, Seaborn) | AWS Glue Studio | Amazon S3 | SQL Server | Power BI | Google Colab

**Dataset:** Sephora Beauty Product Reviews (Kaggle) | 285,000+ customer reviews | 8,400+ products | 100 brands

**Result:** End-to-end data warehouse with star schema design enabling actionable insights across product strategy, pricing, and brand engagement

---

## The Problem

Sephora manages thousands of skincare and beauty products across hundreds of brands. Manually tracking which products customers love, which categories are underperforming, and how reviews and ratings map to business outcomes is impossible at this scale.

This project answers three questions:

1. Which skincare categories, brands, and products drive the most customer engagement?
2. Does price influence customer satisfaction, or do other factors matter more?
3. How can marketing, inventory, and pricing strategies be better aligned with actual customer behavior?

---

## The Data

Two source datasets from Kaggle joined and processed through an AWS Glue ETL pipeline:

| File | Rows | Description |
|---|---|---|
| product_info.csv | 8,494 | Product metadata: name, brand, price, categories, flags (limited edition, online only, Sephora exclusive) |
| reviews (5 files) | 285,412 | Customer reviews: rating, review text, helpfulness score, loves count, submission date |

Key engagement metrics used: loves_count (wishlists), rating (1 to 5 stars), review volume, sentiment polarity score (TextBlob)

---

## The Pipeline

The project runs end to end through six stages:

**Stage 1: Data Ingestion**
Five segmented review CSV files concatenated into a unified DataFrame using Pandas. Product info loaded separately and merged for combined analysis.

**Stage 2: EDA and Data Cleaning**
Missing values identified and handled: rating and review text nulls dropped, non-critical fields filled with placeholder values. Extreme price outliers removed from Fragrance and Bath and Body categories to normalize distributions. Column renamed from user_id to author_id for clarity.

**Stage 3: Text Cleaning and Sentiment Analysis**
Reviews converted to lowercase, stripped of punctuation and digits using regex. TextBlob applied to calculate polarity scores per review. Reviews classified as Positive (score above 0.1), Neutral, or Negative (score below negative 0.1). Over 70% of reviews classified as Positive.

**Stage 4: ETL via AWS Glue Studio**
Two ETL jobs built using AWS Glue Studio visual interface. Raw data stored in Amazon S3 and catalogued in AWS Glue Data Catalog. Transformations applied: derived is_discounted column added to product table (1 if sale price exists, 0 otherwise), value_price_usd dropped as redundant, null review titles filled with placeholder "No Title". Both jobs executed successfully with no errors.

**Stage 5: Data Warehouse Implementation in SQL Server**
Star schema implemented with one fact table and four dimension tables. All tables bulk imported into SQL Server using Flat File Import wizard. Foreign key relationships established for referential integrity.

**Stage 6: Business Intelligence and Reporting in Power BI**
Decomposition tree, correlation matrix, scatter plots, and bar charts built to surface product and brand performance insights. Findings translated into three strategic recommendation areas.

---

## Data Warehouse Schema

Star schema centered on the Combined_Reviews fact table:

| Table | Rows | Description |
|---|---|---|
| Combined_Reviews (Fact) | 278,710 | Core review metrics: rating, helpfulness, feedback counts, is_recommended |
| Dim_Product_Info | 8,401 | Product metadata with derived is_discount flag |
| Dim_Author | 219,346 | Reviewer demographics: skin tone, skin type, eye color, hair color |
| Dim_Brand | 100 | Brand ID and name lookup |
| Dim_Date | 5,319 | Date dimension: day, month, quarter, year, weekday |

---

## Key Findings

Price does not drive satisfaction. The correlation between price and rating is just 0.057 — essentially zero. Products in the $10 to $50 mid-tier range consistently received the highest ratings. Premium brands like Dior did not outperform affordable brands like SEPHORA COLLECTION or tarte in customer satisfaction.

Review volume predicts popularity. loves_count and review volume are moderately correlated (r = 0.68), confirming that engagement metrics are reliable proxies for product success.

Customer interest is concentrated in core categories. Cleansers alone account for 32% of all reviews. Masks and Moisturizers follow. Niche categories like Toners and Makeup Removers received fewer than 2,000 reviews each, signaling limited visibility or demand.

Celebrity brand affinity is real but not the whole story. Fenty Beauty and Rare Beauty lead in loves_count. Sephora Collection performs competitively on value and consistency, showing strong loyalty even without celebrity backing.

Sentiment is broadly positive. Over 70% of reviews scored as Positive using TextBlob polarity analysis, with the distribution peaking around a sentiment score of 0.25.

---

## Business Impact

| Area | Finding | Recommendation |
|---|---|---|
| Product strategy | Cleansers and Moisturizers dominate engagement | Prioritize these categories in marketing spend and inventory planning |
| Pricing | Mid-tier $10 to $50 products outperform premium options in ratings | Justify premium pricing only with strong brand loyalty or unique product value |
| Brand management | Celebrity brands and value brands both drive loyalty through different mechanisms | Invest in hero product promotion and verified review volume to drive engagement |
| Inventory | Niche categories (Toners, Exfoliators, Makeup Removers) underperform | Consider repositioning, bundling, or promotional campaigns for low-engagement segments |

---

## Project Structure

```
sephora-beauty-analytics/
│
├── eda_sentiment_analysis.py     # EDA, text cleaning, sentiment analysis, visualizations
├── create_schema.sql             # Star schema DDL: fact table + 4 dimension tables
├── README.md                     # This file
├── Architecture.jpeg             # Project Architecture and Design Flow
├── data/
│   └── (Download from Kaggle: Sephora Beauty Product Reviews Dataset)
│
└── outputs/
    ├── sentiment_distribution.png
    ├── price_vs_rating_scatter.png
    ├── correlation_matrix.png
    └── loves_count_by_brand.png
```

---

## How to Run

**EDA and Sentiment Analysis:**
1. Download the dataset from Kaggle: search "Sephora Beauty Product Reviews Dataset"
2. Upload product_info.csv and all five review CSV files to your Google Drive
3. Open eda_sentiment_analysis.py in Google Colab
4. Set the file paths in the Data Loading section to match your Google Drive folder
5. Run all cells top to bottom

**Data Warehouse:**
1. Run the SQL scripts in the sql_scripts/ folder in SQL Server to create the schema
2. Use the Flat File Import wizard in SQL Server to bulk load the cleaned CSVs into each table

**ETL:**
The ETL pipeline was built and executed using AWS Glue Studio. Two jobs were run: one for product_info transformations and one for reviews transformations. Glue tables were registered in the AWS Glue Data Catalog pointing to S3 source and destination paths.

---

## Limitations and Assumptions

Dataset reflects Sephora product catalog at a specific point in time and does not capture real-time inventory or pricing changes. Sentiment analysis uses TextBlob polarity which is a lexicon-based approach and may misclassify nuanced beauty reviews. The is_discounted flag is derived from the presence of a sale price and may not capture all promotional scenarios. Star schema was implemented in SQL Server for academic purposes; a production deployment would use a cloud data warehouse such as Redshift or Snowflake.

---

## Authors

**Mohnish Arora** | EDA, data modeling, ETL design, business analysis

Rajasee Thakre | Dataset documentation, problem definition

Rohan Apte | ETL implementation, AWS Glue jobs

Shravani Shete | Data cleaning, SQL implementation

Vaishnav Mulay | Power BI reporting, business implications

University of Arizona, Eller College of Management | MIS 587 Data Warehousing and Business Intelligence | 2025
