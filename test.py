import numpy as np

# Input values for different time periods
value1 = [-0.06, 0.10, -0.04, 0.03, -0.05, -0.02, -0.05, 0.03, 0.09, -0.01]
value2 = [0.00, 0.03, -0.09, 0.07, 0.06, 0.01, -0.06, 0.03, 0.06, -0.10]
value3 = [-0.03, -0.09, 0.06, -0.03, 0.09, -0.07, -0.05, -0.05, -0.04, 0.05]
value4 = [0.03, 0.01, -0.07, 0.00, -0.02, -0.11, 0.02, -0.01, 0.05, 0.05]

# 2SE values corresponding to the measurements
se1 = [0.10, 0.10, 0.11, 0.11, 0.11, 0.11, 0.10, 0.11, 0.09, 0.10]
se2 = [0.12, 0.09, 0.09, 0.09, 0.09, 0.09, 0.08, 0.08, 0.07, 0.09]
se3 = [0.08, 0.12, 0.08, 0.07, 0.09, 0.08, 0.08, 0.06, 0.08, 0.07]
se4 = [0.09, 0.09, 0.10, 0.09, 0.08, 0.10, 0.09, 0.09, 0.09, 0.08]

# Convert 2SE to 1SE by dividing each value by 2
se1 = np.array(se1) / 2
se2 = np.array(se2) / 2
se3 = np.array(se3) / 2
se4 = np.array(se4) / 2

# Combine all values and SE values
all_values = np.array(value1 + value2 + value3 + value4)
all_se = np.array(list(se1) + list(se2) + list(se3) + list(se4))

# Calculate mean of all values
mean_value = np.mean(all_values)

# Calculate H-index for each value
h_index = np.abs(all_values - mean_value) / all_se

# Output H-index results
for i, h in enumerate(h_index):
    print(f"H-index for value {i+1}: {h:.4f}")

# Calculate overall mean H-index
mean_h_index = np.mean(h_index)
print(f"\nOverall mean H-index: {mean_h_index:.4f}")