import pandas as pd
import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt

def create_model():
  """Create a sequential model with multiple hidden layers."""
  # Most simple tf.keras models are sequential.
  model = tf.keras.models.Sequential()

  model.add(tf.keras.layers.Dense(100, activation='relu', input_dim=45, kernel_regularizer=tf.keras.regularizers.l2(l=0.05)))
  model.add(tf.keras.layers.Dense(50, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(l=0.1)))
  model.add(tf.keras.layers.Dense(3, activation='softmax'))

  # Construct the layers into a model that TensorFlow can execute.
  model.compile(optimizer='adam', 
              loss='categorical_crossentropy', 
              metrics=['accuracy'])

  return model           


def train_model(model, features, label, epochs, batch_size):
  """Feed a dataset into the model in order to train it."""

  # Split the dataset into features and label.
  history = model.fit(x=features, y=label, batch_size=batch_size, epochs=epochs, shuffle=True)

  # Get details that will be useful for plotting the loss curve.
  epochs = history.epoch
  hist = pd.DataFrame(history.history)
  loss = hist["loss"]

  return epochs, loss

def convert_to_one_hot(options, data):
  """Encode each element in a data array as a one-hot vector."""
  vec_options = tf.keras.utils.to_categorical(list(range(0,len(options))), num_classes=len(options))

  matrix = []
  for n in data:
      matrix.append(vec_options[options.index(n)])

  return np.array([xi for xi in matrix])

def normalize(df):
  """
  Normalize the values in a dataframe using max/min normalization. This will map every
  data point to a value between 0 and 1. Based on an answer found in this StackOverflow
  thread: 
  https://stackoverflow.com/questions/26414913/normalize-columns-of-pandas-data-frame
  """
  result = df.copy()
  for feature_name in df.columns:
      max_value = df[feature_name].max()
      min_value = df[feature_name].min()
      result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
  return result

def reset(df):
  """Reset the indices in a dataframe"""
  df = df.reset_index()
  return df.drop(columns=['index'])

def plot_the_loss_curve(epochs, mse):
  """Plot a curve of loss vs. epoch."""

  plt.figure()
  plt.xlabel("Epoch")
  plt.ylabel("Loss")

  plt.plot(epochs, mse, label="Loss")
  plt.legend()
  plt.ylim([mse.min()*0.95, mse.max() * 1.03])
  plt.show()  