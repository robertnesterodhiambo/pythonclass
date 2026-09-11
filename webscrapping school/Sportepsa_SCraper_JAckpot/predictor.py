import pandas as pd
import numpy as np
import pickle
from collections import Counter, defaultdict
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

FILE = "jackpot_groups.csv"
COLUMN = "outcome_sequence"

SEQUENCE_LENGTH = 17

# Start testing after this many historical sequences.
# With 300 sequences, 100 is a reasonable starting point.
INITIAL_TRAIN_SIZE = 100

# Recent history used by the prediction model.
# Set to None to use ALL available training history.
RECENT_WINDOW = 100

# N-grams to use
NGRAM_SIZES = [1, 2, 3, 4]

# Output files
BACKTEST_FILE = "walk_forward_predictions.csv"
POSITION_ACCURACY_FILE = "position_accuracy.csv"
SUMMARY_FILE = "model_summary.csv"
FINAL_PREDICTION_FILE = "next_17_prediction.csv"
MODEL_FILE = "jackpot_model.pkl"


# ============================================================
# OUTCOME NAMES
# ============================================================

OUTCOME_NAMES = {
    0: "Draw",
    1: "Home",
    2: "Away"
}


# ============================================================
# 1. LOAD DATA
# ============================================================

print("=" * 80)
print("JACKPOT EXPANDING WALK-FORWARD MODEL")
print("=" * 80)

df = pd.read_csv(FILE)

if COLUMN not in df.columns:
    raise ValueError(
        f"Column '{COLUMN}' was not found.\n"
        f"Available columns: {df.columns.tolist()}"
    )

print("\nOriginal rows:", len(df))


# ============================================================
# 2. CLEAN SEQUENCES
# ============================================================

def clean_sequence(value):

    value = str(value).strip()

    # Keep only 0, 1, 2
    value = "".join(
        c for c in value
        if c in "012"
    )

    return value


df["sequence"] = df[COLUMN].apply(clean_sequence)

# Keep exactly 17 outcomes
valid_df = df[
    df["sequence"].str.len() == SEQUENCE_LENGTH
].copy()

invalid_df = df[
    df["sequence"].str.len() != SEQUENCE_LENGTH
].copy()

sequences = valid_df["sequence"].tolist()

print("Valid 17-outcome sequences:", len(sequences))
print("Invalid sequences:", len(invalid_df))

if len(sequences) < INITIAL_TRAIN_SIZE + 1:

    raise ValueError(
        f"You need at least "
        f"{INITIAL_TRAIN_SIZE + 1} valid sequences."
    )


# ============================================================
# IMPORTANT:
#
# Your file is assumed to be:
#
# TOP    = LATEST
# BOTTOM = OLDEST
#
# Therefore reverse the dataframe so that:
#
# sequences[0] = oldest
# sequences[-1] = latest
#
# ============================================================

sequences = list(reversed(sequences))

print("\nChronological order:")
print("Oldest:", sequences[0])
print("Latest:", sequences[-1])


# ============================================================
# 3. BASIC STATISTICS
# ============================================================

X = np.array([
    [int(c) for c in seq]
    for seq in sequences
])

print("\nSequence matrix:", X.shape)

print("\n" + "=" * 80)
print("OVERALL OUTCOME FREQUENCY")
print("=" * 80)

counts = Counter(X.flatten())

total = len(X.flatten())

for value in [0, 1, 2]:

    print(
        f"{value} = {OUTCOME_NAMES[value]:5s} : "
        f"{counts[value]:5d} "
        f"({counts[value] / total:.2%})"
    )


# ============================================================
# 4. BUILD N-GRAM MODELS
# ============================================================

def build_ngram_models(history):

    models = {}

    for n in NGRAM_SIZES:

        model = defaultdict(Counter)

        for seq in history:

            if len(seq) <= n:
                continue

            for i in range(len(seq) - n):

                pattern = seq[i:i+n]

                next_value = int(
                    seq[i+n]
                )

                model[pattern][next_value] += 1

        models[n] = model

    return models


# ============================================================
# 5. TRANSITION MODEL
# ============================================================

def build_transition_model(history):

    transitions = defaultdict(Counter)

    for seq in history:

        for i in range(len(seq) - 1):

            current = int(seq[i])

            next_value = int(seq[i+1])

            transitions[current][next_value] += 1

    return transitions


# ============================================================
# 6. POSITION MODEL
# ============================================================

