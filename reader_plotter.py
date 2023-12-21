import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import itertools
import pathlib

class DataFormatter:
    def format_pl(self, data, axes, **kwargs):
        # no recursive behavior -> think about it later

        if isinstance(data, dict):
            for key, frame in data.items():
                if isinstance(frame, pd.DataFrame):
                    wavelength = frame[0][1:]
                    del frame[0]

                    wv = wavelength.to_numpy()
                    _wv = [str(i) for i in wv]

                    wavelength = pd.Series(_wv)
                    time = frame.loc[0]
                    frame.drop(0, inplace=True)
                    np_array = frame.to_numpy()

                    # axes
                    axes_formatted = (wavelength, time)

                    ## convert to an NumPy array and then again to a DF with new indices
                    # min_val = min(val.min() for val in array)
                    # max_val = max(val.max() for val in array)

                    frame_formatted = pd.DataFrame(np_array, index=wavelength, columns=time)
                    data[key] = frame_formatted
                    axes[key] = axes_formatted

                    del frame
                    del wv
                    del _wv
                    del np_array
                    del wavelength
                    del time

                else:
                    raise TypeError(f"Supplied type not DataFrame, supplied: {type(data)}")
        else:
            raise TypeError(f"Wrong type supplied -> dict, supplied: {type(data)}")
        return data, axes

    # 28.11.2023
    # data preparation for dat files
    def prepare_dat(self, data, rotate=False):
        row, col = data.shape
        _data = pd.read_csv(data, sep='\s+', low_memory=False, nrows=6, header=None)
        time_stamps = _data.iloc[3:6, 2]
        wavelength = data.iloc[:, 0]
        # new time Series
        time = pd.Series(time_stamps, dtype='float')
        # new wavelength index
        w_index = pd.Series(wavelength, name='wavelength', dtype='float')

        # time stamps from measurement data
        t_min, t_max, t_delta = time
        new_delta = t_max / (col - 1)

        # calculate each time
        cnt = 1
        time_lst = []
        while t_min + new_delta <= t_max + new_delta:
            time_lst.append(round(t_min, 4))
            cnt += 1
            t_min += new_delta

        # new time index
        t_index = pd.Series(time_lst, name='time', dtype='float')

        # DataFrame to array
        array = _data.to_numpy()

        # custom array rotation if needed
        if rotate:
            array = np.rot90(array)

        # create new DataFrame
        data = pd.DataFrame(array, columns=w_index, index=t_index)
        return data


class Reader(DataFormatter):
    def __init__(self, min_val=None, max_val=None):
        self._data = {}
        self._axes = {}
        self._min_val = min_val
        self._max_val = max_val

    # class will be refactored to accommodate further functionality
    # Reader -> only reads relevant data formats
    # and stores data -> format data based on measurement type and data format
    # -> passed on to plotter

    # recognize format of the file
    def read_file_format(self):
        pass

    def read_dat(self, file, *args, **kwargs):
        if isinstance(file, str):
            sample_name = file.split(sep='/')[-1]  # sample name
            _file = pd.read_csv(file, skiprows=11, sep='\s+', header=None, skipfooter=1, engine='python')
            self._data[sample_name] = _file
        else:
            raise TypeError("Not a path")
        return self._data

    # 28.11.2023 this func will be deprecated in near future
    # PL data from In-Situ PL setup
    def read_csv(self, files):
        if isinstance(files, list):
            for num, f in enumerate(files, 1):
                try:
                    _f = pd.read_csv(f, skiprows=28, header=None, low_memory=False)

                    # retrieve sample names -> first implementation, consider a defaultdict?
                    # data management -> sample name, composition, etc.

                    sample_name = self.get_sample_name(f)
                    if sample_name in self._data.keys():
                        print(f'*** {sample_name} exists ***')

                except Exception as e:
                    if type(e).__name__ == 'EmptyDataError':
                        pass
                    else:
                        raise
                else:
                    self._data[sample_name] = _f
        else:
            raise TypeError("Wrong type supplied -> dict")
        return self._data

    def get_min_max_vals(self):
        _vals_list = []
        if self._data:
            for key in self._data.keys():
                value = self._data[key]
                array = value.to_numpy()
                min_val = min(val.min() for val in array)
                max_val = max(val.max() for val in array)
                _vals_list.append((min_val, max_val))
        else:
            raise ValueError("dictionary empty")
        return _vals_list

    @staticmethod
    # get sample_name from metadata
    def get_sample_name(file):
        s = str()
        sample_name = str()
        with open(file, 'r') as f:
            for line, i in enumerate(f):
                # print({f" Nr. {num}: line: {i}"})
                if line == 2:
                    s += i
                    break

        for num, i in enumerate(s):
            # here better code implementation?
            if i == ',':
                sample_name = s[num + 1:(len(s) - 1)]  # get rid of new line
                break
        return sample_name

    def return_iter(self):
        # this yields you data and a key -> sample name
        for key in self._data.keys():
            yield self._data[key], key

    def return_data(self):
        return self._data

    def return_axes(self):
        return self._axes[0]

    def __repr__(self):
        print(self._axes)
        for k, v in self._data.items():
            print(k)
            print(v)
            print(type(v))


