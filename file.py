import pickle

# Reading the .pkl file
with open('dist.pkl', 'rb') as file:
    data = pickle.load(file)

# Now `data` contains the deserialized Python object
print(data)
