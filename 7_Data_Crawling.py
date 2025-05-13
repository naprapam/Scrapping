#Cell untuk Widgets
import ipywidgets as widgets
from IPython.display import display

# Input teks untuk nama kolom
media = widgets.Text(description='Media: ')
keywords = widgets.Text(description='Keyword: ')
Tanggal_Mulai = widgets.DatePicker(description='Tanggal Awal: ')
Tanggal_Akhir = widgets.DatePicker(description='Tanggal Akhir: ')

display(media, keywords, Tanggal_Mulai, Tanggal_Akhir)

#Cell untuk Fungsi Scraping media
from bs4 import BeautifulSoup as bs
import requests as req
import csv
import urllib.parse


nomor = 1
keywords = keywords.get_interact_value()
Media = media.get_interact_value()
query1 = keywords.replace(" ", "+")
query = urllib.parse.quote(keywords)

def sc_detik(keywords):
    page_num = 1
    result = []
    base_url = 'https://www.detik.com/search/searchall?query'
    tanggal1 = Tanggal_Mulai.value.strftime("%d/%m/%Y")
    tanggal2 = Tanggal_Akhir.value.strftime("%d/%m/%Y")
    
    while True:
        url = f'{base_url}={query}&page={page_num}&fromdatex={tanggal1}&todatex={tanggal2}'
        response = req.get(url)

        #Menghentikan loop ketika halaman tidak bisa diakses
        if response.status_code!=200:
            print(f'Gagal mengambil kata tahu pada halaman {page_num}')
            break

        soup = bs(response.text, 'html.parser')
        page_block = soup.find_all('article', class_='list-content__item')

        #Menghentikan loop saat halaman sudah kosong
        if not page_block:
            print(f'Tidak ada berita setelah halaman {page_num-1}')
            break
        
        #Mengambil setiap judul
        for block in page_block:
            tanggal_block = block.find('div', class_='media__date')
            tanggal = tanggal_block.get_text(strip=True)
            judul_block = block.find('h3', class_='media__title')
            judul = judul_block.get_text(strip=True)
            link_item = block.find('a', class_='media__link')
            tautan = link_item['href']
            
            result.append({'Tanggal': tanggal, 'Judul': judul, 'Link': tautan})
        
        page_num += 1
    
    return result

def sc_kompas(keywords):
    page_num = 1
    result = []
    base_url = 'https://search.kompas.com/search?q='
    tanggal1 = Tanggal_Mulai.value.strftime("%Y-%m-%d")
    tanggal2 = Tanggal_Akhir.value.strftime("%Y-%m-%d")
    
    while True:
        url = f'{base_url}={query}&start_date={tanggal1}&end_date={tanggal2}&page={page_num}'
        response = req.get(url)

        #Menghentikan loop ketika halaman tidak bisa diakses
        if response.status_code!=200:
            print(f'Gagal mengambil kata tahu pada halaman {page_num}')
            break

        soup = bs(response.text, 'html.parser')
        page_block = soup.find_all('div', class_='articleItem')

        #Menghentikan loop saat halaman sudah kosong
        if not page_block:
            print(f'Tidak ada berita setelah halaman {page_num-1}')
            break
        
        #Mengambil setiap judul
        for block in page_block:
            link_item = block.find('a', class_='article-link')
            tautan = link_item['href']
            judul_block = block.find('h2', class_='articleTitle')
            judul = judul_block.get_text(strip=True)
            tanggal_block = block.find('div', class_='articlePost-date')
            tanggal = tanggal_block.get_text(strip=True)
            
            result.append({'Tanggal': tanggal, 'Judul': judul, 'Link': tautan})
        
        page_num += 1

    return result

#Cell untuk menampilkan dan menyimpan hasil scraping
nomor = 1


if Media == 'Detik':
    #Memanggil jumlah judul yang ada di halaman ini
    print(f'Banyak Judul (Detik): {len(sc_detik(keywords))}')

    for item in sc_detik(keywords):
        print(f'{nomor}: {item['Judul']}')
        nomor += 1
    sc_media = sc_detik

elif Media == 'Kompas':
    #Memanggil jumlah judul yang ada di halaman ini
    print(f'Banyak Judul (Kompas): {len(sc_kompas(keywords))}')

    for item in sc_kompas(keywords):
        print(f'{nomor}: {item['Tanggal']}, {item['Judul']}, {item['Link']}')
        nomor += 1
    sc_media = sc_kompas

#Simpan Judul
with open(f"{Media}_{keywords}.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Nomor", "Tanggal", "Judul", "Link"]
    writer= csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for i, item in enumerate(sc_media(keywords), start=1):
        item['Nomor'] = i
        writer.writerow(item)