def build_position_model(history):

    position_model = []

    for pos in range(SEQUENCE_LENGTH):

        counts = Counter(
            int(seq[pos])
            for seq in history
        )

        position_model.append(
            counts
        )

    return position_model


# ============================================================
# 7. PREDICTION FUNCTION
# ============================================================

def predict_sequence(history):

    """
    Predict one complete 17-outcome sequence.

    Uses:

    - Position frequencies
    - Transition probabilities
    - 1-gram
    - 2-gram
    - 3-gram
    - 4-gram

    IMPORTANT:
    All models are built ONLY from `history`.
    """

    history = list(history)

    if RECENT_WINDOW is not None:

        recent = history[
            -RECENT_WINDOW:
        ]

    else:

        recent = history

    # --------------------------------------------------------
    # Build models from CURRENT training data
    # --------------------------------------------------------

    position_model = build_position_model(
        recent
    )

    transition_model = build_transition_model(
        recent
    )

    ngram_models = build_ngram_models(
        recent
    )

    prediction = ""

    # ========================================================
    # POSITION 1
    # ========================================================

    scores = {
        0: 0.0,
        1: 0.0,
        2: 0.0
    }

    counts = position_model[0]

    total_count = sum(
        counts.values()
    )

    if total_count > 0:

        for value in [0, 1, 2]:

            probability = (
                counts[value]
                / total_count
            )

            scores[value] += (
                probability * 10
            )

    first = max(
        scores,
        key=scores.get
    )

    prediction += str(first)

    # ========================================================
    # POSITIONS 2 - 17
    # ========================================================

    for pos in range(
        1,
        SEQUENCE_LENGTH
    ):

        scores = {
            0: 0.0,
            1: 0.0,
            2: 0.0
        }

        # ====================================================
        # A. POSITION FREQUENCY
        # ====================================================

        counts = position_model[pos]

        total_count = sum(
            counts.values()
        )

        if total_count > 0:

            for value in [0, 1, 2]:

                probability = (
                    counts[value]
                    / total_count
                )

                scores[value] += (
                    probability * 10
                )

        # ====================================================
        # B. TRANSITION PROBABILITY
        # ====================================================

        previous = int(
            prediction[-1]
        )

        transition_counts = (
            transition_model.get(
                previous,
                Counter()
            )
        )

        transition_total = sum(
            transition_counts.values()
        )

        if transition_total > 0:

            for value in [0, 1, 2]:

                probability = (
                    transition_counts[value]
                    / transition_total
                )

                scores[value] += (
                    probability * 8
                )

        # ====================================================
        # C. N-GRAM PROBABILITIES
        # ====================================================

        for n, weight in [
            (1, 2.0),
            (2, 3.0),
            (3, 4.0),
            (4, 5.0)
        ]:

            if len(prediction) < n:
                continue

            pattern = prediction[-n:]

            model = ngram_models.get(
                n,
                {}
            )

            if pattern not in model:
                continue

            counts = model[pattern]

            total_pattern = sum(
                counts.values()
            )

            if total_pattern == 0:
                continue

            for value in [0, 1, 2]:

                probability = (
                    counts[value]
                    / total_pattern
                )

                scores[value] += (
                    probability * weight
                )

        # ====================================================
        # D. SELECT BEST OUTCOME
        # ====================================================

        best = max(
            scores,
            key=scores.get
        )

        prediction += str(best)

    return prediction


# ============================================================
# 8. WALK-FORWARD / EXPANDING WINDOW TEST
# ============================================================

print("\n" + "=" * 80)
print("EXPANDING WALK-FORWARD TEST")
print("=" * 80)

print(
    f"\nInitial training size: "
    f"{INITIAL_TRAIN_SIZE}"
)

print(
    f"Testing from row "
    f"{INITIAL_TRAIN_SIZE + 1} "
    f"to row "
    f"{len(sequences)}"
)


backtest_results = []


# ============================================================
# MAIN WALK-FORWARD LOOP
# ============================================================

