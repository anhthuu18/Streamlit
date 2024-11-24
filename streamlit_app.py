import streamlit as st
import folium
import time
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import requests
import polyline
from streamlit_folium import folium_static

# Hàm để lấy tọa độ từ địa chỉ
def get_coordinates(address):
    geolocator = Nominatim(user_agent="your_unique_user_agent")
    time.sleep(1)  # Thêm thời gian chờ giữa các yêu cầu
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    return None, None

# Hàm để lấy đường đi giữa hai địa điểm
def get_route(start_coords, end_coords):
    url = f"https://router.project-osrm.org/route/v1/driving/{start_coords[1]},{start_coords[0]};{end_coords[1]},{end_coords[0]}?overview=full"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and data['routes']:
        return data['routes'][0]['geometry']
    return None

# Thuật toán Dijkstra
def dijkstra(graph, start):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_vertex]:
            continue
        
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances

# Đồ thị mẫu - bạn cần cập nhật nó với dữ liệu thực tế
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

st.title("Tìm Khoảng Cách và Đường Đi")

# Nhập địa chỉ
start_address = st.text_input("Nhập địa chỉ xuất phát:")
end_address = st.text_input("Nhập địa chỉ đích:")

if st.button("Tìm Đường"):
    if start_address and end_address:
        start_coords = get_coordinates(start_address)
        end_coords = get_coordinates(end_address)

        if start_coords and end_coords:
            distance = geodesic(start_coords, end_coords).kilometers
            route = get_route(start_coords, end_coords)

            # Sử dụng thuật toán Dijkstra
            start_vertex = 'A'  # Thay thế bằng địa chỉ xuất phát đã được mã hóa
            end_vertex = 'D'    # Thay thế bằng địa chỉ đích đã được mã hóa
            shortest_paths = dijkstra(graph, start_vertex)
            shortest_distance = shortest_paths[end_vertex]

            map = folium.Map(location=start_coords, zoom_start=14)
            folium.Marker(start_coords, popup=f"Xuất phát: {start_address}").add_to(map)
            folium.Marker(end_coords, popup=f"Đích: {end_address}").add_to(map)

            if route:
                points = polyline.decode(route)
                folium.PolyLine(locations=points, color='blue').add_to(map)
            
            folium_static(map)
            st.write(f"Khoảng cách: {distance:.2f} km")
            st.write(f"Khoảng cách ngắn nhất (Dijkstra): {shortest_distance}")

        else:
            st.error("Không tìm thấy tọa độ cho địa chỉ đã nhập!")
    else:
        st.error("Vui lòng nhập cả hai địa chỉ!")