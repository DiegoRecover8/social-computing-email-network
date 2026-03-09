import networkx as nx
from pyvis.network import Network

# Cargar el grafo
G = nx.read_gml("data/processed/epstein_social_graph_cleaned.gml")

# Crear red interactiva
net = Network(
    height="750px",
    width="100%",
    bgcolor="#222222",
    font_color="white"
)

net.from_nx(G)

# Ajustar físicas para layout
net.force_atlas_2based()

# Guardar visualización
net.show("docs/network.html")