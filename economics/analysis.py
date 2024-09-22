import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split

# Load the dataset
file_path = 'sample.csv'
df = pd.read_csv(file_path)

# Function to preprocess data for a specific symbol
def preprocess_data(symbol_df):
    # Select relevant columns
    data = symbol_df[['Date', 'Close']].copy()
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    # Normalize the Close prices
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

    # Create sequences for LSTM
    x_train, y_train = [], []
    sequence_length = 60  # Use 60 days of data
    for i in range(sequence_length, len(scaled_data)):
        x_train.append(scaled_data[i-sequence_length:i, 0])
        y_train.append(scaled_data[i, 0])
    
    x_train, y_train = np.array(x_train), np.array(y_train)

    # Reshape for LSTM [samples, time steps, features]
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    
    return x_train, y_train, scaler

# Function to create the LSTM model
def create_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(1))  # Predicting the next price
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Train and predict for each symbol
unique_symbols = df['Symbol'].unique()
for symbol in unique_symbols:
    symbol_df = df[df['Symbol'] == symbol]
    
    # Preprocess the data
    x_train, y_train, scaler = preprocess_data(symbol_df)

    # Split the data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2, random_state=42)

    # Create and train the LSTM model
    model = create_lstm_model((x_train.shape[1], 1))
    model.fit(x_train, y_train, epochs=50, batch_size=32)

    # Save the model
    model.save(f'lstm_model_{symbol}.h5')
    print(f'Model saved for symbol: {symbol}')
