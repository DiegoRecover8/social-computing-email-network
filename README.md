# Social Computing & Personalization  
## Email Social Network Analysis

Este repositorio contiene el trabajo de la asignatura **Computación Social y Personalización** del Grado en **Ciencia de Datos e Inteligencia Artificial**.

El objetivo del proyecto es **construir y analizar un grafo social a partir de hilos de correos electrónicos**, aplicando técnicas de:

- procesamiento de datos tabulares
- normalización de entidades (entity resolution)
- construcción de grafos sociales
- análisis de redes complejas

---

# Objetivo del proyecto

A partir de un dataset de correos electrónicos:

1. Extraer remitentes y destinatarios
2. Normalizar identidades (entity resolution)
3. Construir un grafo social
4. Exportarlo a formato `.gml` / `.gexf`
5. Analizar métricas de red
6. Visualizar la red en **Gephi**

Cada nodo representa una **persona** y cada arista representa una **interacción por correo electrónico**.

---

# Dataset

El dataset contiene hilos de correos electrónicos estructurados con las siguientes columnas:

| Columna | Descripción |
|------|------|
| `thread_id` | Identificador del hilo |
| `source_file` | Archivo original |
| `subject` | Asunto del hilo |
| `messages` | Lista de mensajes del hilo |
| `message_count` | Número total de mensajes |

Cada mensaje contiene:

```python
{
 "sender": "...",
 "recipients": [...],
 "timestamp": "...",
 "subject": "...",
 "body": "..."
}

Para la construcción del grafo solo se utilizan sender y recipients.

⸻

Metodología

1. Parsing de mensajes

La columna messages se parsea desde JSON para obtener los mensajes individuales.

2. Extracción de interacciones

Se extraen pares:

(sender → recipient)

Si un mensaje tiene múltiples destinatarios se generan múltiples interacciones.

3. Normalización de nombres

Se aplican varias transformaciones:
	•	eliminación de emails <mail>
	•	eliminación de [metadata]
	•	conversión a minúsculas
	•	eliminación de puntuación
	•	normalización de espacios
	•	reordenación Apellido, Nombre → Nombre Apellido

4. Resolución de entidades

Se usa fuzzy matching con un umbral conservador (>0.92) para detectar duplicados.

Ejemplos:

jeffrey epstein
jeffrey e
jeffrey epstein [email]

→ se mapean a una identidad canónica.

5. Construcción del grafo

Se genera un grafo no dirigido donde:

Nodo = persona
Arista = interacción de email
Peso = intensidad de interacción

El peso de cada mensaje se calcula como:

message_count / número_de_mensajes_en_el_hilo


⸻

Estructura del repositorio

social-computing-email-network/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   │   └── epstein_emails.csv
│   │
│   ├── interim/
│   │
│   └── processed/
│       ├── epstein_social_graph.gml
│       ├── epstein_social_graph_cleaned.gml
│       ├── epstein_social_graph_cleaned_with_ids.gml
│       ├── epstein_social_graph_cleaned_with_ids.gexf
│       └── epstein_name_id_mapping.csv
│
├── notebooks/
│   ├── 01_graph_construction.ipynb
│   ├── 02_graph_cleaning.ipynb
│   ├── 03_network_metrics.ipynb
│   └── 04_visualization.ipynb
│
├── src/
│   ├── parsing.py
│   ├── cleaning.py
│   ├── entity_resolution.py
│   ├── graph_building.py
│   ├── graph_postprocessing.py
│   └── metrics.py
│
├── results/
│   ├── metrics/
│   │   ├── degree.csv
│   │   ├── weighted_degree.csv
│   │   ├── betweenness.csv
│   │   ├── closeness.csv
│   │   ├── pagerank.csv
│   │   └── communities.csv
│   │
│   └── summaries/
│       └── graph_summary.json
│
├── reports/
│   ├── figures/
│   │   ├── network_overview.png
│   │   ├── communities.png
│   │   └── central_nodes.png
│   │
│   └── tables/
│       ├── top_degree_nodes.csv
│       ├── top_betweenness_nodes.csv
│       └── top_pagerank_nodes.csv
│
└── docs/
    ├── workflow.md
    ├── gephi_guide.md
    └── methodological_notes.md


⸻

Visualización del grafo

El grafo se puede visualizar usando:
	•	Gephi
	•	NetworkX
	•	Cytoscape

Para Gephi:
	1.	Abrir archivo .gexf
	2.	Aplicar layout ForceAtlas2
	3.	Colorear nodos por modularity class
	4.	Escalar nodos por degree

⸻

Métricas de red analizadas

El proyecto calculará métricas clásicas de redes sociales:

Centralidad
	•	Degree
	•	Weighted Degree
	•	Betweenness
	•	Closeness
	•	Eigenvector
	•	PageRank

Estructura de red
	•	Comunidades (Louvain)
	•	Densidad de red
	•	Componentes conectados

⸻

Reproducibilidad

Instalar dependencias:

pip install -r requirements.txt

Ejecutar notebooks en orden:

01_graph_construction
02_graph_cleaning
03_network_metrics
04_visualization


⸻

Herramientas utilizadas
	•	Python
	•	Pandas
	•	NetworkX
	•	Jupyter Notebook
	•	Gephi

⸻

Estado del proyecto
	•	Construcción inicial del grafo
	•	Limpieza de nodos
	•	Resolución de duplicados
	•	Mapping id-nombre
	•	Cálculo de métricas
	•	Detección de comunidades
	•	Visualización final

⸻

Autor: Diego Recover Parra

Proyecto desarrollado para la asignatura:

Computación Social y Personalización

Grado en Ciencia de Datos e Inteligencia Artificial