for test_index in range(
    INITIAL_TRAIN_SIZE,
    len(sequences)
):

    # --------------------------------------------------------
    # TRAINING DATA
    #
    # Everything BEFORE test_index
    # --------------------------------------------------------

    training_data = sequences[
        :test_index
    ]

    # --------------------------------------------------------
    # ACTUAL FUTURE SEQUENCE
    # --------------------------------------------------------

    actual = sequences[
        test_index
    ]

    # --------------------------------------------------------
    # PREDICT
    # --------------------------------------------------------

    predicted = predict_sequence(
        training_data
    )

    # --------------------------------------------------------
    # COMPARE
    # --------------------------------------------------------

    correct_positions = sum(
        a == p
        for a, p in zip(
            actual,
            predicted
        )
    )

    accuracy = (
        correct_positions
        / SEQUENCE_LENGTH
    )

    exact_match = (
        actual == predicted
    )

    # --------------------------------------------------------
    # Record
    # --------------------------------------------------------

    result = {

        "test_row": test_index + 1,

        "training_sequences":
            len(training_data),

        "actual":
            actual,

        "predicted":
            predicted,

        "correct":
            correct_positions,

        "accuracy":
            accuracy,

        "exact_17_match":
            exact_match
    }

    backtest_results.append(
        result
    )

    # --------------------------------------------------------
    # PRINT PROGRESS
    # --------------------------------------------------------

    print(
        f"Test {test_index + 1:3d} | "
        f"Train {len(training_data):3d} | "
        f"Actual {actual} | "
        f"Predicted {predicted} | "
        f"{correct_positions:2d}/17 "
        f"({accuracy:.1%})"
    )


# ============================================================
# 9. BACKTEST DATAFRAME
# ============================================================

backtest_df = pd.DataFrame(
    backtest_results
)


# ============================================================
# 10. OVERALL PERFORMANCE
# ============================================================

print("\n" + "=" * 80)
print("BACKTEST PERFORMANCE")
print("=" * 80)

total_tests = len(
    backtest_df
)

total_correct = (
    backtest_df["correct"]
    .sum()
)

total_possible = (
    total_tests
    * SEQUENCE_LENGTH
)

overall_accuracy = (
    total_correct
    / total_possible
)

average_sequence_accuracy = (
    backtest_df["accuracy"]
    .mean()
)

exact_matches = (
    backtest_df[
        "exact_17_match"
    ].sum()
)

exact_rate = (
    exact_matches
    / total_tests
)


print(
    f"\nNumber of test sequences : "
    f"{total_tests}"
)

print(
    f"Total correct positions  : "
    f"{total_correct}"
)

print(
    f"Total possible positions : "
    f"{total_possible}"
)

print(
    f"\nOverall position accuracy: "
    f"{overall_accuracy:.2%}"
)

print(
    f"Average sequence accuracy: "
    f"{average_sequence_accuracy:.2%}"
)

print(
    f"Exact 17/17 matches      : "
    f"{exact_matches}"
)

print(
    f"Exact sequence rate      : "
    f"{exact_rate:.4%}"
)


# ============================================================
# 11. DISTRIBUTION OF PREDICTION ACCURACY
# ============================================================

print("\n" + "=" * 80)
print("CORRECT POSITIONS DISTRIBUTION")
print("=" * 80)

distribution = (
    backtest_df[
        "correct"
    ]
    .value_counts()
    .sort_index()
)

for correct, count in distribution.items():

    percentage = (
        count / total_tests
    )

    print(
        f"{correct:2d}/17 : "
        f"{count:3d} sequences "
        f"({percentage:.2%})"
    )


# ============================================================
# 12. POSITION-BY-POSITION ACCURACY
# ============================================================

print("\n" + "=" * 80)
print("POSITION-BY-POSITION ACCURACY")
print("=" * 80)

position_results = []

for pos in range(
    SEQUENCE_LENGTH
):

    correct = 0

    for _, row in backtest_df.iterrows():

        if (
            row["actual"][pos]
            ==
            row["predicted"][pos]
        ):

            correct += 1

    accuracy = (
        correct
        / total_tests
    )

    position_results.append({

        "position":
            pos + 1,

        "correct":
            correct,

        "total":
            total_tests,

        "accuracy":
            accuracy
    })


position_accuracy_df = pd.DataFrame(
    position_results
)

print(
    position_accuracy_df.to_string(
        index=False
    )
)


# ============================================================
# 13. CONFUSION COUNTS
# ============================================================

print("\n" + "=" * 80)
print("PREDICTION CONFUSION COUNTS")
print("=" * 80)

confusion = Counter()

for _, row in backtest_df.iterrows():

    actual = row["actual"]

    predicted = row["predicted"]

    for a, p in zip(
        actual,
        predicted
    ):

        confusion[
            (int(a), int(p))
        ] += 1


print(
    "\nActual → Predicted"
)

for actual in [0, 1, 2]:

    for predicted in [0, 1, 2]:

        count = confusion[
            (actual, predicted)
        ]

        print(
            f"{actual} ({OUTCOME_NAMES[actual]:5s}) "
            f"→ "
            f"{predicted} ({OUTCOME_NAMES[predicted]:5s}) "
            f": {count}"
        )


