import pathlib

import reader_plotter as rd

#path = pathlib.Path('/Users/alexander/Desktop/HZB_UV_vis_Laytec/PL_data/2023_11_30')
#path = pathlib.Path('/Users/alexander/Documents/HZB Arbeit/Messungen/in-situ_PL/Data/2023-11-9')

#path = pathlib.Path('/Users/alexander/Desktop/HZB_UV_vis_Laytec/PL_data/2023_11_30/PL_49')
#path = pathlib.Path('/Users/alexander/Desktop/HZB_UV_vis_Laytec/PL_data/extern/2023-01-12/good_runs')
path = pathlib.Path('/Users/alexander/Desktop/HZB_UV_vis_Laytec/PL_data/2024-03-06')
lst = list(path.rglob('*.csv'))

#print(lst)
r = rd.Reader()
r.read_csv(lst)
# r.__repr__()
data = r._data
axes = r._axes
d, axs = r.format_pl(data, axes)

#print(d)
#print(axs)


# axes = r.return_axes()
#vals = r.get_min_max_vals()
p1 = rd.Plotter((10, 10))
p2 = rd.Plotter((10, 10))

kwargs = {
    'orientation': 'vertical',
    'format' : 'dat',
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
    dat_files = []

    for file in folder_path.rglob("*.dat"):
        if file.is_file():
            dat_files.append(file.name)

    return dat_files

dat_files = find_dat_files(dat_path)
print(dat_files)

#ref = '/Volumes/Data Storag/Reflectance Probe/2024-04-09/9/RUN@15.15.05/run_15_15.dat'
ref = '/Volumes/Data Storag/Reflectance Probe/2024-04-18/18/RUN@15.58.20/S-10_run_15_58.dat'
#ref = '/Volumes/Data Storag/Reflectance Probe/2024-04-18/18/RUN@15.46.08/S-9_15_46.dat'
#ref = '/Volumes/Data Storag/Reflectance Probe/2024-04-18/18/RUN@15.36.08/S-8_15_36.dat'
#ref = '/Volumes/Data Storag/Reflectance Probe/2024-04-18/18/RUN@15.22.04/S-7_run_15_22.dat'

#ref = '/Volumes/Data Storag/Reflectance Probe/2024-04-09/9/RUN@13.50.45/run_13_50.dat'
#ref = '/Users/alexander/Desktop/HZB_UV_vis_Laytec/reflectance_data/2023-12-14/14/dat files/AT-55.dat'
#ref56 = '/Users/alexander/Desktop/HZB_UV_vis_Laytec/reflectance_data/2023-12-14/14/dat files/AT-65.dat'
#pl30 = '/Users/alexander/Desktop/HZB_UV_vis_Laytec/AT_PL38.dat'

pl = rd.Reader()
pl_data = pl.read_dat(ref)
pl.read_dat(ref)

formatted = pl.format_dat(pl_data, flip=True)
pl_plotter = rd.Plotter()
#pl_plotter2 = rd.Plotter()

#pl_plotter.plot_heatmap(formatted, axes=None, zoom=(400, 1000, 17, 25), **kwargs)
pl_plotter.plot_heatmap(formatted, axes=None, zoom=None, **kwargs)
#pl_plotter.plot_heatmap(formatted, axes=None, zoom=(400, 1000, 20, 100), **kwargs)
#pl_plotter2.plot_heatmap(formatted, axes=None, zoom=None, **kwargs)

