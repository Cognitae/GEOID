# Geoid Height Calculator

## Description
The Geoid Height Calculator is a Python-based GUI application that calculates the geoid height for a given latitude and longitude using the NGS Geoid Height Service API. The application provides results in both meters and feet, with rounded and unrounded values displayed.

## Features
- **Modern GUI**: Built with `CustomTkinter` for a sleek and user-friendly interface.
- **Dark/Light Mode Toggle**: Easily switch between appearance modes for comfortable use.
- **Clipboard Copy**: Quickly copy calculated values (in meters or feet) to the clipboard.
- **Custom Icons**: Includes distinct icons for the application window and `.exe` file.

## Requirements
- Python 3.8 or later
- Required libraries:
  - `customtkinter`
  - `requests`
  - `pyperclip`

## Installation
1. Clone or download the project to your local machine.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python GEOID.py
   ```

## Packaging as an Executable
To create a standalone `.exe` file:
1. Ensure PyInstaller is installed:
   ```bash
   pip install pyinstaller
   ```
2. Package the application:
   ```bash
   python -m PyInstaller --onefile --windowed --icon=Resources/GEOID.ico GEOID.py
   ```
3. The `.exe` file will be available in the `dist` directory.

## Usage
1. Enter the latitude and longitude in decimal degrees.
2. Click "Calculate" to fetch the geoid height.
3. View the results (rounded and unrounded) in meters and feet.
4. Click on the clickable labels to copy rounded values to the clipboard.
5. Toggle between dark and light modes using the switch.

## Customization
- To modify the icons, replace the `.ico` files in the `Resources` directory.
- Adjust the appearance themes in the code (`ctk.set_default_color_theme`).

## Contributing
Feel free to fork the repository, make changes, and submit a pull request.

