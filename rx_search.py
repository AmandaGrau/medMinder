import requests

# Notes and 'To Do':
# install/import requests
# relavent data: brand_name, gerneric_name, unii code

# function that queries openfda with search term
def query_openfda(brand_name):
    # variable to store search url for making requests to Open FDA
    url = f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:\"{brand_name}\""
    # store response from the request
    response = requests.get(url)
    # check response/status code from browser - 200 is good
    if response.status_code == 200:
        # get and store the relevant information needed from the response (json)
        api_data = response.json()

        # Variable to store extracted data from the response
        results = []
        # loop over response to get brand name, generic name, and unii code, and store results
        for item in api_data.get("results", []):
            openfda = item.get("openfda", {})
            result = {
                "brand_name": openfda.get("brand_name", [""])[0],
                "generic_name": openfda.get("generic_name", [""])[0],
                "unii": openfda.get("unii", [""])[0]
            }
            # Add extracted data to med_results
            results.append(result)
        return results
    # return an empty if there is an error
    else:
        return []