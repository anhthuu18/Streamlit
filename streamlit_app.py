import streamlit as st
import folium
import matplotlib.pyplot as plt
import requests

# Hàm để lấy tọa độ từ địa điểm
def get_coordinates(api_key, location):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()
        if results['status'] == 'OK':
            lat = results['results'][0]['geometry']['location']['lat']
            lon = results['results'][0]['geometry']['location']['lng']
            return lat, lon
    return None, None

# Hàm tạo bản đồ với Folium
def create_map(lat, lon):
    return folium.Map(location=[lat, lon], zoom_start=10)

# Hàm vẽ đường đi bằng Matplotlib
def plot_route_with_matplotlib(latitudes, longitudes):
    plt.figure(figsize=(10, 6))
    plt.plot(longitudes, latitudes, marker='o', color='blue', linestyle='-')
    plt.title("Đường đi giữa hai địa điểm")
    plt.xlabel("Kinh độ")
    plt.ylabel("Vĩ độ")
    plt.grid()
    plt.show()

st.title("Hiển Thị Bản Đồ và Đường Đi")

# Nhập địa điểm
start_location = st.text_input("Nhập địa điểm bắt đầu:")
end_location = st.text_input("Nhập địa điểm kết thúc:")
api_key = st.text_input("Nhập API Key của bạn:", type="password")

if st.button("Hiển Thị Bản Đồ"):
    if start_location and end_location and api_key:
        # Lấy tọa độ từ địa điểm
        start_lat, start_lon = get_coordinates(api_key, start_location)
        end_lat, end_lon = get_coordinates(api_key, end_location)
        
        if start_lat is not None and end_lat is not None:
            # Tạo bản đồ
            map = create_map(start_lat, start_lon)
            folium.Marker([start_lat, start_lon], popup="Điểm Bắt Đầu").add_to(map)
            folium.Marker([end_lat, end_lon], popup="Điểm Kết Thúc").add_to(map)
            folium.PolyLine([[start_lat, start_lon], [end_lat, end_lon]], color='blue', weight=5, opacity=0.7).add_to(map)

            # Hiển thị bản đồ
            st.write(map._repr_html_(), unsafe_allow_html=True)
            
            # Vẽ đường đi bằng Matplotlib
            plot_route_with_matplotlib([start_lat, end_lat], [start_lon, end_lon])
        else:
            st.error("Không tìm thấy tọa độ cho địa điểm đã nhập!")
    else:
        st.error("Vui lòng nhập đầy đủ thông tin!")