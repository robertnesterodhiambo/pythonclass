import pandas as pd
import numpy as np
import pickle
from collections import Counter, defaultdict


# ============================================================
# CONFIGURATION
# ============================================================

CSV_FILE = "jackpot_groups.csv"
COLUMN = "outcome_sequence"

SEQ_LEN = 17

# Initial historical data before outer testing begins
INITIAL_TRAIN_SIZE = 100

# Models using recent history
RECENT_WINDOWS = [20, 50, 100]

# N-gram orders
NGRAM_ORDERS = [2, 3, 4]

# Percentage of the AVAILABLE training history used for
# inner model selection
VALIDATION_FRACTION = 0.30


# ============================================================
# OUTPUT FILES
# ============================================================

INVALID_FILE = "invalid_sequences.csv"

BACKTEST_FILE = "walk_forward_predictions.csv"

MODEL_COMPARISON_FILE = "model_comparison.csv"

POSITION_COMPARISON_FILE = (
    "position_model_comparison.csv"
)

ADAPTIVE_POSITION_FILE = (
    "adaptive_position_accuracy.csv"
)

FINAL_MODELS_FILE = (
    "final_models_after_backtest.csv"
)

PERIOD_FILE = (
    "period_performance.csv"
)

DISTRIBUTION_FILE = (
    "prediction_distribution.csv"
)

NEXT_FILE = (
    "next_17_prediction.csv"
)

MODEL_FILE = (
    "jackpot_model.pkl"
)


# ============================================================
# OUTCOME NAMES
# ============================================================

OUTCOME_NAMES = {
    0: "Draw",
    1: "Home",
    2: "Away"
}


# ============================================================
# VALIDATE SEQUENCE
# ============================================================

def normalize_sequence(value):

    if pd.isna(value):
        return None

    value = str(value).strip()

    if len(value) != SEQ_LEN:
        return None

    if not all(
        character in "012"
        for character in value
    ):
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
        f"Column '{COLUMN}' not found.\n"
        f"Available columns: {list(df.columns)}"
    )


df["clean_sequence"] = df[
    COLUMN
].apply(
    normalize_sequence
)


valid_df = df[
    df["clean_sequence"].notna()
].copy()


invalid_df = df[
    df["clean_sequence"].isna()
].copy()


print(
    f"Original rows: {len(df)}"
)

print(
    f"Valid 17-outcome sequences: "
    f"{len(valid_df)}"
)

print(
    f"Invalid sequences: "
    f"{len(invalid_df)}"
)


# ============================================================
# SAVE INVALID ROWS
# ============================================================

if len(invalid_df) > 0:

    invalid_df.to_csv(
        INVALID_FILE,
        index=False
    )

    print(
        f"Invalid rows saved to "
        f"{INVALID_FILE}"
    )


# ============================================================
# CHRONOLOGICAL ORDER
# ============================================================
#
# CSV:
#
# newest
# newest
# newest
# ...
# oldest
#
# Reverse it:
#
# oldest
# oldest
# ...
# newest
#
# ============================================================

sequences = list(
    reversed(
        valid_df[
            "clean_sequence"
        ].tolist()
    )
)


if len(sequences) <= INITIAL_TRAIN_SIZE:

    raise ValueError(
        "Not enough valid sequences."
    )


print()
print("Chronological order:")

print(
    f"Oldest: {sequences[0]}"
)

print(
    f"Latest: {sequences[-1]}"
)


# ============================================================
# MATRIX
# ============================================================

X = np.array(
    [
        [
            int(character)
            for character in sequence
        ]
        for sequence in sequences
    ],
    dtype=int
)


print()
print(
    f"Sequence matrix: {X.shape}"
)


# ============================================================
# OVERALL FREQUENCY
# ============================================================

print()
print("=" * 70)
print("OVERALL OUTCOME FREQUENCY")
print("=" * 70)

all_values = X.flatten()

overall_counts = Counter(
    all_values
)

for outcome in [0, 1, 2]:

    count = overall_counts[
        outcome
    ]

    percentage = (
        count
        /
        len(all_values)
        *
        100
    )

    print(
        f"{outcome} = "
        f"{OUTCOME_NAMES[outcome]:5s} : "
        f"{count:5d} "
        f"({percentage:.2f}%)"
    )