# ============================================================
# 14. TRAIN FINAL MODEL ON ALL 300 SEQUENCES
# ============================================================

print("\n" + "=" * 80)
print("TRAINING FINAL MODEL")
print("=" * 80)

print(
    f"\nTraining on all "
    f"{len(sequences)} "
    f"historical sequences..."
)


final_position_model = build_position_model(
    sequences
)

final_transition_model = build_transition_model(
    sequences
)

final_ngram_models = build_ngram_models(
    sequences
)


# ============================================================
# 15. PREDICT NEXT UNKNOWN SEQUENCE
# ============================================================

next_prediction = predict_sequence(
    sequences
)


print("\n" + "=" * 80)
print("NEXT POSSIBLE SEQUENCE")
print("=" * 80)

print(
    "\nPredicted next 17 outcomes:"
)

print(
    next_prediction
)


# ============================================================
# 16. DISPLAY INDIVIDUAL MATCH PREDICTIONS
# ============================================================

print("\nPosition-by-position prediction:")

for position, value in enumerate(
    next_prediction,
    start=1
):

    value = int(value)

    print(
        f"{position:2d}. "
        f"{value} = "
        f"{OUTCOME_NAMES[value]}"
    )


# ============================================================
# 17. SAVE NEXT PREDICTION
# ============================================================

prediction_rows = []

for position, value in enumerate(
    next_prediction,
    start=1
):

    value = int(value)

    prediction_rows.append({

        "position":
            position,

        "prediction":
            value,

        "outcome":
            OUTCOME_NAMES[value],

        "sequence":
            next_prediction
    })


prediction_df = pd.DataFrame(
    prediction_rows
)

prediction_df.to_csv(
    FINAL_PREDICTION_FILE,
    index=False
)


# ============================================================
# 18. SAVE BACKTEST RESULTS
# ============================================================

backtest_df.to_csv(
    BACKTEST_FILE,
    index=False
)

position_accuracy_df.to_csv(
    POSITION_ACCURACY_FILE,
    index=False
)


# ============================================================
# 19. MODEL SUMMARY
# ============================================================

summary_df = pd.DataFrame([{

    "historical_sequences":
        len(sequences),

    "initial_train_size":
        INITIAL_TRAIN_SIZE,

    "test_sequences":
        total_tests,

    "overall_position_accuracy":
        overall_accuracy,

    "average_sequence_accuracy":
        average_sequence_accuracy,

    "exact_17_matches":
        exact_matches,

    "exact_sequence_rate":
        exact_rate,

    "next_prediction":
        next_prediction
}])


summary_df.to_csv(
    SUMMARY_FILE,
    index=False
)


# ============================================================
# 20. SAVE THE MODEL
# ============================================================

model_package = {

    "model_type":
        "Expanding Walk-Forward N-Gram/Transition Model",

    "sequence_length":
        SEQUENCE_LENGTH,

    "recent_window":
        RECENT_WINDOW,

    "ngram_sizes":
        NGRAM_SIZES,

    "historical_sequences":
        sequences,

    "position_model":
        final_position_model,

    "transition_model":
        final_transition_model,

    "ngram_models":
        final_ngram_models,

    "next_prediction":
        next_prediction,

    "backtest_accuracy":
        overall_accuracy,

    "exact_match_rate":
        exact_rate
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
# 21. SHOW LAST BACKTEST RESULTS
# ============================================================

print("\n" + "=" * 80)
print("LAST 10 WALK-FORWARD PREDICTIONS")
print("=" * 80)

print(
    backtest_df.tail(10).to_string(
        index=False
    )
)


# ============================================================
# 22. FINISHED
# ============================================================

print("\n" + "=" * 80)
print("MODEL TRAINING COMPLETE")
print("=" * 80)

print(
    f"""
Historical sequences : {len(sequences)}
Backtest sequences   : {total_tests}

Overall accuracy     : {overall_accuracy:.2%}
Average seq accuracy : {average_sequence_accuracy:.2%}

Exact 17/17 matches  : {exact_matches}
Exact match rate     : {exact_rate:.4%}

NEXT PREDICTION
---------------
{next_prediction}

FILES CREATED
-------------
{BACKTEST_FILE}
{POSITION_ACCURACY_FILE}
{SUMMARY_FILE}
{FINAL_PREDICTION_FILE}
{MODEL_FILE}

The trained model has been saved.
"""
)

print("=" * 80)