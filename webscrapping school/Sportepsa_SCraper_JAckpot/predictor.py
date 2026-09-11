import pandas as pd
import numpy as np
import pickle
from collections import Counter, defaultdict
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

CSV_FILE = "jackpot_groups.csv"
COLUMN = "outcome_sequence"

# Number of outcomes in one jackpot
SEQ_LEN = 17

# Initial number of historical jackpots used before testing
INITIAL_TRAIN_SIZE = 100

# Recent-history windows to test
RECENT_WINDOWS = [20, 30, 50, 75, 100]

# N-gram sizes to test
NGRAM_ORDERS = [2, 3, 4]

# Output files
BACKTEST_FILE = "walk_forward_model_selection.csv"
POSITION_MODEL_FILE = "best_model_per_position.csv"
POSITION_ACCURACY_FILE = "position_model_accuracy.csv"
NEXT_PREDICTION_FILE = "next_17_prediction.csv"
MODEL_FILE = "jackpot_model.pkl"


# ============================================================
# BASIC HELPERS
# ============================================================

OUTCOMES = ["0", "1", "2"]


def normalize_sequence(value):
    """
    Convert a CSV value into a clean 17-character sequence.

    Valid:
        00121212001212210

    Invalid:
        anything containing characters other than 0,1,2
        or anything not exactly 17 characters
    """

    if pd.isna(value):
        return None

    value = str(value).strip()

    if len(value) != SEQ_LEN:
        return None

    if not all(char in OUTCOMES for char in value):
        return None

    return value


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("LOADING DATA")
print("=" * 70)

df = pd.read_csv(CSV_FILE)

if COLUMN not in df.columns:
    raise ValueError(
        f"Column '{COLUMN}' was not found.\n"
        f"Available columns: {list(df.columns)}"
    )

original_rows = len(df)

df["clean_sequence"] = df[COLUMN].apply(normalize_sequence)

valid_df = df[df["clean_sequence"].notna()].copy()
invalid_df = df[df["clean_sequence"].isna()].copy()

print(f"Original rows: {original_rows}")
print(f"Valid 17-outcome sequences: {len(valid_df)}")
print(f"Invalid sequences: {len(invalid_df)}")

if len(valid_df) <= INITIAL_TRAIN_SIZE:
    raise ValueError(
        f"Not enough valid sequences.\n"
        f"Need more than {INITIAL_TRAIN_SIZE}, "
        f"but only found {len(valid_df)}."
    )


# ============================================================
# IMPORTANT:
# CSV HAS LATEST AT TOP
#
# Therefore reverse the valid rows so that:
#
# oldest
#   ↓
# newest
#
# ============================================================

sequences = valid_df["clean_sequence"].tolist()

sequences = list(reversed(sequences))

print()
print("Chronological order:")
print(f"Oldest: {sequences[0]}")
print(f"Latest: {sequences[-1]}")

X = np.array(
    [[int(char) for char in sequence] for sequence in sequences],
    dtype=int
)

print()
print(f"Sequence matrix: {X.shape}")


# ============================================================
# OVERALL FREQUENCY
# ============================================================

all_values = X.flatten()

counts = Counter(all_values)

print()
print("=" * 70)
print("OVERALL OUTCOME FREQUENCY")
print("=" * 70)

for outcome in [0, 1, 2]:
    count = counts[outcome]
    percentage = count / len(all_values) * 100

    print(
        f"{outcome} = "
        f"{['Draw', 'Home', 'Away'][outcome]:5s} : "
        f"{count:5d} "
        f"({percentage:.2f}%)"
    )


# ============================================================
# MODEL 1:
# POSITION FREQUENCY
# ============================================================

def predict_position_frequency(train, position):
    """
    Predict using the most common outcome for this position.
    """

    values = train[:, position]

    counts = Counter(values)

    return counts.most_common(1)[0][0]


# ============================================================
# MODEL 2:
# RECENT POSITION FREQUENCY
# ============================================================

def predict_recent_frequency(train, position, window):
    """
    Predict using only the most recent N jackpots.
    """

    recent = train[-window:, position]

    counts = Counter(recent)

    return counts.most_common(1)[0][0]


# ============================================================
# MODEL 3:
# WEIGHTED RECENT FREQUENCY
# ============================================================

