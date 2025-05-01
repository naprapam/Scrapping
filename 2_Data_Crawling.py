import requests as req
from bs4 import BeautifulSoup as bs
import csv

#Judul untuk 1 tanggal yang sama
BASE_URL = 'https://indeks.kompas.com/?site=all&date=2024-01-01'
page_num = 1
result = []
nomor = 0

while True:
    url1 = f"{BASE_URL}&page={page_num}"

    response = req.get(url1)
    if response.status_code !=200:
        print(f'failed to retrieve page {page_num}')
        break
    
    soup = bs(response.text, 'html.parser')
    page_block = soup.find_all('div', class_='articleItem-box')

    if not page_block:
        print(f'No more data found on page{page_num}')
        break

    for block in page_block:
        judul_block = block.find('h2', class_='articleTitle')
        judul = judul_block.get_text(strip=True)
        

        result.append({'Judul': judul})

    page_num += 1
    

#Memanggil jumlah judul yang ada di seluruh halaman
print(f'Banyak Judul: {len(result)}')

#Menampilkan judul
for item in result:
    nomor+=1
    print(f'{nomor}: {item['Judul']}') 

#Simpan ke csv
with open("Kompas_Judul2.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Nomor", "Judul"]
    writer= csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for i, item in enumerate(result, start=1):
        item['Nomor'] = i
        writer.writerow(item)
