import streamlit as st
import folium
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt

# Hàm tạo bản đồ với Folium
def create_map(lat, lon):
    return folium.Map(location=[lat, lon], zoom_start=13)

# Hàm để chuyển đổi địa chỉ thành tọa độ
def get_coordinates(address):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    return None, None

# Hàm vẽ biểu đồ với Matplotlib
def plot_coordinates(lat, lon):
    plt.figure(figsize=(8, 5))
    plt.scatter(lon, lat, color='blue')
    plt.title("Vị Trí Địa Điểm")
    plt.xlabel("Kinh Độ")
    plt.ylabel("Vĩ Độ")
    plt.grid()
    plt.xlim(lon - 0.1, lon + 0.1)
    plt.ylim(lat - 0.1, lat + 0.1)
    plt.axhline(y=lat, color='r', linestyle='--')
    plt.axvline(x=lon, color='r', linestyle='--')
    plt.show()

st.title("Hiển Thị Bản Đồ và Biểu Đồ Địa Điểm")

# Nhập địa chỉ
address = st.text_input("Nhập địa chỉ (ví dụ: 58 Phố Huế, Hà Nội):")

if st.button("Hiển Thị Bản Đồ"):
    if address:
        # Lấy tọa độ từ địa chỉ
        lat, lon = get_coordinates(address)
        
        if lat is not None and lon is not None:
            # Tạo bản đồ
            map = create_map(lat, lon)
            # Đánh dấu địa điểm trên bản đồ
            folium.Marker([lat, lon], popup=address).add_to(map)

            # Hiển thị bản đồ
            st.write(map._repr_html_(), unsafe_allow_html=True)

            # Vẽ biểu đồ
            plot_coordinates(lat, lon)
            st.pyplot()  # Hiển thị biểu đồ trong Streamlit
        else:
            st.error("Không tìm thấy địa chỉ đã nhập!")
    else:
        st.error("Vui lòng nhập địa chỉ!")