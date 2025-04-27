import cv2
from pyzbar import pyzbar

# Ürün veri tabanı (barkod -> (ürün ismi, fiyatı, ağırlığı))
urunler = {
    '1': ('Beyaz Çikolata', 25, 100),    # 100 gram
    '2': ('Bitter Çikolata', 30, 120),   # 120 gram
    '3': ('Sütlü Çikolata', 28, 110)     # 110 gram
}

# Sepet bilgisi
okutulan_urun_sayisi = 0
toplam_fiyat = 0
toplam_agirlik = 0  # Toplam ağırlık

# Son okutulan barkodları takip etmek için
onceki_barkodlar = set()

def read_barcodes(frame):
    global okutulan_urun_sayisi, toplam_fiyat, toplam_agirlik, onceki_barkodlar

    barcodes = pyzbar.decode(frame)
    guncel_barkodlar = set()

    for barcode in barcodes:
        barcode_info = barcode.data.decode('utf-8')
        guncel_barkodlar.add(barcode_info)

        # Eğer bu barkod önceki frame’de yoksa, yeni okutulmuş demektir
        if barcode_info not in onceki_barkodlar:
            urun_bilgisi = urunler.get(barcode_info, ('Bilinmeyen Ürün', 0, 0))
            urun_adi, fiyat, agirlik = urun_bilgisi

            okutulan_urun_sayisi += 1
            toplam_fiyat += fiyat
            toplam_agirlik += agirlik

            print(f"Okunan Barkod: {barcode_info} -> Ürün: {urun_adi} -> Fiyat: {fiyat} TL -> Ağırlık: {agirlik}g")

        # Barkodun etrafına dikdörtgen çizelim
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        urun_bilgisi = urunler.get(barcode_info, ('Bilinmeyen Ürün', 0, 0))
        urun_adi, _, _ = urun_bilgisi
        cv2.putText(frame, urun_adi, (x + 6, y - 6), font, 0.8, (255, 255, 255), 1)

    # Son frame’de görülen barkodlar güncellenir
    onceki_barkodlar = guncel_barkodlar

    return frame

def main():
    global okutulan_urun_sayisi, toplam_fiyat, toplam_agirlik

    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()

    while ret:
        ret, frame = camera.read()
        frame = read_barcodes(frame)

        # Sağ üst köşeye Ürün Sayısı, Toplam Fiyat ve Toplam Ağırlık yaz
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, f"Urun Sayisi: {okutulan_urun_sayisi}", (10, 30), font, 0.8, (0, 255, 255), 2)
        cv2.putText(frame, f"Toplam Fiyat: {toplam_fiyat} TL", (10, 65), font, 0.8, (0, 255, 255), 2)
        cv2.putText(frame, f"Toplam Agirlik: {toplam_agirlik} g", (10, 100), font, 0.8, (0, 255, 255), 2)

        cv2.imshow('Baggy Alisveris Ekrani', frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC tusu
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
