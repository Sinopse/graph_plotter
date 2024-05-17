import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

#file_path = r"D:\Seafile\Code\DataExamples\Alex_S-4_14_26.dat"
file_path = '/Volumes/Data Storag/Reflectance Probe/2024-04-18/18/RUN@15.58.20/S-10_run_15_58.dat'


# Read the data from the file
with open(file_path, 'r') as file:
    lines = file.readlines()

# Extract metadata for time information

FIRSTZ = float(lines[4].split('=')[1].strip())
LASTZ = float(lines[5].split('=')[1].strip())
DELTAZ = float(lines[6].split('=')[1].strip())

# Skip the first 11 lines (metadata) and stop at the "END" string
data_lines = []
for line in lines[11:]:
    if "END" in line:
        break
    data_lines.append(line.strip())

# Convert the data lines to a NumPy array
data = np.array([list(map(float, line.split())) for line in data_lines])

# Number of rows and columns in the data
num_rows, num_cols = data.shape

# Generate the time array
time_array = np.linspace(0, LASTZ - FIRSTZ, num_cols)  # It sets t0 = 0

# Extract 5 evenly spaced time stamps
time_indices = np.linspace(0, num_cols - 1, 5, dtype=int)

# Extract the wavelength column (first column)
wavelength = data[:, 0]


def plot_evenly(peak_values, num_plots):
    # Extract 5 evenly spaced columns (excluding the first column)
    time_indices = np.linspace(1, num_cols - 1, num_plots, dtype=int)

    # Plotting the selected columns with respect to wavelength
    plt.figure(figsize=(10, 6))
    for i in time_indices:
        peaks = peak_values[i]
        time_stamp = time_array[i]
        values = data[:, i]
        plt.plot(wavelength, values, label=f'Time {time_stamp:.2f}')
        plt.plot(wavelength[peaks], values[peaks], "x", label=f'Peaks Time {time_stamp:.2f}')
    plt.xlabel('Wavelength')
    plt.ylabel('Value')
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    #plt.legend()
    plt.title('Selected Columns vs. Wavelength')
    plt.show()


def find_peaks_process():
    # Extract 5 evenly spaced columns (excluding the first column)
    time_index = np.linspace(1, num_cols - 1, 5, dtype=int)

    # Finding peaks
    peaks_found = []
    for i in range(num_cols):
        values = data[:, i]
        time_stamp = time_array[i]
        peaks, _ = find_peaks(values, prominence=0.01, distance=25)  # Adjust these parameters as needed
        filtered_peaks = peaks[(peaks >= 102) & (peaks <= 1070)]  # 150=450nm & 1070=1005nm
        peaks_found.append(filtered_peaks)

    return peaks_found


show_plots = 10
peaks_list = find_peaks_process()
plot_evenly(peaks_list, show_plots)

