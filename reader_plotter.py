import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import itertools
import pathlib
import gc

class DataFormatter:
    def format_pl(self, data, axes, **kwargs):
        # no recursive behavior -> think about it later

        if isinstance(data, dict):
            for key, frame in data.items():
                if isinstance(frame, pd.DataFrame):
                    wavelength = frame[0][1:]
                    del frame[0]

                    wv = wavelength.to_numpy()
                    _wv = [float(i) for i in wv]

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

                    # clean-up
                    del frame
                    del wv
                    del _wv
                    del np_array
                    del wavelength
                    del time
                    gc.collect() # that makes difference? runtime?

                else:
                    raise TypeError(f"Supplied type not DataFrame, supplied: {type(data)}")
        else:
            raise TypeError(f"Wrong type supplied -> dict, supplied: {type(data)}")
        return data, axes

    # 28.11.2023
    # data preparation for dat files
    def format_dat(self, data, flip=False, time=None):
        if isinstance(data, Reader):
            if hasattr(data, '_data') and hasattr(data, '_time_data'):
                for key, dataframe in data.__dict__['_data'].items():
                    row, col = dataframe.shape
                    print(f'row: {row} \ncol: {col}\n')

                    # time Series
                    if key in data.__dict__['_time_data']:
                        _time_data = data.__dict__['_time_data'][key]
                        time_stamps = _time_data.iloc[3:6, 2]
                        time = pd.Series(time_stamps, dtype='float')

                    wavelength = dataframe.iloc[:, 0]
                    del dataframe[0]

                    # new wavelength index
                    w_index = pd.Series(wavelength, name='wavelength', dtype='float')

                    # time stamps from measurement data
                    t_min, t_max, t_delta = time
                    print(t_min, t_max, t_delta)
                    new_delta = (t_max - t_min) / (col - 1) # minus the first columns with wavelength vals
                    new_delta = round(new_delta, 10)
                    print('calculated: ', new_delta)

                    # calculate each time
                    new_time = t_min
                    cnt = 0
                    time_lst = []
                    #while t_min + new_delta <= t_max + new_delta:
                    #while new_time + new_delta <= t_max + new_delta:
                    while cnt != col - 1:
                        time_lst.append(round(new_time, 4))
                        cnt += 1
                        new_time += new_delta

                    # new time index
                    t_index = pd.Series(time_lst, name='time', dtype='float')
                    #t_index.sort_values(ascending=False)

                    # DataFrame to array
                    np_array = dataframe.to_numpy()

                    # custom array rotation if needed
                    _data = pd.DataFrame(np_array, index=w_index, columns=t_index)

                    if flip:
                        np_array = np.rot90(np_array)
                        _data = pd.DataFrame(np_array, index=t_index, columns=w_index)

                    # create new DataFrame
                    data.__dict__['_data'][key] = _data

                #print(data)

                # clean-up
                del dataframe #??? needed here?
                del _data
                del _time_data
                del np_array
                del t_index
                del w_index
                gc.collect()
        else:
            raise TypeError(f"Wrong type supplied -> dict, supplied: {type(data)}")
        return data.__dict__['_data']


