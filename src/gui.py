import tkinter as tk
from tkinter import ttk
import api as api

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("macro-manager")
        self.geometry("600x800")
        self.api = api.FoodDataCentralAPI()
        self.selectedfdcIds = []
        self.foodsToProcess = []
        self.create_widgets()


    """
    create_widgets

    This method creates the widgets for the GUI.
    """
    def create_widgets(self):
        self.APIKey_label = tk.Label(self, text="Enter API Key:")
        self.APIKey_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.APIKey_entry = tk.Entry(self)
        self.APIKey_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.APIKey_button = tk.Button(self, text="Submit", command=self.submitAPIKey)
        self.APIKey_button.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        self.APIKey_display = tk.Text(self, height=1, width=50, state='disabled')
        self.APIKey_display.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="w")

        self.foods_label = tk.Label(self, text="Enter Foods (comma separated):")
        self.foods_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.foods_entry = tk.Entry(self)
        self.foods_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="w")

        self.getMacros_button = tk.Button(self, text="Get Macros", command=self.submitGetMacros)
        self.getMacros_button.grid(row=2, column=2, padx=10, pady=10, sticky="w")

        self.mainWindow_frame = tk.Frame(self, width=400, height=300, bg="white")
        self.mainWindow_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)


    """
    submitAPIKey

    This method is called when the user clicks the "Submit" button for the API key.
    """
    def submitAPIKey(self):
        if self.APIKey_entry.get():
            API_KEY = self.APIKey_entry.get()
            self.api.setAPIKey(API_KEY)
            self.APIKey_entry.delete(0, tk.END)
            self.APIKey_display.config(state='normal')
            self.APIKey_display.delete(1.0, tk.END)
            self.APIKey_display.insert(tk.END, API_KEY)
            self.APIKey_display.config(state='disabled')


    """
    submitGetMacros

    This method is called when the user clicks the "Get Macros" button.
    """
    def submitGetMacros(self):
        if self.foods_entry.get():
            if not self.api.key:
                print("API key is not set. Please set the API key first.")
                return
            foods = self.foods_entry.get().split(",")
            self.foods_entry.delete(0, tk.END)
            self.foodsToProcess = [food.strip() for food in foods]
            self.processNextFood()

    
    """
    processNextFood

    This method processes the next food in the list of foods to process.
    """
    def processNextFood(self):
        if self.foodsToProcess:
            food = self.foodsToProcess.pop(0)
            options = self.api.getfdcIdOptions(food)
            self.displayFoodOptions(food, options)
        else:
            self.displayNutrientProfile()


    """
    displayFoodOptions

    This method displays the food options for the user to select from.  
    """
    def displayFoodOptions(self, food, options):
        for widget in self.mainWindow_frame.winfo_children():
            widget.destroy()
        
        label = tk.Label(self.mainWindow_frame, text=f"Select an option for {food}:")
        label.pack(pady=10)

        self.food_options = tk.StringVar(value=[f"{opt[0]} (fdcId: {opt[1]})" for opt in options])
        
        listbox_frame = tk.Frame(self.mainWindow_frame)
        listbox_frame.pack(pady=10)

        scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
        listbox = tk.Listbox(listbox_frame, listvariable=self.food_options, height=10, width=70, yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.pack(side="left", fill="both", expand=True)

        select_button = tk.Button(self.mainWindow_frame, text="Select", command=lambda: self.selectFoodOption(listbox, options))
        select_button.pack(pady=10)


    """
    selectFoodOption

    This method is called when the user selects a food option from the listbox.
    """
    def selectFoodOption(self, listbox, options):
        selectedIndex = listbox.curselection()
        if selectedIndex:
            selectedOption = options[selectedIndex[0]]
            self.selectedfdcIds.append(selectedOption[1])
            print(f"Selected fdcId: {selectedOption[1]}")
            self.processNextFood()


    """
    displayNutrientProfile

    This method is called when the user has selected all food options.
    """
    def displayNutrientProfile(self):
        for widget in self.mainWindow_frame.winfo_children():
            widget.destroy()

        totalNutrients = self.api.getMacros(self.selectedfdcIds)

        label = tk.Label(self.mainWindow_frame, text="Total Nutrient Profile:")
        label.pack(pady=10)

        canvas = tk.Canvas(self.mainWindow_frame)
        scrollbar = tk.Scrollbar(self.mainWindow_frame, orient="vertical", command=canvas.yview)
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

        for nutrient, data in totalNutrients.items():
            formattedAmount = f"{data['amount']:.3f}"
            nutrient_label = tk.Label(scrollable_frame, text=f"{nutrient}: {formattedAmount} {data['unit']}")
            nutrient_label.pack(pady=2)


    """
    clearMainWindow

    This method clears the main window frame.
    """
    def clearMainWindow(self):
        for widget in self.mainWindow_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    gui = GUI()
    gui.mainloop()