import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

results = []
# Zwiększ liczbę w range(1, 4), aby pobrać jeszcze więcej stron
for page in range(1, 4):
    url = f"https://books.toscrape.com/catalogue/page-{page}.html"
    print(f"Pobieranie danych ze strony nr {page}...")
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', class_='product_pod')

    for book in books:
        title = book.h3.a['title']
        
        # 1. Czyszczenie ceny
        raw_price = book.find('p', class_='price_color').text
        clean_price = float("".join(char for char in raw_price if char.isdigit() or char == '.'))
        
        # 2. Pobieranie oceny (jest zapisana jako klasa tekstowa, np. "star-rating Three")
        rating_classes = book.find('p', class_='star-rating')['class']
        rating = rating_classes[1] # Wyciąga słowo "Three", "Four" itp.

        results.append({
            'Title': title,
            'Price (£)': clean_price,
            'Rating': rating
        })
    
    # Krótka pauza, żeby nie przeciążyć serwera (dobra praktyka scrapera)
    time.sleep(1)

# --- ANALIZA DANYCH (Wklej to tutaj) ---
df = pd.DataFrame(results)

# Zamieniamy oceny tekstowe na liczby, żeby móc je profesjonalnie sortować
rating_dict = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
df['Rating_Num'] = df['Rating'].map(rating_dict)

# Liczymy średnią cenę dla każdej kategorii ocen (np. średnia cena książek z 5 gwiazdkami)
avg_prices = df.groupby('Rating')['Price (£)'].mean().sort_values()

print("\n--- ANALIZA ---")
print("Średnie ceny według ocen:")
print(avg_prices)

# --- WIZUALIZACJA ---
# --- WIZUALIZACJA (Nowa, ładniejsza wersja) ---
import matplotlib.pyplot as plt
import seaborn as sns

# Ustawiamy styl "whitegrid" - czysty i nowoczesny
sns.set_style("whitegrid")

# Tworzymy figurę o dobrych proporcjach
plt.figure(figsize=(12, 7))

# 1. Tworzymy ładny wykres słupkowy (Bar Chart)
# 'palette="viridis"' nadaje automatycznie spójne, ładne kolory
barplot = sns.barplot(x='Rating', y='Price (£)', data=df, 
                      order=['One', 'Two', 'Three', 'Four', 'Five'],
                      palette="viridis", ci=None) # ci=None usuwa słupki błędu

# 2. Dodajemy tytuł i etykiety osi po angielsku (pod GitHub)
plt.title('Average Book Prices by Rating Category', fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Star Rating', fontsize=14)
plt.ylabel('Average Price (£)', fontsize=14)

# 3. Formatowanie osi Y (dodajemy znak £ i zaokrąglamy do 2 miejsc po przecinku)
from matplotlib.ticker import StrMethodFormatter
plt.gca().yaxis.set_major_formatter(StrMethodFormatter('£{x:.2f}'))

# 4. Dodajemy etykiety z wartościami nad słupkami, żeby wykres był "interaktywny"
for p in barplot.patches:
    barplot.annotate(format(p.get_height(), '.2f') + ' £', 
                     (p.get_x() + p.get_width() / 2., p.get_height()), 
                     ha = 'center', va = 'center', 
                     xytext = (0, 10), 
                     textcoords = 'offset points',
                     fontsize=12, fontweight='bold')

# 5. Zapisujemy do pliku
plt.tight_layout()
plt.savefig('average_price_by_rating.png')

# Zapis do Excela z dwoma arkuszami
with pd.ExcelWriter('Mega_Books_Report.xlsx') as writer:
    df.to_excel(writer, sheet_name='All_Books', index=False)
    avg_prices.to_excel(writer, sheet_name='Average_Prices_Analysis')

print("\nProjekt 2 zakończony! Nowy wykres zapisany jako 'average_price_by_rating.png'.")

# Zapis do Excela z dwoma arkuszami: dane źródłowe i gotowa analiza
with pd.ExcelWriter('Mega_Books_Report.xlsx') as writer:
    df.to_excel(writer, sheet_name='All_Books', index=False)
    avg_prices.to_excel(writer, sheet_name='Average_Prices_Analysis')

print("\n--- PROJEKT 2 ZAKOŃCZONY SUKCESEM ---")
print("1. Raport Excel z analizą: Mega_Books_Report.xlsx")
print("2. Wykres analizy cen: price_analysis.png")