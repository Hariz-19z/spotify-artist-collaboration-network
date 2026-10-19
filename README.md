# Spotify Artist Collaboration Network

An interactive **Graph Visualization (GV) project** that explores relationships between Spotify artists using network analysis, graph theory, and community detection.

The project represents artists as nodes and their collaborations as edges, helping visualize how artists are connected and how groups or communities form within a music network.

## Project Overview

Music artists often collaborate with one another, creating networks of relationships across genres and communities. This project uses graph visualization techniques to explore these relationships and understand the structure of an artist collaboration network.

## Objectives

- Represent artist collaborations as a graph.
- Analyze artist connectivity using graph theory metrics.
- Visualize degree distribution and genre-based clusters.
- Identify communities within the network.
- Provide an interactive HTML visualization for exploring the network.

## Technologies Used

- **Python** — core programming and analysis
- **NetworkX** — graph creation and network analysis
- **Matplotlib** — graph and statistical visualizations
- **Pandas** — tabular data handling
- **D3.js** — interactive browser-based graph visualization
- **HTML, CSS and JavaScript** — interactive visualization interface

## Project Features

### 1. Artist Collaboration Network
Visualizes relationships between artists through nodes and edges.

### 2. Degree Distribution
Explores how many connections artists have and how connectivity varies across the network.

### 3. Genre Clusters
Visualizes groups of artists associated with similar genres or network communities.

### 4. Network Metrics
Analyzes properties such as degree, graph density, connected components, isolated nodes and pendant nodes.

### 5. Community Detection
Uses the greedy modularity community detection algorithm to identify groups of closely connected nodes.

### 6. Interactive Visualization
Includes HTML-based visualizations for exploring the network in a web browser.

## Project Structure

```text
GV_Project/
├── network_analysis.py
├── interactive_network.html
├── Spotify_Artist_Collaboration_Network_White_Background.html
├── collaboration_network.png
├── degree_distribution.png
├── genre_clusters.png
├── degree_table.csv
├── summary_metrics.csv
├── Project_Report.md
├── Spotify_Music_Network_Presentation_Final.pptx
├── requirements.txt
└── README.md
```

## How to Run

### Prerequisites
- Python 3
- Required Python libraries
- A modern web browser

### Run the Python Analysis

Clone the repository:

```bash
git clone https://github.com/Hariz-19z/spotify-artist-collaboration-network.git
cd spotify-artist-collaboration-network
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the analysis:

```bash
python network_analysis.py
```

### Open the Interactive Visualization

Open `interactive_network.html` or `Spotify_Artist_Collaboration_Network_White_Background.html` in a modern web browser.

If the HTML uses external JavaScript libraries or data files, an internet connection or a local web server may be required.

## Project Visualizations

The repository includes:

- `collaboration_network.png` — artist collaboration graph
- `degree_distribution.png` — distribution of node degrees
- `genre_clusters.png` — genre or community cluster visualization

## Applications

- Understanding artist collaboration patterns
- Exploring music communities and genre relationships
- Applying graph theory to real-world networks
- Learning network analysis and interactive data visualization

## Future Improvements

- Add more artists and collaboration data.
- Introduce interactive genre and artist filters.
- Improve community-level analysis.
- Add more network centrality metrics.
- Deploy the interactive visualization online.

## Dataset and Credits

The project uses a Spotify artist collaboration network dataset. Please refer to the original dataset source for its provenance, licensing and attribution requirements.

## Author

**Hariz-19z**

GitHub: [@Hariz-19z](https://github.com/Hariz-19z)

---

*Developed as an academic Graph Visualization project exploring music networks and graph theory.*
