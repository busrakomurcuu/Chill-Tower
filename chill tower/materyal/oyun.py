# -*- coding: utf-8 -*-
"""
Created on Thu May 16 01:29:05 2024

@author: ecems
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May 15 21:11:41 2024
@author: ecems
"""

import pygame as pg 
import random, sys

pg.init()

SCREEN_WIDTH = 350
SCREEN_HEIGHT = 500

ekran = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
zaman = pg.time.Clock()

pg.display.set_caption("ICY TOWER")

zemin = pg.image.load(r"C:\Users\BÜŞRA\Desktop\oyunson\Yeni klasör\zemin_buz.jpg")
background = pg.image.load(r"C:\Users\BÜŞRA\Desktop\oyunson\Yeni klasör\background2.jpg")
background = pg.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

karakter = pg.image.load(r"C:\Users\BÜŞRA\Desktop\oyunson\Yeni klasör\karakter_ucak.png")
karakter_rect = karakter.get_rect(center = (50,256))

zemin_x_poz = 0
yercekimi = 0.125
karakterHareketi = 0

buz_sutun = pg.image.load(r"C:\Users\BÜŞRA\Desktop\oyunson\Yeni klasör\ice.png")
buz_sutun_list = []
sutun_uret = pg.USEREVENT + 0
pg.time.set_timer(sutun_uret, 1200)
sutun_yukseklik = [200,250,300,350,400]

oyun_aktif = False
oyun_basla = pg.image.load(r"C:\Users\BÜŞRA\Desktop\oyunson\Yeni klasör\başlangıç.png")
oyun_basla_rect = oyun_basla.get_rect(center=(140,180))
oyun_basla = pg.transform.rotozoom(oyun_basla,0,1.4)

oyun_bitti_img = pg.image.load(r"C:\Users\BÜŞRA\Desktop\oyunson\Yeni klasör\oyun_bitti.png")
oyun_bitti_img = pg.transform.rotozoom(oyun_basla,0,1.4)
oyun_bitti_rect = oyun_bitti_img.get_rect(center=(140,180))

yildiz = pg.image.load(r"C:\Users\BÜŞRA\Desktop\oyunson\Yeni klasör\star.png")
yildiz = pg.transform.scale(yildiz, (30, 30))  # Yıldız boyutunu ayarlayın
yildiz_rect_list = []

skor = 0
rekor = 0
skor_yüzeyi = False

yazı_tipi = pg.font.Font("04B_19.TTF",40)

zıplama_ses = pg.mixer.Sound("uçma.ogg")
olme_ses = pg.mixer.Sound("çarpma.wav")
yıldız_toplama_ses = pg.mixer.Sound("geçme.ogg")

def zemin_konumlandırma():
    ekran.blit(zemin, (zemin_x_poz, 450))
    ekran.blit(zemin, (zemin_x_poz+zemin.get_width(), 450))
    
def sutun_olusturma():
    random_sutun_pozisyon = random.choice(sutun_yukseklik)
    alt_sutun = buz_sutun.get_rect(midtop = (400,random_sutun_pozisyon))
    ust_sutun = buz_sutun.get_rect(midbottom = (400,random_sutun_pozisyon - 150))
    return alt_sutun, ust_sutun

def sutun_yerlestirme(sutunlar):
    for sutun in sutunlar:
        ekran.blit(buz_sutun, sutun)
        
def sutun_tasıma(sutunlar):
    for sutun in sutunlar:
        sutun.centerx -= 3
    return sutunlar

def carpısma(sutunlar):
    for sutun in sutunlar:
        if karakter_rect.colliderect(sutun):
            olme_ses.play()
            return True  # Çarpışma oldu, oyun devam etmeyecek
        if karakter_rect.top <= -50 or karakter_rect.bottom >= 450:
            return True  # Ekranın üst veya alt sınırına çarptı, oyun devam etmeyecek
    return False  # Hiçbir çarpışma olmadı, oyun devam edecek

# Yıldız oluşturma fonksiyonu
def yildiz_olustur():
    # Sütunların altında yer alacak bir yıldız oluşturmak için, sütunların alt kısmını baz alarak yıldız oluşturabiliriz.
    # Bunu yapmak için buz_sutun_listesi içindeki her sütunun alt sınırlarını kullanabiliriz.
    sütun_alt_konumlar = [sutun.bottom for sutun in buz_sutun_list]
    if sütun_alt_konumlar:  # Eğer buz_sutun_listesi boş değilse (yani ekranda sütunlar varsa)
        yildiz_y = random.choice(sütun_alt_konumlar)  # Yıldızın y konumunu rastgele bir sütunun alt kısmından seç
    else:
        # Eğer ekranda hiç sütun yoksa, yıldızın y konumunu rastgele bir yükseklikte seç
        yildiz_y = random.randint(50, SCREEN_HEIGHT - 50)
    yildiz_x = SCREEN_WIDTH + random.randint(50, 200)  # Yıldızın sağ taraftan ekrana girme mesafesi
    yildiz_rect = yildiz.get_rect(center=(yildiz_x, yildiz_y))
    return yildiz_rect


