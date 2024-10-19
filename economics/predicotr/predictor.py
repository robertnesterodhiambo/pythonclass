import os
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

# Step 1: Load CSV Data
file_path = '/root/Stock/Models/sample.csv'
df = pd.read_csv(file_path)

# Step 2: Get the list of available models from the ~/Models folder
models_dir = '/root/Stock/Models'
available_models = [f.split('_')[-1].replace('.h5', '') for f in os.listdir(models_dir) if f.startswith('lstm_model')]

# Function to predict next open price based on available models
def predict_next_open(symbol):
    # Check if the symbol has a corresponding model
    if symbol not in available_models:
        print(f"No model available for symbol: {symbol}")
        return

    # Filter data for the specific symbol
    symbol_data = df[df['Symbol'] == symbol]

    if symbol_data.empty:
        print(f"No data available for symbol: {symbol}")
        return

    # Step 3: Preprocess Data (Use columns: Open, High, Low, Close, Volume)
    data = symbol_data[['Open', 'High', 'Low', 'Close', 'Volume']].values

    # Normalize data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    # Prepare the data for LSTM (e.g., last 60 days)
    sequence_length = 60
    if len(scaled_data) < sequence_length:
        print(f"Not enough data to predict for symbol: {symbol}")
        return

    x_input = []
    for i in range(sequence_length, len(scaled_data)):
        x_input.append(scaled_data[i-sequence_length:i])

    # Convert to numpy array and reshape for LSTM (samples, time steps, features)
    x_input = np.array(x_input)

    # Step 4: Load the LSTM Model for the given symbol
    model_path = f'{models_dir}/lstm_model_{symbol}.h5'
    model = load_model(model_path)
    print(f"Loaded model for {symbol}")

    # Step 5: Predict the next open price
    # Use the most recent sequence of data
    last_sequence = x_input[-1].reshape(1, sequence_length, 5)  # Reshape for prediction
    predicted_open_scaled = model.predict(last_sequence)

    # Step 6: Inverse scaling to get the actual price
    predicted_open = scaler.inverse_transform([predicted_open_scaled[0]])[0][0]

    # Display predicted next open price
    print(f"Predicted next open price for {symbol}: {predicted_open}")
    return predicted_open

# List of available symbols that the user can predict for
print("Available symbols for prediction:", available_models)

# Example usage: Predict next open price for a specific symbol
symbol_to_predict = 'ADBE'  # Change this to any available symbol from the list
predict_next_open(symbol_to_predict)