# ============================================================
# MODEL 1
# POSITION FREQUENCY
# ============================================================

def position_frequency(
    train,
    position
):

    values = train[:, position]

    counts = Counter(values)

    return counts.most_common(1)[0][0]


# ============================================================
# MODEL 2
# MOST RECENT
# ============================================================

def most_recent(
    train,
    position
):

    return int(
        train[-1, position]
    )


# ============================================================
# MODEL 3
# RECENT FREQUENCY
# ============================================================

def recent_frequency(
    train,
    position,
    window
):

    window = min(
        window,
        len(train)
    )

    values = train[
        -window:,
        position
    ]

    counts = Counter(values)

    return counts.most_common(1)[0][0]


# ============================================================
# MODEL 4
# WEIGHTED RECENT FREQUENCY
# ============================================================

def weighted_frequency(
    train,
    position,
    window
):

    window = min(
        window,
        len(train)
    )

    values = train[
        -window:,
        position
    ]

    scores = {
        0: 0.0,
        1: 0.0,
        2: 0.0
    }

    for index, value in enumerate(values):

        weight = index + 1

        scores[
            int(value)
        ] += weight

    return max(
        scores,
        key=scores.get
    )


# ============================================================
# MODEL 5
# MARKOV
# ============================================================

def markov_prediction(
    train,
    position
):

    if position == 0:

        return position_frequency(
            train,
            position
        )

    transitions = defaultdict(
        Counter
    )

    for row in train:

        previous = int(
            row[position - 1]
        )

        current = int(
            row[position]
        )

        transitions[
            previous
        ][current] += 1

    latest_previous = int(
        train[-1, position - 1]
    )

    if latest_previous in transitions:

        return transitions[
            latest_previous
        ].most_common(1)[0][0]

    return position_frequency(
        train,
        position
    )


# ============================================================
# MODEL 6
# N-GRAM
# ============================================================

def ngram_prediction(
    train,
    position,
    order
):

    if position < order:

        return position_frequency(
            train,
            position
        )

    model = defaultdict(
        Counter
    )

    for row in train:

        context = tuple(
            int(x)
            for x in row[
                position - order:
                position
            ]
        )

        target = int(
            row[position]
        )

        model[
            context
        ][target] += 1

    latest_context = tuple(
        int(x)
        for x in train[
            -1,
            position - order:
            position
        ]
    )

    if latest_context in model:

        return model[
            latest_context
        ].most_common(1)[0][0]

    return position_frequency(
        train,
        position
    )


# ============================================================
# MODEL 7
# RECENT N-GRAM
# ============================================================

def recent_ngram_prediction(
    train,
    position,
    order,
    window
):

    window = min(
        window,
        len(train)
    )

    recent = train[
        -window:
    ]

    if position < order:

        return recent_frequency(
            train,
            position,
            window
        )

    model = defaultdict(
        Counter
    )

    for row in recent:

        context = tuple(
            int(x)
            for x in row[
                position - order:
                position
            ]
        )

        target = int(
            row[position]
        )

        model[
            context
        ][target] += 1

    latest_context = tuple(
        int(x)
        for x in recent[
            -1,
            position - order:
            position
        ]
    )

    if latest_context in model:

        return model[
            latest_context
        ].most_common(1)[0][0]

    return recent_frequency(
        train,
        position,
        window
    )


# ============================================================
# BUILD CANDIDATE MODEL LIST
# ============================================================

MODEL_NAMES = [

    "position_frequency",

    "most_recent",

]

for window in RECENT_WINDOWS:

    MODEL_NAMES.append(
        f"recent_frequency_{window}"
    )

    MODEL_NAMES.append(
        f"weighted_frequency_{window}"
    )


MODEL_NAMES.append(
    "markov"
)


for order in NGRAM_ORDERS:

    MODEL_NAMES.append(
        f"ngram_{order}"
    )

    for window in RECENT_WINDOWS:

        MODEL_NAMES.append(
            f"recent_ngram_{order}_{window}"
        )


print()
print(
    f"Candidate models: "
    f"{len(MODEL_NAMES)}"
)


# ============================================================
# UNIVERSAL MODEL PREDICTOR
# ============================================================

