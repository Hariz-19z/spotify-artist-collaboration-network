
import os
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
from itertools import combinations
from networkx.algorithms.community import greedy_modularity_communities

plt.rcParams["figure.dpi"] = 150
OUT = os.path.dirname(os.path.abspath(__file__))

# PART 2 : DATA PREPARATION  


artist_genre = {
    "Taylor Swift": "Pop", "Ed Sheeran": "Pop", "Justin Bieber": "Pop",
    "Dua Lipa": "Pop", "Selena Gomez": "Pop", "Ariana Grande": "Pop",
    "Sia": "Pop",
    "Drake": "Hip-Hop", "Kendrick Lamar": "Hip-Hop", "Travis Scott": "Hip-Hop",
    "Post Malone": "Hip-Hop", "Cardi B": "Hip-Hop", "Nicki Minaj": "Hip-Hop",
    "Eminem": "Hip-Hop", "Jay-Z": "Hip-Hop",
    "The Weeknd": "R&B", "SZA": "R&B", "Beyonce": "R&B", "Rihanna": "R&B",
    "Bruno Mars": "R&B",
    "Calvin Harris": "EDM", "David Guetta": "EDM", "Marshmello": "EDM",
    "Zedd": "EDM", "Kygo": "EDM",
    "Imagine Dragons": "Rock", "Twenty One Pilots": "Rock",
    "Bad Bunny": "Latin", "J Balvin": "Latin", "Karol G": "Latin",
}

collaborations = [
    ("Taylor Swift", "Ed Sheeran"),
    ("Ed Sheeran", "Justin Bieber"),
    ("Dua Lipa", "Calvin Harris"),
    ("Calvin Harris", "Rihanna"),
    ("Rihanna", "Drake"),
    ("Drake", "Kendrick Lamar"),
    ("Drake", "Travis Scott"),
    ("Travis Scott", "Post Malone"),
    ("Cardi B", "Nicki Minaj"),
    ("Cardi B", "Bruno Mars"),
    ("The Weeknd", "Ariana Grande"),
    ("Ariana Grande", "Nicki Minaj"),
    ("Nicki Minaj", "Eminem"),
    ("Eminem", "Rihanna"),
    ("SZA", "Kendrick Lamar"),
    ("Beyonce", "Jay-Z"),
    ("Marshmello", "Selena Gomez"),
    ("David Guetta", "Sia"),
    ("David Guetta", "Justin Bieber"),
    ("Zedd", "Selena Gomez"),
    ("Kygo", "Selena Gomez"),
    ("Imagine Dragons", "Kendrick Lamar"),
    ("Bad Bunny", "J Balvin"),
    ("J Balvin", "Karol G"),
    ("Bad Bunny", "Cardi B"),
    ("Bad Bunny", "J Balvin"),      
    ("Bad Bunny", "Drake"),
]

# Build the undirected simple graph
G = nx.Graph()
for artist, genre in artist_genre.items():
    G.add_node(artist, genre=genre)
G.add_edges_from(collaborations)          
G.add_node("Twenty One Pilots", genre="Rock")   

print(f"Graph loaded: {G.number_of_nodes()} artists (vertices), "
      f"{G.number_of_edges()} collaborations (edges)")

# PART 1 : GRAPH FUNDAMENTALS  


degree_dict = dict(G.degree())
degree_df = (pd.DataFrame(degree_dict.items(), columns=["Artist", "Degree"])
             .sort_values("Degree", ascending=False).reset_index(drop=True))

isolated_vertices = list(nx.isolates(G))
pendent_vertices = [n for n, d in degree_dict.items() if d == 1]

print("\n--- PART 1: Graph Fundamentals ---")
print(f"Is graph finite?           Yes -> |V|={G.number_of_nodes()}, |E|={G.number_of_edges()}")
print(f"Isolated vertices (deg=0): {isolated_vertices}")
print(f"Pendent vertices  (deg=1): {pendent_vertices}")
print(f"Max degree artist:         {degree_df.iloc[0]['Artist']} (deg={degree_df.iloc[0]['Degree']})")
print(f"Average degree:            {np.mean(list(degree_dict.values())):.2f}")

# Complement of the graph: two artists are connected in G_complement if they have
# NOT collaborated -- a direct application of the "Complement of a Graph" topic.
G_complement = nx.complement(G)
print(f"Complement graph:          {G_complement.number_of_nodes()} vertices, "
      f"{G_complement.number_of_edges()} edges (non-collaborating artist pairs)")

