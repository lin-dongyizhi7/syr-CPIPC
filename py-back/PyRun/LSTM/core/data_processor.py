import math
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler  # 标准化工具

class DataLoader():

    def __init__(self, filename, data, split):
        # if filename:
        #     dataframe = pd.read_csv(filename)
        # else:
        #     dataframe = pd.DataFrame(data)
        dataframe = pd.read_csv(filename) if filename else pd.DataFrame(data)
        i_split = int(len(dataframe) * split)
        cols = dataframe.columns.tolist()[1:]
        print(cols)
        self.data_full = dataframe.get(cols).values
        self.data_train = dataframe.get(cols).values[:i_split]
        self.data_test = dataframe.get(cols).values[i_split:]
        self.len_train = len(self.data_train)
        self.len_test = len(self.data_test)
        self.len_full = len(self.data_full)
        self.in_cols = cols
        self.len_train_windows = None

    def get_test_data(self, seq_len, normalise):

        data_windows = []
        for i in range(self.len_test - seq_len):
            data_windows.append(self.data_test[i:i+seq_len])

        data_window = np.array(data_windows).astype(float)
        data_windows = self.normalise_windows(data_window, single_window=False) if normalise else data_window

        x = data_windows[:, :-1]
        y = data_windows[:, -1, [0]]
        return x,y

    def get_train_data(self, seq_len, normalise):

        data_x = []
        data_y = []
        for i in range(self.len_train - seq_len):
            x, y = self._next_window(i, seq_len, normalise)
            data_x.append(x)
            data_y.append(y)
        return np.array(data_x), np.array(data_y)

    def get_full_data(self, seq_len, normalise):#修改+

        data_x = []
        data_y = []
        for i in range(self.len_full - seq_len):
            x, y = self._next_window_full(i, seq_len, normalise)
            data_x.append(x)
            data_y.append(y)
        return np.array(data_x), np.array(data_y)

    def generate_train_batch(self, seq_len, batch_size, normalise):
        
        i = 0
        while i < (self.len_train - seq_len):
            x_batch = []
            y_batch = []
            for b in range(batch_size):
                if i >= (self.len_train - seq_len):
                    # stop-condition for a smaller final batch if data doesn't divide evenly
                    yield np.array(x_batch), np.array(y_batch)
                    i = 0
                x, y = self._next_window(i, seq_len, normalise)
                x_batch.append(x)
                y_batch.append(y)
                i += 1
            yield np.array(x_batch), np.array(y_batch)

    def _next_window(self, i, seq_len, normalise):
        window0 = self.data_train[i:i+seq_len]
        window = self.normalise_windows(window0, single_window=True)[0] if normalise else window0
        x = window[:-1]
        y = window[-1, [0]]
        return x, y

    def _next_window_full(self, i, seq_len, normalise):
        window0 = self.data_full[i:i+seq_len]
        window = self.normalise_windows(window0, single_window=True)[0] if normalise else window0
        x = window[:-1]
        y = window[-1, [0]]
        return x, y

    def normalise_windows(self, window_data, single_window=False):
        normalised_data = []
        window_data = [window_data] if single_window else window_data
        for window in window_data:
            normalised_window = []
            for col_i in range(window.shape[1]):
                normalised_col = [((float(p) / float(window[0, col_i])) - 1) for p in window[:, col_i]]
                normalised_window.append(normalised_col)
            normalised_window = np.array(normalised_window).T 
            normalised_data.append(normalised_window)
        return np.array(normalised_data)