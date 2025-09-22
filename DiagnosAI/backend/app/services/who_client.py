import requests

def fetch_countries():
    url = "https://ghoapi.azureedge.net/api/DIMENSION/COUNTRY/DimensionValues"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    countries = [(item["Code"], item["Title"]) for item in data["value"]]
    return countries

def fetch_indicators_for_country(country_code):
    url = f"https://ghoapi.azureedge.net/api/GHO?filter=SpatialDim eq '{country_code}'"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data.get("value", [])

def interactive_who_explorer():
    print("Fetching countries from WHO...")
    countries = fetch_countries()

    # Display countries with index
    for idx, (code, name) in enumerate(countries, start=1):
        print(f"{idx}. {name} ({code})")
    
    while True:
        try:
            choice = int(input("\nEnter the number of the country to explore (0 to exit): "))
            if choice == 0:
                print("Exiting WHO data explorer. Goodbye!")
                break
            if choice < 1 or choice > len(countries):
                print("Invalid input. Please enter a valid number.")
                continue
            selected_code, selected_name = countries[choice-1]
            print(f"\nFetching health indicators for {selected_name} ({selected_code})...\n")
            
            indicators = fetch_indicators_for_country(selected_code)
            if not indicators:
                print("No indicators found for this country.")
            else:
                # Display indicator details
                for ind in indicators[:10]:  # show up to 10 for brevity
                    print(f"Indicator: {ind.get('IndicatorName')}")
                    print(f"   Year: {ind.get('Year')}")
                    print(f"   Data Value: {ind.get('DisplayValue')}")
                    print(f"   Source: {ind.get('Dim1')}")
                    print()
            print("-----")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    interactive_who_explorer()
