import pandas as pd
import re

# Sample DataFrame
data = {
    'Title': [
        'Einfamilienhaus zum Kauf - Düsseldorf - 435.900 €',
        'Villa zum Kauf - Düsseldorf / Benrath - Preis auf Anfrage',
        'Einfamilienhaus zum Kauf - Düsseldorf- Angermu...',
        'Mehrfamilienhaus zum Kauf - Düsseldorf - 995.0...',
        'Mehrfamilienhaus zum Kauf - Düsseldorf - 3.500...',
        'Bungalow zum Kauf - Düsseldorf - 326.400 € - 4...',
        'Mehrfamilienhaus zum Kauf - Düsseldorf - 895.0...',
        'Einfamilienhaus zum Kauf - Düsseldorf / Unterb...'
    ],
    'About': [
        'Einfamilienhaus zum Kauf',
        'Villa zum Kauf',
        'Einfamilienhaus zum Kauf',
        'Mehrfamilienhaus zum Kauf',
        'Mehrfamilienhaus zum Kauf',
        'Bungalow zum Kauf',
        'Mehrfamilienhaus zum Kauf',
        'Einfamilienhaus zum Kauf'
    ],
    'Price': [
        '435.900 €',
        'Preis auf Anfrage',
        '706.400 €',
        '995.000 €',
        '3.500.000 €',
        '326.400 €',
        '895.000 €',
        '1.320.000 €'
    ],
    'Location': [
        'Stockum, Düsseldorf (40474)',
        'Benrath, Düsseldorf / Benrath (40597)',
        'Kaiserswerth, Düsseldorf- Angermund (40489)',
        'Bilk, Düsseldorf (40221)',
        'Benrath, Düsseldorf (40597)',
        'Stockum, Düsseldorf (40474)',
        'Bertha-von-Suttner-Straße 43, Hellerhof, Düsse...',
        'Unterbach, Düsseldorf / Unterbach (40627)'
    ],
    'Rooms': [
        '5 Zimmer',
        '5 Zimmer',
        '5 Zimmer',
        '5 Zimmer',
        '5 Zimmer',
        '5 Zimmer',
        '5 Zimmer',
        '5 Zimmer'
    ],
    'Size': [
        '5 Zimmer, 183 m²',
        '5 Zimmer, 340 m², 782 m² Grundstück',
        '4 Zimmer, 122 m², 299 m² Grundstück',
        '272 m², 370 m² Grundstück',
        '14 Zimmer, 579 m², 2.328 m² Grundstück',
        '4 Zimmer, 106 m²',
        '7 Zimmer, 250 m², 297 m² Grundstück',
        '5,5 Zimmer, 192,3 m², 392,2 m² Grundstück'
    ]
}

df = pd.DataFrame(data)

def clean_data(df):
    # Split Location into Address, City_Region, and City (Zip)
    def split_location(location):
        address = ""
        city_region = ""
        city_zip = ""
        
        if ',' in location:
            parts = location.split(',')
            if len(parts) == 3:
                address, city_region, city_zip = parts
            elif len(parts) == 2:
                city_region, city_zip = parts
        if '(' in city_zip and ')' in city_zip:
            city_zip = city_zip.split('(')[-1][:-1].strip()

        return pd.Series([address.strip(), city_region.strip(), city_zip.strip()])

    df[['Address', 'City_Region', 'City_Zip']] = df['Location'].apply(split_location)
    df = df.drop(columns='Location')

    # Convert Price to integer
    def convert_price(price):
        if 'Preis auf Anfrage' in price:
            return 0
        return int(price.replace('.', '').replace(' €', ''))

    df['Price'] = df['Price'].apply(convert_price)

    # Convert Rooms to integer
    df['Rooms'] = df['Rooms'].apply(lambda x: int(x.split()[0]))

    # Process Size and create new columns
    def process_size(size_str):
        zimmer = 0
        size = 0.0
        grundstueck = 0.0
        
        # Extract Zimmer
        zimmer_match = re.search(r'(\d+[,.\d]*) Zimmer', size_str)
        if zimmer_match:
            zimmer = float(zimmer_match.group(1).replace(',', '.'))
        
        # Extract Size (m²)
        size_match = re.search(r'(\d+[,.\d]*) m²(?! Grundstück)', size_str)
        if size_match:
            size = float(size_match.group(1).replace(',', '.'))
        
        # Extract Grundstück (m²)
        grundstueck_match = re.search(r'(\d+[,.\d]*) m² Grundstück', size_str)
        if grundstueck_match:
            grundstueck = float(grundstueck_match.group(1).replace(',', '.'))
        
        return pd.Series([zimmer, size, grundstueck])

    df[['Zimmer', 'Size_SqM', 'Grundstueck_SqM']] = df['Size'].apply(process_size)
    df = df.drop(columns='Size')
    
    return df

df_cleaned = clean_data(df)
df_cleaned.head()