def predict_weighted_frequency(train, position, window):
    """
    More recent jackpots receive more weight.
    """

    recent = train[-window:, position]

    scores = {
        0: 0.0,
        1: 0.0,
        2: 0.0
    }

    total = len(recent)

    for i, value in enumerate(recent):

        # Oldest gets smaller weight.
        # Newest gets largest weight.
        weight = i + 1

        scores[int(value)] += weight

    return max(scores, key=scores.get)


# ============================================================
# MODEL 4:
# MARKOV / TRANSITION MODEL
# ============================================================

def predict_markov(train, position):
    """
    Predict the current position using the previous position.

    Example:

    position 5 depends on position 4.

    We learn:

        previous outcome -> current outcome
    """

    if position == 0:
        return predict_position_frequency(train, position)

    previous = train[:, position - 1]
    current = train[:, position]

    transitions = defaultdict(Counter)

    for prev_value, current_value in zip(previous, current):
        transitions[int(prev_value)][int(current_value)] += 1

    # Use the most common previous-position outcome
    latest_previous = int(train[-1, position - 1])

    if latest_previous in transitions:
        return transitions[latest_previous].most_common(1)[0][0]

    return predict_position_frequency(train, position)


# ============================================================
# MODEL 5:
# N-GRAM MODEL
# ============================================================

def build_ngram_model(train, position, order):
    """
    Build an n-gram model using previous outcomes.

    For example with order=3:

        [position-3, position-2, position-1]
                    ↓
              current outcome
    """

    model = defaultdict(Counter)

    if position < order:
        return model

    for row in train:

        start = position - order

        context = tuple(
            int(x)
            for x in row[start:position]
        )

        target = int(row[position])

        model[context][target] += 1

    return model


def predict_ngram(train, position, order):
    """
    Predict using the most recent context.
    """

    if position < order:
        return predict_position_frequency(train, position)

    model = build_ngram_model(
        train,
        position,
        order
    )

    context = tuple(
        int(x)
        for x in train[-1, position - order:position]
    )

    if context in model:

        return model[context].most_common(1)[0][0]

    # Backoff if exact context has never appeared
    return predict_position_frequency(
        train,
        position
    )


# ============================================================
# MODEL 6:
# RECENT N-GRAM
# ============================================================

def predict_recent_ngram(
    train,
    position,
    order,
    window
):
    """
    N-gram model trained only on recent history.
    """

    if position < order:
        return predict_recent_frequency(
            train,
            position,
            window
        )

    recent = train[-window:]

    model = build_ngram_model(
        recent,
        position,
        order
    )

    context = tuple(
        int(x)
        for x in recent[-1, position - order:position]
    )

    if context in model:
        return model[context].most_common(1)[0][0]

    return predict_recent_frequency(
        train,
        position,
        window
    )


# ============================================================
# LIST OF CANDIDATE MODELS
# ============================================================

def get_model_names():
    """
    Return every candidate strategy.
    """

    models = []

    models.append(
        "position_frequency"
    )

    for window in RECENT_WINDOWS:

        models.append(
            f"recent_frequency_{window}"
        )

        models.append(
            f"weighted_frequency_{window}"
        )

    models.append(
        "markov"
    )

    for order in NGRAM_ORDERS:

        models.append(
            f"ngram_{order}"
        )

        for window in RECENT_WINDOWS:

            models.append(
                f"recent_ngram_{order}_{window}"
            )

    return models


MODEL_NAMES = get_model_names()


# ============================================================
# RUN ONE MODEL
# ============================================================

def predict_with_model(
    train,
    position,
    model_name
):

    # --------------------------------------------------------
    # Position frequency
    # --------------------------------------------------------

    if model_name == "position_frequency":

        return predict_position_frequency(
            train,
            position
        )

    # --------------------------------------------------------
    # Recent frequency
    # --------------------------------------------------------

    if model_name.startswith(
        "recent_frequency_"
    ):

        window = int(
            model_name.split("_")[-1]
        )

        window = min(
            window,
            len(train)
        )

        return predict_recent_frequency(
            train,
            position,
            window
        )

    # --------------------------------------------------------
    # Weighted frequency
    # --------------------------------------------------------

    if model_name.startswith(
        "weighted_frequency_"
    ):

        window = int(
            model_name.split("_")[-1]
        )

        window = min(
            window,
            len(train)
        )

        return predict_weighted_frequency(
            train,
            position,
            window
        )

    # --------------------------------------------------------
    # Markov
    # --------------------------------------------------------

    if model_name == "markov":

        return predict_markov(
            train,
            position
        )

    # --------------------------------------------------------
    # NGRAM
    # --------------------------------------------------------

    if model_name.startswith("ngram_"):

        order = int(
            model_name.split("_")[1]
        )

        return predict_ngram(
            train,
            position,
            order
        )

    # --------------------------------------------------------
    # RECENT NGRAM
    # --------------------------------------------------------

    if model_name.startswith(
        "recent_ngram_"
    ):

        parts = model_name.split("_")

        order = int(parts[2])
        window = int(parts[3])

        window = min(
            window,
            len(train)
        )

        return predict_recent_ngram(
            train,
            position,
            order,
            window
        )

    raise ValueError(
        f"Unknown model: {model_name}"
    )


