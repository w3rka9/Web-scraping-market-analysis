import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

results = []
# Include a loop to scrape multiple pages
for page in range(1, 4):
    url = f"https://books.toscrape.com/catalogue/page-{page}.html"
    print(f"Downloading data from page {page}...")
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', class_='product_pod')

    for book in books:
        title = book.h3.a['title']
        
        # Cleaning the price data
        raw_price = book.find('p', class_='price_color').text
        clean_price = float("".join(char for char in raw_price if char.isdigit() or char == '.'))
        
        # Downloading the rating 
        rating_classes = book.find('p', class_='star-rating')['class']
        rating = rating_classes[1] 

        results.append({
            'Title': title,
            'Price (£)': clean_price,
            'Rating': rating
        })
    
    time.sleep(1)

# Data analysis
df = pd.DataFrame(results)

# Price changing to numeric and mapping ratings to numbers for analysis
rating_dict = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
df['Rating_Num'] = df['Rating'].map(rating_dict)

# Average price by rating
avg_prices = df.groupby('Rating')['Price (£)'].mean().sort_values()

print("\n--- ANALYSIS ---")
print("Average prices by rating:")
print(avg_prices)

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

plt.figure(figsize=(12, 7))

# Creating bar chart with Seaborn
barplot = sns.barplot(x='Rating', y='Price (£)', data=df, 
                      order=['One', 'Two', 'Three', 'Four', 'Five'],
                      palette="viridis", ci=None) 

plt.title('Average Book Prices by Rating Category', fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Star Rating', fontsize=14)
plt.ylabel('Average Price (£)', fontsize=14)

# Formating y-axis to show prices in £
from matplotlib.ticker import StrMethodFormatter
plt.gca().yaxis.set_major_formatter(StrMethodFormatter('£{x:.2f}'))

# Adding tags with price values on top of bars
for p in barplot.patches:
    barplot.annotate(format(p.get_height(), '.2f') + ' £', 
                     (p.get_x() + p.get_width() / 2., p.get_height()), 
                     ha = 'center', va = 'center', 
                     xytext = (0, 10), 
                     textcoords = 'offset points',
                     fontsize=12, fontweight='bold')

# Saving to file
plt.tight_layout()
plt.savefig('average_price_by_rating.png')

# Saving to Excel with two sheets: raw data and analysis
with pd.ExcelWriter('Mega_Books_Report.xlsx') as writer:
    df.to_excel(writer, sheet_name='All_Books', index=False)
    avg_prices.to_excel(writer, sheet_name='Average_Prices_Analysis')

print("\nProject is done 'average_price_by_rating.png'.")

with pd.ExcelWriter('Mega_Books_Report.xlsx') as writer:
    df.to_excel(writer, sheet_name='All_Books', index=False)
    avg_prices.to_excel(writer, sheet_name='Average_Prices_Analysis')

print("\n--- PROJECT COMPLETED ---")
print("1. Excel report with analysis: Mega_Books_Report.xlsx")
print("2. Price analysis chart: price_analysis.png")