import requests
from bs4 import BeautifulSoup
import re

token   = "sizin_bot_idniz"      #telegram token -> @jiyanos_bot
tr_chat_id = "sizin_kanal_idniz" #telegram id    -> t.me/kuponkodu

file = open("site.txt","r",encoding="utf-8")
site_adres = file.read()
file.close()

def dilTara(dil, chat_id):
    sayac        = 0
    url          = site_adres + '/language/' + dil + '/1'
    r            = requests.get(url)
    soup         = BeautifulSoup(r.content, 'lxml')
    sayfasayisi  = soup.find('div', {'class', 'ui grid'}).find_all('li')
    sayfa_sayisi = int(sayfasayisi[0].text)

    for k in range(sayfa_sayisi):
        url  = site_adres +'/language/' + dil + '/' + str(k)
        r    = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        data = soup.find_all('a', {'class': 'card-header'})

        for i in data:
            sayac += 1            
            url2      = site_adres + "/go/" + i.get('href')[34::]
            r2        = requests.get(url2)
            soup2     = BeautifulSoup(r2.content, 'lxml')
            ok        = re.search('<a href="(https://www.udemy.com/course.*)" target=', str(soup2))
            kursLinki = ok.group(1)
            linkKont = kursLinki.find('couponCode')

            if linkKont != -1:
                print(str(sayac).rjust(2, "0"), '- ', sep='', end='')
                print(end='')
                print(i.text)
                print(kursLinki)
                print('-' * 103)
                requests.post(url='https://api.telegram.org/bot{0}/sendMessage'.format(token), data={'chat_id': chat_id, 'text': kursLinki}).json()
          
            if sayac % 40 == 0:
               input('*** Devam etmek için [ENTER] tuşuna basınız *** \n')
            

def tara():
    while True:
        print("""#################### erhanurgun.com.tr ####################
                1. [TR] Udemy Kursları""")
        cevap = input('Kurs seçiniz : ')
        print("#" * 52,"\n")
        if cevap == '1':
            dilTara('Turkish', tr_chat_id)
        else:
            print('-' * 52)
            print('Lütfen iki seçenekten birini seçiniz...')
            print('-' * 52, '\n')

try:
    tara()
except:
    tara()