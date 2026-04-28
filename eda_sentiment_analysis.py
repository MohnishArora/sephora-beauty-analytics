# ============================================================
# Sephora Beauty Analytics | EDA and Sentiment Analysis
# University of Arizona | MIS 587 | 2025
# ============================================================
# Tools: Python, Pandas, TextBlob, Matplotlib, Seaborn
# Run in Google Colab after mounting Google Drive
# ============================================================

# ── STEP 0: Install dependencies ──────────────────────────
# Uncomment and run if not already installed
# !pip install textblob pandas matplotlib seaborn

# ── STEP 1: Mount Google Drive ────────────────────────────
from google.colab import drive
drive.mount('/content/drive')

# ── STEP 2: Import libraries ──────────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import string
from textblob import TextBlob

# ── STEP 3: Data loading ──────────────────────────────────
# UPDATE THESE PATHS to match your Google Drive folder structure
DATA_PATH = "/content/drive/MyDrive/MIS 587"

product_info = pd.read_csv(f'{DATA_PATH}/product_info.csv')
product_info_skincare = pd.read_csv(f'{DATA_PATH}/product_info_skincare.csv')

review_files = [
    f'{DATA_PATH}/reviews_0-250_masked.csv',
    f'{DATA_PATH}/reviews_250-500_masked.csv',
    f'{DATA_PATH}/reviews_500-750_masked.csv',
    f'{DATA_PATH}/reviews_750-1250_masked.csv',
    f'{DATA_PATH}/reviews_1250-end_masked.csv'
]

reviews = pd.concat([pd.read_csv(file) for file in review_files], ignore_index=True)

print(f"Product info rows: {len(product_info)}")
print(f"Reviews rows: {len(reviews)}")

# ── STEP 4: Missing value assessment ─────────────────────
print("\nMissing values in product_info:")
print(product_info.isnull().sum())

print("\nMissing values in reviews:")
print(reviews.isnull().sum())

# ── STEP 5: Data cleaning ─────────────────────────────────
# Drop rows with missing review text or rating
reviews.dropna(subset=['review_text', 'rating'], inplace=True)

# Fill non-critical missing values
reviews.fillna({'review_title': 'No Title'}, inplace=True)
product_info.fillna('Unknown', inplace=True)

# Drop unnecessary columns
if 'Unnamed: 0.1' in reviews.columns:
    reviews.drop(columns=['Unnamed: 0.1'], inplace=True)

# Rename user_id to author_id
if 'user_id' in reviews.columns:
    reviews.rename(columns={'user_id': 'author_id'}, inplace=True)

print(f"\nReviews after cleaning: {len(reviews)} rows")

# ── STEP 6: Outlier removal ───────────────────────────────
# Remove extreme price outliers from Fragrance and Bath & Body
for category in ['Fragrance', 'Bath & Body']:
    mask = product_info['primary_category'] == category
    q99 = product_info.loc[mask, 'price_usd'].quantile(0.99)
    product_info = product_info[~(mask & (product_info['price_usd'] > q99))]

print(f"Product info after outlier removal: {len(product_info)} rows")

# ── STEP 7: Text cleaning ─────────────────────────────────
def clean_text(text):
    text = str(text).lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
    text = re.sub(r'\d+', '', text)
    text = text.strip()
    return text

reviews['clean_review_text'] = reviews['review_text'].apply(clean_text)
print("\nText cleaning complete.")

# ── STEP 8: Sentiment analysis ────────────────────────────
def get_sentiment(text):
    try:
        return TextBlob(text).sentiment.polarity
    except:
        return 0

def categorize_sentiment(score):
    if score > 0.1:
        return 'Positive'
    elif score < -0.1:
        return 'Negative'
    else:
        return 'Neutral'

reviews['sentiment_score'] = reviews['clean_review_text'].apply(get_sentiment)
reviews['sentiment_label'] = reviews['sentiment_score'].apply(categorize_sentiment)

sentiment_counts = reviews['sentiment_label'].value_counts()
print("\nSentiment distribution:")
print(sentiment_counts)
print(f"Positive reviews: {sentiment_counts.get('Positive', 0) / len(reviews) * 100:.1f}%")

# ── STEP 9: Descriptive statistics ───────────────────────
print("\nReview descriptive stats:")
print(reviews[['rating', 'helpfulness']].describe())

print("\nProduct price descriptive stats:")
print(product_info[['price_usd']].describe())

# ── STEP 10: Visualizations ──────────────────────────────

# 10.1 Sentiment score distribution
plt.figure(figsize=(10, 5))
plt.hist(reviews['sentiment_score'], bins=50, color='mediumpurple', edgecolor='white', alpha=0.8)
plt.title('Sentiment Score Distribution')
plt.xlabel('Sentiment Score')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('sentiment_distribution.png', dpi=150)
plt.show()

# 10.2 Price vs rating scatter for top 5 brands
top_brands = product_info['brand_name'].value_counts().head(5).index.tolist()
top_df = product_info[product_info['brand_name'].isin(top_brands)]

plt.figure(figsize=(10, 6))
for brand in top_brands:
    subset = top_df[top_df['brand_name'] == brand]
    plt.scatter(subset['price_usd'], subset['rating'], label=brand, alpha=0.6, s=30)
plt.title('Price vs Rating by Top 5 Brands')
plt.xlabel('Price (USD)')
plt.ylabel('Rating')
plt.legend()
plt.tight_layout()
plt.savefig('price_vs_rating_scatter.png', dpi=150)
plt.show()

# 10.3 Correlation heatmap
numeric_cols = ['loves_count', 'rating', 'reviews', 'price_usd', 'value_price_usd', 'sale_price_usd']
available = [c for c in numeric_cols if c in product_info.columns]
corr = product_info[available].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0)
plt.title('Correlation Matrix of Numeric Features')
plt.tight_layout()
plt.savefig('correlation_matrix.png', dpi=150)
plt.show()

# 10.4 Price distribution before and after outlier removal by category
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for i, category in enumerate(['Fragrance', 'Bath & Body']):
    subset = product_info[product_info['primary_category'] == category]['price_usd']
    axes[i].boxplot(subset)
    axes[i].set_title(f'{category} (after outlier removal)')
    axes[i].set_ylabel('Price (USD)')
plt.suptitle('Price Distribution After Outlier Removal')
plt.tight_layout()
plt.savefig('price_distribution.png', dpi=150)
plt.show()

print("\nAll visualizations saved.")
print("EDA and sentiment analysis complete.")