# ============================================================
# MODEL SELECTION
# ============================================================
#
# IMPORTANT:
#
# We cannot simply test every model against the current
# jackpot and then choose the winner.
#
# That would leak the answer.
#
# Instead:
#
# At each prediction point:
#
#     training history
#            ↓
#     evaluate models on earlier history
#            ↓
#     choose best model
#            ↓
#     predict current unseen jackpot
#
# ============================================================

def choose_best_model(
    train,
    position
):
    """
    Select the best model for a position using ONLY
    information available inside the training set.

    We perform an inner walk-forward validation.

    The final part of the training history becomes the
    validation section.
    """

    n = len(train)

    # Need enough history for meaningful validation
    if n < 50:

        return "position_frequency"

    # Use approximately last 30% as validation,
    # but at least 10 observations.
    validation_size = max(
        10,
        int(n * 0.30)
    )

    validation_start = n - validation_size

    scores = {
        model: {
            "correct": 0,
            "total": 0
        }
        for model in MODEL_NAMES
    }

    # --------------------------------------------------------
    # Inner walk-forward validation
    # --------------------------------------------------------

    for validation_index in range(
        validation_start,
        n
    ):

        inner_train = train[:validation_index]

        actual = int(
            train[validation_index, position]
        )

        for model_name in MODEL_NAMES:

            try:

                prediction = predict_with_model(
                    inner_train,
                    position,
                    model_name
                )

                if prediction == actual:
                    scores[model_name]["correct"] += 1

                scores[model_name]["total"] += 1

            except Exception:

                # If a model cannot produce a prediction,
                # simply don't score it.
                pass

    # --------------------------------------------------------
    # Calculate accuracy
    # --------------------------------------------------------

    model_accuracy = {}

    for model_name, score in scores.items():

        if score["total"] == 0:

            model_accuracy[model_name] = 0.0

        else:

            model_accuracy[model_name] = (
                score["correct"]
                /
                score["total"]
            )

    # --------------------------------------------------------
    # Find best model
    # --------------------------------------------------------

    best_model = max(
        model_accuracy,
        key=model_accuracy.get
    )

    return best_model


# ============================================================
# WALK-FORWARD BACKTEST
# ============================================================

print()
print("=" * 70)
print("WALK-FORWARD MODEL SELECTION")
print("=" * 70)

print(
    f"Initial training size: "
    f"{INITIAL_TRAIN_SIZE}"
)

print(
    f"Candidate models: "
    f"{len(MODEL_NAMES)}"
)

print(
    f"Positions: "
    f"{SEQ_LEN}"
)

# Results
backtest_rows = []

position_correct = Counter()
position_total = Counter()

sequence_correct_counts = []

# Track selected model usage
selected_model_usage = Counter()

# ------------------------------------------------------------
# Outer walk-forward loop
# ------------------------------------------------------------