def predict_with_model(
    train,
    position,
    model_name
):

    if model_name == "position_frequency":

        return position_frequency(
            train,
            position
        )


    if model_name == "most_recent":

        return most_recent(
            train,
            position
        )


    if model_name.startswith(
        "recent_frequency_"
    ):

        window = int(
            model_name.split("_")[-1]
        )

        return recent_frequency(
            train,
            position,
            window
        )


    if model_name.startswith(
        "weighted_frequency_"
    ):

        window = int(
            model_name.split("_")[-1]
        )

        return weighted_frequency(
            train,
            position,
            window
        )


    if model_name == "markov":

        return markov_prediction(
            train,
            position
        )


    if model_name.startswith(
        "recent_ngram_"
    ):

        parts = model_name.split("_")

        order = int(parts[2])

        window = int(parts[3])

        return recent_ngram_prediction(
            train,
            position,
            order,
            window
        )


    if model_name.startswith(
        "ngram_"
    ):

        order = int(
            model_name.split("_")[1]
        )

        return ngram_prediction(
            train,
            position,
            order
        )


    raise ValueError(
        f"Unknown model: {model_name}"
    )


# ============================================================
# LEAKAGE-FREE INNER MODEL SELECTION
# ============================================================
#
# IMPORTANT:
#
# This function receives ONLY the history available BEFORE
# the outer test jackpot.
#
# It does NOT receive the outer test outcome.
#
# It uses an INNER validation period to decide which model
# should make the outer prediction.
#
# ============================================================

def choose_best_model(
    train,
    position
):

    n = len(train)

    if n < 50:

        return "position_frequency"


    validation_size = max(
        10,
        int(
            n
            *
            VALIDATION_FRACTION
        )
    )


    validation_start = (
        n
        -
        validation_size
    )


    scores = {
        model: {
            "correct": 0,
            "total": 0
        }
        for model in MODEL_NAMES
    }


    # --------------------------------------------------------
    # INNER WALK-FORWARD
    # --------------------------------------------------------

    for validation_index in range(
        validation_start,
        n
    ):

        inner_train = train[
            :validation_index
        ]

        actual = int(
            train[
                validation_index,
                position
            ]
        )


        for model_name in MODEL_NAMES:

            try:

                prediction = predict_with_model(
                    inner_train,
                    position,
                    model_name
                )

                scores[
                    model_name
                ]["total"] += 1


                if prediction == actual:

                    scores[
                        model_name
                    ]["correct"] += 1


            except Exception:

                pass


    # --------------------------------------------------------
    # ACCURACY
    # --------------------------------------------------------

    accuracies = {}

    for model_name in MODEL_NAMES:

        total = scores[
            model_name
        ]["total"]

        correct = scores[
            model_name
        ]["correct"]


        if total == 0:

            accuracies[
                model_name
            ] = 0.0

        else:

            accuracies[
                model_name
            ] = correct / total


    # --------------------------------------------------------
    # BEST MODEL
    # --------------------------------------------------------
    #
    # IMPORTANT:
    #
    # This selection is based ONLY on inner history.
    #
    # --------------------------------------------------------

    best_model = max(
        accuracies,
        key=accuracies.get
    )


    return best_model


# ============================================================
# OUTER WALK-FORWARD TEST
# ============================================================
#
# This is the TRUE OUT-OF-SAMPLE EVALUATION.
#
# For test_index:
#
#     train = everything BEFORE test_index
#
#     choose model using train ONLY
#
#     predict test_index
#
#     THEN reveal actual test_index
#
#     score it
#
#     add it to history
#
# ============================================================

print()
print("=" * 70)
print("LEAKAGE-FREE OUTER WALK-FORWARD TEST")
print("=" * 70)

print(
    f"Initial training size: "
    f"{INITIAL_TRAIN_SIZE}"
)

print(
    f"Outer test sequences: "
    f"{len(X) - INITIAL_TRAIN_SIZE}"
)


# ============================================================
# STORAGE
# ============================================================

backtest_rows = []


# Fixed-model statistics
model_correct = Counter()
model_total = Counter()

model_exact_matches = Counter()

model_correct_distribution = defaultdict(
    Counter
)


# Adaptive statistics
adaptive_correct = Counter()
adaptive_total = Counter()

adaptive_exact_matches = 0

adaptive_correct_distribution = Counter()


# Adaptive model selected over time
adaptive_model_usage = Counter()


