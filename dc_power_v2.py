import tkinter as tk
from tkinter import filedialog
import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline, pchip
import matplotlib.pyplot as plt

# Global variable to store the selected file path
selected_file_path = None

def process_data(file_path, selected_file_path_2):
    # Import data from Excel file using pandas
    df = pd.read_excel(file_path)

    # 
    df2 = pd.read_excel(selected_file_path_2)
    data_column = df2.iloc[0:7, 2].values
    print(data_column)

    # Extract columns to be used
    Selion = df.iloc[:, 0]
    mP = df.iloc[:, 1]

    # Define duty cycle values for interpolation
    T = 24
    DCm = np.array([[10, data_column[0]/T],
                    [20, data_column[1]/T],
                    [30, data_column[2]/T],
                    [40, data_column[3]/T],
                    [50, data_column[4]/T],
                    [63, data_column[5]/T]])

    xq = np.arange(0, 64, 1)

    # Interpolate duty cycle values using PCHIP
    pchip_interpolator = pchip(DCm[:, 0], DCm[:, 1])
    DC1 = pchip_interpolator(xq)

    # Use CubicSpline for cubic interpolation
    cubic_spline = CubicSpline(DCm[:, 0], DCm[:, 1])
    DC2 = cubic_spline(xq)

    # Calculate peak power
    P = mP / DC1

    # Plot duty cycle and peak power
    plt.figure()

    plt.subplot(2, 1, 1)
    plt.plot(xq, DC1, 'r*', xq, DC2, 'gx', DCm[:, 0], DCm[:, 1], '.')
    plt.ylabel('Duty Cycle')
    plt.xlabel('Selion')
    plt.legend(['PCHIP', 'Spline', 'Measured DC'])

    plt.subplot(2, 1, 2)
    plt.plot(Selion, P, Selion, df.iloc[:, 6])
    plt.ylabel('Peak Power')
    plt.xlabel('Selion')
    plt.legend(['Interpolated P', 'Measured P'])

    plt.show()

def browse_file():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename(title="Select File", filetypes=[("All Files", "*.*")])
    # Update the label to show the selected file path
    file_label.config(text=f"Selected File: {selected_file_path}")
    # Close the file dialog
    root.update_idletasks()

  
def browse_file_2():
    global selected_file_path_2
    selected_file_path_2 = filedialog.askopenfilename(title="Select File 2", filetypes=[("All Files", "*.*")])
    # Update the label to show the selected file path
    file_label_2.config(text=f"Selected File 2: {selected_file_path_2}")
    # Close the file dialog
    root.update_idletasks()

def run_process_data():
    global selected_file_path, selected_file_path_2
    process_data(selected_file_path, selected_file_path_2)

# Create GUI
root = tk.Tk()
root.title("Data Processing GUI")

browse_button = tk.Button(root, text="Browse data file", command=browse_file)
browse_button.pack(pady=10)

file_label = tk.Label(root, text="Selected File: None")
file_label.pack(pady=10)

browse_button_2 = tk.Button(root, text="Browse pulse width file", command=browse_file_2)
browse_button_2.pack(pady=5)

# browse second file
file_label_2 = tk.Label(root, text="Selected File: None")
file_label_2.pack(pady=5)


run_button = tk.Button(root, text="Run", command=run_process_data)
run_button.pack(pady=10)

root.mainloop()
