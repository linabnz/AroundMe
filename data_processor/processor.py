import pandas as pd
import sys
from difflib import get_close_matches
import codecs
from utils import get_staged_data_path, translate_text


def load_data():
    """Load all required datasets."""
    try:
        street_data = pd.read_csv(get_staged_data_path("street"))
        parking_data = pd.read_csv(get_staged_data_path("parking"), sep=",")
        museum_data = pd.read_csv(get_staged_data_path("museum"))
        toilets_data = pd.read_csv(get_staged_data_path("toilets"))
        sports_data = pd.read_csv(get_staged_data_path("sports"))
        return street_data, parking_data, museum_data, toilets_data, sports_data
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)


def get_user_input():
    """Retrieve and validate user input."""
    if len(sys.argv) < 2:
        print("Error: Please provide a search term as an argument.")
        sys.exit(1)
    return sys.argv[1].strip().upper()


def find_closest_match(research, data, column):
    """Find exact or close matches in the data."""
    if research not in data[column].values:
        print(f"No exact match found for '{research}'. Looking for close matches...")
        suggestions = get_close_matches(research, data[column].unique(), n=3, cutoff=0.6)
        if suggestions:
            print("Did you mean one of the following?")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"{i}. {suggestion}")
            return suggestions
        else:
            print("No close matches found. Exiting script.")
            sys.exit(1)
    return [research]


def select_match(suggestions):
    """Prompt the user to select a match from suggestions."""
    print("Enter the number of the correct match, or 0 to exit.")
    try:
        choice = int(input("Your choice: ").strip())
        if choice == 0:
            print("Exiting script. No match selected.")
            sys.exit(1)
        elif 1 <= choice <= len(suggestions):
            return suggestions[choice - 1]
        else:
            print("Invalid choice. Exiting script.")
            sys.exit(1)
    except ValueError:
        print("Invalid input. Please enter a number. Exiting script.")
        sys.exit(1)


def process_street_data(street_data):
    """Process street data to filter and enhance it."""
    if not street_data.empty:
        street_data["historique"] = street_data["historique"].apply(translate_text)
        street_data["orig"] = street_data["orig"].apply(translate_text)
        street_data["Description"] = (
            "Historical name: " + street_data["historique"].astype(str) + "\n" +
            "Original name: " + street_data["orig"].astype(str) + "\n" +
            "District: " + street_data["arrdt"].astype(str) + "\n" +
            "Neighborhood: " + street_data["quartier"].astype(str) + "\n"
        )
    return street_data


def process_parking_data(parking_data, typo_list):
    """Process parking data to filter and enhance it."""
    parking_data["typo_match"] = parking_data["adresse_normalized"].apply(
        lambda x: next((typo for typo in typo_list if typo in x), None)
    )
    filtered_parking_data = parking_data[parking_data["typo_match"].notna()].copy()
    if not filtered_parking_data.empty:
        filtered_parking_data["Description"] = (
            "Name: " + filtered_parking_data["nom"].astype(str) + "\n" +
            "Address: " + filtered_parking_data["adresse"].astype(str) + "\n" +
            "Number of Spaces: " + filtered_parking_data["nb_places"].astype(str) + "\n" +
            "Rate 1h: " + filtered_parking_data["tarif_1h"].map(lambda x: f"{x:.2f} €" if x != "not specified" else x) + "\n" +
            "Rate 2h: " + filtered_parking_data["tarif_2h"].map(lambda x: f"{x:.2f} €" if x != "not specified" else x) + "\n" +
            "Rate 3h: " + filtered_parking_data["tarif_3h"].map(lambda x: f"{x:.2f} €" if x != "not specified" else x) + "\n" +
            "Rate 4h: " + filtered_parking_data["tarif_4h"].map(lambda x: f"{x:.2f} €" if x != "not specified" else x) + "\n" +
            "Rate 24h: " + filtered_parking_data["tarif_24h"].map(lambda x: f"{x:.2f} €" if x != "not specified" else x) + "\n" +
            "Free: " + filtered_parking_data["gratuit"].astype(str) + "\n"
        )
    return filtered_parking_data