degree_df.to_csv(f"{OUT}/degree_table.csv", index=False)


# PART 3 : VISUAL MAPPING & GESTALT PRINCIPLES 

genre_palette = {
    "Pop": "#e63946", "Hip-Hop": "#457b9d", "R&B": "#f4a261",
    "EDM": "#2a9d8f", "Rock": "#6a4c93", "Latin": "#ffb703",
}
node_colors = [genre_palette[G.nodes[n]["genre"]] for n in G.nodes()]
node_sizes = [300 + degree_dict[n] * 260 for n in G.nodes()]

pos = nx.spring_layout(G, seed=42, k=0.6)  # force-directed layout -> Gestalt proximity


# PART 4 : NETWORK VISUALIZATION  


fig, ax = plt.subplots(figsize=(12, 9))
nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.35, edge_color="#999999", width=1.4)
nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=node_sizes,
                        edgecolors="white", linewidths=1.2)
nx.draw_networkx_labels(G, pos, ax=ax, font_size=8, font_weight="bold")

legend_handles = [mpatches.Patch(color=c, label=g) for g, c in genre_palette.items()]
ax.legend(handles=legend_handles, title="Genre", loc="upper left", frameon=False)
ax.set_title("Spotify Artist Collaboration Network\n"
             "(node size = number of collaborations, color = genre)", fontsize=13)
ax.axis("off")
plt.tight_layout()
plt.savefig(f"{OUT}/collaboration_network.png", bbox_inches="tight")
plt.close()
print("\nSaved: collaboration_network.png")

# Degree distribution bar chart (raw pattern that is hard to read straight from a table)
fig, ax = plt.subplots(figsize=(10, 5))
top15 = degree_df.head(15)
ax.barh(top15["Artist"][::-1], top15["Degree"][::-1], color="#457b9d")
ax.set_xlabel("Number of collaborations (degree)")
ax.set_title("Top Connected Artists by Collaboration Degree")
plt.tight_layout()
plt.savefig(f"{OUT}/degree_distribution.png", bbox_inches="tight")
plt.close()
print("Saved: degree_distribution.png")


# PART 5 : GENRE CLUSTER / COMMUNITY DETECTION 

communities = list(greedy_modularity_communities(G))
community_map = {}
for i, comm in enumerate(communities):
    for artist in comm:
        community_map[artist] = i

community_colors = plt.cm.tab10.colors
node_comm_colors = [community_colors[community_map[n] % 10] for n in G.nodes()]

fig, ax = plt.subplots(figsize=(12, 9))
nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.3, edge_color="#999999")
nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_comm_colors, node_size=node_sizes,
                        edgecolors="white", linewidths=1.2)
nx.draw_networkx_labels(G, pos, ax=ax, font_size=8, font_weight="bold")
ax.set_title(f"Detected Collaboration Communities (modularity-based, k={len(communities)})\n"
             "Color = structural cluster, NOT the stated genre label", fontsize=12)
ax.axis("off")
plt.tight_layout()
plt.savefig(f"{OUT}/genre_clusters.png", bbox_inches="tight")
plt.close()
print("Saved: genre_clusters.png")

print("\n--- PART 5: Detected communities vs stated genre ---")
for i, comm in enumerate(communities):
    genres_in_comm = sorted(set(G.nodes[a]["genre"] for a in comm))
    print(f"Community {i}: {sorted(comm)}")
    print(f"   Genres present: {genres_in_comm}")


# PART 6 : SUMMARY METRICS TABLE 


summary = {
    "Vertices (artists)": G.number_of_nodes(),
    "Edges (collaborations)": G.number_of_edges(),
    "Isolated vertices": len(isolated_vertices),
    "Pendent vertices": len(pendent_vertices),
    "Average degree": round(np.mean(list(degree_dict.values())), 2),
    "Density": round(nx.density(G), 3),
    "Connected components": nx.number_connected_components(G),
    "Detected communities": len(communities),
    "Complement graph edges": G_complement.number_of_edges(),
}
pd.DataFrame(summary.items(), columns=["Metric", "Value"]).to_csv(
    f"{OUT}/summary_metrics.csv", index=False)
print("\n--- Summary metrics ---")
for k, v in summary.items():
    print(f"{k:30s}: {v}")

print("\nAll outputs written to", OUT)