for test_index in range(
    INITIAL_TRAIN_SIZE,
    len(X)
):

    train = X[:test_index]

    actual_sequence = X[test_index]

    predicted_sequence = []

    selected_models = []

    # --------------------------------------------------------
    # Predict each of the 17 positions independently
    # --------------------------------------------------------

    for position in range(SEQ_LEN):

        best_model = choose_best_model(
            train,
            position
        )

        prediction = predict_with_model(
            train,
            position,
            best_model
        )

        predicted_sequence.append(
            int(prediction)
        )

        selected_models.append(
            best_model
        )

        selected_model_usage[
            best_model
        ] += 1

        # Accuracy
        position_total[position] += 1

        if int(prediction) == int(
            actual_sequence[position]
        ):
            position_correct[position] += 1

    predicted_sequence = np.array(
        predicted_sequence
    )

    # --------------------------------------------------------
    # Sequence accuracy
    # --------------------------------------------------------

    correct_positions = int(
        np.sum(
            predicted_sequence
            ==
            actual_sequence
        )
    )

    sequence_correct_counts.append(
        correct_positions
    )

    # --------------------------------------------------------
    # Save row
    # --------------------------------------------------------

    row = {
        "historical_index": test_index,
        "actual_sequence": "".join(
            map(str, actual_sequence)
        ),
        "predicted_sequence": "".join(
            map(str, predicted_sequence)
        ),
        "correct_positions": correct_positions,
        "sequence_accuracy": (
            correct_positions
            /
            SEQ_LEN
        )
    }

    for position in range(SEQ_LEN):

        row[
            f"actual_{position + 1}"
        ] = int(
            actual_sequence[position]
        )

        row[
            f"prediction_{position + 1}"
        ] = int(
            predicted_sequence[position]
        )

        row[
            f"model_{position + 1}"
        ] = selected_models[position]

    backtest_rows.append(row)

    # --------------------------------------------------------
    # Progress
    # --------------------------------------------------------

    if (
        (test_index - INITIAL_TRAIN_SIZE + 1)
        % 10 == 0
        or
        test_index == len(X) - 1
    ):

        completed = (
            test_index
            -
            INITIAL_TRAIN_SIZE
            +
            1
        )

        total_tests = (
            len(X)
            -
            INITIAL_TRAIN_SIZE
        )

        print(
            f"Processed "
            f"{completed}/{total_tests}"
        )


# ============================================================
# BACKTEST DATAFRAME
# ============================================================

backtest_df = pd.DataFrame(
    backtest_rows
)

backtest_df.to_csv(
    BACKTEST_FILE,
    index=False
)


# ============================================================
# OVERALL BACKTEST ACCURACY
# ============================================================

total_correct = sum(
    position_correct.values()
)

total_predictions = sum(
    position_total.values()
)

overall_accuracy = (
    total_correct
    /
    total_predictions
)

average_sequence_accuracy = np.mean(
    [
        x / SEQ_LEN
        for x in sequence_correct_counts
    ]
)

exact_matches = sum(
    x == SEQ_LEN
    for x in sequence_correct_counts
)


print()
print("=" * 70)
print("BACKTEST RESULTS")
print("=" * 70)

print(
    f"Test sequences: "
    f"{len(backtest_df)}"
)

print(
    f"Tested positions: "
    f"{total_predictions}"
)

print(
    f"Correct positions: "
    f"{total_correct}"
)

print(
    f"Overall position accuracy: "
    f"{overall_accuracy * 100:.2f}%"
)

print(
    f"Average sequence accuracy: "
    f"{average_sequence_accuracy * 100:.2f}%"
)

print(
    f"Exact 17/17 matches: "
    f"{exact_matches}"
)


# ============================================================
# POSITION-BY-POSITION RESULTS
# ============================================================

position_rows = []

print()
print("=" * 70)
print("POSITION-BY-POSITION MODEL PERFORMANCE")
print("=" * 70)

for position in range(SEQ_LEN):

    correct = position_correct[position]
    total = position_total[position]

    accuracy = (
        correct / total
        if total > 0
        else 0
    )

    position_rows.append({
        "position": position + 1,
        "correct": correct,
        "total": total,
        "accuracy": accuracy
    })

    print(
        f"Position {position + 1:2d}: "
        f"{correct:3d}/{total:3d} "
        f"= {accuracy * 100:6.2f}%"
    )


position_accuracy_df = pd.DataFrame(
    position_rows
)

position_accuracy_df.to_csv(
    POSITION_ACCURACY_FILE,
    index=False
)


# ============================================================
# MOST COMMON NUMBER OF CORRECT POSITIONS
# ============================================================

distribution = Counter(
    sequence_correct_counts
)

print()
print("=" * 70)
print("CORRECT-POSITION DISTRIBUTION")
print("=" * 70)

for correct_positions in sorted(
    distribution
):

    count = distribution[
        correct_positions
    ]

    percentage = (
        count
        /
        len(sequence_correct_counts)
        *
        100
    )

    print(
        f"{correct_positions:2d}/17 : "
        f"{count:3d} sequences "
        f"({percentage:5.2f}%)"
    )


# ============================================================
# SELECT FINAL MODEL FOR EACH POSITION
# ============================================================
#
# Now that we have completed the historical backtest,
# determine the final model for each position.
#
# We use ALL historical data.
#
# ============================================================

