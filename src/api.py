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
        

    def getFoodData(self, foods: list):
        fdcIds = "/foods?"
        for food in foods:
            fdcId = self.getfdcId(food)
            fdcIds += f"fdcIds={fdcId}&"
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

        for i, food in enumerate(foods):
            print(f"\nShowing nutrients for {food}:\n")
            for nutrient in responseList[i]:
                nutrient_name = nutrient['nutrient']['name']
                amount = nutrient['amount']
                unit = nutrient['nutrient']['unitName']
                print(f"{nutrient_name}: {amount} {unit}")

            
# Main function for testing
def main():
    api = FoodDataCentralAPI()

    # Test with multiple food inputs
    foods = ["avocado","apple"]
    fdcId = api.getMacros(foods)

if __name__ == "__main__":
    main()