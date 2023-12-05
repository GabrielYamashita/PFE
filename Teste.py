
import numpy as np
import pandas as pd
from scipy.optimize import minimize

np.set_printoptions(formatter={'float': '{:0.6f}'.format})


data = {
    'param_min': [-2, -2, -2, 0, -3],
    'param_max': [2, 2, 0.1, 5, 2],
    'application': ['app1', 'app2', 'app3', 'app4', 'app5']
}

data = pd.DataFrame(data)
data.set_index('application', inplace=True)  # Set 'application' as the index


# Define the Rosenbrock function
def rosenbrock(x):
    return sum(100.0 * (x[1:] - x[:-1]**2)**2 + (1 - x[:-1])**2)

# Define individual ranges for each parameter
param_ranges = [(-2, 2), (-2, 2), (-1, 0.2), (0, 5), (-3, 2)]

def optimize_fixed_parameters(num_fixed_params):
    # Generate an initial guess within the specified ranges
    initial_guess = np.array([0.1, 0.2, 0.95, 0.5, 0.4])
    print(initial_guess)
    
    # Fix the specified number of parameters
    for i in num_fixed_params:
        param_ranges[i] = (initial_guess[i], initial_guess[i])
    
    # Use minimize to find the minimum within the modified ranges
    result = minimize(rosenbrock, initial_guess, bounds=param_ranges)
    
    return result

# Specify the number of parameters to fix
values_to_find = ['app4']
indices = [data.index.get_loc(name) for name in values_to_find]
print(indices)
num_fixed_params = indices



# Perform optimization with the specified number of fixed parameters
result = optimize_fixed_parameters(num_fixed_params)

# Print the result
print(result.x)
# print(result.fun)


