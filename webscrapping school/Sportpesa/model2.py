"""
jackpot_predictor.py

Reads 'jackpot_results.csv' (Date,Picks), trains a seq2seq LSTM to predict the next 17-pick combination,
evaluates, saves model, and prints predicted combination plus position-wise probabilities.

Author: (generated for you)
"""

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, RepeatVector, TimeDistributed, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.utils import to_categorical

# -----------------------------
#  CONFIG
# -----------------------------
CSV_PATH = "jackpot_results.csv"
PAST_SEQ = 20         # number of previous full-17 lines used to predict the next full-17 line
BATCH_SIZE = 32
EPOCHS = 100
MODEL_PATH = "jackpot_lstm_best.h5"
RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)

# -----------------------------
#  HELPERS: encode/decode
# -----------------------------
symbol_to_idx = {"1": 0, "X": 1, "2": 2}
idx_to_symbol = {v: k for k, v in symbol_to_idx.items()}
NUM_CLASSES = 3
SEQ_LEN = 17  # each line is 17 outcomes

def encode_sequence(seq_str):
    """Convert '11X21...' => array of integers shape (17,)"""
    return np.array([symbol_to_idx[c] for c in seq_str.strip()])

def decode_sequence(arr):
    """Convert integer array => '1X2...'"""
    return "".join(idx_to_symbol[int(x)] for x in arr)

def sample_from_probs(probs, temperature=1.0):
    """Sample an integer index from a probability vector with temperature"""
    if temperature <= 0:
        return int(np.argmax(probs))
    p = np.log(np.maximum(probs, 1e-12)) / temperature
    p = np.exp(p - np.max(p))
    p = p / p.sum()
    return int(np.random.choice(len(p), p=p))

# -----------------------------
#  LOAD & PREPARE DATA
# -----------------------------
df = pd.read_csv(CSV_PATH)

# Ensure columns exist
if "Picks" not in df.columns:
    raise ValueError("CSV must contain a 'Picks' column with 17-character strings")

