import tkinter as tk
import api as api

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("macro-manager")
        self.geometry("600x400")
        self.api = api.FoodDataCentralAPI()
        self.create_widgets()

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

    def submitAPIKey(self):
        if self.APIKey_entry.get():
            API_KEY = self.APIKey_entry.get()
            self.api.setAPIKey(API_KEY)
            self.APIKey_entry.delete(0, tk.END)
            self.APIKey_display.config(state='normal')
            self.APIKey_display.delete(1.0, tk.END)
            self.APIKey_display.insert(tk.END, API_KEY)
            self.APIKey_display.config(state='disabled')


    def submitGetMacros(self):
        if self.foods_entry.get():
            if not self.api.key:
                print("API key is not set. Please set the API key first.")
                return
            foods = self.foods_entry.get().split(",")
            self.foods_entry.delete(0, tk.END)
            foods = [food.strip() for food in foods]
            self.selectedfdcIds = []

            def displayFoodOptions(foodIndex):
                if foodIndex >= len(foods):
                    return

                food = foods[foodIndex]
                options = self.api.getfdcIdOptions(food)
                if not options:
                    displayFoodOptions(foodIndex + 1)
                    return

                for widget in self.mainWindow_frame.winfo_children():
                    widget.destroy()

                tk.Label(self.mainWindow_frame, text=f"Select option for: {food}").pack(anchor="w")

                varList = []
                for option in options:
                    var = tk.BooleanVar()
                    chk = tk.Checkbutton(self.mainWindow_frame, text=option[0], variable=var)  # Accessing the first element of the tuple
                    chk.pack(anchor="w")
                    varList.append((var, option[1]))  # Accessing the second element of the tuple

                def confirmSelection():
                    for var, fdcId in varList:
                        if var.get():
                            self.selectedfdcIds.append(fdcId)
                    displayFoodOptions(foodIndex + 1)

                tk.Button(self.mainWindow_frame, text="Confirm", command=confirmSelection).pack(anchor="w")

            displayFoodOptions(0)

if __name__ == "__main__":
    gui = GUI()
    gui.mainloop()