# Position-specific fixed-model statistics
model_position_correct = Counter()
model_position_total = Counter()


# ============================================================
# OUTER LOOP
# ============================================================

for test_index in range(
    INITIAL_TRAIN_SIZE,
    len(X)
):

    # --------------------------------------------------------
    # CRITICAL:
    #
    # The test jackpot is NOT in train.
    # --------------------------------------------------------

    train = X[
        :test_index
    ]

    actual = X[
        test_index
    ]


    row = {
        "historical_index":
            test_index,

        "actual_sequence":
            "".join(
                map(str, actual)
            )
    }


    # ========================================================
    # FIXED BASELINES / MODELS
    # ========================================================

    for model_name in MODEL_NAMES:

        predictions = []


        for position in range(
            SEQ_LEN
        ):

            prediction = predict_with_model(
                train,
                position,
                model_name
            )

            prediction = int(
                prediction
            )

            predictions.append(
                prediction
            )


            model_total[
                model_name
            ] += 1


            model_position_total[
                (
                    model_name,
                    position
                )
            ] += 1


            if prediction == int(
                actual[position]
            ):

                model_correct[
                    model_name
                ] += 1

                model_position_correct[
                    (
                        model_name,
                        position
                    )
                ] += 1


        predictions = np.array(
            predictions
        )


        correct_positions = int(
            np.sum(
                predictions == actual
            )
        )


        if correct_positions == SEQ_LEN:

            model_exact_matches[
                model_name
            ] += 1


        model_correct_distribution[
            model_name
        ][
            correct_positions
        ] += 1


        row[
            f"{model_name}_prediction"
        ] = "".join(
            map(str, predictions)
        )


        row[
            f"{model_name}_correct"
        ] = correct_positions


    # ========================================================
    # ADAPTIVE MODEL
    # ========================================================
    #
    # Model selection occurs BEFORE seeing `actual`.
    #
    # ========================================================

    adaptive_predictions = []

    adaptive_selected_models = []


    for position in range(
        SEQ_LEN
    ):

        # ----------------------------------------------------
        # Select using ONLY train
        # ----------------------------------------------------

        best_model = choose_best_model(
            train,
            position
        )


        adaptive_model_usage[
            best_model
        ] += 1


        # ----------------------------------------------------
        # Predict using ONLY train
        # ----------------------------------------------------

        prediction = predict_with_model(
            train,
            position,
            best_model
        )


        prediction = int(
            prediction
        )


        adaptive_predictions.append(
            prediction
        )

        adaptive_selected_models.append(
            best_model
        )


        adaptive_total[
            position
        ] += 1


        # ----------------------------------------------------
        # Score AFTER prediction
        # ----------------------------------------------------

        if prediction == int(
            actual[position]
        ):

            adaptive_correct[
                position
            ] += 1


    adaptive_predictions = np.array(
        adaptive_predictions
    )


    adaptive_correct_positions = int(
        np.sum(
            adaptive_predictions == actual
        )
    )


    adaptive_correct_distribution[
        adaptive_correct_positions
    ] += 1


    if (
        adaptive_correct_positions
        ==
        SEQ_LEN
    ):

        adaptive_exact_matches += 1


    row[
        "adaptive_prediction"
    ] = "".join(
        map(str, adaptive_predictions)
    )


    row[
        "adaptive_correct"
    ] = adaptive_correct_positions


    for position in range(
        SEQ_LEN
    ):

        row[
            f"adaptive_model_{position + 1}"
        ] = adaptive_selected_models[
            position
        ]


    backtest_rows.append(
        row
    )


    # ========================================================
    # PROGRESS
    # ========================================================

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


    if (
        completed % 10 == 0
        or
        completed == total_tests
    ):

        print(
            f"Processed "
            f"{completed}/{total_tests}"
        )


# ============================================================
# SAVE BACKTEST
# ============================================================

backtest_df = pd.DataFrame(
    backtest_rows
)

backtest_df.to_csv(
    BACKTEST_FILE,
    index=False
)


# ============================================================
# MODEL COMPARISON
# ============================================================
#
# These fixed models were NEVER selected using the outer
# test results.
#
# They are therefore legitimate out-of-sample comparisons.
#
# ============================================================

comparison_rows = []


