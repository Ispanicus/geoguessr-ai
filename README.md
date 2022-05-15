# geoguessr-ai

Choropleth.ipynb
    Used to create choropleth in paper

cosine_sim_correction
    Data filtering using cosine similarity script

country_to_region.ipynb
country_to_region.json
    Manually checking what the largest sub-region in a country was. Purpose was to potentially do a larger scale State-level experiment. Was not used.

Distance_correction.ipynb
distance_correction.py
    Scripts for mapillary data filtering as well as development notebook

GeoEst_Metadata.py
    Script to quickly get GeoEstimation metadata using multiprocessing. Metadata was for all prediction coordinates provided by running GeoEstimation on entire Mapillary.
    Was not used as we checked the usage guidelines of the API and the limit of 1 request per second was too limiting to run this script.

Region_to_country.ipynb
    Manual creation of which countries exist in which regions dataset.

Utils.py
    contains some utility functions that were used repeatedly across multiple notebooks

explore_15labels.ipynb
    used to create some of the confusion matrices in the paper
explorecsv_results.ipynb
    used to explore results using confusion matrices etc.
explorecsv_results_climates.ipynb
    used to explore climate results

label_counts.py
    original script to get counts of labels in LAION. Used simple string matching on prefixes. i.e "Cali" would match with "California".
label_counts_tokens.py
    multiprocessing script used to get counts of labels in LAION. Used CLIP's tokenizer to check if a label's tokens were a subset of a caption's tokens.
label_counts_tokens_climate.py
label_counts_tokens_climate_simp.py
    multiprocessing script used to get counts of label in LAION for original climate labels and manually created climate labels.



mapillary.ipynb
    used to do some initial processing of Mapillary dataset. Moved files into single folder. Visualized location of mapillary on world map. Used naive approach for guessing country which was scrapped.
overpass.ipynb
    attempt to use overpass API directly to get metadata for Mapillary. Was unsuccessful.

prompt_engineering.py
    used to create all prompts for mixedprompt experiment