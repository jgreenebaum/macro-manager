import tkinter as tk
from tkinter import ttk
import api as api

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("macro-manager")
        self.geometry("600x800")
        self.api = api.FoodDataCentralAPI()
        self.selected_fdc_ids = []
        self.foods_to_process = []
        self.create_widgets()

    def create_widgets(self):
        """
        Creates the widgets for the GUI.

        Args:
            None

        Returns:
            None
        """
        self.api_key_label = tk.Label(self, text="Enter API Key:")
        self.api_key_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.api_key_entry = tk.Entry(self)
        self.api_key_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.api_key_button = tk.Button(self, text="Submit", command=self.submit_api_key)
        self.api_key_button.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        self.api_key_display = tk.Text(self, height=1, width=50, state='disabled')
        self.api_key_display.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="w")

        self.foods_label = tk.Label(self, text="Enter Foods (comma separated):")
        self.foods_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.foods_entry = tk.Entry(self)
        self.foods_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="w")

        self.getMacros_button = tk.Button(self, text="Get Macros", command=self.submit_get_macros)
        self.getMacros_button.grid(row=2, column=2, padx=10, pady=10, sticky="w")

        self.main_window_frame = tk.Frame(self, width=400, height=300, bg="white")
        self.main_window_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

    def submit_api_key(self):
        """
        This method is called when the user clicks the "Submit" button for the API key.

        Args:
            None
        
        Returns:
            None
        """
        if self.api_key_entry.get():
            API_KEY = self.api_key_entry.get()
            self.api.set_api_key(API_KEY)
            self.api_key_entry.delete(0, tk.END)
            self.api_key_display.config(state='normal')
            self.api_key_display.delete(1.0, tk.END)
            self.api_key_display.insert(tk.END, API_KEY)
            self.api_key_display.config(state='disabled')

    """
    submit_get_macros

    This method is called when the user clicks the "Get Macros" button.
    """
    def submit_get_macros(self):
        if self.foods_entry.get():
            if not self.api.key:
                print("API key is not set. Please set the API key first.")
                return
            foods = self.foods_entry.get().split(",")
            self.foods_entry.delete(0, tk.END)
            self.foods_to_process = [food.strip() for food in foods]
            self.process_next_food()

    def process_next_food(self):
        """
        Processes the next food in the list of foods to process.

        Args:
            None
        
        Returns:
            None
        """
        if self.foods_to_process:
            food = self.foods_to_process.pop(0)
            options = self.api.get_fdc_id_options(food)
            self.display_food_options(food, options)
        else:
            self.display_nutrient_profile()

    def display_food_options(self, food, options):
        """
        Displays the food options for the user to select from.

        Args:
            food (str): The food name.
            options (list): The list of food options.

        Returns:
            None
        """
        for widget in self.main_window_frame.winfo_children():
            widget.destroy()
        
        label = tk.Label(self.main_window_frame, text=f"Select an option for {food}:")
        label.pack(pady=10)

        self.food_options = tk.StringVar(value=[f"{opt[0]} (fdc_id: {opt[1]})" for opt in options])
        
        listbox_frame = tk.Frame(self.main_window_frame)
        listbox_frame.pack(pady=10)

        scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
        listbox = tk.Listbox(listbox_frame, listvariable=self.food_options, height=10, width=70, yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.pack(side="left", fill="both", expand=True)

        select_button = tk.Button(self.main_window_frame, text="Select", command=lambda: self.select_food_option(listbox, options))
        select_button.pack(pady=10)

    def select_food_option(self, listbox, options):
        """
        Selects the food option that the user has selected.
        
        Args:
            listbox (tk.Listbox): The listbox containing the food options.
            options (list): The list of food options.
        
        Returns:
            None
        """   
        selected_index = listbox.curselection()
        if selected_index:
            selected_option = options[selected_index[0]]
            self.selected_fdc_ids.append(selected_option[1])
            print(f"Selected fdc_id: {selected_option[1]}")
            self.process_next_food()

    def display_nutrient_profile(self):
        """
        Displays the total nutrient profile for the selected foods.

        Args:
            None

        Returns:
            None     
        """
        for widget in self.main_window_frame.winfo_children():
            widget.destroy()

        total_nutrients = self.api.get_macros(self.selected_fdc_ids)

        label = tk.Label(self.main_window_frame, text="Total Nutrient Profile:")
        label.pack(pady=10)

        canvas = tk.Canvas(self.main_window_frame)
        scrollbar = tk.Scrollbar(self.main_window_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for nutrient, data in total_nutrients.items():
            formatted_amount = f"{data['amount']:.3f}"
            nutrient_label = tk.Label(scrollable_frame, text=f"{nutrient}: {formatted_amount} {data['unit']}")
            nutrient_label.pack(pady=2)

    def clear_main_window(self):
        """
        Clears the main window frame.

        Args:
            None

        Returns:
            None 
        """
        for widget in self.main_window_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    gui = GUI()
    gui.mainloop()