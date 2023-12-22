import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#pl30 = '/Users/alexander/Desktop/HZB_UV_vis_Laytec/reflectance_data/2023-11-9/PL_30.dat'
pl30 = '/Users/alexander/Desktop/HZB_UV_vis_Laytec/reflectance_data/2023-12-14/14/dat files/AT-55.dat'


# DataFrame read
df_pl30 = pd.read_csv(pl30, skiprows=11, sep='\s+', header=None, skipfooter=1, engine='python')

print(df_pl30)
#print(df_pl30.iloc[:, 0]) # col selection
#print(len(df_pl30.iloc[0])) # length od the row

row, col = df_pl30.shape # number of data before deleting first row
print(f'row: {row} \ncol: {col}\n')

# read time stamps -> begin, end, delta
# read wavelength
df_pl30_time = pd.read_csv(pl30, sep='\s+', low_memory=False, nrows=6, header=None)
time_stamps = df_pl30_time.iloc[3:6, 2]
wavelength = df_pl30.iloc[:, 0]
del df_pl30[0]
#print('Wavelength:\n', wavelength)

# new time Series
time = pd.Series(time_stamps, dtype='float')
# new Wavelength Series
w_index = pd.Series(wavelength, name='wavelength', dtype='float')
#print(time)
#print(w_index)

t_min, t_max, t_delta = time
new_delta = t_max / (col - 1)
print(f'new delta: {new_delta}\n')

#print(isinstance(t_min, str))
#print(t_min, t_max, t_delta)

#cols_values = t_max // t_delta
cols_values = t_max // new_delta
cols_values_1 = t_max / t_min

print('with new delta: ', cols_values)
print(cols_values_1)

cnt = 1
time_lst = []
while t_min + new_delta <= t_max + new_delta:
    time_lst.append(round(t_min, 4))
    cnt += 1
    t_min += new_delta

t_index = pd.Series(time_lst, name='time', dtype='float')
#print('len:', len(t_index), '\n')
#print(t_index.min())
#print(t_index.max())

# convert DF to an array
# rotate 90 deg
array = df_pl30.to_numpy()
#array = np.rot90(array)

# create new DF
#data = pd.DataFrame(array, columns=w_index, index=t_index) # with rotation
data = pd.DataFrame(array, index=w_index, columns=t_index)
print(data)
#print(data.index)
#print(data.columns)

def plot(data):
    plt.figure(figsize=(5, 5), dpi=100)
    plt.imshow(data,
               #extent=(w_index.min(), w_index.max(), t_index.min(), t_index.max()),
               interpolation='nearest',
               aspect='auto')

    plt.show()

# spectra from at defined time
def time_stamp():
    interference_pat_wv1 = data.iloc[700]
    interference_pat_wv2 = data.iloc[50]
    fig, axs = plt.subplots(2)
    axs[0].plot(interference_pat_wv1)
    axs[1].plot(interference_pat_wv2)
    plt.show()

plot(data)
time_stamp()