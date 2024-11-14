import streamlit as st
import folium
import requests

# Hàm để lấy đường đi từ Google Maps API
def get_directions(api_key, origin, destination):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        directions = response.json()
        if directions['status'] == 'OK':
            return directions['routes'][0]['legs'][0]['steps']
        else:
            return None
    return None

# Hàm để vẽ đường đi lên bản đồ
def plot_route(steps):
    route_map = folium.Map(location=[0, 0], zoom_start=2)
    points = []

    for step in steps:
        lat = step['end_location']['lat']
        lng = step['end_location']['lng']
        points.append((lat, lng))
        folium.Marker([lat, lng], popup=step['html_instructions']).add_to(route_map)

    # Vẽ đường đi
    folium.PolyLine(points, color='blue', weight=5, opacity=0.7).add_to(route_map)

    return route_map

st.title("Tìm Đường Đi Trên Google Maps")

# Nhập thông tin từ người dùng
origin = st.text_input("Nhập địa điểm bắt đầu:")
destination = st.text_input("Nhập địa điểm kết thúc:")
api_key = st.text_input("Nhập API Key của bạn:", type="password")

if st.button("Tìm đường đi"):
    if origin and destination and api_key:
        steps = get_directions(api_key, origin, destination)
        if steps:
            st.write("Đường đi từ {} đến {}:".format(origin, destination))
            route_map = plot_route(steps)
            st.write(route_map._repr_html_(), unsafe_allow_html=True)
        else:
            st.error("Không tìm thấy đường đi!")
    else:
        st.error("Vui lòng nhập đầy đủ thông tin!")