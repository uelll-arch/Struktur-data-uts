"""Mini Project Struktur Data - Perpustakaan Mini"""
from datetime import datetime, timedelta

# ==================== DATA ====================
# Array 1D: daftar semua buku
data_buku = [
    {"id": "B001", "judul": "Algoritma dan Pemrograman", "pengarang": "Rinaldi Munir", "tahun": 2016, "tersedia": True},
    {"id": "B002", "judul": "Laskar Pelangi", "pengarang": "Andrea Hirata", "tahun": 2005, "tersedia": True},
    {"id": "B003", "judul": "Struktur Data dengan Python", "pengarang": "Budi Raharjo", "tahun": 2019, "tersedia": True},
    {"id": "B004", "judul": "Bumi Manusia", "pengarang": "Pramoedya Ananta Toer", "tahun": 1980, "tersedia": True},
    {"id": "B005", "judul": "Basis Data", "pengarang": "Abdul Kadir", "tahun": 2014, "tersedia": True},
]

# nomor terakhir dipakai untuk membuat ID buku baru
nomor_terakhir = 5

# Array 2D: denah rak (3 baris x 4 kolom), isinya ID buku atau None kalau kosong
rak = [
    [None, None, None, None],
    [None, None, None, None],
    [None, None, None, None],
]

# ==================== TAMPILAN ====================
def tampilkan_buku(daftar):
    print()
    print(f"{'ID':<6}{'Judul':<30}{'Pengarang':<24}{'Tahun':<7}{'Status':<10}Jatuh Tempo")
    hari_ini = datetime.now().date()

    for buku in daftar:
        if buku["tersedia"]:
            status = "Tersedia"
        else:
            status = "Dipinjam"

        # jatuh tempo hanya ada kalau buku sedang dipinjam
        if "jatuh_tempo" in buku:
            tempo = str(buku["jatuh_tempo"])
            if buku["jatuh_tempo"] < hari_ini:
                tempo = tempo + " (TELAT)"
        else:
            tempo = "-"

        print(f"{buku['id']:<6}{buku['judul']:<30}{buku['pengarang']:<24}{buku['tahun']:<7}{status:<10}{tempo}")

# ==================== RAK (ARRAY 2D) ====================
def taruh_di_rak(id_buku):
    for i in range(len(rak)):
        for j in range(len(rak[i])):
            if rak[i][j] is None:
                rak[i][j] = id_buku
                return True
    print("Rak penuh, buku tetap tercatat tapi tidak punya tempat di rak.")
    return False

def ambil_dari_rak(id_buku):
    for i in range(len(rak)):
        for j in range(len(rak[i])):
            if rak[i][j] == id_buku:
                rak[i][j] = None

def lihat_rak():
    for i in range(len(rak)):
        print(f"Rak {i + 1}:", end=" ")
        for j in range(len(rak[i])):
            if rak[i][j] is None:
                print(f"{'[kosong]':<9}", end="  ")
            else:
                print(f"{rak[i][j]:<9}", end="  ")
        print()

# ==================== OPERASI BUKU ====================
def tambah_buku():
    global nomor_terakhir

    judul = input("Judul: ")
    pengarang = input("Pengarang: ")
    tahun = input("Tahun: ")

    if not tahun.isdigit():
        print("Tahun harus berupa angka.")
        return

    nomor_terakhir += 1
    id_baru = "B" + str(nomor_terakhir).zfill(3)  # contoh: B006

    buku_baru = {
        "id": id_baru,
        "judul": judul,
        "pengarang": pengarang,
        "tahun": int(tahun),
        "tersedia": True,
    }
    data_buku.append(buku_baru)
    taruh_di_rak(id_baru)
    print("Buku berhasil ditambahkan dengan ID", id_baru)

def hapus_buku():
    id_cari = input("ID buku yang dihapus: ").upper()

    for i in range(len(data_buku)):
        if data_buku[i]["id"] == id_cari:
            data_buku.pop(i)
            ambil_dari_rak(id_cari)
            print("Buku berhasil dihapus.")
            return

    print("ID tidak ditemukan.")

def ubah_status_pinjam():
    id_cari = input("ID buku: ").upper()

    for buku in data_buku:
        if buku["id"] == id_cari:
            if buku["tersedia"]:
                # buku dipinjam, batas pengembalian 7 hari
                buku["tersedia"] = False
                buku["jatuh_tempo"] = datetime.now().date() + timedelta(days=7)
                print("Buku dipinjam. Jatuh tempo:", buku["jatuh_tempo"])
            else:
                # buku dikembalikan, hapus data jatuh tempo
                buku["tersedia"] = True
                del buku["jatuh_tempo"]
                print("Buku sudah dikembalikan.")
            return

    print("ID tidak ditemukan.")

# ==================== SEARCHING ====================
def linear_search(daftar, kata_kunci):
    hasil = []
    langkah = 0
    for buku in daftar:
        langkah += 1
        if kata_kunci.lower() in buku["judul"].lower():
            hasil.append(buku)
    return hasil, langkah

