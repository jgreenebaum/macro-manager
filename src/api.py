import requests
import os
from collections import defaultdict

class FoodDataCentralAPI:
    def __init__(self):
        self.key = None
        self.baseUrl = "https://api.nal.usda.gov/fdc/v1"


    def setAPIKey(self, key: str):
        self.key = key


    def getfdcIdOptions(self, food: str):
        if not self.key:
            raise ValueError("API key is not set. Please set the API key first.")
        
        url = f"{self.baseUrl}/foods/search?query={food}&dataType=Survey%20(FNDDS)&api_key={self.key}"
        response = requests.get(url)

        # Handle errors if request fails
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            return None
        
        foods = response.json().get('foods', [])

        # No results
        if not foods:
            print(f"No results found for '{food}'.")
            return []

        # Collect name/id pairs
        nameAndIdPairList = [(foodItem['description'], foodItem['fdcId']) for foodItem in foods]
        return nameAndIdPairList
    

    def getFoodData(self, foods: list):
        if not self.key:
            raise ValueError("API key is not set. Please set the API key first.")
        
        fdcIds = "/foods?"
        for food in foods:
            fdcIds += f"fdcIds={food}&"
        url = f"{self.baseUrl}{fdcIds}api_key={self.key}"
        response = requests.get(url)
        
        # Handle errors if request fails
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            return None
        
        # Save all food nutrient data to a list
        foodNutrientsList = [food["foodNutrients"] for food in response.json()]
        return foodNutrientsList


    def getMacros(self, foods: list):
        responseList = self.getFoodData(foods)

        totalNutrients = defaultdict(lambda: {"amount": 0.0, "unit": ""})

        # Iterate over each food's nutrient data
        for foodNutrients in responseList:
            for nutrient in foodNutrients:
                nutrient_name = nutrient['nutrient']['name']
                amount = nutrient['amount']
                unit = nutrient['nutrient']['unitName']

                # If the nutrient is already in totalNutrients, add the amount
                if nutrient_name in totalNutrients:
                    totalNutrients[nutrient_name]["amount"] += amount
                else:
                    totalNutrients[nutrient_name] = {"amount": amount, "unit": unit}

        # Return total nutrient profile
        return totalNutrients

            
# Main function for testing
def main():
    api = FoodDataCentralAPI()

    # Test with multiple food inputs
    foods = ["avocado","apple"]
    fdcId = api.getMacros(foods)

if __name__ == "__main__":
    main()