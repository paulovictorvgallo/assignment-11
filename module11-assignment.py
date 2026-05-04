# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Welcome message
print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Create a seed for reproducibility
np.random.seed(42)

# Generate dates for 8 quarters (Q1 2022 - Q4 2023)
quarters = pd.date_range(start='2022-01-01', periods=8, freq='QE')
quarter_labels = ['Q1 2022', 'Q2 2022', 'Q3 2022', 'Q4 2022', 
                 'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']

# Store locations
locations = ['Tampa', 'Miami', 'Orlando', 'Jacksonville']

# Product categories
categories = ['Electronics', 'Clothing', 'Home Goods', 'Sporting Goods', 'Beauty']

# Generate quarterly sales data for each location and category
quarterly_data = []

for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            # Base sales with seasonal pattern (Q4 higher, Q1 lower)
            base_sales = np.random.normal(loc=100000, scale=20000)
            seasonal_factor = 1.0
            if quarter.quarter == 4:  # Q4 (holiday boost)
                seasonal_factor = 1.3
            elif quarter.quarter == 1:  # Q1 (post-holiday dip)
                seasonal_factor = 0.8
            
            # Location effect
            location_factor = {
                'Tampa': 1.0,
                'Miami': 1.2,
                'Orlando': 0.9,
                'Jacksonville': 0.8
            }[location]
            
            # Category effect
            category_factor = {
                'Electronics': 1.5,
                'Clothing': 1.0,
                'Home Goods': 0.8,
                'Sporting Goods': 0.7,
                'Beauty': 0.9
            }[category]
            
            # Growth trend over time (5% per year, quarterly compounded)
            growth_factor = (1 + 0.05/4) ** quarter_idx
            
            # Calculate sales with some randomness
            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales = sales * np.random.normal(loc=1.0, scale=0.1)
            
            # Advertising spend (correlated with sales but with diminishing returns)
            ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(loc=1.0, scale=0.2)
            
            # Record
            quarterly_data.append({
                'Quarter': quarter,
                'QuarterLabel': quarter_labels[quarter_idx],
                'Location': location,
                'Category': category,
                'Sales': round(sales, 2),
                'AdSpend': round(ad_spend, 2),
                'Year': quarter.year
            })

# Create customer data
customer_data = []
total_customers = 2000

# Age distribution parameters for each location
age_params = {
    'Tampa': (45, 15),      # Older demographic
    'Miami': (35, 12),      # Younger demographic
    'Orlando': (38, 14),    # Mixed demographic
    'Jacksonville': (42, 13)  # Middle-aged demographic
}

for location in locations:
    # Generate ages based on location demographics
    mean_age, std_age = age_params[location]
    customer_count = int(total_customers * {
        'Tampa': 0.3,
        'Miami': 0.35,
        'Orlando': 0.2,
        'Jacksonville': 0.15
    }[location])
    
    ages = np.random.normal(loc=mean_age, scale=std_age, size=customer_count)
    ages = np.clip(ages, 18, 80).astype(int)
    
    # Generate purchase amounts
    for age in ages:
        # Younger and older customers spend differently across categories
        if age < 30:
            category_preference = np.random.choice(categories, p=[0.3, 0.3, 0.1, 0.2, 0.1])
        elif age < 50:
            category_preference = np.random.choice(categories, p=[0.25, 0.2, 0.25, 0.15, 0.15])
        else:
            category_preference = np.random.choice(categories, p=[0.15, 0.1, 0.35, 0.1, 0.3])
        
        # Purchase amount based on age and category
        base_amount = np.random.gamma(shape=5, scale=20)
        
        # Product tier (budget, mid-range, premium)
        price_tier = np.random.choice(['Budget', 'Mid-range', 'Premium'], 
                                     p=[0.3, 0.5, 0.2])
        
        tier_factor = {'Budget': 0.7, 'Mid-range': 1.0, 'Premium': 1.8}[price_tier]
        
        purchase_amount = base_amount * tier_factor
        
        customer_data.append({
            'Location': location,
            'Age': age,
            'Category': category_preference,
            'PurchaseAmount': round(purchase_amount, 2),
            'PriceTier': price_tier
        })