class Reader(DataFormatter):
    def __init__(self, min_val=None, max_val=None):
        self._data = {}
        self._time_data = {}
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


        if isinstance(file, str) or isinstance(file, pathlib.PosixPath):
            sample_name = file.split(sep='/')[-1]  # sample name
            _file = pd.read_csv(file, skiprows=11, sep='\s+', header=None, skipfooter=1, engine='python')
            self._data[sample_name] = _file

            _time_data = pd.read_csv(file, sep='\s+', low_memory=False, nrows=6, header=None)
            self._time_data[sample_name] = _time_data

        else:
            raise TypeError("Not a path")
        return self

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

    def _prepare_dat(self, data, idxs, rows, *args, **kwargs):
        x1_idx, x2_idx, y1_idx, y2_idx, = idxs
        data = data.iloc[(rows - y2_idx):(rows - y1_idx), x1_idx:x2_idx]
        return data

    def _prepare_csv(self, data, idxs, *args, **kwargs):
        x1_idx, x2_idx, y1_idx, y2_idx, = idxs
        data = data.iloc[y1_idx:y2_idx, x1_idx:x2_idx]
        return data


    # function that plots heatmaps -> fig_size and grid_spec can
    # be set separately via @property
    # grid_spec derived from the number of dictionary keys in your data

    def plot_heatmap(self, data, axes, orientation, format, zoom, min_max_vals=None,
                     x=0,
                     y=0,
                     # zoom=None,
                     # min_max_vals=None,
                     # orientation='vertical',
                     ):
        # define number of cols and rows
        if isinstance(data, dict):
            cnt = len(data)
            print(cnt)

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

            # assign x, y axs
            if isinstance(axes, dict) and not None: # x and y cant be = 0!
                for key in axes.keys():
                    y, x = axes[key]
            else:
                pass

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

            if zoom:
                for index, key in enumerate(data.keys(), 1):
                    d = data[key]

                    if isinstance(zoom, tuple) or isinstance(zoom, list):
                        ### what if data is flipped? ### -> check condition

                        x1, x2, y1, y2, *rest = zoom
                        # bounding box that the image will fill
                        # -> coincides with the axes units
                        self.extent = (x1, x2, y1, y2)
                        print(x1, x2)
                        print(y1, y2)

                        # assign axis from DataFrame
                        y = [i for i in d.index]
                        x = [i for i in d.columns]
                        rows, cols = d.shape

                        # translate coordinates into indices
                        # maye need to introduce more precise rounding
                        # leave last item in the list and access first element -> index

                        x1_idx = [[i, x] for i, x in enumerate(x) if x <= x1]
                        x2_idx = [[i, x] for i, x in enumerate(x) if x <= x2]

                        y1_idx = [[i, x] for i, x in enumerate(y) if x <= y1]
                        y2_idx = [[i, x] for i, x in enumerate(y) if x <= y2]

                        # check if there are empty lists
                        # a more efficient way of writing the same thing below?
                        if x1_idx:
                            x1_idx = x1_idx.pop()[0]
                        else:
                            x1_idx = 0

                        if x2_idx:
                            x2_idx = x2_idx.pop()[0]
                        else:
                            x1_idx = 0

                        if y1_idx:
                            y1_idx = y1_idx.pop()[0]
                        else:
                            y1_idx = 0

                        if y2_idx:
                            y2_idx = y2_idx.pop()[0]
                        else:
                            y2_idx = 0

                        idxs = [x1_idx, x2_idx, y1_idx, y2_idx]
                        # print(x1_idx, x2_idx)
                        # print("y1: ", y1_idx, "y2: ", y2_idx)
                        # print('lower limit', row - y1_idx)
                        #print(f'indices: y2 = {y2_idx}, y1 = {row - y1_idx} \n')

                        # slice of the DataFrame for zoom

                        if format == 'dat':
                            d = self._prepare_dat(d, idxs, rows)
                            data[key] = d
                        elif format == 'csv':
                            d = self._prepare_csv(d, idxs)
                            data[key] = d
                        else:
                            pass

            #else:
                #self.extent = [x.iloc[0], x.iloc[-1], y.iloc[0], x.iloc[-1] ]


            ######
            # get plot indices right
            # original line
            for index, key in enumerate(data.keys(), 1):
                # for index, key, ax in zip(data, data.keys(), axs.flat):
                # select dataframe with key

                plt.subplot(self.rows, self.cols, index)
                d = data[key]

                #print(d.index)
                #print(d)

                # extent indiciduallly or for all graphs

                self.extent = (d.columns[0], d.columns[-1], d.index[0], d.index[-1])


                # zoom window coordinates

                plt.imshow(d,
                           extent=self.extent,
                           interpolation='nearest',
                           origin='upper',
                           aspect='auto')

                plt.title(str(key), y=0.8,
                          loc='left',
                          color='white')

                #fig.text(0.5, 0.05, 'Time / s', ha='center', fontsize=16)
                fig.text(0.05, 0.45, 'Time / s', ha='center', rotation='vertical', fontsize=16)
                fig.text(0.5, 0.05, 'Wavelength / nm', ha='center', rotation='horizontal', fontsize=16)
                plt.colorbar()
            plt.show()
        else:
            raise TypeError(f"Wrong type supplied -> dict, supplied: {type(data)}")

plt.close(fig='all')

# check difference 