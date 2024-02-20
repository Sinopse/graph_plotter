import pathlib

import reader_plotter as rd

#path = pathlib.Path('/Users/alexander/Desktop/HZB_UV_vis_Laytec/PL_data/2023_11_30')
#path = pathlib.Path('/Users/alexander/Documents/HZB Arbeit/Messungen/in-situ_PL/Data/2023-11-9')

#path = pathlib.Path('/Users/alexander/Desktop/HZB_UV_vis_Laytec/PL_data/2023_11_30/PL_49')
path = pathlib.Path('/Users/alexander/Desktop/HZB_UV_vis_Laytec/PL_data/extern/2023-01-12/good_runs')
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
p2 = rd.Plotter()

kwargs = {
    'orientation': 'vertical',
    'format' : 'dat',
    'min_max_vals': None,

}

# introduce as **kwargs
#p1.plot_heatmap(d, axes, zoom=(0, 60, 500, 900), **kwargs)
#p2.plot_heatmap(d, axes, zoom=None, **kwargs)

# reföectanse data
#ref55 = '/Users/alexander/Desktop/HZB_UV_vis_Laytec/reflectance_data/2023-12-14/14/dat files/AT-55.dat'
ref56 = '/Users/alexander/Desktop/HZB_UV_vis_Laytec/reflectance_data/2023-12-14/14/dat files/AT-57.dat'
#pl30 = '/Users/alexander/Desktop/HZB_UV_vis_Laytec/AT_PL38.dat'

pl = rd.Reader()
pl_data = pl.read_dat(ref56)
#pl.read_dat(ref56)

formatted = pl.format_dat(pl_data, flip=True)
pl_plotter = rd.Plotter()
#pl_plotter2 = rd.Plotter()

#pl_plotter.plot_heatmap(formatted, axes=None, zoom=(400, 1000, 17, 25), **kwargs)
pl_plotter.plot_heatmap(formatted, axes=None, zoom=None, **kwargs)
#pl_plotter.plot_heatmap(formatted, axes=None, zoom=(5, 60, 400, 800), **kwargs)
#pl_plotter2.plot_heatmap(formatted, axes=None, zoom=None, **kwargs)