def yildiz_ekle():
    for yildiz_rect in yildiz_rect_list:
        ekran.blit(yildiz, yildiz_rect)

# Yıldız hareketi
def yildiz_hareket():
    for yildiz_rect in yildiz_rect_list:
        yildiz_rect.centerx -= 3  # Yıldızın sola doğru hareket hızı

# Yıldız kontrolü
def yildiz_kontrol():
    for yildiz_rect in yildiz_rect_list:
        if karakter_rect.colliderect(yildiz_rect):
            yıldız_toplama_ses.play()
            yildiz_rect_list.remove(yildiz_rect)
            return True  # Yıldıza çarpışma oldu, puan kazan
    return False  # Hiçbir yıldıza çarpılmadı

def rekor_guncelle(skor,rekor):
    if skor > rekor:
        rekor = skor
    return rekor

def skor_goster(oyun_durum):
    if oyun_durum == "oyun_bitti":
        if skor < 0:
            skor_yüzeyi = yazı_tipi.render(str(int(0)), True,(255,255,255))
        if skor > 0:
            skor_yüzeyi = yazı_tipi.render(f'Skor: {int(skor)}', True,(255,255,255))
        skor_rect = skor_yüzeyi.get_rect(center=(144,50))
        ekran.blit(skor_yüzeyi,skor_rect)
        
        """rekor_yüzeyi = yazı_tipi.render((f'Rekor: {int(rekor)}', True,(255,255,255)))
        rekor_rect = rekor_yüzeyi.get_rect(center = (144,425))"""
    if oyun_durum == "main_oyun":
        if skor < 0:
            skor_yüzeyi = yazı_tipi.render(str(int(0)), True,(255,255,255))
        if skor > 0:
            skor_yüzeyi = yazı_tipi.render(f'Skor: {int(skor)}', True,(255,255,255))
        
    
    
# OYUN DÖNGÜMÜZ
while True:
    for olay in pg.event.get():
        if olay.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if olay.type == pg.KEYDOWN:
            if olay.key == pg.K_SPACE and oyun_aktif == True:
                karakterHareketi = 0
                karakterHareketi -= 5
                zıplama_ses.play()
            if olay.key == pg.K_SPACE and oyun_aktif == False:
                oyun_aktif = True
                buz_sutun_list.clear()
                karakter_rect.center = (50, 256)
                karakter_ivme = 0
                skor = 0
                skor_yüzeyi = True
        if olay.type == sutun_uret:  # sutun_uret çalıştığı anda sutun listesine sutun ekleyeceğiz
            buz_sutun_list.extend(sutun_olusturma())
    
    ekran.blit(background, (0, 0))  # döngü bittikten sonra direkt arka plan çalışması iyi
    
    # ÇARPIŞMA KONTROLÜ
    if oyun_aktif:
        if carpısma(buz_sutun_list):
            oyun_aktif = False  # Çarpışma olduğunda oyun duracak
            if skor > rekor:  # Eğer skor rekoru geçtiyse, rekoru güncelle
                rekor = skor
        else:
            buz_sutun_list = sutun_tasıma(buz_sutun_list)
            sutun_yerlestirme(buz_sutun_list)  # karakter_rect in merkez y sine yercekimini ekliyoruz.
            karakterHareketi += yercekimi  # ivme arttıkça karakterin hızı artıyor
            karakter_rect.centery += karakterHareketi
            ekran.blit(karakter, karakter_rect)
            if random.randint(0, 100) < 2:  # Her frame'de bir yıldız ekleme şansı
                yildiz_rect_list.append(yildiz_olustur())
            yildiz_ekle()
            yildiz_hareket()
            # Yıldız çarpışma kontrolü
            if yildiz_kontrol():
                skor += 1
    else:
        ekran.blit(oyun_basla, oyun_basla_rect)
        if skor > 0:  # Oyun bittiğinde ve skor varsa rekoru ekrana yazdır
            rekor_yazi = yazı_tipi.render(f'Rekor: {rekor}', True, (255, 255, 255))
            rekor_rect = rekor_yazi.get_rect(center=(SCREEN_WIDTH // 2, 100))
            ekran.blit(rekor_yazi, rekor_rect)
    
    if skor_yüzeyi:
        # Skoru göster
        skor_yüzeyi = yazı_tipi.render(f'Skor: {skor}', True, (255, 255, 255))
        skor_rect = skor_yüzeyi.get_rect(center=(SCREEN_WIDTH // 2, 50))
        ekran.blit(skor_yüzeyi, skor_rect)
    
    
    # ZEMİN
    zemin_x_poz -= 3  # zemin her bir frame de üç sola kayıyor
    zemin_konumlandırma()
    if zemin_x_poz <= -350:  # zemin ekranın sonuna geldiğinde tekrar başa dönsün ve animasyon oluşsun
        zemin_x_poz = 0
    
    pg.display.update()
    zaman.tick(60)
