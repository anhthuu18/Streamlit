import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(G, path=None):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10)
    if path:
        nx.draw_networkx_edges(G, pos, edgelist=path, edge_color='red', width=2)
    plt.axis('off')
    plt.show()

st.title("Giải bài toán tìm đường đi")

# Tạo đồ thị
G = nx.Graph()
G.add_edge('A', 'B', weight=1)
G.add_edge('A', 'C', weight=4)
G.add_edge('B', 'C', weight=2)
G.add_edge('B', 'D', weight=5)
G.add_edge('C', 'D', weight=1)

start = st.selectbox("Chọn đỉnh bắt đầu:", G.nodes())
end = st.selectbox("Chọn đỉnh kết thúc:", G.nodes())

if st.button("Tìm đường đi"):
    path = nx.dijkstra_path(G, start, end)
    st.write("Đường đi ngắn nhất từ {} đến {}: {}".format(start, end, path))
    
    draw_graph(G, path)

    # Vẽ đồ thị
    fig, ax = plt.subplots()
    draw_graph(G, path)
    st.pyplot(fig)