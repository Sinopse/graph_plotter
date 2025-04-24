import math
import os

import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

import reader_plotter as rd

# list or dict
def read_data_csv(file_path, save=False):
    data = {}

    if isinstance(file_path, dict):
        file_path = file_path.values()
    elif isinstance(file_path, list):
        pass
    else:
        raise TypeError("Wrong type supplied -> only list and dict")

    for num, f in enumerate(file_path, 1):
        try:
            df = pd.read_csv(f, skiprows=28, index_col=0, low_memory=False)

            sample_name = f.split('/')[-1]
            # sample_name = sample_name.split('_')[0]

            df.columns = '0.' + df.columns.str.split('.', n=1).str[-1]
            df.columns = df.columns.astype(float)

            result = [df.columns[0]]
            current_value = df.columns[0]

            diff = 0
            for i in range(1, len(df.columns)):
                if df.columns[i] < df.columns[i - 1]:
                    diff = (df.columns[i] + 1 - df.columns[i - 1])
                    current_value += diff
                    result.append(current_value)
                else:
                    diff = (df.columns[i] - df.columns[i - 1])
                    current_value += diff
                    result.append(current_value)

            # print(len(result))
            df.columns = result

            if save:
                df.to_csv(f'{sample_name}')

            if sample_name in data.keys():
                print(f'*** {sample_name} exists ***')

        except Exception as e:
            if type(e).__name__ == 'EmptyDataError':
                pass
            else:
                pass
        else:
            data[sample_name] = df

    return data


def read_data_dat(file_path):
    dat_data = {}

    if isinstance(file_path, dict):
        file_path = file_path.values()
    elif isinstance(file_path, list):
        pass
    else:
        #raise TypeError("Wrong type supplied -> only list and dict")
        file_path = [file_path]

    # Read the data from the file
    for num, f in enumerate(file_path, 1):
        try:
            with open(f, 'r') as file:
                lines = file.readlines()
                print(f'*** reading {file} ***')
                sample_name = f.split('/')[-1]

            FIRSTZ = float(lines[4].split('=')[1].strip())
            LASTZ = float(lines[5].split('=')[1].strip())
            DELTAZ = float(lines[6].split('=')[1].strip())

            # Skip the first 11 lines (metadata) and stop at the "END" string
            data_lines = []
            for line in lines[11:]:
                if "END" in line:
                    break
                data_lines.append(line.strip())

            # filename = file_path.split(('/'))[-1]

            # Convert the data lines to a NumPy array
            data = np.array([list(map(float, line.split())) for line in data_lines])

            # Number of rows and columns in the data
            num_rows, num_cols = data.shape

            # Generate the time array
            time_array = np.linspace(FIRSTZ, LASTZ, num_cols)  # It sets t0 = 0
            time = pd.Series(time_array, name="Time", dtype="float")
            time = time.round(4)

            # Extract 5 evenly spaced time stamps
            # time_indices = np.linspace(0, num_cols - 1, 5, dtype=int)

            # Extract the wavelength column (first column)
            wavelength_array = data[:, 0]
            wavelength = pd.Series(wavelength_array, name="Wavelength", dtype="float")

            data = np.rot90(data)

            df = pd.DataFrame(data, index=time, columns=wavelength)
            # df = df.iloc[::-1]
            dat_data[sample_name] = df
        except:
            raise

    return dat_data


