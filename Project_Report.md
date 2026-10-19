# Visualizing Music Networks: Spotify Artist Collaborations and Genre Clusters

**Course:** DSE3151 – Graph Visualization, B.Tech. CSE (DS), V Semester
**Department:** Data Science and Engineering, Manipal University Jaipur
**Student:** Faizaan

---

## 1. Objective

To apply graph-theoretic and visualization principles taught in DSE3151 to a real
domain — the Spotify artist ecosystem — by representing artists as vertices and
collaborations as edges, then using visual mapping, Gestalt-informed design, and
cluster detection to surface patterns (influential artists, genre-crossing
collaborations, isolated acts) that are not visible in a raw list of tracks.

This directly targets three Course Outcomes:

| CO | Statement | Addressed by |
|---|---|---|
| DSE3151.1 | Understand basic graph definitions, types, and visualization scope | Part 1 |
| DSE3151.2 | Design effective data visualizations to provide new insights | Parts 3–4 |
| DSE3151.3 | Apply graph visualization principles to real-world problems | Whole project |
| DSE3151.4 | Describe volumetric data / visualization of groups (clusters, networks) | Part 5 |
| DSE3151.5 | Illustrate visualization techniques and evaluate them | Part 6 |

---

## 2. Data

Spotify's own Web API does not expose a direct "who collaborated with whom" endpoint
at scale without extended access, so the network here is built from a **curated
sample of 30 well-known, publicly documented artist collaborations** (e.g. *"Everything
Has Changed"* – Taylor Swift & Ed Sheeran; *"Mia"* – Bad Bunny & Drake) spanning six
genres: Pop, Hip-Hop, R&B, EDM, Rock, and Latin. This keeps the project fully
reproducible offline while preserving realistic network structure (hub artists,
cross-genre bridges, and isolated nodes).

**To extend this with live data:** pull an artist's `top-tracks` and track credits via
the Spotify Web API (`GET /v1/artists/{id}/top-tracks`), parse featured-artist credits
from each track's artist list, and feed the resulting edge list into the same
pipeline used below — the graph-construction and visualization code does not need to
change.

---

## 3. Part 1 — Graph Fundamentals (DSE3151.1)

The collaboration network is modeled as a **simple, undirected, finite graph**
`G = (V, E)`, since a collaboration is symmetric (if A collaborated with B, B
collaborated with A) and duplicate credits on the same pair collapse to one edge.

| Concept from syllabus | Value in this graph |
|---|---|
| Finite graph | `\|V\|` = 30 artists, `\|E\|` = 26 collaborations |
| Degree of a vertex | Ranges from 0 to 4; **Drake** has the highest degree (4) |
| Isolated vertex (degree 0) | **Twenty One Pilots** — no collaboration edges |
| Pendent vertex (degree 1) | 14 artists, e.g. Taylor Swift, SZA, Beyoncé, Karol G |
| Average degree | 1.73 |
| Complement of the graph | 409 edges — i.e. 409 artist pairs that have **not** collaborated |
| Connected components | 5 — the network is not fully connected |

The complement graph is a direct application of the syllabus's "Complement of a
Graph" topic: it reframes the same 30 artists around the *absence* of a relationship,
which is a common technique for spotting unexploited pairings (e.g. potential
collaboration recommendations).

---

## 4. Part 3 — Visual Mapping & Gestalt Principles (DSE3151.2)

Each visual channel was chosen deliberately, tied to a specific Gestalt principle
from the syllabus rather than picked by default:

| Visual channel | Data mapped | Gestalt principle applied |
|---|---|---|
| Node **color** | Genre (6-category palette) | **Similarity** — same-genre artists read as one group at a glance |
| Node **size** | Degree (collaboration count) | Visual weight / emphasis — hubs are found instantly, reducing search time |
| Node **position** | Force-directed (spring) layout | **Proximity** — frequently co-collaborating artists are pulled physically closer |
| Edge **opacity** (low, grey) | — | Keeps edges as background so nodes (the primary data) remain dominant, directly countering **information overload** |
| Legend | Genre-to-color key | Removes the need to memorize the mapping, lowering cognitive load |

This mapping was validated against Munzner's *Visualization Analysis and Design*
reference model referenced in the syllabus: data (artist/genre/collaboration) →
visual encoding (color/size/position) → view (force-directed network).

---

## 5. Part 4 — Network Visualization (DSE3151.3 / DSE3151.4)

`collaboration_network.png` — static view, genre-colored, degree-sized.

`interactive_network.html` — interactive version (drag nodes, hover for detail,
click an artist to isolate their ego-network, toggle genre filters, switch between
genre-coloring and detected-cluster coloring). This satisfies the "Interaction
Techniques in Visualization" and "Visualization of Groups: Networks" sections of the
syllabus (Lectures 14 and 23).

Reading the static network: Drake (Hip-Hop) and Cardi B (Hip-Hop) act as **bridge
nodes** connecting otherwise separate genre neighborhoods (e.g. Drake links to
Bad Bunny/Latin and Kendrick Lamar/Hip-Hop; Cardi B links to Bruno Mars/R&B and
Nicki Minaj/Hip-Hop). Twenty One Pilots sits fully disconnected — a pattern invisible
in a flat spreadsheet of tracks but obvious the moment it's drawn as a graph.

---

## 6. Part 5 — Genre Cluster Detection (DSE3151.4)

Beyond the *stated* genre labels, a **modularity-based community detection**
algorithm (`greedy_modularity_communities`, NetworkX) was run purely on graph
structure — it has no knowledge of genre — to see whether collaboration patterns
naturally reproduce genre boundaries.

`genre_clusters.png` shows the result: **7 structural communities**, several of which
mix genres:

- Community 0 mixes **Pop, R&B, Hip-Hop, and EDM** (Ariana Grande, The Weeknd, Nicki
  Minaj, Rihanna, Calvin Harris) — reflecting how mainstream pop/R&B/hip-hop
  regularly cross over.
- Community 3 mixes **Hip-Hop, Latin, and R&B** (Bad Bunny, Cardi B, Bruno Mars,
  J Balvin, Karol G).
- Community 6 is a singleton — Twenty One Pilots, matching its isolated-vertex status
  from Part 1.

**Key insight:** structural clusters (who actually works together) do not line up
cleanly with marketing genre labels — collaboration is a better predictor of "who's
in the same creative circle" than genre metadata alone. This is exactly the kind of
pattern the brief asked for: "visual patterns that are difficult to see in raw data."

---

## 7. Part 6 — Evaluating the Visualization (DSE3151.5)

Following the syllabus's "Evaluating Visualizations" topic (Lecture 31), the design
is assessed against standard criteria:

| Criterion | Assessment |
|---|---|
| **Expressiveness** | Encodings match data type — categorical genre → categorical color; quantitative degree → quantitative size. No channel is misused. |
| **Effectiveness** | Color and size are high-precision pre-attentive channels, appropriate given only 30 nodes; would need to switch to a matrix view or aggregation for hundreds of nodes (avoids "hairball" overload at scale). |
| **Clutter / overload** | Addressed via muted edge styling, genre-filter toggle in the interactive version, and click-to-isolate ego-network interaction. |
| **Discoverability of insight** | Bridge artists and isolated vertices are identifiable within seconds — a clear improvement over scanning a 26-row edge list. |
| **Limitation** | Sample size (30 artists) is small by design for course-project clarity; a production version should pull the full Spotify collaboration graph. |

---

## 8. Files in this Project

| File | Purpose |
|---|---|
| `network_analysis.py` | Full pipeline: graph construction, Part 1–6 metrics, static visualizations |
| `interactive_network.html` | Interactive D3.js force-directed network (open in any browser) |
| `collaboration_network.png` | Static genre-colored network (Part 4) |
| `degree_distribution.png` | Top artists by collaboration degree |
| `genre_clusters.png` | Detected communities vs. stated genre (Part 5) |
| `degree_table.csv` | Full degree table for every artist |
| `summary_metrics.csv` | All graph-theoretic summary statistics (Part 1 & 6) |

---

## 9. Conclusion

This project demonstrates the full DSE3151 pipeline end to end: starting from
fundamental graph definitions (finite graphs, degree, isolated/pendent vertices,
complement), through Gestalt-informed visual mapping and visual analytics, to
network/cluster visualization of groups, and finally a structured evaluation of the
resulting design. The Spotify artist-collaboration domain proved well suited to this
pipeline because it naturally produces the hub, bridge, and isolated-vertex patterns
that graph visualization is designed to reveal.
