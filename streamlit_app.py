import streamlit as st
import folium
import time
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import requests
import polyline
from streamlit_folium import folium_static

# Đồ thị mẫu (có thể thay đổi theo yêu cầu thực tế)
graph = {
    "A": {"B": 1, "C": 4},
    "B": {"A": 1, "C": 2, "D": 5},
    "C": {"A": 4, "B": 2, "D": 1},
    "D": {"B": 5, "C": 1}
}

# Hàm để lấy tọa độ từ địa chỉ
def get_coordinates(address):
    geolocator = Nominatim(user_agent="your_unique_user_agent")
    time.sleep(1)
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    return None, None

# Hàm Dijkstra để tìm đường đi ngắn nhất
def dijkstra(graph, start):
    shortest_paths = {vertex: float('infinity') for vertex in graph}
    shortest_paths[start] = 0
    unvisited_vertices = list(graph.keys())
    previous_vertices = {vertex: None for vertex in graph}

    while unvisited_vertices:
        current_vertex = min(
            unvisited_vertices, key=lambda vertex: shortest_paths[vertex]
        )

        if shortest_paths[current_vertex] == float('infinity'):
            break

        for neighbor, weight in graph[current_vertex].items():
            alternative_route = shortest_paths[current_vertex] + weight
            if alternative_route < shortest_paths[neighbor]:
                shortest_paths[neighbor] = alternative_route
                previous_vertices[neighbor] = current_vertex

        unvisited_vertices.remove(current_vertex)

    return previous_vertices, shortest_paths

# Hàm để lấy đường đi giữa hai địa điểm
def get_route(start, end):
    previous_vertices, shortest_paths = dijkstra(graph, start)
    path = []
    current_vertex = end

    while current_vertex is not None:
        path.append(current_vertex)
        current_vertex = previous_vertices[current_vertex]

    path.reverse()
    return path if shortest_paths[end] < float('infinity') else None

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
            route = get_route("A", "D")  # Giả định sử dụng đỉnh A và D

            map = folium.Map(location=start_coords, zoom_start=14)
            folium.Marker(start_coords, popup=f"Xuất phát: {start_address}").add_to(map)
            folium.Marker(end_coords, popup=f"Đích: {end_address}").add_to(map)

            if route:
                # Giả sử bạn có thể chuyển đổi path thành tọa độ
                # Chưa có phần mã chuyển đổi từ đỉnh thành tọa độ
                # points = polyline.decode(route)
                # folium.PolyLine(locations=points, color='blue').add_to(map)

                st.write(f"Đường đi: {route}")
            
            folium_static(map) 
        else:
            st.error("Không tìm thấy tọa độ cho địa chỉ đã nhập!")
    else:
        st.error("Vui lòng nhập cả hai địa chỉ!")