class Plotter:
    def __init__(self, fig_size=(8, 8)):
        self.x_min = 0
        self.x_max = 0
        self.y_min = 0
        self.y_max = 0

        self.fig_size = fig_size
        self.grid_spec = None
        self.rows = 1
        self.cols = 1
        self.zoom = {}

    def plot_heatmap(self, data, orientation, format, zoom,
                     xlim=None, ylim=None, normalize=False,
                     wspace=0,
                     hspace=0,
                     fig_size=None):

        cnt = len(data)

        if isinstance(data, dict):
            self.cols = math.ceil(math.sqrt(cnt))
            self.rows = math.ceil(cnt / self.cols)

            # check number of graphs, rows and cols
            print(f" Number of graphs: {cnt}, "
                  f" number of rows: {self.rows},"
                  f" number of columns: {self.cols} \n")

        fig, axes = plt.subplots(self.rows, self.cols, figsize=fig_size, sharey=True, sharex=True,
                                 gridspec_kw={'wspace': wspace,
                                              'hspace': hspace})
        if not isinstance(data, dict):
            data = {'key': data}

        if isinstance(axes, np.ndarray):
            axes = axes.ravel()
        else:
            axes = [axes]

        for (i, ax), key in zip(enumerate(axes), data.keys()):
            d = data[key]

            if normalize:
                d = (d - d.min()) / (d.max() - d.min())

            extent = (d.columns[0], d.columns[-1], d.index[0], d.index[-1])
            print(extent)

            ax.imshow(d,
                      extent=extent,
                      cmap='magma',
                      interpolation='nearest',
                      origin='lower',
                      aspect='auto')

            if xlim:
                ax.set_xlim(xlim)

            if ylim:
                ax.set_ylim(ylim)

            columns = d.columns.tolist()
            index = d.index.tolist()

            # axs parameters
            ax.set_title(str(key), y=0.9,
                         loc='center',
                         color='red')

        for i in range(cnt, self.rows * self.cols):
            axes.flat[i].axis('off')

        plt.tight_layout()
        plt.show()

    def plot_xy_data(self, data, num_plots=None, xlim=None, ylim=None):

        # gridspec parameters
        wspace = 0
        hspace = 0

        fig, axes = plt.subplots(self.rows, self.cols, figsize=self.fig_size, sharey=True, sharex=True,
                                 gridspec_kw={'wspace': wspace,
                                              'hspace': hspace})

        for (i, ax), key in zip(enumerate(axes.ravel()), data.keys()):
            d = data[key]

            if num_plots:
                time_indices = np.linspace(1, len(d.columns) - 1, num_plots, dtype=int)
                for j in time_indices:
                    vals = d.iloc[:, j]
                    ax.plot(d.index, vals)
                    ax.set_title(str(key), y=0.8)
                    ax.axvline(x=777, color="red", linestyle="--", linewidth=2)
                    ax.set_xlim(500, 900)
            else:
                for k in range(len(d.columns)):
                    ax.plot(d.index, d.iloc[:, k])
        plt.xlabel('Wavelength')
        plt.ylabel('Intensity')
        plt.show()

    def plot_gradient(self, data, x1_idx=None, x2_idx=None, num_plots=None,
                      normalize=False, normalize_columns=False, savefig=None,
                      xlim=None, ylim=None,
                      colorbar=False):

        cnt = len(data)
        self.cols = math.ceil(math.sqrt(cnt))
        self.rows = math.ceil(cnt / self.cols)

        wspace = 0
        hspace = 0

        fig, axes = plt.subplots(self.rows, self.cols, figsize=self.fig_size, sharey=True, sharex=True,
                                 gridspec_kw={'wspace': wspace,
                                              'hspace': hspace})

        # colormap definition
        cmap = plt.cm.nipy_spectral
        norm = plt.Normalize(vmin=1, vmax=num_plots - 1)
        colors = cmap(norm(range(num_plots)))

        if isinstance(axes, np.ndarray):
            axes = axes.ravel()
        else:
            axes = [axes]

        for (i, ax), key in zip(enumerate(axes), data.keys()):
            d = data[key]

            if normalize:
                d = (d - d.min().min()) / (d.max().max() - d.min().min())

            if num_plots:
                #colors = [cmap(i / num_plots) for i in range(num_plots)]
                time_indices = np.linspace(1, len(d.columns) - 1, num_plots, dtype=int)

                for index, j in enumerate(time_indices):
                    vals = d.iloc[:, j]

                    # normalize intensity

                    if normalize_columns:
                        vals = (vals - vals.min()) / (vals.max() - vals.min())

                    # color = cmap(norm(np.mean(d.index)))
                    ax.plot(d.index, vals, color=colors[index])
                    ax.set_title(str(key), y=0.9)
                    ax.axvline(x=777, color="red", linestyle="--", linewidth=2)


                    if xlim:
                        ax.set_xlim(xlim)

                    if ylim:
                        ax.set_ylim(ylim)

            elif x1_idx or x2_idx:
                time_indices = np.arange(x1_idx, x2_idx, 1)
                colors = [cmap(i / (x2_idx - x1_idx)) for i in range((x2_idx - x1_idx))]

                for index, j in enumerate(time_indices):
                    vals = d.iloc[:, j]

                    # normalize intensity
                    if normalize:
                        vals = (vals - vals.min()) / (vals.max() - vals.min())

                    # color = cmap(norm(np.mean(d.index)))
                    ax.plot(d.index, vals, color=colors[index])
                    ax.set_title(str(key), y=0.8)
                    ax.axvline(x=777, color="red", linestyle="--", linewidth=2)

                    if xlim:
                        ax.set_xlim(xlim)

                    if ylim:
                        ax.set_ylim(ylim)

            else:
                for k in range(len(d.columns)):
                    ax.plot(d.index, d.iloc[:, k])

        # Colorbar
        if colorbar:
            for ax in axes:
                sm = cm.ScalarMappable(cmap=cmap, norm=norm)
                sm.set_array([])
                cbar = plt.colorbar(sm, ax=ax)


        for i in range(cnt, self.rows * self.cols):
            axes.flat[i].axis('off')

        if savefig:
            plt.savefig(os.path.join(savefig, f"{savefig.split('/')[-1]}.png"), dpi=600, bbox_inches='tight')

        plt.xlabel('Wavelength')
        plt.ylabel('Intensity')
        plt.tight_layout()
        plt.show()


