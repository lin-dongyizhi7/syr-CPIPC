import os
import math
import numpy as np
import datetime as dt
import tensorflow as tf
from numpy import newaxis
from core.utils import Timer
# from keras.layers import Dense, Activation, Dropout, LSTM
# from keras.models import Sequential, load_model
# from keras.callbacks import EarlyStopping, ModelCheckpoint
# from tensorflow.keras import Model
# from tensorflow.keras.layers import LSTM,Dropout,Activation,Dense
# from tensorflow.keras import Sequential
# from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow import keras
from kerastuner.tuners import RandomSearch

class Model():
	"""LSTM 模型"""

	def __init__(self):
		self.model = tf.keras.models.Sequential()

	def load_model(self, filepath):
		print('[Model] Loading model from file %s' % filepath)
		self.model =tf.keras.models.load_model(filepath)

	def build_model(self, configs):
		timer = Timer()
		timer.start()

		for layer in configs['model']['layers']:
			neurons = layer['neurons'] if 'neurons' in layer else None
			dropout_rate = layer['rate'] if 'rate' in layer else None
			activation = layer['activation'] if 'activation' in layer else None
			return_seq = layer['return_seq'] if 'return_seq' in layer else None
			input_timesteps = layer['input_timesteps'] if 'input_timesteps' in layer else None
			input_dim = layer['input_dim'] if 'input_dim' in layer else None

			if layer['type'] == 'dense':
				self.model.add(tf.keras.layers.Dense(neurons, activation=activation))
			if layer['type'] == 'lstm':
				self.model.add(tf.keras.layers.LSTM(neurons, input_shape=(input_timesteps, input_dim), return_sequences=return_seq))
			if layer['type'] == 'dropout':
				self.model.add(tf.keras.layers.Dropout(dropout_rate))
			if layer['type'] == 'GRU':
				self.model.add(tf.keras.layers.GRU(neurons, input_shape=(input_timesteps, input_dim), return_sequences=return_seq))

		# self.model.compile(loss=configs['model']['loss'], optimizer=configs['model']['optimizer'])
		self.model.compile(keras.optimizers.Adam(0.0001),loss=configs['model']['loss'])

		print('[Model] Model Compiled')
		timer.stop()
		
		return self.model

	def train(self, x, y, epochs, batch_size, save_dir, validation_split):#修改+data
		timer = Timer()
		timer.start()
		print('[Model] Training Started')
		print('[Model] %s epochs, %s batch size' % (epochs, batch_size))
		
		save_fname = os.path.join(save_dir, '%s-e%s.h5' % (dt.datetime.now().strftime('%d%m%Y-%H%M%S'), str(epochs)))
		callbacks = [
			tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=6),
			tf.keras.callbacks.ModelCheckpoint(filepath=save_fname, monitor='val_loss', save_best_only=True)
		]
		self.model.fit(
			x,
			y,
			epochs=epochs,
			batch_size=batch_size,
			callbacks=callbacks,
			validation_split=validation_split#修改，+
		)
		self.model.save(save_fname)

		print('[Model] Training Completed. Model saved as %s' % save_fname)
		timer.stop()

	def train_generator(self, data_gen, epochs, batch_size, steps_per_epoch, save_dir):
		timer = Timer()
		timer.start()
		print('[Model] Training Started')
		print('[Model] %s epochs, %s batch size, %s batches per epoch' % (epochs, batch_size, steps_per_epoch))
		
		save_fname = os.path.join(save_dir, '%s-e%s.h5' % (dt.datetime.now().strftime('%d%m%Y-%H%M%S'), str(epochs)))
		callbacks = [
			tf.keras.callbacks.ModelCheckpoint(filepath=save_fname, monitor='loss', save_best_only=True)
		]
		self.model.fit_generator(
			data_gen,
			steps_per_epoch=steps_per_epoch,
			epochs=epochs,
			callbacks=callbacks,
			workers=1
		)
		
		print('[Model] Training Completed. Model saved as %s' % save_fname)
		timer.stop()

	def predict_point_by_point(self, data,debug=False):
		if debug == False:
			print('[Model] Predicting Point-by-Point...')
			predicted = self.model.predict(data)
			predicted = np.reshape(predicted, (predicted.size,))
		else:
			print('[Model] Predicting Point-by-Point...')
			print (np.array(data).shape)
			predicted = self.model.predict(data)
			print (np.array(predicted).shape)
			print(predicted)
			predicted = np.reshape(predicted, (predicted.size,))
			print (np.array(predicted).shape)
			print(predicted)
		return predicted

	def predict_sequence_full(self, data, window_size):
		print('[Model] Predicting Sequences Full...')
		curr_frame = data[0]
		predicted = []
		for i in range(len(data)):
			predicted.append(self.model.predict(curr_frame[newaxis,:,:])[0,0])
			curr_frame = curr_frame[1:]
			curr_frame = np.insert(curr_frame, [window_size-2], predicted[-1], axis=0)
		return predicted

	def predict_sequences_multiple(self, data, window_size, prediction_len, debug=False):
		if debug == False:
			print('[Model] Predicting Sequences Multiple...')
			prediction_seqs = []
			for i in range(int(len(data) / prediction_len)):
				curr_frame = data[i * prediction_len]
				predicted = []
				for j in range(prediction_len):
					predicted.append(self.model.predict(curr_frame[newaxis, :, :])[0, 0])
					curr_frame = curr_frame[1:]
					curr_frame = np.insert(curr_frame, [window_size - 2], predicted[-1], axis=0)
				prediction_seqs.append(predicted)
			return np.mean(np.array(prediction_seqs), axis=0)
			# return prediction_seqs
		else:
			print('[Model] Predicting Sequences Multiple...')
			prediction_seqs = []
			for i in range(int(len(data) / prediction_len)):
				print(data.shape)
				curr_frame = data[i * prediction_len]
				print(curr_frame)
				predicted = []
				for j in range(prediction_len):
					predict_result = self.model.predict(curr_frame[newaxis, :, :])
					print(predict_result)
					final_result = predict_result[0, 0]
					predicted.append(final_result)
					curr_frame = curr_frame[1:]
					print(curr_frame)
					curr_frame = np.insert(curr_frame, [window_size - 2], predicted[-1], axis=0)
					print(curr_frame)
				prediction_seqs.append(predicted)

	def predict_next(self, data, prediction_len, debug=False):
		if debug == False:
			print('[Model] Predicting Next...')
			return self.model.predict(data)[0:prediction_len]
		else:
			print('[Model] Predicting Next...')
			print(self.model.predict(data)[0:prediction_len])

