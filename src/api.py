import requests
import os

class FoodDataCentralAPI:
    def __init__(self):
        self.key = os.getenv('API_KEY')
        self.baseUrl = "https://api.nal.usda.gov/fdc/v1"

        if not self.key:
            raise ValueError("API_KEY envrionment variable is not set!")

    def getfdcId(self, food: str):
        url = f"{self.baseUrl}/foods/search?query={food}&dataType=Survey%20(FNDDS)&api_key={self.key}"
        response = requests.get(url)
        
        # Handle errors if request fails
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            return None
        
        foods = response.json().get('foods',[])

        # No results
        if not foods:
            print(f"No results found for '{food}'.")
            return None
        
        # Print all food options
        print(f"Found {len(foods)} options for '{food}':\n")
        for index, foodItem in enumerate(foods, start=1):
            print(f"{index}. {foodItem['description']}")

        # Prompt user
        try:
            choice = int(input(f"\nChoose a number (1-{len(foods)}): "))
            if 1 <= choice <= len(foods):
                selectedfdcId = foods[choice - 1]['fdcId']
                print(f"You selected: {foods[choice - 1]['description']}")
                return selectedfdcId
            else:
                print(f"Invalid choice. Please choose a number between 1 and {len(foods)}.")
                return None
        except ValueError:
            print("Invalid input. Please enter a number.")
            return None
        
    # def getFoodData(self, fdcId: int):
    #     url = f"{self.baseUrl}/food/{fdcId}?api_key={self.key}"
    #     response = requests.get(url)
        
    #     # Handle errors if request fails
    #     if response.status_code != 200:
    #         print(f"Error: {response.status_code}, {response.text}")
    #         return None
        
    #     foodNutrients = response.json().get('foodNutrients', [])
        
    #     # Print the name, amount, and unit of each nutrient
    #     for nutrient in foodNutrients:
    #         nutrient_name = nutrient['nutrient']['name']
    #         amount = nutrient['amount']
    #         unit = nutrient['nutrient']['unitName']
    #         print(f"{nutrient_name}: {amount} {unit}")

    def getFoodData(self, food: str):
        fdcId = self.getfdcId(food)
        url = f"{self.baseUrl}/food/{fdcId}?api_key={self.key}"
        response = requests.get(url)
        
        # Handle errors if request fails
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            return None
        
        foodNutrients = response.json().get('foodNutrients', [])
        
        # Print the name, amount, and unit of each nutrient
        for nutrient in foodNutrients:
            nutrient_name = nutrient['nutrient']['name']
            amount = nutrient['amount']
            unit = nutrient['nutrient']['unitName']
            print(f"{nutrient_name}: {amount} {unit}")

# Main function for testing
def main():
    # api = FoodDataCentralAPI()

    # # Example FDC ID for testing (replace with a valid one)
    # test_fdc_id = 454004  

    # print(f"Fetching food data for FDC ID: {test_fdc_id}")
    # api.getFoodData(test_fdc_id)

    api = FoodDataCentralAPI()

    # Test with a singular food input
    food = "avocado"
    fdcId = api.getFoodData(food)
    if fdcId:
        print(f"Selected fdcId: {fdcId}")

if __name__ == "__main__":
    main()