# Create DataFrames
sales_df = pd.DataFrame(quarterly_data)
customer_df = pd.DataFrame(customer_data)

# Add some calculated columns
sales_df['Quarter_Num'] = sales_df['Quarter'].dt.quarter
sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']

# Print data info
print("\nSales Data Sample:")
print(sales_df.head())
print("\nCustomer Data Sample:")
print(customer_df.head())
print("\nDataFrames created successfully. Ready for visualization!")


# ----- TODO 1: Time Series Visualization - Sales Trends -----

def plot_quarterly_sales_trend():
    """
    Create a line chart showing total sales for each quarter.
    REQUIRED: Return the figure object
    """
    df = sales_df.groupby('QuarterLabel')['Sales'].sum()

    fig, ax = plt.subplots()
    ax.plot(df.index, df.values, marker='o')
    ax.set_title("Quarterly Sales Trend")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Sales")
    ax.grid()

    return fig


# 1.2 Create a multi-line chart comparing sales trends across locations
def plot_location_sales_comparison():
    """
    Create a multi-line chart comparing quarterly sales across different locations.
    REQUIRED: Return the figure object
    """
    df = sales_df.groupby(['QuarterLabel', 'Location'])['Sales'].sum().unstack()

    fig, ax = plt.subplots()

    for loc in df.columns:
        ax.plot(df.index, df[loc], marker='o', label=loc)

    ax.set_title("Sales by Location")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Sales")
    ax.legend()
    ax.grid()

    return fig


# ----- TODO 2: Categorical Comparison -----

def plot_category_performance_by_location():
    """
    Create a grouped bar chart showing how each product category performs in different locations.
    REQUIRED: Return the figure object
    """
    latest = sales_df[sales_df['QuarterLabel'] == 'Q4 2023']
    df = latest.groupby(['Location', 'Category'])['Sales'].sum().unstack()

    fig, ax = plt.subplots()
    df.plot(kind='bar', ax=ax)

    ax.set_title("Category Performance by Location")
    ax.set_xlabel("Location")
    ax.set_ylabel("Sales")

    return fig


def plot_sales_composition_by_location():
    """
    Create a stacked bar chart showing the composition of sales across categories for each location.
    REQUIRED: Return the figure object
    """
    df = sales_df.groupby(['Location', 'Category'])['Sales'].sum().unstack()
    df_pct = df.div(df.sum(axis=1), axis=0)

    fig, ax = plt.subplots()
    df_pct.plot(kind='bar', stacked=True, ax=ax)

    ax.set_title("Sales Composition by Location")
    ax.set_ylabel("Percentage")

    return fig


# ----- TODO 3: Relationship Analysis - Advertising and Sales -----

def plot_ad_spend_vs_sales():
    """
    Create a scatter plot to visualize the relationship between advertising spend and sales.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots()

    x = sales_df['AdSpend']
    y = sales_df['Sales']

    ax.scatter(x, y)

    # best fit line
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    ax.plot(x, p(x))

    # ✅ FIX FOR TEST (IMPORTANT)
    ax.set_xlabel("Ad Spend")
    ax.set_ylabel("Sales")
    ax.set_title("Ad Spend vs Sales")

    return fig


def plot_ad_efficiency_over_time():
    """
    Create a line chart showing how efficient advertising spend has been over time.
    REQUIRED: Return the figure object
    """
    df = sales_df.groupby('QuarterLabel')['SalesPerDollarSpent'].mean()

    fig, ax = plt.subplots()
    ax.plot(df.index, df.values, marker='o')

    ax.set_title("Ad Efficiency Over Time")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Efficiency")

    return fig


# ----- TODO 4: Distribution Analysis -----

def plot_customer_age_distribution():
    """
    Create histograms showing the age distribution of customers, both overall and by location.
    REQUIRED: Return the figure object
    """
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    for ax, loc in zip(axes.flatten(), locations):
        data = customer_df[customer_df['Location'] == loc]['Age']
        ax.hist(data, bins=15)
        ax.set_title(loc)

    return fig


def plot_purchase_by_age_group():
    """
    Create box plots showing purchase amounts across different age groups.
    REQUIRED: Return the figure object
    """
    bins = [18, 30, 45, 60, 80]
    labels = ['18-30', '31-45', '46-60', '61+']

    customer_df['AgeGroup'] = pd.cut(customer_df['Age'], bins=bins, labels=labels)

    fig, ax = plt.subplots()
    customer_df.boxplot(column='PurchaseAmount', by='AgeGroup', ax=ax)
    plt.suptitle("")

    return fig


# ----- TODO 5: Sales Distribution -----

def plot_purchase_amount_distribution():
    """
    Create a histogram showing the distribution of purchase amounts.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots()
    ax.hist(customer_df['PurchaseAmount'], bins=20)
    ax.set_title("Purchase Amount Distribution")
    ax.set_xlabel("Amount")
    ax.set_ylabel("Frequency")

    return fig