def process_museum_data(museum_data, typo_list):
    """Process museum data to filter and enhance it."""
    museum_data["typo_match"] = museum_data["adresse_normalized"].apply(
        lambda x: next((typo for typo in typo_list if typo in x), None)
    )
    filtered_museum_data = museum_data[museum_data["typo_match"].notna()].copy()
    if not filtered_museum_data.empty:
        filtered_museum_data["Description"] = (
            "Name: " + filtered_museum_data["name"].astype(str) + "\n" +
            "Address: " + filtered_museum_data["adresse"].astype(str) + "\n" 
        )
    return filtered_museum_data


def process_toilets_data(toilets_data, typo_list):
    """Process toilets data to filter and enhance it."""
    toilets_data["typo_match"] = toilets_data["adresse_normalized"].astype(str).apply(
        lambda x: next((typo for typo in typo_list if typo in x), None)
    )
    filtered_toilets_data = toilets_data[toilets_data["typo_match"].notna()].copy()
    if not filtered_toilets_data.empty:
        filtered_toilets_data["Description"] = (
            "Address: " + filtered_toilets_data["ADRESSE"].astype(str) + "\n" +
            "Accessible for disabled persons: " + filtered_toilets_data["ACCES_PMR"].astype(str) + "\n"
        )
    return filtered_toilets_data

def process_sports_data(sports_data, typo_list):
    """Process sports data to filter and enhance it."""
    sports_data["typo_match"] = sports_data["adresse_normalized"].astype(str).apply(
        lambda x: next((typo for typo in typo_list if typo in x), None)
    )
    filtered_sports_data = sports_data[sports_data["typo_match"].notna()].copy()
    if not filtered_sports_data.empty:
        filtered_sports_data["Description"] = (
            "Name: " + filtered_sports_data["name"].astype(str) + "\n" +
            "Address: " + filtered_sports_data["adresse"].astype(str) + "\n" 
        )
    return filtered_sports_data


def main():
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
    research = get_user_input()
    print(f"Extracting information about {research}...")

    street_data, parking_data, museum_data, toilets_data, sports_data = load_data()
    suggestions = find_closest_match(research, street_data, "typo")

    if len(suggestions) > 1:
        research = select_match(suggestions)
    else:
        research = suggestions[0]

    print(f"Exact match found for '{research}'")
    filtered_street_data = street_data[street_data["typo"] == research].copy()
    if filtered_street_data.empty:
        print(f"No data found for '{research}'. This should not happen if a suggestion was accepted.")
        sys.exit(1)

    filtered_street_data = process_street_data(filtered_street_data)
    typo_list = filtered_street_data["typo_normalized"].tolist()

    filtered_parking_data = process_parking_data(parking_data, typo_list)
    filtered_museum_data = process_museum_data(museum_data, typo_list)
    filtered_toilets_data = process_toilets_data(toilets_data, typo_list)
    filtered_sports_data = process_sports_data(sports_data, typo_list)
    
    print("\n------------------RESULTS------------------")
    print("Street Information:")
    print("\n".join(filtered_street_data["Description"]))

    if not filtered_parking_data.empty:
        print("\nParking Information:")
        print("\n".join(filtered_parking_data["Description"]))
    else:
        print("No parking data found for the given query.")

    if not filtered_museum_data.empty:
        print("\nMuseum Information:")
        print("\n".join(filtered_museum_data["Description"]))
    else:
        print("No museum data found for the given query.")

    if not filtered_toilets_data.empty:
        print("\nPublic Toilets Information:")
        print("\n".join(filtered_toilets_data["Description"]))
    else:
        print("No public toilets data found for the given query.")

    if not filtered_sports_data.empty:
        print("\nSports Facilities Information:")
        print("\n".join(filtered_sports_data["Description"]))
    else:
        print("No sports facilities data found for the given query.")

if __name__ == "__main__":
    main()