class Plotter:
    def __init__(self, fig_size=(8, 8)):
        self.fig_size = fig_size
        self.grid_spec = None
        self.rows = 1
        self.cols = 1
        self.zoom = {}
        self.extent = None

    def plot_graph(self):
        raise NotImplementedError

    # function that plots heatmaps -> fig_size and grid_spec can
    # be set separately via @property
    # grid_spec derived from the number of dictionary keys in your data

    def plot_heatmap(self, data, axes, orientation, zoom, min_max_vals,
                     # zoom=None,
                     # min_max_vals=None,
                     # orientation='vertical',
                     ):
        # define number of cols and rows
        cnt = len(data)

        if orientation == 'vertical':
            if cnt == 1:
                pass
            elif cnt == 2:
                self.rows = cnt
            elif cnt > 2 and cnt % 2 == 0:
                self.rows = cnt // 2
                self.cols = self.rows // 2
            else:
                self.rows = cnt // 2
                self.cols = cnt // self.rows
                self.rows += 1

        elif orientation == 'horizontal':
            if cnt == 1:
                pass
            elif cnt == 2:
                self.cols = cnt
            elif cnt > 2 and cnt % 2 == 0:
                self.cols = cnt // 2
                self.rows = self.cols // 2
            else:
                self.cols = cnt // 2
                self.rows = self.cols - self.rows
        else:
            raise ValueError('Orientation not defined: horizontal or vertical')

        # check number of graphs, rows and cols
        print(cnt, self.rows, self.cols)

        # assign x, y
        y, x = axes

        # assign min and max values for all colours
        if min_max_vals is None:
            pass
        else:
            min_max_vals_unpacked = list(itertools.chain(*min_max_vals))
            min_val = min(min_max_vals_unpacked)
            max_val = max(min_max_vals_unpacked)
            # print(min_max_vals_unpacked)

        fig = plt.figure(figsize=self.fig_size)
        gs = fig.add_gridspec(nrows=self.rows, ncols=self.cols, hspace=0, wspace=0)
        axs = gs.subplots(sharex=True, sharey=True)

        ######
        # get plot indices right
        # original line
        for index, key in enumerate(data.keys(), 1):
            # for index, key, ax in zip(data, data.keys(), axs.flat):
            # select dataframe with key

            plt.subplot(self.rows, self.cols, index)
            d = data[key]

            # zoom window coordinates
            if zoom:
                if isinstance(zoom, tuple) or isinstance(zoom, list):
                    x1, x2, y1, y2, *rest = zoom
                    # bounding boy that the image will fill
                    # -> coincides with the axes units
                    self.extent = (x1, x2, y1, y2)

                    # translate coordinates into indices
                    # maye need to introduce more precise rounding
                    # leave last item in the list and access first element -> index
                    x1_idx = [[i, x] for i, x in enumerate(x) if x <= x1].pop()[0]
                    x2_idx = [[i, x] for i, x in enumerate(x) if x <= x2].pop()[0]

                    y1_idx = [[i, x] for i, x in enumerate(y) if x <= y1].pop()[0]
                    y2_idx = [[i, x] for i, x in enumerate(y) if x <= y2].pop()[0]

                    # slice of the DataFrame for zoom
                    d = d.iloc[y1_idx:y2_idx, x1_idx:x2_idx]
                else:
                    raise TypeError("Supplied type must be tuple or list!")
            else:
                self.extent = (x.min(), x.max(), y.min(), y.max())

            plt.imshow(d,
                       extent=self.extent,
                       interpolation='nearest',
                       aspect='auto')

            plt.title(str(key), y=0.8,
                      loc='left',
                      color='white')

            fig.text(0.5, 0.05, 'Time / s', ha='center', fontsize=16)
            fig.text(0.05, 0.45, 'Wavelength / nm', ha='center', rotation='vertical', fontsize=16)

        plt.show()


plt.close(fig='all')

# check difference 