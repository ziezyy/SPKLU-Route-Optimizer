from geopy.distance import geodesic

lokasi_mobil = (-6.1804066, 106.8229008)
lokasi_spklu = (-6.179912, 106.822161)

jarak = geodesic(lokasi_mobil, lokasi_spklu).km
print("Jarak :", round(jarak, 2), "km")

#link docs: 
# https://docs.google.com/document/d/12DxXOaWuUorrHAV5yR25AHzc_ZfqQF0qLwKseSLH4b8/edit?usp=sharing