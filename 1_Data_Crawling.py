import requests as req
from bs4 import BeautifulSoup as bs

#Judul untuk 1 halaman yang sama
response = req.get('https://indeks.kompas.com/?site=all&date=2024-01-01&page=3')
soup = bs(response.text, 'html.parser')
page_block = soup.find_all('div', class_='articleItem-box')

#Memanggil jumlah judul yang ada di halaman ini
print(f'Banyak Judul: {len(page_block)}')

#Mengambil setiap judul
result = []
for block in page_block:
    judul_block = block.find('h2', class_='articleTitle')
    judul = judul_block.get_text(strip=True)

    kategori_block = block.find('div', class_='articlePost-subtitle')
    kategori = kategori_block.get_text(strip=True)

    result.append({'Judul': judul, 'Kategori': kategori})

#Menampilkan judul
for item in result:
    print(f'Judul: {item['Judul']} - Kategori: {item['Kategori']}') 
