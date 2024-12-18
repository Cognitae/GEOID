import customtkinter as ctk
from tkinter import messagebox
import requests
import pyperclip
import sys
import os

# Conversion factor from meters to feet
METER_TO_FEET = 3.28083333

def resource_path(relative_path):
    """Get the absolute path to the resource, works for both .py and .exe."""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

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
    rounded_meters = round(geoid_height_meters, 3)
    rounded_feet = round(geoid_height_feet, 3)

    # Display unrounded results
    result_var.set(f"Geoid height at latitude {lat}, longitude {lon}:\n"
                   f"In meters (unrounded): {geoid_height_meters:.6f}\n"
                   f"In feet (unrounded): {geoid_height_feet:.6f}")

    # Update the clickable label for rounded values
    rounded_label_feet.configure(text=f"Click to copy: {rounded_feet:.3f} feet")
    rounded_label_feet.bind("<Button-1>", lambda e: copy_to_clipboard(f"{rounded_feet:.3f} feet"))

    rounded_label_meters.configure(text=f"Click to copy: {rounded_meters:.3f} meters")
    rounded_label_meters.bind("<Button-1>", lambda e: copy_to_clipboard(f"{rounded_meters:.3f} meters"))

def copy_to_clipboard(value):
    """
    Copies the provided value to the system clipboard and shows a confirmation message.
    """
    pyperclip.copy(value)
    show_auto_closing_message(f"{value} has been copied to the clipboard.")

def show_auto_closing_message(message, duration=1500):
    """
    Displays a temporary message box that auto-closes after a specified duration (in milliseconds).
    """
    temp_window = ctk.CTkToplevel(root)
    temp_window.title("Copied")
    temp_window.geometry("300x100")
    temp_window.resizable(False, False)
    ctk.CTkLabel(temp_window, text=message, padx=20, pady=20).pack()
    temp_window.after(duration, temp_window.destroy)
    temp_window.attributes("-topmost", True)
    temp_window.focus_force()

def toggle_appearance_mode():
    """
    Toggles between light and dark appearance modes and adjusts text colors for visibility.
    """
    current_mode = ctk.get_appearance_mode()
    new_mode = "Light" if current_mode == "Dark" else "Dark"
    ctk.set_appearance_mode(new_mode)
    text_color = "#4CAF50" if new_mode == "Dark" else "#0000FF"
    rounded_label_feet.configure(text_color=text_color)
    rounded_label_meters.configure(text_color=text_color)

# Set up the main application window
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Geoid Height Calculator")
icon_path = resource_path('Resources/CDT.ico')
root.iconbitmap(icon_path)

# Latitude input
ctk.CTkLabel(root, text="Latitude (decimal degrees):").grid(row=0, column=0, padx=10, pady=5)
lat_entry = ctk.CTkEntry(root)
lat_entry.grid(row=0, column=1, padx=10, pady=5)

# Longitude input
ctk.CTkLabel(root, text="Longitude (decimal degrees):").grid(row=1, column=0, padx=10, pady=5)
lon_entry = ctk.CTkEntry(root)
lon_entry.grid(row=1, column=1, padx=10, pady=5)

# Calculate button
calc_button = ctk.CTkButton(root, text="Calculate", command=calculate)
calc_button.grid(row=2, column=0, columnspan=2, pady=10)

# Result display
result_var = ctk.StringVar()
result_label = ctk.CTkLabel(root, textvariable=result_var, justify="left")
result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Clickable labels
rounded_label_feet = ctk.CTkLabel(root, text="", text_color="#4CAF50", cursor="hand2")
rounded_label_feet.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
rounded_label_meters = ctk.CTkLabel(root, text="", text_color="#4CAF50", cursor="hand2")
rounded_label_meters.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

# Appearance mode toggle switch
appearance_mode_switch = ctk.CTkSwitch(root, text="Dark Mode", command=toggle_appearance_mode)
appearance_mode_switch.grid(row=6, column=0, columnspan=2, pady=10)
appearance_mode_switch.select()

# Start the GUI event loop
root.mainloop()
