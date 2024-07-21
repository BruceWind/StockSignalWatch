import numpy as np

def calculate_mean(data):
  """
  ignore value: NaN
  """
  valid_data = np.array(data)[~np.isnan(data)]
  return np.mean(valid_data)

def calculate_median(data):
  """
  ignore value: NaN
  """
  valid_data = np.array(data)[~np.isnan(data)]
  return np.median(valid_data)
def calculate_max(data):
  """
  ignore value: NaN
  """
  valid_data = np.array(data)[~np.isnan(data)]
  return np.max(valid_data)

def calculate_min(data):
  """
  to ignore value: NaN
  """
  valid_data = np.array(data)[~np.isnan(data)]
  return np.min(valid_data)