# Normalize and sort by date to ensure chronological order.
# Try parsing Date; if parsing fails, assume the file is already chronological.
try:
    df["Date_parsed"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    if df["Date_parsed"].isnull().all():
        # fallback: don't sort
        print("Warning: could not parse dates; using file order as chronological.")
    else:
        df = df.sort_values("Date_parsed").reset_index(drop=True)
except Exception as e:
    print("Date parsing warning:", e)

# Keep only rows where Picks length == 17
df["Picks"] = df["Picks"].astype(str).str.strip()
df = df[df["Picks"].str.len() == SEQ_LEN].reset_index(drop=True)
N = len(df)
if N < 2:
    raise ValueError("Not enough valid rows in CSV. Need at least 2 rows of 17-length picks.")

print(f"Loaded {N} valid sequences (each length {SEQ_LEN}).")

# Build encoded array shape (N, 17)
encoded_all = np.vstack([encode_sequence(s) for s in df["Picks"].tolist()])  # shape (N,17)

# If PAST_SEQ is too large, reduce it
if PAST_SEQ >= N:
    PAST_SEQ = max(1, N - 1)
    print(f"PAST_SEQ reduced to {PAST_SEQ} (because data has only {N} rows).")

# -----------------------------
#  Create sliding-window supervised pairs
#  X: previous PAST_SEQ lines -> shape (samples, PAST_SEQ, 17)
#  Y: next line -> shape (samples, 17)
# -----------------------------
X_list, Y_list = [], []
for i in range(N - PAST_SEQ):
    X_list.append(encoded_all[i:i + PAST_SEQ])   # (PAST_SEQ, 17)
    Y_list.append(encoded_all[i + PAST_SEQ])     # (17,)

X = np.array(X_list)  # (samples, PAST_SEQ, 17)
Y = np.array(Y_list)  # (samples, 17)

print(f"Created supervised dataset: {X.shape[0]} samples, each input shape {X.shape[1:]} -> output {Y.shape[1:]}")

# Reshape inputs for LSTM: features-per-timestep = 17 (we treat each previous 17-line as one timestep with 17 features)
# So input shape is (samples, timesteps=PAST_SEQ, features=17)

# One-hot encode Y to shape (samples, 17, NUM_CLASSES)
Y_cat = np.array([to_categorical(row, num_classes=NUM_CLASSES) for row in Y])  # shape (samples, 17, 3)

# -----------------------------
#  Train / Val / Test split
# -----------------------------
# Keep chronological order when splitting (no leakage). We'll take last chunk as test, previous chunk as val.
samples = X.shape[0]
test_size = int(0.15 * samples)  # 15% test
val_size = int(0.15 * samples)   # 15% val
train_size = samples - test_size - val_size
if train_size <= 0:
    # fallback to a simpler split
    train_size = max(1, samples - 2)
    val_size = 1
    test_size = samples - train_size - val_size

X_train = X[:train_size]
Y_train = Y_cat[:train_size]
X_val = X[train_size:train_size + val_size]
Y_val = Y_cat[train_size:train_size + val_size]
X_test = X[train_size + val_size:]
Y_test = Y_cat[train_size + val_size:]

print("Split sizes -> train:", X_train.shape[0], "val:", X_val.shape[0], "test:", X_test.shape[0])

# -----------------------------
#  MODEL: Encoder (timesteps -> vector) -> RepeatVector(17) -> Decoder LSTM -> TimeDistributed(Dense(3))
# -----------------------------
from tensorflow.keras import regularizers

reg = 1e-4
drop_rate = 0.25

model = Sequential([
    LSTM(128, input_shape=(PAST_SEQ, SEQ_LEN), kernel_regularizer=regularizers.l2(reg)),
    Dropout(drop_rate),
    RepeatVector(SEQ_LEN),
    LSTM(128, return_sequences=True, kernel_regularizer=regularizers.l2(reg)),
    Dropout(drop_rate),
    TimeDistributed(Dense(NUM_CLASSES, activation="softmax"))
])

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
model.summary()

# -----------------------------
#  CALLBACKS
# -----------------------------
callbacks = [
    EarlyStopping(monitor="val_loss", patience=12, restore_best_weights=True, verbose=1),
    ModelCheckpoint(MODEL_PATH, monitor="val_loss", save_best_only=True, verbose=1)
]

# -----------------------------
#  TRAIN
# -----------------------------
history = model.fit(
    X_train, Y_train,
    validation_data=(X_val, Y_val),
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    callbacks=callbacks,
    verbose=2
)

# -----------------------------
#  EVALUATE
# -----------------------------
loss, acc = model.evaluate(X_test, Y_test, verbose=0)
print(f"\nTest Accuracy: {acc*100:.2f}%  |  Test Loss: {loss:.4f}")

# -----------------------------
#  PREDICT next 17-pick combination using the most recent PAST_SEQ lines
# -----------------------------
last_input = encoded_all[-PAST_SEQ:].reshape(1, PAST_SEQ, SEQ_LEN)  # shape (1, PAST_SEQ, 17)
pred_probs = model.predict(last_input, verbose=0)[0]  # shape (17, 3)

pred_indices = np.argmax(pred_probs, axis=1)
pred_string = decode_sequence(pred_indices)
print("\n==============================")
print(" NEXT 17-PICK PREDICTION (argmax)")
print("==============================")
print(pred_string)

# print per-position top-3 probs
print("\nPer-position top probabilities (pos: [symbol,prob, ...]):")
for i in range(SEQ_LEN):
    probs = pred_probs[i]
    top_idxs = np.argsort(probs)[::-1][:3]
    top = [(idx_to_symbol[idx], float(probs[idx])) for idx in top_idxs]
    print(f"Pos {i+1}: {top}")

# -----------------------------
#  SAMPLE multiple candidate combinations using temperature sampling
# -----------------------------
def generate_candidates(n=10, temperature=1.0):
    candidates = []
    for _ in range(n):
        sampled = []
        for pos in range(SEQ_LEN):
            sampled_idx = sample_from_probs(pred_probs[pos], temperature=temperature)
            sampled.append(sampled_idx)
        candidates.append(decode_sequence(sampled))
    return candidates

print("\nSampled candidates (temperature=1.0):")
for cand in generate_candidates(n=10, temperature=1.0):
    print(cand)

# -----------------------------
#  Save final model if checkpoint not used (checkpoint already saved best)
# -----------------------------
if not os.path.exists(MODEL_PATH):
    model.save(MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
else:
    print(f"Best model already saved as {MODEL_PATH}")

# -----------------------------
#  Optional: show train history brief
# -----------------------------
try:
    import matplotlib.pyplot as plt
    plt.figure(figsize=(9,4))
    plt.plot(history.history.get("loss", []), label="train loss")
    plt.plot(history.history.get("val_loss", []), label="val loss")
    plt.legend()
    plt.title("Loss")
    plt.show()
except Exception:
    # matplotlib optional
    pass

print("\nDone.")
