import pathlib

import reader_plotter as rd

#path = pathlib.Path('/Users/alexander/Desktop/HZB_UV_vis_Laytec/PL_data/2023_11_30')
#path = pathlib.Path('/Users/alexander/Documents/HZB Arbeit/Messungen/in-situ_PL/Data/2023-11-9')

#path = pathlib.Path('/Users/alexander/Desktop/HZB_UV_vis_Laytec/PL_data/2023_11_30/PL_49')
#path = pathlib.Path('/Users/alexander/Desktop/HZB_UV_vis_Laytec/PL_data/extern/2023-01-12/good_runs')
#path = pathlib.Path('/Users/alexander/Desktop/HZB_UV_vis_Laytec/PL_data/2024-03-06')
path = pathlib.Path('/Volumes/DATA/SDC_Experimente/2025-03-06/2025-03-06')
lst = list(path.rglob('*.csv'))

#print(lst)
#r = rd.Reader()
#r.read_csv(lst)
# r.__repr__()
#data = r._data
#axes = r._axes
#d, axs = r.format_pl(data, axes)

#print(d)
#print(axs)


# axes = r.return_axes()
#vals = r.get_min_max_vals()
#p1 = rd.Plotter((10, 10))
#p2 = rd.Plotter((10, 10))

kwargs = {
    'orientation': 'vertical',
    'format' : 'csv',
    'min_max_vals': None,

}

# introduce as **kwargs
#p1.plot_heatmap(d, axes, zoom=(0, 50, 300, 100 ), **kwargs)
#p2.plot_heatmap(d, axes, zoom=None, **kwargs)

# REFLECTANCE DATA ###
#########

dat_path = pathlib.Path('/Volumes/Data Storag/Reflectance Probe/2024-04-18')
dat_lst = list(path.rglob('*.dat'))

def find_dat_files(folder):
    folder_path = pathlib.Path(folder)
    dat_files = {}

    for file in folder_path.rglob("*.dat"):
        if file.is_file():
            dat_files[file.name] = file


    return dat_files

dat_files = find_dat_files(dat_path)

keys_to_delete = list(dat_files.keys())[:2]

# Delete first two keys
#for key in keys_to_delete:
#    del dat_files[key]


### measurement 18.04.2024 ###

measurement_data = {
#'15_58' : '/Volumes/Data Storag/Reflectance Probe/2024-04-18/18/RUN@15.58.20/S-10_run_15_58.dat',
 #'15_46' : '/Volumes/Data Storag/Reflectance Probe/2024-04-18/18/RUN@15.46.08/S-9_15_46.dat',
 #'15_36' : '/Volumes/Data Storag/Reflectance Probe/2024-04-18/18/RUN@15.36.08/S-8_15_36.dat',
 #'15_22' : '/Volumes/Data Storag/Reflectance Probe/2024-04-18/18/RUN@15.22.04/S-7_run_15_22.dat'
#'/Users/alexander/Desktop/HZB_UV_vis_Laytec/reflectance_data/2023-12-14/14/dat files/AT-55.dat'
}

Reader = rd.Reader()
#pl_data = reader.read_dat(measurement_data)


### measurement 07.05.2024 ###

#folder_21_08 = '/Volumes/Data Storag/Reflectance Probe/2024-05-07/dat'
#folder_06_05 = '/Users/alexander/Desktop/HZB_UV_vis_Laytec/reflectance_data/2023-12-14/14/dat files'
#folder_06_05 = '/Volumes/Data Storag/Reflectance Probe/2024-05-07/7/RUN@14.26.51'
#folder_23_07 = '/Volumes/Data Storag/Reflectance Probe/2024-07-19/19'
#folder_23_07 = '/Volumes/Data Storag/Reflectance Probe/2024-07-04/4'
#folder_21_08 = '/Volumes/Data Storag/Reflectance Probe/2024-04-18/18'
#folder_21_08 = '/Volumes/Data Storag/Reflectance Probe/2024-04-09/9'

#folder_21_08 = '/Volumes/DATA/2024-12-23'   23-12-24
#folder_21_08 = '/Volumes/DATA/2025-01-07/1/7'
#folder_21_08 = '/Volumes/DATA/2025-01-27/27'
#folder_21_08 = '/Volumes/DATA/Max_Grischek_SDC/2/14'
#folder_21_08 = '/Volumes/DATA/SDC_Experimente/2025-02-27/27'
#folder_21_08 = '/Volumes/DATA/SDC_Experimente/2025-03-06/6'


folder_21_08 ='/Volumes/DATA/SDC_Experimente/2025-03-06/6' # PL data 6.03.2025


### aBOMA PL test ###
#aboma = '/Users/alexander/Desktop/Aboma unfinished/voc paper/insitu abs and PL/JD_Aboma_PL_test'


#data_06_05_24 = find_dat_files(folder_21_08)

#print(data_06_05_24)

### use this when folder

#read_06_05 = Reader.read_dat(data_06_05_24)


### use this when single spectra ###

#read_06_05 = Reader.read_dat('/Volumes/DATA/2025-01-27/27/RUN@18.16.07/run_18_16.dat')
#read_06_05 = Reader.read_dat('/Volumes/DATA/2025-01-27/27/RUN@17.47.18/run_17_47.dat')
read_06_05 = Reader.read_dat('/Volumes/DATA/SDC_Experimente/2025-03-06/6/RUN@20.05.46/run_20_05_22_30_100_15s.dat')

formatted = Reader.format_dat(read_06_05, flip=True)


data_dict = {}
for key, value in formatted.items():
    data_dict[key] = value.to_dict(orient='index')

pl_plotter = rd.Plotter(fig_size=(10, 10))

#pl_plotter.plot_heatmap(formatted, axes=None, zoom=None, wspace=0, hspace=0.15, **kwargs)

#pl_plotter.plot_heatmap(formatted, axes=None, zoom=(400, 1000, 0.01, 60), **kwargs)   ##äorignal line

#pl_plotter.plot_heatmap(formatted, axes=None, zoom=(400, 1000, 39, 41), **kwargs)
pl_plotter.plot_heatmap(formatted, axes=None, zoom=None, **kwargs)
#pl_plotter.plot_heatmap(formatted, axes=None, zoom=(400, 1000, 0.01, 50), **kwargs)
#pl_plotter2.plot_heatmap(formatted, axes=None, zoom=None, **kwargs)

print(data_dict.keys())