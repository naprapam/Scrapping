from encodings.punycode import T
import requests as req
from bs4 import BeautifulSoup as bs
import csv

#Judul di setiap tanggal dan hamalan pada bulan yang sama
BASE_URL_M = 'https://indeks.kompas.com/?site=all&date=2024-'
page_num_m = 1
day_m = 1
month = 1
result_m = []
nomor_m = 0

for month in range(1,13): #Mendefinisikan Bulan
    for day_m in range(1,32): #Mendefinisikan Tanggal
        #Menjalankan pengambilan judul
        while True:
            url_m = f'{BASE_URL_M}{month}-{day_m}&page={page_num_m}'
                
            response_m = req.get(url_m)    

            #Menghentikan loop ketika tidak diijinkan masuk oleh website       
            if response_m.status_code !=200:
                print(f'failed to retrieve day {day_m}-{month}-2024 page {page_num_m}')
                break

            #Jika diijinkan, lanjut mengambil judul        
            soup = bs(response_m.text, 'html.parser')
            page_item = soup.find_all('div', class_='articleItem')

            #Menghentikan loop ketika sudah tidak ada konten di halaman tersebut        
            if not page_item:
                print(f'Tidak menemukan data pada Tanggal {day_m}-{month}-2024 setelah Halaman {page_num_m-1}')
                page_num_m = 1 #reset halaman ketika pada hari tersebut telah selesai
                break
                
            #Mengambil judul   
            for link in page_item:
                link_item = link.find('a', class_='article-link')
                tautan = link_item['href']
                judul_item = link.find('h2', class_='articleTitle')
                judul = judul_item.get_text(strip=True)           
                                   
                result_m.append({'Tanggal': day_m, 'Bulan': month, 'Judul': judul, 'Link': tautan}) #Menyimpan judul
           
            page_num_m += 1 #Menambah halaman untuk kelanjutan looping, karena looping akan memutar di halaman yang sama tanpa variabel ini            
           
        #Memanggil jumlah judul yang ada di seluruh halaman
        print(f'Banyak Judul Tanggal {day_m}-{month}-2024: {len(result_m)}')

        #Menampilkan judul 
        for item in result_m:
            nomor_m+=1

        #Simpan ke csv
        with open("Kompas_thn_Judul+Link1.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["Nomor", "Tanggal", "Bulan", "Judul", "Link"]
            writer= csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
        
            for i, item in enumerate(result_m, start=1):
                item['Nomor'] = i
                writer.writerow(item)
