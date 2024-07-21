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

def find_third_largest(arr):
    """Find the third largest number in the array, ignoring NaN values."""
    # Convert input to a NumPy array
    arr = np.array(arr)
    
    # Remove NaN values
    arr = arr[~np.isnan(arr)]
    
    # Check the length of the array
    if len(arr) == 0:
        return None  # No valid numbers
    elif len(arr) <= 3:
        return np.max(arr)  # Return the maximum if 1-3 numbers
    
    # Get unique values and sort in descending order
    unique_arr = np.unique(arr)
    sorted_arr = np.sort(unique_arr)[::-1]
    
    # Return the third largest number
    return sorted_arr[2]

def find_largest(arr):
    """Find the largest number in the array, ignoring NaN values."""
    # Convert input to a NumPy array
    arr = np.array(arr)
    
    # Remove NaN values
    arr = arr[~np.isnan(arr)]
    
    # Check the length of the array
    if len(arr) == 0:
        return None  # No valid numbers
    
    # Return the largest number
    return np.max(arr)


def find_third_smallest(arr):
    """Find the third smallest number in the array, ignoring NaN values."""
    # Convert input to a NumPy array
    arr = np.array(arr)
    
    # Remove NaN values
    arr = arr[~np.isnan(arr)]
    
    # Check the length of the array
    if len(arr) == 0:
        return None  # No valid numbers
    elif len(arr) <= 3:
        return np.min(arr)  # Return the minimum if 1-3 numbers
    
    # Sort the array
    sorted_arr = np.sort(arr)
    
    # Return the third smallest number
    return sorted_arr[2]

def find_smallest(arr):
    """Find the third smallest number in the array, ignoring NaN values."""
    # Convert input to a NumPy array
    arr = np.array(arr)
    
    # Remove NaN values
    arr = arr[~np.isnan(arr)]
    
    # Check the length of the array
    if len(arr) == 0:
        return None  # No valid numbers
    
    # Return the third smallest number
    return np.min(arr) 