def find_files(directory, file_format):
    csv_files = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(file_format):
                csv_files[file] = (os.path.join(root, file))
    return csv_files


pl_data = '/Volumes/DATA/in-situ_PL/2025-03-06'
# files = find_csv_files('/Volumes/DATA/SDC_Experimente/2025-03-06/2025-03-06/81')
files = find_files(pl_data, file_format=".csv")

print(files)

data = read_data_csv(files, save=True)

for k in data.keys():
    print(k)

# dict key removal
keys_to_remove = {'23_PL_measurement.csv', '87_run_18_34_88_90_100.csv'}
data = {k: v for k, v in data.items() if k not in keys_to_remove}
print("*** Keys after removal ***")
print(data.keys())

# plot parameters
kwargs = {
    'orientation': 'vertical',
    'format': 'csv',
    'fig_size': (10, 10),
    'zoom': None,
}

### Normalization
scaler = MinMaxScaler()

P = Plotter()
P.plot_heatmap(data, xlim=(100, 200), ylim=(500, 1500), **kwargs)

### plot x,y ###
xy_data = P.plot_xy_data(data, 20)
pl_xy = P.plot_gradient(data, num_plots=30, normalize=True, ylim=(-0.1, 2))
P.plot_gradient(data, x1_idx=100, x2_idx=200, ylim=(0, 1000))

### slice df based on intensity threshold
threshold = 800


def slice_threshold(data, threshold, normalize=False):
    df_slice = {}

    if isinstance(data, dict):
        for k, d in data.items():
            if normalize:
                d = (d - d.min()) / (d.max() - d.min())

            for i, col in enumerate(d.columns):
                # if d[col].max() > threshold:
                if threshold < d[col].mean():
                    d = d.iloc[:, i:]
                    df_slice[k] = d
                    break
    return df_slice


def normalize_start_point(data_dict, idx_list=None, sample_list=None):
    df_dict_norm = {}

    for key in data_dict.keys():
        d = data_dict.get(key)
        start = d.columns[0]
        d.columns = d.columns.to_series().apply(lambda x: x - start)
        df_dict_norm[key] = d

    return df_dict_norm


sliced_data = slice_threshold(data, threshold=90)
P.plot_gradient(sliced_data, x1_idx=0, x2_idx=200)
P.plot_heatmap(data, **kwargs)
P.plot_heatmap(sliced_data, normalize=False, **kwargs)

delay_keys = {'23_run_20_05_22_30_100_15s.csv', '93_run_19_34_94_30_100_5s.csv', '95_run_19_51_96_30_100_10s.csv'}
no_delay = {k: v for k, v in data.items() if k not in delay_keys}

no_delay_sliced = slice_threshold(no_delay, threshold=90)
#
# ### run91 slice
no_delay_sliced_run91 = slice_threshold(no_delay, threshold=150)
run91 = no_delay_sliced_run91.get('91_run_19_14_92_90_100.csv')
no_delay_sliced['91_run_19_14_92_90_100.csv'] = run91
no_delay_sliced_norm_start = normalize_start_point(no_delay_sliced)
#
# # P.plot_heatmap(k, normalize=False, **kwargs)
P.plot_heatmap(no_delay_sliced, xlim=(0, 300), ylim=(800, 1500), normalize=False, **kwargs)
#
delay = {k: v for k, v in data.items() if k in delay_keys}
delay_sliced = {k: v for k, v in data.items() if k in delay_keys}
#delay_sliced = slice_threshold(delay_sliced, threshold=90)
P.plot_heatmap(delay_sliced, xlim=(0, 300), ylim=(800, 1500), normalize=False, **kwargs)

P.plot_gradient(sliced_df, x1_idx=0, x2_idx=400)
# P.plot_heatmap(sliced_df, xlim=(0, 400), ylim=(500, 1500), **kwargs)

### Reflectance data 06.03.2025 ###
# reflectance = '/Volumes/DATA/SDC_Experimente/2025-03-06/6/RUN@18.16.23/'
# # reflectance = '/Volumes/DATA/SDC_Experimente/2025-03-06/6'
# reflectance_data_files = find_files(reflectance, file_format=".dat")
# print(reflectance_data_files)
#
# rdata = read_data_dat(reflectance_data_files)
# P = Plotter()
# P.plot_heatmap(rdata, **kwargs)
# # r_xy = P.plot_gradient(data, num_plots=50, savefig=reflectance)
#
# R = rd.Reader()
# r= R.read_dat(reflectance_data_files)
# f = R.format_dat(r)
# P.plot_heatmap(f, **kwargs)


### 28.03. Data for curve fitting
# run_18_16 = find_files(file_path, file_format=".dat")
# run_18_16_dat = read_data_dat(run_18_16)
# run_18_16_xy = P.plot_gradient(run_18_16_dat, num_plots=10)
