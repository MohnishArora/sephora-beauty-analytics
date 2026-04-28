-- ============================================================
-- Sephora Beauty Analytics | Data Warehouse SQL Scripts
-- Star Schema: 1 Fact Table + 4 Dimension Tables
-- University of Arizona | MIS 587 | 2025
-- ============================================================

-- ────────────────────────────────────────────
-- FACT TABLE: Combined_Reviews_FactTable
-- Granularity: one row per customer review
-- ────────────────────────────────────────────
CREATE TABLE Combined_Reviews_FactTable (
    author_id                NVARCHAR(255),
    rating                   INT,
    is_recommended           INT,
    helpfulness              DECIMAL(10,4),
    total_feedback_count     INT,
    total_neg_feedback_count INT,
    total_pos_feedback_count INT,
    submission_time          NVARCHAR(MAX),
    review_text              NVARCHAR(MAX),
    review_title             NVARCHAR(MAX),  -- nulls imputed with 'No Title' during ETL
    product_id               NVARCHAR(255),
    price_usd                DECIMAL(10,2),
    review_id                NVARCHAR(255),
    BrandID                  NVARCHAR(255)
);

-- ────────────────────────────────────────────
-- DIMENSION: Dim_Product_Info
-- 8,401 rows | product metadata + derived flags
-- ────────────────────────────────────────────
CREATE TABLE Dim_Product_Info (
    product_id          NVARCHAR(255),
    product_name        NVARCHAR(MAX),
    brand_id            NVARCHAR(255),
    brand_name          NVARCHAR(MAX),
    loves_count         INT,
    rating              DECIMAL(4,2),
    reviews             INT,
    size                NVARCHAR(255),
    variation_type      NVARCHAR(255),
    variation_value     NVARCHAR(255),
    variation_desc      NVARCHAR(MAX),
    ingredients         NVARCHAR(MAX),
    price_usd           DECIMAL(10,2),
    sale_price_usd      DECIMAL(10,2),
    limited_edition     INT,
    [new]               INT,
    online_only         NVARCHAR(MAX),
    out_of_stock        INT,
    sephora_exclusive   INT,
    highlights          NVARCHAR(MAX),
    primary_category    NVARCHAR(255),
    secondary_category  NVARCHAR(255),
    tertiary_category   NVARCHAR(255),
    child_count         INT,
    child_max_price     DECIMAL(10,2),
    child_min_price     DECIMAL(10,2),
    is_discount         INT,            -- derived: 1 if sale_price_usd is not null, else 0
    is_skincare         INT
);

-- ────────────────────────────────────────────
-- DIMENSION: Dim_Author
-- 219,346 rows | reviewer demographics
-- ────────────────────────────────────────────
CREATE TABLE Dim_Author (
    author_id   NVARCHAR(255),
    eye_color   NVARCHAR(255),
    hair_color  NVARCHAR(255),
    skin_tone   NVARCHAR(255),
    skin_type   NVARCHAR(255)
);

-- ────────────────────────────────────────────
-- DIMENSION: Dim_Brand
-- 100 rows | brand lookup table
-- ────────────────────────────────────────────
CREATE TABLE Dim_Brand (
    brand_id    NVARCHAR(255),
    brand_name  NVARCHAR(MAX)
);

-- ────────────────────────────────────────────
-- DIMENSION: Dim_Date
-- 5,319 rows | temporal analysis
-- ────────────────────────────────────────────
CREATE TABLE Dim_Date (
    [date]         DATE,
    year           INT,
    month_number   INT,
    month_name     NVARCHAR(50),
    quarter        NVARCHAR(50),
    weekday        NVARCHAR(50),
    weekday_number INT
);
