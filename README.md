# Social Computing & Personalization / Computación Social y Personalización

[![Interactive Graph](https://img.shields.io/badge/Interactive%20Graph-Web%20Viewer-blue?style=for-the-badge)](https://email-web-graph.vercel.app/)

## Email Social Network Analysis from the Epstein Email Corpus
## Análisis de red social a partir del corpus de correos de Epstein

This repository contains the practical work developed for the course **Computación Social y Personalización** in the Degree in **Ciencia de Datos e Inteligencia Artificial**.  
Este repositorio contiene el trabajo práctico desarrollado para la asignatura **Computación Social y Personalización** del Grado en **Ciencia de Datos e Inteligencia Artificial**.

The project studies an email corpus as a **social network**, transforming raw email threads into a graph representation and analyzing its structural properties through network science techniques.  
El proyecto estudia un corpus de correos electrónicos como una **red social**, transformando hilos de correo en una representación en forma de grafo y analizando sus propiedades estructurales mediante técnicas de análisis de redes.

---

## 1. Project Overview / Descripción general del proyecto

The main goal of this project is to build and analyze a social graph from a collection of email threads.  
El objetivo principal de este proyecto es construir y analizar un grafo social a partir de una colección de hilos de correos electrónicos.

Each node represents an individual, and each edge represents an email interaction between two individuals.  
Cada nodo representa a una persona y cada arista representa una interacción por correo electrónico entre dos personas.

The workflow includes:  
El flujo de trabajo incluye:

1. parsing the raw email-thread dataset / parseo del dataset original;
2. extracting senders and recipients / extracción de remitentes y destinatarios;
3. cleaning and normalizing person entities / limpieza y normalización de identidades;
4. building a weighted social graph / construcción de un grafo social ponderado;
5. exporting the network into graph formats (`.gml`, `.gexf`) / exportación a formatos de grafo;
6. computing network metrics and exploring community structure / cálculo de métricas y detección de comunidades;
7. visualizing the network in Gephi and Python / visualización en Gephi y Python.

---

## 2. Research Motivation / Motivación del análisis

Email archives are useful for studying relational structure because they preserve direct interactions between actors.  
Los archivos de correo son útiles para estudiar estructura relacional porque preservan interacciones directas entre actores.

In this project, the dataset is treated mainly as a source of **observable communication links**, rather than as a corpus for semantic text analysis.  
En este proyecto, el dataset se trata principalmente como una fuente de **enlaces de comunicación observables**, más que como un corpus para análisis semántico del texto.

From a social computing perspective, this makes it possible to ask questions such as:  
Desde la perspectiva de la computación social, esto permite plantear preguntas como:

- Which actors are structurally central in the network?  
  Qué actores son estructuralmente centrales en la red.
- Is the graph sparse or highly connected?  
  El grafo es disperso o está muy conectado.
- Are there bridge nodes connecting separate parts of the network?  
  Existen nodos puente que conectan partes separadas de la red.
- Can meaningful communities be detected?  
  Se pueden detectar comunidades significativas.

---

## 3. Dataset / Conjunto de datos

The raw dataset is a CSV file containing email threads.  
El dataset original es un archivo CSV que contiene hilos de correo electrónico.

Main columns:  
Columnas principales:

| Column | Description (EN) | Descripción (ES) |
|---|---|---|
| `thread_id` | Thread identifier | Identificador del hilo |
| `source_file` | Original file name | Archivo fuente original |
| `subject` | Thread subject | Asunto del hilo |
| `messages` | JSON-like list of messages | Lista tipo JSON de mensajes |
| `message_count` | Number of messages in the thread | Número de mensajes del hilo |

Each message usually contains:  
Cada mensaje suele contener:

```python
{
    "sender": "...",
    "recipients": [...],
    "timestamp": "...",
    "subject": "...",
    "body": "..."
}
```

For graph construction, the most relevant fields are:  
Para la construcción del grafo, los campos más relevantes son:

- `sender`
- `recipients`

The project intentionally prioritizes relational structure over semantic content.  
El proyecto prioriza intencionadamente la estructura relacional frente al contenido semántico.

---

## 4. Methodology / Metodología

### 4.1 Parsing and extraction / Parseo y extracción

The messages column is parsed to recover the individual messages contained in each thread.  
La columna `messages` se parsea para recuperar los mensajes individuales contenidos en cada hilo.

From each message, sender–recipient interactions are extracted.  
De cada mensaje se extraen interacciones remitente–destinatario.

If one message contains multiple recipients, multiple interactions are generated.  
Si un mensaje contiene varios destinatarios, se generan múltiples interacciones.

---

### 4.2 Entity cleaning and normalization / Limpieza y normalización de identidades

Since the same person may appear under slightly different names, a conservative entity-resolution strategy is applied.  
Dado que una misma persona puede aparecer bajo variantes ligeramente distintas de nombre, se aplica una estrategia conservadora de resolución de entidades.

The normalization process includes:  
El proceso de normalización incluye:

- lowercasing / conversión a minúsculas;
- removing punctuation / eliminación de puntuación;
- trimming whitespace / normalización de espacios;
- removing embedded emails and metadata / eliminación de correos incrustados y metadatos;
- standardizing formats such as *Surname, Name* / estandarización de formatos tipo *Apellido, Nombre*;
- conservative fuzzy matching / fuzzy matching conservador.

This step reduces false duplicates while avoiding overly aggressive merges.  
Este paso reduce duplicados falsos evitando fusiones excesivamente agresivas.

---

### 4.3 Graph construction / Construcción del grafo

A social graph is built where:  
Se construye un grafo social donde:

- node = person / nodo = persona
- edge = email interaction / arista = interacción por correo
- weight = interaction intensity / peso = intensidad de interacción

The graph is treated as undirected for the main analysis.  
El grafo se trata como no dirigido para el análisis principal.

---

### 4.4 Edge weighting / Ponderación de aristas

The weight assigned to a message-level interaction is derived from thread information using:
El peso asignado a una interacción a nivel de mensaje se deriva de la información del hilo usando:

`message_count / number_of_messages_in_thread`

This allows interaction strength to reflect communication intensity within each thread.  
Esto permite que la intensidad de la relación refleje la intensidad comunicativa dentro de cada hilo.

---

### 4.5 Graph cleaning and post-processing / Limpieza y postprocesado del grafo

After the initial graph is built, additional cleaning is performed to:
Tras construir el grafo inicial, se realiza una limpieza adicional para:

- remove malformed or meaningless labels / eliminar etiquetas malformadas o irrelevantes;
- merge obvious remaining duplicates / fusionar duplicados evidentes;
- create a stable mapping between node IDs and labels / crear un mapping estable entre IDs y nombres.

---

## 5. Repository Structure / Estructura del repositorio

```text
social-computing-email-network/
│
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
│
├── data/
│   ├── raw/
│   │   └── epstein_emails.csv
│   │
│   └── processed/
│       ├── epstein_name_id_mapping.csv
│       ├── epstein_social_graph_cleaned.gexf
│       ├── epstein_social_graph_cleaned.gml
│       └── epstein_social_graph.gml
│
└── notebooks/
    ├── 01_graph_construction.ipynb
    ├── 02_graph_cleaning.ipynb
    ├── 03_network_metrics.ipynb
    └── 04_visualization.ipynb
```

---

## 6. Main Outputs / Resultados principales

The project currently includes the following outputs:  
El proyecto incluye actualmente los siguientes resultados:

- an initial graph in `.gml` format / un grafo inicial en formato `.gml`;
- a cleaned graph / un grafo limpio;
- a cleaned graph with consistent node IDs / un grafo limpio con IDs consistentes;
- a `.gexf` version for Gephi / una versión `.gexf` para Gephi;
- a node ID/name mapping file / un archivo de mapping entre IDs y nombres;
- notebooks documenting graph construction, cleaning and metrics / notebooks que documentan construcción, limpieza y métricas.

These outputs support both reproducibility and subsequent analysis.  
Estos resultados facilitan tanto la reproducibilidad como el análisis posterior.

---

## 7. Network Analysis / Análisis de red

The analytical stage focuses on basic and intermediate network measures.  
La fase analítica se centra en medidas básicas e intermedias de análisis de redes.

### Node-level metrics / Métricas a nivel de nodo

- Degree / Grado
- Weighted degree / Grado ponderado
- Betweenness centrality / Centralidad de intermediación
- Closeness centrality / Centralidad de cercanía
- PageRank

### Global and meso-scale properties / Propiedades globales y meso-estructurales

- Density / Densidad
- Connected components / Componentes conexas
- Clustering
- Community detection / Detección de comunidades:
  - Louvain
  - Girvan–Newman
  - InfoMap

These metrics are intended to support a structural interpretation of the graph.  
Estas métricas están orientadas a apoyar una interpretación estructural del grafo.

---

## 8. Visualization / Visualización

The graph can be explored in:  
El grafo puede explorarse en:

- **Gephi**
- **NetworkX**
- **Cytoscape**
- **Interactive web viewer / Visor web interactivo**: https://email-web-graph.vercel.app/

### Interactive web visualization / Visualización web interactiva

An interactive browser-based version of the graph is available at:  
Existe una versión interactiva del grafo accesible desde navegador en:

- https://email-web-graph.vercel.app/

This web application complements the static visualizations and allows dynamic exploration of nodes, edges and graph structure.  
Esta aplicación web complementa las visualizaciones estáticas y permite explorar dinámicamente nodos, aristas y la estructura general del grafo.

---

## 9. Reproducibility / Reproducibilidad

Install dependencies / Instalar dependencias:

```bash
pip install -r requirements.txt
```

Suggested execution order / Orden de ejecución recomendado:

1. `01_graph_construction.ipynb`
2. `02_graph_cleaning.ipynb`
3. `03_network_metrics.ipynb`
4. `04_visualization.ipynb`

This order reproduces the pipeline from raw data to network analysis.  
Este orden reproduce el flujo desde los datos originales hasta el análisis de red.

---

## 10. Limitations / Limitaciones

This project has several important limitations:  
Este proyecto presenta varias limitaciones importantes:

- the graph depends on entity-normalization choices; / el grafo depende de las decisiones de normalización de entidades;
- some merges require conservative manual judgment; / algunas fusiones requieren juicio manual conservador;
- the network reflects available communications, not all real-world ties; / la red refleja comunicaciones disponibles, no todos los lazos reales;
- community detection may vary depending on algorithm and parameters; / la detección de comunidades puede variar según el algoritmo y sus parámetros;
- visual interpretation depends on layout and filtering choices. / la interpretación visual depende del layout y de los filtros aplicados.

These limitations must be considered when interpreting the results.  
Estas limitaciones deben tenerse en cuenta al interpretar los resultados.

---