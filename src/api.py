import requests
import logging
from urllib.parse import quote
from collections import defaultdict

class FoodDataCentralAPI:
    def __init__(self):
        self.key = None
        self.baseUrl = "https://api.nal.usda.gov/fdc/v1"

    def set_api_key(self, key: str):
        """
        Sets the API key for the FoodDataCentralAPI instance.
        
        Args:
            key (str): The API key to set.
        """
        self.key = key

    def get_fdc_id_options(self, food: str):
        """
        Fetches FDC ID options for a given food query.

        Args:
            food (str): The food to search for.
        
        Returns:
            list: A list of tuples containing the food name and its FDC ID.
        """
        if not self.key:
            raise ValueError("API key is not set. Please set the API key first.")
        
        url = f"{self.baseUrl}/foods/search?query={quote(str(food))}&dataType=Survey%20(FNDDS)&api_key={self.key}"
        response = requests.get(url)

        # Handle errors if request fails
        if response.status_code != 200:
            logging.error(f"Error: {response.status_code}, {response.text}")
            return None
        
        foods = response.json().get('foods', [])

        # No results
        if not foods:
            logging.info(f"No results found for {food}")
            return []

        # Collect name/id pairs
        name_and_id_pair_list = [(food_item['description'], food_item['fdcId']) for food_item in foods]
        return name_and_id_pair_list
    
    def get_food_data(self, foods: list):
        """
        Fetches food data for a list of foods.

        Args:
            foods (list): A list of FDC IDs to fetch data for.

        Returns:
            list: A list of food nutrient data.      
        """
        if not self.key:
            raise ValueError("API key is not set. Please set the API key first.")
        
        fdc_ids = "/foods?"
        for food in foods:
            fdc_ids += f"fdcIds={quote(str(food))}&"
        url = f"{self.baseUrl}{fdc_ids}api_key={self.key}"
        response = requests.get(url)
        
        # Handle errors if request fails
        if response.status_code != 200:
            logging.error(f"Error: {response.status_code}, {response.text}")
            return None
        
        # Save all food nutrient data to a list
        food_nutrients_list = [food["foodNutrients"] for food in response.json()]
        return food_nutrients_list

    def get_macros(self, foods: list):
        """
        Fetches the total nutrient profile for a list of foods.

        Args:
            foods (list): A list of foods to fetch data for.
        
        Returns:
            dict: A dictionary containing the total nutrient profile.
        """
        response_list = self.getFoodData(foods)

        total_nutrients = defaultdict(lambda: {"amount": 0.0, "unit": ""})

        # Iterate over each food's nutrient data
        for food_nutrients in response_list:
            for nutrient in food_nutrients:
                nutrient_name = nutrient['nutrient']['name']
                amount = nutrient['amount']
                unit = nutrient['nutrient']['unitName']

                # If the nutrient is already in total_nutrients, add the amount
                if nutrient_name in total_nutrients:
                    total_nutrients[nutrient_name]["amount"] += amount
                else:
                    total_nutrients[nutrient_name] = {"amount": amount, "unit": unit}

        # Return total nutrient profile
        return total_nutrients
