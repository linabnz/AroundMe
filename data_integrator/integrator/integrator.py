from utils import get_data_path, load_json_data, normalize_adress, fill_string_not_specified
import pandas as pd

# Traitement des données de rue
def process_street_data():
    street_data = pd.read_csv(get_data_path("street"))
    columns_to_keep = ["typo", "orig", "historique", "typvoie", "arrdt", "quartier", "longueur", "largeur", "geo_point_2d"]
    street_data = street_data[columns_to_keep]
    street_data["Ylat"] = street_data["geo_point_2d"].str.split(', ', expand=True)[0].astype(float)
    street_data["Xlong"] = street_data["geo_point_2d"].str.split(', ', expand=True)[1].astype(float)
    street_data["typo_normalized"] = street_data["typo"].apply(normalize_adress)
    street_data = fill_string_not_specified(street_data)
    street_data.to_csv(get_data_path("street", "staged"), index=False)

# Traitement des données de parking
def process_parking_data():
    parking_data = pd.read_csv(get_data_path("parking"), sep=";")
    parking_data = parking_data[parking_data["insee"].astype(str).str.startswith("75")].copy()
    parking_data["gratuit"] = parking_data["gratuit"].map({1: "yes", 0: "no"})
    parking_data["Arrondissement"] = parking_data["insee"].astype(str).str[-2:] + "e"
    parking_data["adresse_normalized"] = parking_data["adresse"].apply(normalize_adress)
    parking_data = fill_string_not_specified(parking_data)
    parking_data.to_csv(get_data_path("parking", "staged"), index=False)

# Traitement des données de toilettes publiques
def process_toilets_data():
    toilets_data = pd.read_csv(get_data_path("toilets"), sep=";")
    toilets_data["adresse_normalized"] = toilets_data["ADRESSE"].apply(normalize_adress)
    toilets_data["ACCES_PMR"] = toilets_data["ACCES_PMR"].map({"Oui": "yes", "Non": "no"})
    toilets_data[["Ylat", "Xlong"]] = toilets_data["geo_point_2d"].str.split(', ', expand=True).astype(float)
    toilets_data["adresse"] = toilets_data["ADRESSE"]
    toilets_data = fill_string_not_specified(toilets_data)
    toilets_data.to_csv(get_data_path("toilets", "staged"), index=False)

# Traitement des données de musées
def process_museum_data():
    museum_data_raw_path = get_data_path("museum")
    museum_data = load_json_data(museum_data_raw_path)
    museum_data = pd.DataFrame({
        "Xlong": [feature["geometry"]["coordinates"][0] for feature in museum_data["features"]],
        "Ylat": [feature["geometry"]["coordinates"][1] for feature in museum_data["features"]],
        "name": [feature["properties"].get("l_ep_min", "not specified") for feature in museum_data["features"]],
        "adresse": [feature["properties"].get("adresse", "not specified") for feature in museum_data["features"]],
        "c_postal": [feature["properties"].get("c_postal", "not specified") for feature in museum_data["features"]],
    })
    museum_data["adresse_normalized"] = museum_data["adresse"].apply(normalize_adress)
    museum_data_filtered = museum_data[museum_data["c_postal"].astype(str).str.startswith("75")].copy()
    museum_data_filtered = fill_string_not_specified(museum_data_filtered)
    museum_data_filtered.to_csv(get_data_path("museum", "staged"), index=False)

# Traitement des données de sport
def process_sports_data():
    sports_data_raw_path = get_data_path("sports")
    sports_data = load_json_data(sports_data_raw_path)
    sports_data_df = pd.DataFrame({
    "Xlong": [feature["geometry"]["coordinates"][0] for feature in sports_data["features"]],
    "Ylat": [feature["geometry"]["coordinates"][1] for feature in sports_data["features"]],
    "name": [feature["properties"]["l_ep_maj"] for feature in sports_data["features"]],
    "adresse": [f"{feature['properties'].get('n_voie', '')} {feature['properties'].get('c_suf1', '')} {feature['properties'].get('c_suf2', '')} {feature['properties'].get('c_suf3', '')} {feature['properties'].get('c_desi', '')} {feature['properties'].get('c_liaison', '')} {feature['properties'].get('l_voie', '')}" for feature in sports_data["features"]],
    "annee_creation": [feature["properties"]["d_annee_cr"] for feature in sports_data["features"]],
    "public": [feature["properties"]["b_public"] for feature in sports_data["features"]],
    "c_postal": [feature["properties"]["c_postal"] for feature in sports_data["features"]],
})
    sports_data_df["adresse_normalized"] = sports_data_df["adresse"].apply(normalize_adress) # vérifier
    sports_data_df = fill_string_not_specified(sports_data_df)
    sports_data_df.to_csv(get_data_path("sports", "staged"), index=False)

# Exécution des processus
if __name__ == "__main__":
    process_street_data()
    process_parking_data()
    process_toilets_data()
    process_museum_data()
    process_sports_data()
    print("Integration done!")