for model_name in MODEL_NAMES:

    correct = model_correct[
        model_name
    ]

    total = model_total[
        model_name
    ]

    accuracy = (
        correct / total
        if total > 0
        else 0
    )


    distribution = (
        model_correct_distribution[
            model_name
        ]
    )


    total_sequences = sum(
        distribution.values()
    )


    average_correct = (
        sum(
            correct_positions * count
            for correct_positions, count
            in distribution.items()
        )
        /
        total_sequences
    )


    comparison_rows.append({

        "model":
            model_name,

        "correct_positions":
            correct,

        "total_positions":
            total,

        "accuracy":
            accuracy,

        "accuracy_percent":
            accuracy * 100,

        "exact_17_matches":
            model_exact_matches[
                model_name
            ],

        "average_correct_per_sequence":
            average_correct
    })


# ============================================================
# ADAPTIVE RESULT
# ============================================================
#
# This is the IMPORTANT number.
#
# It is generated using nested walk-forward selection.
#
# Therefore it is the unbiased estimate of the adaptive
# strategy on the outer test period.
#
# ============================================================

adaptive_total_all = sum(
    adaptive_total.values()
)

adaptive_correct_all = sum(
    adaptive_correct.values()
)

adaptive_accuracy = (
    adaptive_correct_all
    /
    adaptive_total_all
)


adaptive_average_correct = (
    sum(
        correct_positions * count
        for correct_positions, count
        in adaptive_correct_distribution.items()
    )
    /
    sum(
        adaptive_correct_distribution.values()
    )
)


comparison_rows.append({

    "model":
        "ADAPTIVE_NESTED",

    "correct_positions":
        adaptive_correct_all,

    "total_positions":
        adaptive_total_all,

    "accuracy":
        adaptive_accuracy,

    "accuracy_percent":
        adaptive_accuracy * 100,

    "exact_17_matches":
        adaptive_exact_matches,

    "average_correct_per_sequence":
        adaptive_average_correct
})


comparison_df = pd.DataFrame(
    comparison_rows
)

comparison_df = comparison_df.sort_values(
    "accuracy",
    ascending=False
)


comparison_df.to_csv(
    MODEL_COMPARISON_FILE,
    index=False
)


# ============================================================
# PRINT COMPARISON
# ============================================================

print()
print("=" * 70)
print("LEAKAGE-FREE MODEL COMPARISON")
print("=" * 70)

print(
    comparison_df[
        [
            "model",
            "accuracy_percent",
            "average_correct_per_sequence",
            "exact_17_matches"
        ]
    ].to_string(
        index=False,
        formatters={
            "accuracy_percent":
                "{:.2f}".format,

            "average_correct_per_sequence":
                "{:.2f}".format
        }
    )
)


# ============================================================
# ADAPTIVE POSITION ACCURACY
# ============================================================

adaptive_position_rows = []


print()
print("=" * 70)
print("ADAPTIVE OUT-OF-SAMPLE POSITION ACCURACY")
print("=" * 70)


for position in range(
    SEQ_LEN
):

    correct = adaptive_correct[
        position
    ]

    total = adaptive_total[
        position
    ]

    accuracy = (
        correct / total
        if total > 0
        else 0
    )


    adaptive_position_rows.append({

        "position":
            position + 1,

        "correct":
            correct,

        "total":
            total,

        "accuracy":
            accuracy,

        "accuracy_percent":
            accuracy * 100
    })


    print(
        f"Position "
        f"{position + 1:2d}: "
        f"{correct:3d}/{total:3d} "
        f"= {accuracy * 100:6.2f}%"
    )


adaptive_position_df = pd.DataFrame(
    adaptive_position_rows
)

adaptive_position_df.to_csv(
    ADAPTIVE_POSITION_FILE,
    index=False
)


# ============================================================
# FIXED MODEL POSITION COMPARISON
# ============================================================
#
# This is descriptive only.
#
# We DO NOT use this table to claim an unbiased adaptive
# strategy.
#
# It simply shows how each fixed strategy performed.
#
# ============================================================

position_rows = []


for position in range(
    SEQ_LEN
):

    for model_name in MODEL_NAMES:

        correct = model_position_correct[
            (
                model_name,
                position
            )
        ]

        total = model_position_total[
            (
                model_name,
                position
            )
        ]

        accuracy = (
            correct / total
            if total > 0
            else 0
        )


        position_rows.append({

            "position":
                position + 1,

            "model":
                model_name,

            "correct":
                correct,

            "total":
                total,

            "accuracy":
                accuracy,

            "accuracy_percent":
                accuracy * 100
        })


