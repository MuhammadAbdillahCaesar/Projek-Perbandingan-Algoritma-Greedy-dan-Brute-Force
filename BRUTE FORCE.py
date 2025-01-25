import pandas as pd

# Membaca dataset
dataset = pd.read_excel('corrected_fruit_dataset.xlsx')

# Fungsi brute force untuk knapsack dengan memoization
def knapsack_brute_force(items, capacity):
    n = len(items)
    
    # Dictionary untuk memoization
    memo = {}
    
    # Fungsi rekursif dengan memoization
    def knapsack_recursive(index, current_weight, current_value, current_combination):
        # Jika sudah di luar index barang
        if index == n:
            return current_value, current_combination
        
        # Memoization key berdasarkan state (index, current_weight)
        key = (index, current_weight)
        if key in memo:
            return memo[key]
        
        # Inisialisasi variabel
        best_value = current_value
        best_combination = current_combination
        
        # Pilih untuk tidak mengambil barang ini
        val_without_item, comb_without_item = knapsack_recursive(index + 1, current_weight, current_value, current_combination)
        if val_without_item > best_value:
            best_value = val_without_item
            best_combination = comb_without_item
        
        # Pilih untuk mengambil barang ini jika muat di knapsack
        item_weight = items[index][1]
        item_value = items[index][2]
        if current_weight + item_weight <= capacity:
            val_with_item, comb_with_item = knapsack_recursive(index + 1, current_weight + item_weight, current_value + item_value, current_combination + [(items[index][0], item_weight)])
            if val_with_item > best_value:
                best_value = val_with_item
                best_combination = comb_with_item
        
        # Simpan hasil ke memo
        memo[key] = (best_value, best_combination)
        return memo[key]
    
    # Mulai pencarian dari barang pertama
    return knapsack_recursive(0, 0, 0, [])

# Konversi dataset menjadi list yang berisi (nama, berat, harga, rasio harga/berat)
items = []
for index, row in dataset.iterrows():
    items.append((row['Name'], row['Weight (kg)'], row['Value (Ribu IDR)'], row['Ratio ']))

# Sortir items berdasarkan rasio harga/berat untuk memprioritaskan barang bernilai tinggi
items.sort(key=lambda x: x[3], reverse=True)

# Kapasitas kendaraan berdasarkan pilihan user
vehicle_choice = input("Pilih kendaraan (motor/mobil/truk): ").lower()
if vehicle_choice == "motor":
    capacity = 50
elif vehicle_choice == "mobil":
    capacity = 150
elif vehicle_choice == "truk":
    capacity = 1000
else:
    print("Pilihan kendaraan tidak valid.")
    exit()

# Hitung solusi untuk kendaraan yang dipilih
best_value, best_combination = knapsack_brute_force(items, capacity)

# Hitung total berat barang yang dipilih
total_weight = sum(item[1] for item in best_combination)

# Output hasil
best_value_formatted = f"Rp{best_value:,.0f}".replace(",", ".") + ".000"  # Modify this line
print(f"Hasil untuk kendaraan {vehicle_choice}:")
print(f"Total nilai: {best_value_formatted}")
print(f"Total berat: {total_weight} kg")
print("Barang yang dipilih:")
for item in best_combination:
    print(f" - {item[0]} (Berat: {item[1]} kg)")