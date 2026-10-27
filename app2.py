#import utuk bca, hitng, visualisasi
import pandas as pd
from geopy.distance import geodesic
import folium
import requests

data = pd.read_csv("dataset_mobil.csv")

print(data.dtypes)
print("=== Sistem penentuan rute SPKLU ===" )

#input info kendraan
lat_mobil = float(input("masukkan latitude mobil :"))
lon_mobil = float(input("mmasukkan longitude mobil :"))
battery_percent = float(
    input("Masukkan sisa baterai saat ini (%) : ")
)
#simpan lokasi
lokasi_mobil = (lat_mobil, lon_mobil)
print("Jumlah data SPKLU :", len(data))

kapasitas_baterai = 50 #kWh
#asumsi knsmsi enrgi
efisiensi = 6 #km/kWh
energi_tersisa = (battery_percent / 100) * kapasitas_baterai
jarak_maksimum = (energi_tersisa * efisiensi)

print("\nEnergi tersisa :", round(energi_tersisa,2), "kWh")
print("Estimasi jarak tempuh :", round(jarak_maksimum,2), "km")

#list spklu
spklu = []

#ulng  iterasi
print("\n=== Proses hitung jarak ===")
for i in range(len(data)):
    #ambil koordinat/valid
    lokasi_spklu = (
        data.iloc[i]["Lat"],
        data.iloc[i]["Lon"]
    )

    #hitung jarak
    jarak  = geodesic(
        lokasi_mobil, lokasi_spklu
    ).km

    print("\nSPKLU :", data.iloc[i]["nama_spklu"])
    print("Jarak :", round(jarak, 2), "km")
    
    if jarak <= jarak_maksimum:
        spklu.append({
            "index": i,
            "jarak": jarak,
            "daya_kw": data.iloc[i]["Daya_kw"]
        })
        print("Status : Dapat dijangkau")
    else:
        print("Status : Tidak dapat dijangkau")

if len(spklu) ==0:
     print("\nTidak ada SPKLU yang dapat dijangkau.")
     exit()

#proses dp btoom up
print("\n=== Proses dynamic programming ===")
n = len(spklu)

dp = [0] * n
parent = [-1] * n
ranking = []
for i in range(n):
    jarak = spklu[i]["jarak"]
    daya = spklu[i]["daya_kw"]

    energi_charge = kapasitas_baterai - energi_tersisa
    waktu_charge = energi_charge / daya
    cost = jarak + (waktu_charge * 10)
    ranking.append({"index": i,"cost": cost})

    if i == 0:
        dp[i] = cost
        parent[i] = i
    else:
        if cost < dp[i-1]:
            dp[i] = cost
            parent[i] = i
        else:
            dp[i] = dp[i-1]
            parent[i] = parent[i-1]
      
    print(f"\nState ke-{i+1}")
    print("SPKLU :", data.iloc[
        spklu[i]["index"]
    ]["nama_spklu"])

    print("Cost  :", round(cost,2))
    print("DP    :", round(dp[i],2))
    print("Parent :", parent[i])
    print(
        f"f[{i}] = min(f[{i-1}], {round(cost,2)})"
        if i > 0
        else f"f[0] = {round(cost,2)}"
    )

#pnelusuran
print("\n=== Penelusuran Balik ===")
ranking.sort(key=lambda x: x["cost"])

for urutan, item in enumerate(ranking[:3], start=1):

    idx = item["index"]
    data_idx = spklu[idx]["index"]
    print(f"\nHasil ke-{urutan}")
    print("SPKLU :", data.iloc[data_idx]["nama_spklu"])
    print("Alamat :", data.iloc[data_idx]["alamat"])
    print("Cost :", round(item["cost"], 2))
    print("Jarak :", round(spklu[idx]["jarak"], 2), "km")
    print("Daya :", spklu[idx]["daya_kw"], "kW")

best_idx = ranking[0]["index"]
hasil = spklu[best_idx]
index_terpilih = spklu[best_idx]["index"]

ranking.sort(key=lambda x: x["cost"])
print("\n=== Ranking SPKLU Terbaik ===")

for urutan, item in enumerate(ranking,start=1):

    idx = item["index"]
    print(f"\nRanking {urutan}")
    print("SPKLU :",data.iloc[spklu[idx]["index"]]["nama_spklu"])
    print("Alamat :", data.iloc[ spklu[idx]["index"] ]["alamat"])
    print("Cost :",round(item["cost"],2))

print("\n=== HASIL OPTIMASI ===")
print("SPKLU Terpilih :", data.iloc[index_terpilih]["nama_spklu"],)
print("Alamat :", data.iloc[index_terpilih]["alamat"])
print("Jarak :", round(hasil["jarak"],2), "km")
print("Daya Charger :", hasil["daya_kw"], "kW")


#maps
map_spklu = folium.Map(
    location=lokasi_mobil,
    zoom_start=13
)

#marker lkasi mobil
folium.Marker(
    location=lokasi_mobil,
    popup='Lokasi mobil',
    icon=folium.Icon(color='red')
).add_to(map_spklu)

#smua spklu
for i in range(len(data)):

    folium.Marker(
        location=[
            data.iloc[i]["Lat"],
            data.iloc[i]["Lon"]
        ],
        #informssi
        popup=(
            f"{data.iloc[i]['nama_spklu']}<br>"
            f"Alamat : {data.iloc[i]['alamat']}"
        ),
        #mncul nma spklu
        tooltip=data.iloc[i]["nama_spklu"],
        icon=folium.Icon(color="gray", icon="info-sign")

    ).add_to(map_spklu)

#spklu hsil optimasi
ranking.sort(key=lambda x: x["cost"])

warna = ["green", "blue", "orange"]

for urutan, item in enumerate(ranking[:3]):

    idx = item["index"]
    data_idx = spklu[idx]["index"]

    lat_spklu = data.iloc[data_idx]["Lat"]
    lon_spklu = data.iloc[data_idx]["Lon"]

    folium.Marker(
        location=[lat_spklu, lon_spklu],
        popup=(
            f"Ranking {urutan+1}<br>"
            f"{data.iloc[data_idx]['nama_spklu']}<br>"
            f"Cost : {round(item['cost'],2)}"
        ),
        tooltip=f"SPKLU Ranking {urutan+1}",
        icon=folium.Icon(color=warna[urutan])
    ).add_to(map_spklu)

best_idx = ranking[0]["index"]
data_idx = spklu[best_idx]["index"]

lat_spklu = data.iloc[data_idx]["Lat"]
lon_spklu = data.iloc[data_idx]["Lon"]
    #Routing (OSRM API= Open Source Routing Machine)
    #garis jalan
url = (
    f"http://router.project-osrm.org/route/v1/driving/"
    f"{lon_mobil},{lat_mobil};"
    f"{lon_spklu},{lat_spklu}"
    f"?overview=full&geometries=geojson"
)

response = requests.get(url)
data_route = response.json()
route = data_route['routes'][0]['geometry']['coordinates']
#susundta koordnat jlan
route_coords = []

#lopp koor
for point in route:
     route_coords.append([ #dblik krna format osrm lon, lat
        point[1],
        point[0]
    ])
#gmbr 
folium.PolyLine(
    route_coords,
    color="blue",
     weight=5
).add_to(map_spklu)

#simppan maps
map_spklu.save("map_spklu1.html")
print("\nMap berhasil disimpan dengan nama 'map_spklu1.html'")