position_comparison_df = pd.DataFrame(
    position_rows
)


position_comparison_df.to_csv(
    POSITION_COMPARISON_FILE,
    index=False
)


# ============================================================
# CHRONOLOGICAL PERIOD ANALYSIS
# ============================================================

print()
print("=" * 70)
print("CHRONOLOGICAL ADAPTIVE PERFORMANCE")
print("=" * 70)


test_count = len(
    backtest_df
)

period_size = max(
    1,
    test_count // 5
)


period_rows = []


for period in range(5):

    start = (
        period
        *
        period_size
    )


    if period == 4:

        end = test_count

    else:

        end = min(
            (period + 1)
            *
            period_size,
            test_count
        )


    period_data = backtest_df.iloc[
        start:end
    ]


    if len(period_data) == 0:

        continue


    correct = period_data[
        "adaptive_correct"
    ].sum()


    total = (
        len(period_data)
        *
        SEQ_LEN
    )


    accuracy = (
        correct
        /
        total
    )


    exact = (
        period_data[
            "adaptive_correct"
        ]
        ==
        SEQ_LEN
    ).sum()


    average_correct = (
        period_data[
            "adaptive_correct"
        ].mean()
    )


    period_rows.append({

        "period":
            period + 1,

        "sequences":
            len(period_data),

        "accuracy":
            accuracy,

        "accuracy_percent":
            accuracy * 100,

        "average_correct":
            average_correct,

        "exact_17":
            exact
    })


    print(
        f"Period {period + 1}: "
        f"{len(period_data)} sequences | "
        f"{accuracy * 100:.2f}% | "
        f"{average_correct:.2f}/17 | "
        f"exact={exact}"
    )


period_df = pd.DataFrame(
    period_rows
)

period_df.to_csv(
    PERIOD_FILE,
    index=False
)


# ============================================================
# ADAPTIVE DISTRIBUTION
# ============================================================

distribution_rows = []

total_adaptive_sequences = sum(
    adaptive_correct_distribution.values()
)


for correct_positions in range(
    SEQ_LEN + 1
):

    count = adaptive_correct_distribution.get(
        correct_positions,
        0
    )


    percentage = (
        count
        /
        total_adaptive_sequences
        *
        100
        if total_adaptive_sequences > 0
        else 0
    )


    distribution_rows.append({

        "correct_positions":
            correct_positions,

        "sequences":
            count,

        "percentage":
            percentage
    })


distribution_df = pd.DataFrame(
    distribution_rows
)


distribution_df.to_csv(
    DISTRIBUTION_FILE,
    index=False
)


# ============================================================
# THRESHOLD RESULTS
# ============================================================

print()
print("=" * 70)
print("ADAPTIVE THRESHOLD PERFORMANCE")
print("=" * 70)


for threshold in [
    5, 6, 7, 8, 9,
    10, 11, 12, 13,
    14, 15, 16, 17
]:

    count = sum(
        value
        for correct, value
        in adaptive_correct_distribution.items()
        if correct >= threshold
    )


    percentage = (
        count
        /
        total_adaptive_sequences
        *
        100
    )


    print(
        f"{threshold:2d}+/17 : "
        f"{count:3d} "
        f"({percentage:5.2f}%)"
    )


# ============================================================
# FINAL MODEL SELECTION
# ============================================================
#
# IMPORTANT:
#
# We are now AFTER the complete historical backtest.
#
# The outer test results are NEVER used to select a model
# for the OUTER TEST.
#
# For future prediction, however, all historical jackpots
# are now available.
#
# We can therefore perform model selection using the full
# available historical data.
#
# This selection is NOT part of the reported backtest.
#
# ============================================================

print()
print("=" * 70)
print("FINAL MODEL SELECTION FOR FUTURE PREDICTION")
print("=" * 70)


final_models = []

final_model_rows = []


for position in range(
    SEQ_LEN
):

    best_model = choose_best_model(
        X,
        position
    )


    final_models.append(
        best_model
    )


    final_model_rows.append({

        "position":
            position + 1,

        "selected_model":
            best_model
    })


    print(
        f"Position "
        f"{position + 1:2d}: "
        f"{best_model}"
    )