def plot_sales_by_price_tier():
    """
    Create a pie chart showing the breakdown of sales by price tier.
    REQUIRED: Return the figure object
    """
    df = customer_df.groupby('PriceTier')['PurchaseAmount'].sum()

    fig, ax = plt.subplots()
    ax.pie(df, labels=df.index, autopct='%1.1f%%')

    return fig


# ----- TODO 6: Market Share Analysis -----

def plot_category_market_share():
    """
    Create a pie chart showing the market share of each product category.
    REQUIRED: Return the figure object
    """
    df = sales_df.groupby('Category')['Sales'].sum()

    fig, ax = plt.subplots()
    ax.pie(df, labels=df.index, autopct='%1.1f%%')

    return fig


def plot_location_sales_distribution():
    """
    Create a pie chart showing the distribution of sales across different store locations.
    REQUIRED: Return the figure object
    """
    df = sales_df.groupby('Location')['Sales'].sum()

    fig, ax = plt.subplots()
    ax.pie(df, labels=df.index, autopct='%1.1f%%')

    return fig


# ----- TODO 7: Comprehensive Dashboard -----

def create_business_dashboard():
    """
    Create a comprehensive dashboard with multiple subplots highlighting key business insights.
    REQUIRED: Return the figure object with at least 4 subplots
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    sales_df.groupby('QuarterLabel')['Sales'].sum().plot(ax=axes[0, 0])
    axes[0, 0].set_title("Sales Trend")

    sales_df.groupby(['QuarterLabel', 'Location'])['Sales'].sum().unstack().plot(ax=axes[0, 1])
    axes[0, 1].set_title("Location Comparison")

    sales_df.groupby('QuarterLabel')['SalesPerDollarSpent'].mean().plot(ax=axes[1, 0])
    axes[1, 0].set_title("Ad Efficiency")

    sales_df.groupby('Category')['Sales'].sum().plot(kind='pie', ax=axes[1, 1], autopct='%1.1f%%')
    axes[1, 1].set_title("Category Share")

    plt.tight_layout()
    return fig


# ----- MAIN FUNCTION -----

def main():
    print("\n" + "=" * 60)
    print("SUNCOAST RETAIL VISUAL ANALYSIS RESULTS")
    print("=" * 60)

    plot_quarterly_sales_trend()
    plot_location_sales_comparison()
    plot_category_performance_by_location()
    plot_sales_composition_by_location()
    plot_ad_spend_vs_sales()
    plot_ad_efficiency_over_time()
    plot_customer_age_distribution()
    plot_purchase_by_age_group()
    plot_purchase_amount_distribution()
    plot_sales_by_price_tier()
    plot_category_market_share()
    plot_location_sales_distribution()
    create_business_dashboard()

    print("\nKEY BUSINESS INSIGHTS:")
    print("""
- Sales increase over time with seasonal spikes in Q4
- Miami is the strongest market
- Electronics dominate revenue
- Ads increase sales but with diminishing returns
- Customer demographics vary by location
- Mid-range products perform best overall
""")

    plt.show()


if __name__ == "__main__":
    main()