def binary_search(daftar, id_cari):
    # syarat: daftar sudah terurut berdasarkan ID
    kiri = 0
    kanan = len(daftar) - 1
    langkah = 0

    while kiri <= kanan:
        langkah += 1
        tengah = (kiri + kanan) // 2

        if daftar[tengah]["id"] == id_cari:
            return tengah, langkah
        elif daftar[tengah]["id"] < id_cari:
            kiri = tengah + 1   # cari di sisi kanan
        else:
            kanan = tengah - 1  # cari di sisi kiri

    return -1, langkah

def binary_search_rekursif(daftar, id_cari, kiri, kanan):
    if kiri > kanan:
        return -1

    tengah = (kiri + kanan) // 2

    if daftar[tengah]["id"] == id_cari:
        return tengah
    elif daftar[tengah]["id"] < id_cari:
        return binary_search_rekursif(daftar, id_cari, tengah + 1, kanan)
    else:
        return binary_search_rekursif(daftar, id_cari, kiri, tengah - 1)

# ==================== SORTING ====================
def bubble_sort(daftar, kunci):
    # bandingkan dua buku yang bersebelahan, tukar kalau urutannya salah
    n = len(daftar)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            nilai_a = daftar[j][kunci]
            nilai_b = daftar[j + 1][kunci]

            # judul dibandingkan dengan huruf kecil supaya A dan a dianggap sama
            if kunci == "judul":
                nilai_a = nilai_a.lower()
                nilai_b = nilai_b.lower()

            if nilai_a > nilai_b:
                daftar[j], daftar[j + 1] = daftar[j + 1], daftar[j]

# ==================== REKURSIF ====================
def hitung_tersedia(daftar, indeks=0):
    # base case: sudah sampai akhir daftar
    if indeks == len(daftar):
        return 0

    if daftar[indeks]["tersedia"]:
        return 1 + hitung_tersedia(daftar, indeks + 1)
    else:
        return 0 + hitung_tersedia(daftar, indeks + 1)

def tampil_judul_rekursif(daftar, indeks=0):
    # base case: berhenti kalau indeks sudah melewati data terakhir
    if indeks < len(daftar):
        print(f"{indeks + 1}. {daftar[indeks]['judul']}")
        tampil_judul_rekursif(daftar, indeks + 1)

# ==================== FUNGSI MENU ====================
def menu_cari_judul():
    kata_kunci = input("Kata kunci judul: ")
    hasil, langkah = linear_search(data_buku, kata_kunci)

    if len(hasil) > 0:
        tampilkan_buku(hasil)
    else:
        print("Buku tidak ditemukan.")
    print("Jumlah langkah pencarian:", langkah)

def menu_cari_id():
    id_cari = input("ID buku: ").upper()

    # binary search butuh data terurut, jadi urutkan salinannya dulu
    # (data_buku asli tidak berubah)
    salinan = data_buku.copy()
    bubble_sort(salinan, "id")

    posisi, langkah = binary_search(salinan, id_cari)
    posisi_rekursif = binary_search_rekursif(salinan, id_cari, 0, len(salinan) - 1)

    if posisi != -1:
        tampilkan_buku([salinan[posisi]])
    else:
        print("Buku tidak ditemukan.")
    print("Langkah binary search:", langkah)
    print("Hasil versi rekursif sama:", posisi == posisi_rekursif)

def menu_urutkan():
    print("Urutkan berdasarkan:")
    print("1. Judul")
    print("2. Tahun")
    print("3. ID")
    pilih = input("Pilih (1/2/3): ")

    if pilih == "1":
        kunci = "judul"
    elif pilih == "2":
        kunci = "tahun"
    elif pilih == "3":
        kunci = "id"
    else:
        print("Pilihan tidak valid.")
        return

    bubble_sort(data_buku, kunci)
    tampilkan_buku(data_buku)

def menu_statistik():
    jumlah = hitung_tersedia(data_buku)
    print(f"Buku tersedia: {jumlah} dari {len(data_buku)}")
    print("Daftar judul buku:")
    tampil_judul_rekursif(data_buku)

# ==================== PROGRAM UTAMA ====================
# taruh semua buku awal ke rak
for buku in data_buku:
    taruh_di_rak(buku["id"])

while True:
    print("\n=== PERPUSTAKAAN MINI ===")
    print("1. Tampilkan Semua Buku")
    print("2. Tambah Buku Baru")
    print("3. Hapus Buku")
    print("4. Ubah Status Peminjaman")
    print("5. Lihat Denah Rak")
    print("6. Cari Judul Buku")
    print("7. Cari ID Buku")
    print("8. Urutkan Daftar")
    print("9. Statistik Buku")
    pilihan = input("Pilih menu (0 untuk keluar): ")

    if pilihan == "0":
        print("Terima kasih telah menggunakan sistem!")
        break
    elif pilihan == "1":
        tampilkan_buku(data_buku)
    elif pilihan == "2":
        tambah_buku()
    elif pilihan == "3":
        hapus_buku()
    elif pilihan == "4":
        ubah_status_pinjam()
    elif pilihan == "5":
        lihat_rak()
    elif pilihan == "6":
        menu_cari_judul()
    elif pilihan == "7":
        menu_cari_id()
    elif pilihan == "8":
        menu_urutkan()
    elif pilihan == "9":
        menu_statistik()
    else:
        print("Pilihan tidak valid. Silakan coba lagi.")