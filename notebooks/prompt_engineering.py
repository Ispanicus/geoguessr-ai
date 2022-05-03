import json

def get_prompts():
    with open("../pickles/region_to_country.json") as file:
        region_to_country = json.load(file)

    caribbean = {country:"an island country in the caribbean" for country in region_to_country["caribbean"]}
    greenland = {'Greenland':"a country in the arctic"}
    baltic = {country: "a european country in the baltic" for country in region_to_country["baltic"]}
    balkan = {country: "a european country in the balkans" for country in region_to_country["balkan"]}
    western_europe = {country: "a western european country" for country in region_to_country["western europe"]}
    southern_europe = {country: "a southern european country" for country in region_to_country["southern europe"]}
    eastern_europe = {country: "an eastern european country" for country in region_to_country["eastern europe"]}
    northern_europe = {country: "a northern european country" for country in region_to_country['northern europe']}
    middle_east = {country: "a country in the middle east" for country in region_to_country["middle east"]}
    north_africa = {country: "a country in north africa" for country in region_to_country["north africa"]}
    west_africa = {country: "a country in west africa" for country in region_to_country["west africa"]}
    east_africa = {country: "a country in east africa" for country in region_to_country["east africa"]}
    central_africa = {country: "a country in central africa" for country in region_to_country["central africa"]}
    southern_africa = {country: "a country in southern africa" for country in region_to_country["southern africa"]}
    sub_saharan_africa = {country: "a country in sub-saharan africa" for country in region_to_country["sub-saharan africa"]}
    central_asia = {country: "a country in central asia" for country in region_to_country["central asia"]}
    east_asia = {country: "a country in east asia" for country in region_to_country["east asia"]}
    south_asia = {country: "a country in south asia" for country in region_to_country["south asia"]}
    far_east_asia = {country: "a country in far east asia" for country in region_to_country["far east asia"]}
    south_east_asia = {country: "a country in south east asia" for country in region_to_country["south east asia"]}
    western_asia = {country: "a country in western asia" for country in region_to_country["western asia"]}
    oceania = {country: "a country in oceania" for country in region_to_country["oceania"]}
    polynesia = {country: "an island country in polynesia" for country in region_to_country["polynesia"]}
    micronesia = {country: "an island country in micronesia " for country in region_to_country["micronesia"]}
    north_america = {country: "a country in north america" for country in region_to_country["north america"]}
    south_america = {country: "a country in south america" for country in region_to_country["south america"]}
    central_america = {country: "a country in central america" for country in region_to_country["central america"]}
    latin_america = {country: "a country in latin america" for country in region_to_country["latin america"]}

    prompt_list_temp= [caribbean,greenland,baltic,balkan,western_europe,southern_europe,eastern_europe,northern_europe,middle_east,north_africa,west_africa,east_africa,central_africa,southern_africa,sub_saharan_africa,central_asia,east_asia,south_asia,far_east_asia,south_east_asia,western_asia,oceania,polynesia,micronesia,north_america,south_america,central_america,latin_america]
    prompt_dict = {}
    for lst in prompt_list_temp:
        for pair in lst.items():
            prompt_dict[f"This is a photo of {pair[0]}, {pair[1]}."] = pair[0].split(',')[0]
    return prompt_dict



