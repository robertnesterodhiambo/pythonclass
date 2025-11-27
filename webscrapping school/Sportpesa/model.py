import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, RepeatVector, TimeDistributed
from tensorflow.keras.utils import to_categorical

# ==========================================
# LOAD CSV
# ==========================================
df = pd.read_csv("jackpot_results.csv")
df["Picks"] = df["Picks"].astype(str)
df["SeqList"] = df["Picks"].apply(lambda x: list(x))

# Flatten all characters for label encoding
all_symbols = [c for seq in df["SeqList"] for c in seq]

# Encode 1→0, X→1, 2→2
encoder = LabelEncoder()
encoder.fit(all_symbols)

encoded_sequences = [encoder.transform(seq) for seq in df["SeqList"]]
encoded_sequences = np.array(encoded_sequences)

# ==========================================
# CREATE SUPERVISED DATA (Seq → Next Seq)
# ==========================================
X = []
Y = []

for i in range(len(encoded_sequences) - 1):
    X.append(encoded_sequences[i])      # seq(t)
    Y.append(encoded_sequences[i + 1])  # seq(t+1)

X = np.array(X)
Y = np.array(Y)

# Reshape for LSTM: (samples, timesteps, features)
X = X.reshape(X.shape[0], 17, 1)
Y = Y.reshape(Y.shape[0], 17, 1)

# One-hot encode Y for seq-to-seq classification
Y_cat = to_categorical(Y, num_classes=3)

# ==========================================
# TRAIN / TEST SPLIT
# last one is test
# ==========================================
train_size = len(X) - 1
X_train = X[:train_size]
Y_train = Y_cat[:train_size]

X_test = X[train_size:]
Y_test = Y_cat[train_size:]

# ==========================================
# BUILD SEQ2SEQ MODEL (ENCODER → DECODER LSTM)
# ==========================================
model = Sequential()
model.add(LSTM(64, input_shape=(17, 1)))
model.add(RepeatVector(17))                # repeat output 17 times
model.add(LSTM(64, return_sequences=True))
model.add(TimeDistributed(Dense(3, activation="softmax")))

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

print("TRAINING MODEL...")
model.fit(X_train, Y_train, epochs=150, verbose=1)

# ==========================================
# TEST ACCURACY
# ==========================================
loss, acc = model.evaluate(X_test, Y_test, verbose=0)
print(f"\nTest Accuracy: {acc*100:.2f}%")

# ==========================================
# PREDICT NEXT 17-PICK COMBINATION
# ==========================================
last_seq = encoded_sequences[-1].reshape(1, 17, 1)
prediction = model.predict(last_seq, verbose=0)

# Convert probabilities → class index
prediction_encoded = np.argmax(prediction, axis=2).flatten()

# Decode back to 1 / X / 2
predicted_seq = encoder.inverse_transform(prediction_encoded)
predicted_string = "".join(predicted_seq)

print("\n==============================")
print("  NEXT 17-PICK PREDICTION")
print("==============================")
print(predicted_string)

