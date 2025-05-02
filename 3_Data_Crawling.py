from encodings.punycode import T
import requests as req
from bs4 import BeautifulSoup as bs
import csv

#Judul di setiap tanggal dan hamalan pada bulan yang sama
BASE_URL_ = 'https://indeks.kompas.com/?site=all&date=2024-01-'
page_num_ = 1
day_ = 1
result_ = []
nomor_ = 0

for day_ in range(1,35): #Mendefinisikan Tanggal
    
    #Menjalankan pengambilan judul
    while True:
        url_ = f'{BASE_URL_}{day_}&page={page_num_}'
                
        response_ = req.get(url_)    

        #Menghentikan loop ketika tidak diijinkan masuk oleh website       
        if response_.status_code !=200:
            print(f'failed to retrieve day {day_}-01-2024 page {page_num_}')
            break

        #Jika diijinkan, lanjut mengambil judul        
        soup = bs(response_.text, 'html.parser')
        page_block = soup.find_all('div', class_='articleItem-box')

        #Menghentikan loop ketika sudah tidak ada konten di halaman tersebut        
        if not page_block:
            print(f'Tidak menemukan data pada Tanggal {day_}-01-2024 setelah Halaman {page_num_-1}')
            page_num_ = 1 #reset halaman ketika pada hari tersebut telah selesai
            break
                
        #Mengambil judul   
        for block in page_block:
            judul_block = block.find('h2', class_='articleTitle')
            judul = judul_block.get_text(strip=True)
                    
            result_.append({'Tanggal': day_, 'Judul': judul}) #Menyimpan judul
        
        page_num_ += 1 #Menambah halaman untuk kelanjutan looping, karena looping akan memutar di halaman yang sama tanpa variabel ini
    

    #Memanggil jumlah judul yang ada di seluruh halaman
    print(f'Banyak Judul Tanggal {day_}-01-2024: {len(result_)}')

    #Menampilkan judul 
    for item in result_:
        nomor_+=1

    #Simpan ke csv
    with open("Kompas_bln_Judul9.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Nomor", "Tanggal", "Judul"]
        writer= csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        
        for i, item in enumerate(result_, start=1):
            item['Nomor'] = i
            writer.writerow(item)
