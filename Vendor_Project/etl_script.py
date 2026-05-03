import pandas as pd
from sqlalchemy import create_engine

print("Connecting to database...")
engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')

print("Extracting data...")
df = pd.read_sql("SELECT * FROM vendor_performance_summary", engine)

print("Transforming data...")
df['Profit_Margin_%'] = (df['total_profit'] / df['total_sales']) * 100

def categorize_vendor(row):
    if row['Profit_Margin_%'] < 10:
        return 'Underperforming - Review Pricing'
    elif row['total_sales'] > 50000 and row['Profit_Margin_%'] >= 20:
        return 'Top Vendor - Prioritize'
    else:
        return 'Stable'

df['Vendor_Status'] = df.apply(categorize_vendor, axis=1)

print("Exporting data...")
output_file = 'Cleaned_Vendor_Data_For_BI.csv'
df.to_csv(output_file, index=False)
print(f"Success! Saved to {output_file}. Ready for Power BI.")