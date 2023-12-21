import pathlib

import reader_plotter as rd

path = pathlib.Path('/Users/alexander/Desktop/HZB_UV_vis_Laytec/PL_data/2023_11_30')

#path = pathlib.Path('/Users/alexander/Desktop/HZB_UV_vis_Laytec/PL_data/2023_11_30/PL_49')
lst = list(path.rglob('*.csv'))

#print(lst)
r = rd.Reader()
r.to_dict(lst)
r.traverse_dict()
dic = r.return_data()
axes = r.return_axes()
vals = r.get_min_max_vals()
p1 = rd.Plotter()
p2 = rd.Plotter((14, 14))

kwargs = {
    'orientation': 'vertical',
    'min_max_vals': vals,

}

# introduce as **kwargs
p1.plot_heatmap(dic, axes, zoom=(20, 60, 600, 800), **kwargs)
p2.plot_heatmap(dic, axes, zoom=None, **kwargs)