final_models_df = pd.DataFrame(
    final_model_rows
)


final_models_df.to_csv(
    FINAL_MODELS_FILE,
    index=False
)


# ============================================================
# FINAL NEXT 17 PREDICTION
# ============================================================
#
# Now use ALL historical jackpots.
#
# ============================================================

print()
print("=" * 70)
print("FINAL NEXT 17 PREDICTION")
print("=" * 70)


next_predictions = []

next_details = []


for position in range(
    SEQ_LEN
):

    model_name = final_models[
        position
    ]


    prediction = predict_with_model(
        X,
        position,
        model_name
    )


    prediction = int(
        prediction
    )


    next_predictions.append(
        prediction
    )


    next_details.append({

        "position":
            position + 1,

        "prediction":
            prediction,

        "outcome":
            OUTCOME_NAMES[
                prediction
            ],

        "model":
            model_name
    })


    print(
        f"{position + 1:2d}. "
        f"{prediction} = "
        f"{OUTCOME_NAMES[prediction]:5s} "
        f"({model_name})"
    )


# ============================================================
# FINAL SEQUENCE
# ============================================================

next_sequence = "".join(
    map(str, next_predictions)
)


print()
print(
    "NEXT SEQUENCE:"
)

print()
print(
    next_sequence
)


# ============================================================
# SAVE NEXT PREDICTION
# ============================================================

next_df = pd.DataFrame(
    next_details
)


next_df.to_csv(
    NEXT_FILE,
    index=False
)


# ============================================================
# SAVE MODEL
# ============================================================

model_package = {

    "sequence_length":
        SEQ_LEN,

    "initial_train_size":
        INITIAL_TRAIN_SIZE,

    "recent_windows":
        RECENT_WINDOWS,

    "ngram_orders":
        NGRAM_ORDERS,

    "validation_fraction":
        VALIDATION_FRACTION,

    "candidate_models":
        MODEL_NAMES,

    "historical_sequences":
        sequences,

    "historical_matrix":
        X,

    "final_models":
        final_models,

    "next_prediction":
        next_sequence,

    "outcome_mapping":
        OUTCOME_NAMES,

    # Explicitly record that outer evaluation is nested
    "evaluation_method":
        "nested_expanding_walk_forward",

    "outer_test_start":
        INITIAL_TRAIN_SIZE
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
# FINAL REPORT
# ============================================================

print()
print("=" * 70)
print("FINAL REPORT")
print("=" * 70)


print()
print(
    f"Nested adaptive accuracy: "
    f"{adaptive_accuracy * 100:.2f}%"
)


print(
    f"Average correct per jackpot: "
    f"{adaptive_average_correct:.2f}/17"
)


print(
    f"Exact 17/17 matches: "
    f"{adaptive_exact_matches}"
)


# ------------------------------------------------------------
# Baseline comparison
# ------------------------------------------------------------

baseline_df = comparison_df[
    comparison_df["model"] != "ADAPTIVE_NESTED"
]


best_baseline = baseline_df.iloc[
    0
]


print()
print(
    f"Best fixed strategy: "
    f"{best_baseline['model']}"
)


print(
    f"Best fixed strategy accuracy: "
    f"{best_baseline['accuracy_percent']:.2f}%"
)


difference = (
    adaptive_accuracy
    -
    best_baseline["accuracy"]
)


print(
    f"Adaptive advantage over best "
    f"fixed strategy: "
    f"{difference * 100:+.2f} percentage points"
)


print()
print(
    "NEXT PREDICTION:"
)

print(
    next_sequence
)


print()
print("=" * 70)
print("FILES CREATED")
print("=" * 70)

files = [

    INVALID_FILE,

    BACKTEST_FILE,

    MODEL_COMPARISON_FILE,

    POSITION_COMPARISON_FILE,

    ADAPTIVE_POSITION_FILE,

    FINAL_MODELS_FILE,

    PERIOD_FILE,

    DISTRIBUTION_FILE,

    NEXT_FILE,

    MODEL_FILE
]


for number, filename in enumerate(
    files,
    1
):

    print(
        f"{number}. {filename}"
    )


print()
print("=" * 70)
print("DONE")
print("=" * 70)
