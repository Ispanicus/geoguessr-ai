# geoguessr-ai

A repository supporting the paper [Exploring CLIP’s Geo-location capabilities](CLIP_Geolocation.pdf), which examines the potential of the CLIP model to infer geographic context from images.

## Table of Contents

- [Project Overview](#project-overview)
- [Paper](#paper)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Data](#data)
- [Directory Structure](#directory-structure)
- [Usage](#usage)
  - [CLI Scripts](#cli-scripts)
  - [Jupyter Notebooks](#jupyter-notebooks)
  - [HPC Jobs](#hpc-jobs)
- [Results and Figures](#results-and-figures)
- [Acknowledgements](#acknowledgements)

## Project Overview

This project explores the geo-location capabilities of OpenAI’s CLIP model through a series of experiments predicting geographic metadata such as country, region, and climate labels from images. Inspired by the GeoGuessr game, we evaluate CLIP on Mapillary and climate datasets to understand its ability to encode spatial information.

## Paper

Please refer to the full details in the paper:

- **PDF**: [Exploring CLIP’s Geo-location capabilities](CLIP_Geolocation.pdf)

## Prerequisites

- Python 3.8 or higher
- pip
- (Optional) NVIDIA GPU with CUDA support for accelerated CLIP inference

## Installation

1. Clone the repository and enter the folder:

    ```bash
    git clone https://github.com/<your_org>/geoguessr-ai.git
    cd geoguessr-ai
    ```

2. (Optional but recommended) Create a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required Python packages:

    ```bash
    pip install torch torchvision
    pip install git+https://github.com/openai/CLIP.git
    pip install pandas geopandas shapely tqdm pillow geopy
    ```

## Data

Several data sources are used in this project:

| Directory       | Description                                                  |
|-----------------|--------------------------------------------------------------|
| `inputdata/`    | Raw CSV files with image IDs and labels (country, city, etc.)|
| `geoinputdata/` | Input CSVs for CLIP geo-estimation experiments               |
| `georesultcsv/` | Output from external geo-estimation models                   |
| `SHP/`          | Shapefiles for world administrative boundaries               |
| `pickles/`      | Serialized intermediate data                                 |
| `label_counts/` | Label frequency counts on LAION captions                     |

## Directory Structure

```
.
├── CLIP_Geolocation.pdf           # Paper PDF
├── CountryData.py                 # Reverse geocoding with geopy
├── ModelRun3all.py                # Standard CLIP experiments
├── ModelRun4Region.py             # Region-level CLIP experiments
├── ModelRun4Country.py            # Two-stage region→country experiments
├── ModelRunMixedPrompt.py         # Mixed prompt design experiments
├── inputdata/                     # Raw CSV datasets
├── geoinputdata/                  # Geo-estimation model inputs
├── georesultcsv/                  # Geo-estimation model outputs
├── SHP/                           # Shapefile data (world boundaries)
├── pickles/                       # Intermediate data (pickle/json)
├── label_counts/                  # LAION label frequency outputs
├── resultcsv/                     # Final experiment results CSVs
├── figures/                       # Figures for the paper
├── notebooks/                     # Jupyter notebooks for EDA & plotting
├── jobs/                          # HPC job submission scripts
├── outfiles/                      # HPC job logs
└── README.md                      # Project overview (this file)
```

## Usage

### CLI Scripts

- **CountryData.py**: Reverse geocode Mapillary metadata.
    ```bash
    python CountryData.py path/to/train.json
    ```
- **ModelRun3all.py**: Run baseline experiments (all tasks).
    ```bash
    python ModelRun3all.py
    ```
- **ModelRun4Region.py**: Region-level classification.
    ```bash
    python ModelRun4Region.py
    ```
- **ModelRun4Country.py**: Two-stage region→country classification.
    ```bash
    python ModelRun4Country.py
    ```
- **ModelRunMixedPrompt.py**: Mixed-prompt engineering experiments.
    ```bash
    python ModelRunMixedPrompt.py
    ```

_Read the docstrings at the top of each script for additional arguments._

### Jupyter Notebooks

Key notebooks for data exploration and visualization:

- `notebooks/mapillary.ipynb`: Processing Mapillary dataset and basic visualizations.
- `notebooks/GeoEst_Metadata.py`: Multiprocessing reverse geocoding pipeline.
- `notebooks/prompt_engineering.py`: Building mixed prompts for CLIP.
- `notebooks/explorecsv_results.ipynb`: Confusion matrix and result analysis.
- `notebooks/choropleth.ipynb`: Generating choropleth maps.
- `notebooks/Climate.ipynb`: Climate label assignment and plotting.

### HPC Jobs

Use the scripts in `jobs/` to submit batch jobs on an HPC cluster. A helper script `jobs/runall` is provided to launch standard experiments.

## Results and Figures

- **Results CSVs**: Output tables are found in `resultcsv/` and `georesultcsv/`.
- **Paper Figures**: Pre-generated figures are stored in `figures/`.

## Acknowledgements

- This work is built on OpenAI’s CLIP model.
- Mapillary dataset for images.
- LAION dataset as a proxy for CLIP's training data.
- Geopandas and geopy for geospatial processing.