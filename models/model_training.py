import configparser, json, os, random
import tensorflow as tf
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np
from keras import optimizers
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.callbacks import CSVLogger
from keras.callbacks import ReduceLROnPlateau
from model_builder import ModelBuilder
from data_generator import DataGenerator
from sklearn.metrics import confusion_matrix

config = configparser.ConfigParser()
config.read('training_config.ini')
config.sections()

callbacks = []
if json.loads(config['DEFAULT']['use_csv_logger']):
    csv_logger = CSVLogger('testlog.csv', append=True, separator=';')
    callbacks.append(csv_logger)

if json.loads(config['DEFAULT']['use_model_checkpoint']):
    mode    = config['model-checkpoint']['mode']
    monitor = config['model-checkpoint']['monitor']
    sbo     = config['model-checkpoint']['save_best_only']
    file_p  = config['model-checkpoint']['file_path']
    mcp_save = ModelCheckpoint(file_p, save_best_only=sbo, monitor=monitor, mode=mode)
    callbacks.append(mcp_save)

if json.loads(config['DEFAULT']['use_early_stopping']):
    mode     = config['early-stopping']['mode']
    monitor  = config['early-stopping']['monitor']
    patience = json.loads(config['early-stopping']['patience'])
    early_stopping = EarlyStopping(monitor=monitor, patience=patience, mode=mode)
    callbacks.append(early_stopping)

if json.loads(config['DEFAULT']['use_reduce_lr_loss']):
    mode     = config['reduce-lr-loss']['mode']
    monitor  = config['reduce-lr-loss']['monitor']
    factor   = json.loads(config['reduce-lr-loss']['factor'])
    patience = json.loads(config['reduce-lr-loss']['patience'])
    eps      = json.loads(config['reduce-lr-loss']['epsilon'])
    reduce_lr_loss = ReduceLROnPlateau(monitor=monitor, factor=factor, patience=patience, epsilon=eps, mode=mode)
    callbacks.append(reduce_lr_loss)

# Default configdata
train_data_dir = config['DEFAULT']['train_data']
test_data_dir  = config['DEFAULT']['test_data']
classes        = json.loads(config['DEFAULT']['classes'])

# Model-parameters configdata TODO - Maybe change the val-range implementation
curr_model  = config['model-parameters']['model']
data_shape  = json.loads(config['model-parameters']['input_shape'])
n_channels  = json.loads(config['model-parameters']['n_channels'])
input_shape = tuple(data_shape + [n_channels])

#Optimizer-hyperparameters configdata
optimizer  = config['optimizer-hyperparameters']['optimizer']
loss       = config['optimizer-hyperparameters']['loss']
lr         = json.loads(config['optimizer-hyperparameters']['learning_rate'])

batch_size = json.loads(config['optimizer-hyperparameters']['batch_size'])
epochs     = json.loads(config['optimizer-hyperparameters']['epochs'])
steps      = json.loads(config['optimizer-hyperparameters']['steps_per_epoch'])
metrics    = json.loads(config['optimizer-hyperparameters']['metrics'])

model = ModelBuilder(curr_model, classes, input_shape=input_shape)

'Load pre-trained weights if wanted'
if json.loads(config['DEFAULT']['use_load_weights']):
    weight_folder = config['load-weights']['weights_folder']
    weights       = config['load-weights']['weights']
    model.load_weights(os.path.join(weight_folder, weights))

train_data = os.listdir(train_data_dir)
data_len   = len(train_data)

random.shuffle(train_data)

val_range  = json.loads(config['model-parameters']['val_range'])
train_data = train_data[int(data_len * val_range) + 1:]
val_data   = train_data[:int(data_len * val_range)]

train_datagen = DataGenerator(train_data_dir, train_data, classes, 
                              n_channels=n_channels, dim=data_shape, 
                              batch_size=batch_size, rescale=255)

val_datagen = DataGenerator(train_data_dir, val_data, classes,
                            n_channels=n_channels, dim=data_shape, 
                            batch_size=batch_size, rescale=255)

model.compile_model(optimizer=optimizer, 
                    loss=loss, 
                    metrics=metrics, 
                    learning_rate=lr)

history = model.fit_model(
          train_gen=train_datagen,
          val_gen=val_datagen,
          steps_per_epoch=steps, 
          val_steps_per_epoch=steps,
          epochs=epochs,
          callbacks=callbacks)