print()
print("=" * 70)
print("FINAL MODEL SELECTION")
print("=" * 70)

final_models = []

for position in range(SEQ_LEN):

    best_model = choose_best_model(
        X,
        position
    )

    final_models.append(
        best_model
    )

    # Calculate final model validation score
    validation_size = max(
        10,
        int(len(X) * 0.30)
    )

    validation_start = (
        len(X)
        -
        validation_size
    )

    correct = 0
    total = 0

    for validation_index in range(
        validation_start,
        len(X)
    ):

        validation_train = X[
            :validation_index
        ]

        actual = int(
            X[
                validation_index,
                position
            ]
        )

        try:

            prediction = predict_with_model(
                validation_train,
                position,
                best_model
            )

            if prediction == actual:
                correct += 1

            total += 1

        except Exception:

            pass

    validation_accuracy = (
        correct / total
        if total > 0
        else 0
    )

    print(
        f"Position {position + 1:2d}: "
        f"{best_model:30s} "
        f"{validation_accuracy * 100:6.2f}%"
    )


# ============================================================
# SAVE FINAL MODEL TABLE
# ============================================================

final_model_rows = []

for position, model_name in enumerate(
    final_models
):

    final_model_rows.append({
        "position": position + 1,
        "selected_model": model_name
    })


final_model_df = pd.DataFrame(
    final_model_rows
)

final_model_df.to_csv(
    POSITION_MODEL_FILE,
    index=False
)


# ============================================================
# FINAL NEXT 17 PREDICTION
# ============================================================
#
# Use all available historical data.
#
# Each position gets its own selected model.
#
# ============================================================

print()
print("=" * 70)
print("PREDICTING NEXT 17 OUTCOMES")
print("=" * 70)

next_prediction = []

prediction_details = []

for position in range(SEQ_LEN):

    model_name = final_models[position]

    prediction = predict_with_model(
        X,
        position,
        model_name
    )

    prediction = int(prediction)

    next_prediction.append(
        prediction
    )

    prediction_details.append({
        "position": position + 1,
        "prediction": prediction,
        "outcome_name": {
            0: "Draw",
            1: "Home",
            2: "Away"
        }[prediction],
        "model": model_name
    })


# ============================================================
# FINAL SEQUENCE
# ============================================================

next_sequence = "".join(
    map(str, next_prediction)
)

print()
print(
    f"NEXT 17-OUTCOME PREDICTION:"
)

print()
print(
    next_sequence
)

print()

for item in prediction_details:

    print(
        f"{item['position']:2d}. "
        f"{item['prediction']} = "
        f"{item['outcome_name']:5s} "
        f"({item['model']})"
    )


# ============================================================
# SAVE NEXT PREDICTION
# ============================================================

next_prediction_df = pd.DataFrame(
    prediction_details
)

next_prediction_df.to_csv(
    NEXT_PREDICTION_FILE,
    index=False
)


# ============================================================
# MODEL OBJECT FOR PICKLE
# ============================================================
#
# This stores:
#
# - historical data
# - selected model per position
# - configuration
# - next prediction
#
# ============================================================

model_package = {

    "sequence_length": SEQ_LEN,

    "initial_train_size":
        INITIAL_TRAIN_SIZE,

    "recent_windows":
        RECENT_WINDOWS,

    "ngram_orders":
        NGRAM_ORDERS,

    "model_names":
        MODEL_NAMES,

    "historical_sequences":
        sequences,

    "historical_matrix":
        X,

    "selected_models":
        final_models,

    "next_prediction":
        next_sequence,

    "outcome_mapping": {
        0: "Draw",
        1: "Home",
        2: "Away"
    }
}


with open(
    MODEL_FILE,
    "wb"
) as file:

    pickle.dump(
        model_package,
        file
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

print()
print("=" * 70)
print("FILES CREATED")
print("=" * 70)

print(
    f"1. {BACKTEST_FILE}"
)

print(
    f"2. {POSITION_MODEL_FILE}"
)

print(
    f"3. {POSITION_ACCURACY_FILE}"
)

print(
    f"4. {NEXT_PREDICTION_FILE}"
)

print(
    f"5. {MODEL_FILE}"
)

print()
print("=" * 70)
print("DONE")
print("=" * 70)

print()
print(
    "Final predicted sequence:"
)

print(
    next_sequence
)

print()