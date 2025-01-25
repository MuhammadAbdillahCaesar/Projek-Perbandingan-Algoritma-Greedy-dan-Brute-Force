import pandas as pd

# Membaca dataset dari file Excel
# Dataset berisi data mengenai barang yang tersedia, termasuk nama, berat, nilai (dalam ribuan IDR), dan rasio nilai/berat.
dataset = pd.read_excel('corrected_fruit_dataset.xlsx')

# Fungsi greedy untuk menyelesaikan masalah knapsack
# Fungsi ini memilih barang-barang berdasarkan rasio nilai/beratnya, selama total berat tidak melebihi kapasitas.
def knapsack_greedy_fixed(barang, kapasitas):
    total_nilai = 0  # Total nilai dari barang yang terpilih
    total_berat = 0  # Total berat dari barang yang terpilih
    barang_terpilih = []  # Daftar untuk menyimpan barang-barang yang terpilih

    # Iterasi melalui setiap barang
    for item in barang:
        nama_item, berat_item, nilai_item, rasio_item = item
        
        # Periksa apakah berat barang dapat ditambahkan ke dalam knapsack
        if total_berat + berat_item <= kapasitas:
            # Jika iya, tambahkan barang ke daftar terpilih
            barang_terpilih.append((nama_item, berat_item))
            total_berat += berat_item  # Perbarui total berat
            total_nilai += nilai_item  # Perbarui total nilai
        else:
            # Jika barang tidak muat, lanjutkan ke barang berikutnya
            continue

    # Kembalikan total nilai dan daftar barang yang terpilih
    return total_nilai, barang_terpilih

# Konversi dataset menjadi list barang yang berisi nama, berat, harga, dan rasio harga/berat
barang = []
for index, row in dataset.iterrows():
    barang.append((row['Name'], row['Weight (kg)'], row['Value (Ribu IDR)'], row['Ratio ']))

# Urutkan barang berdasarkan rasio harga/berat dari yang tertinggi ke terendah
# Barang dengan rasio tertinggi akan diprioritaskan untuk dipilih
barang.sort(key=lambda x: x[3], reverse=True)

# Menentukan kapasitas kendaraan berdasarkan input pengguna
# Pengguna memilih salah satu dari tiga opsi kendaraan (motor, mobil, atau truk)
# Setiap kendaraan memiliki kapasitas berat yang berbeda
pilihan_kendaraan = input("Pilih kendaraan (motor/mobil/truk): ").lower()
if pilihan_kendaraan == "motor":
    kapasitas = 50  # Kapasitas motor (kg)
elif pilihan_kendaraan == "mobil":
    kapasitas = 150  # Kapasitas mobil (kg)
elif pilihan_kendaraan == "truk":
    kapasitas = 1000  # Kapasitas truk (kg)
else:
    # Jika input tidak valid, program akan keluar
    print("Pilihan kendaraan tidak valid.")
    exit()

# Menghitung nilai maksimum dan kombinasi barang terbaik untuk kendaraan yang dipilih
nilai_terbaik, kombinasi_terbaik = knapsack_greedy_fixed(barang, kapasitas)

# Menghitung total berat barang yang dipilih
total_berat = sum(item[1] for item in kombinasi_terbaik)

# Format nilai terbaik dalam bentuk IDR (Ribu IDR) dengan pemisah ribuan titik dan tambahan ".000"
nilai_terbaik_formatted = f"Rp{nilai_terbaik:,.0f}".replace(",", ".") + ".000"

# Tampilkan hasil ke pengguna
print(f"Hasil untuk kendaraan {pilihan_kendaraan}:")
print(f"Total nilai: {nilai_terbaik_formatted}")
print(f"Total berat: {total_berat} kg")
print("Barang yang dipilih:")
for item in kombinasi_terbaik:
    print(f" - {item[0]} (Berat: {item[1]} kg)")
