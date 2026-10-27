# SPKLU Route Optimizer

Program Python untuk mencari SPKLU (Stasiun Pengisian Kendaraan Listrik Umum) terbaik berdasarkan lokasi mobil dan sisa baterai. Program menghitung jarak ke setiap SPKLU, memilih yang terjangkau, meranking berdasarkan jarak dan waktu pengisian, lalu menampilkan rute terbaik di peta.

## Fitur

- Input lokasi mobil (latitude, longitude) dan sisa baterai (%)
- Estimasi jarak tempuh dari sisa baterai
- Perhitungan jarak ke setiap SPKLU dengan `geopy` (geodesic)
- Penyaringan SPKLU yang dapat dijangkau
- Ranking SPKLU dengan dynamic programming (jarak + waktu pengisian)
- Rute jalan ke SPKLU terbaik dari OSRM
- Peta interaktif hasil visualisasi (`map_spklu1.html`)

## Cara Kerja

1. Program membaca data SPKLU dari `dataset_mobil.csv`.
2. Sisa baterai diubah menjadi estimasi jarak tempuh (asumsi: baterai 50 kWh, efisiensi 6 km/kWh).
3. SPKLU di luar jangkauan dibuang.
4. Setiap SPKLU dihitung cost-nya: `cost = jarak + (waktu_charge x 10)`.
5. SPKLU dengan cost terendah dipilih sebagai hasil terbaik.
6. Rute dari lokasi mobil ke SPKLU terbaik digambar di peta.

## Teknologi

| Kategori | Teknologi |
|---|---|
| Bahasa | Python 3 |
| Library | pandas, geopy, folium, requests |
| Routing | OSRM (Open Source Routing Machine) |
| Data | CSV (14 SPKLU di Jakarta) |

## Instalasi

```bash
git clone https://github.com/ziezyy/SPKLU-Route-Optimizer.git
cd SPKLU-Route-Optimizer
pip install -r requirements.txt
```

## Cara Menjalankan

```bash
python app2.py
```

Lalu isi data yang diminta, misalnya:

```
masukkan latitude mobil : -6.1804066
masukkan longitude mobil : 106.8229008
Masukkan sisa baterai saat ini (%) : 40
```

Hasilnya berupa ranking SPKLU di terminal dan file `map_spklu1.html`. Buka file itu di browser untuk melihat peta. Program membutuhkan koneksi internet untuk mengambil rute dari OSRM.


## Struktur File

| File | Keterangan |
|---|---|
| `app2.py` | Program utama |
| `jarak.py` | Contoh perhitungan jarak dua titik |
| `dataset_mobil.csv` | Data SPKLU (nama, koordinat, daya, tipe charger, alamat) |
| `dataset_mobil.xlsx` | Versi Excel dari dataset |
| `map_spklu1.html` | Contoh peta hasil program |

## Penulis

[FJ] - [GitHub](https://github.com/ziezyy)