import tkinter as tk
from tkinter import messagebox
import requests
import pyperclip

# Conversion factor from meters to feet
METER_TO_FEET = 3.28083333

def get_geoid_height(lat, lon):
    """
    Fetches the geoid height for the given latitude and longitude using the NGS Geoid Height Service API.
    """
    api_url = "https://geodesy.noaa.gov/api/geoid/ght"
    params = {
        'lat': lat,
        'lon': lon,
        'model': 14  # GEOID18 model ID
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        geoid_height_meters = data.get('geoidHeight')
        if geoid_height_meters is None:
            messagebox.showerror("Error", "Geoid height not found in the response.")
            return None
        return geoid_height_meters
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"An error occurred while fetching geoid height: {e}")
        return None

def calculate():
    try:
        lat = float(lat_entry.get())
        lon = float(lon_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values for latitude and longitude.")
        return

    geoid_height_meters = get_geoid_height(lat, lon)
    if geoid_height_meters is None:
        return

    geoid_height_feet = geoid_height_meters * METER_TO_FEET
    rounded_feet = round(geoid_height_feet, 3)

    result_var.set(f"Geoid height at latitude {lat}, longitude {lon}:\n"
                   f"In meters: {geoid_height_meters:.6f}\n"
                   f"In feet: {geoid_height_feet:.6f}\n"
                   f"Rounded to the nearest thousandth: {rounded_feet}")

    # Update the clickable label with the rounded value
    rounded_label.config(text=f"Click to copy: {rounded_feet} feet")
    rounded_label.bind("<Button-1>", lambda e: copy_to_clipboard(rounded_feet))

def copy_to_clipboard(value):
    """
    Copies the provided value to the system clipboard and shows a confirmation message.
    """
    pyperclip.copy(value)
    show_auto_closing_message(f"{value} feet has been copied to the clipboard.")

def show_auto_closing_message(message, duration=500):
    """
    Displays a temporary message box that auto-closes after a specified duration (in milliseconds).
    """
    # Create a top-level window
    temp_window = tk.Toplevel(root)
    temp_window.title("Copied")
    temp_window.geometry("300x100")
    temp_window.resizable(False, False)

    # Center the window on the screen
    window_width = 300
    window_height = 100
    screen_width = temp_window.winfo_screenwidth()
    screen_height = temp_window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    temp_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    # Display the message
    tk.Label(temp_window, text=message, padx=20, pady=20).pack()

    # Schedule the window to close after the specified duration
    temp_window.after(duration, temp_window.destroy)

    # Ensure the window is on top and focus is set
    temp_window.attributes("-topmost", True)
    temp_window.focus_force()

# Set up the main application window
root = tk.Tk()
root.title("Geoid Height Calculator")

# Latitude input
tk.Label(root, text="Latitude (decimal degrees):").grid(row=0, column=0, padx=10, pady=5)
lat_entry = tk.Entry(root)
lat_entry.grid(row=0, column=1, padx=10, pady=5)

# Longitude input
tk.Label(root, text="Longitude (decimal degrees):").grid(row=1, column=0, padx=10, pady=5)
lon_entry = tk.Entry(root)
lon_entry.grid(row=1, column=1, padx=10, pady=5)

# Calculate button
calc_button = tk.Button(root, text="Calculate", command=calculate)
calc_button.grid(row=2, column=0, columnspan=2, pady=10)

# Result display
result_var = tk.StringVar()
result_label = tk.Label(root, textvariable=result_var, justify=tk.LEFT)
result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Clickable label for rounded value
rounded_label = tk.Label(root, text="", fg="blue", cursor="hand2")
rounded_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

# Start the GUI event loop
root.mainloop()
