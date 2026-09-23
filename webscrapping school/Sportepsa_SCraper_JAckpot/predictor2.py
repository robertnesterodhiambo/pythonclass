import pandas as pd
import numpy as np
import pickle

from collections import Counter, defaultdict
from pathlib import Path

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline


# ============================================================
# CONFIGURATION
# ============================================================

CSV_FILE = "jackpot_groups.csv"
COLUMN = "outcome_sequence"

SEQ_LEN = 17

# Initial outer training history
INITIAL_TRAIN_SIZE = 100

# Recent windows
RECENT_WINDOWS = [20, 50, 100]

# N-gram orders
NGRAM_ORDERS = [2, 3, 4]

# Inner validation
VALIDATION_FRACTION = 0.30

# Minimum observations before logistic regression
MIN_LOGISTIC_TRAIN = 30

# Ensemble components
COMPONENTS = [
    "recent_frequency",
    "markov",
    "ngram_2",
    "ngram_3",
    "ngram_4",
    "logistic",
]

# Candidate recent-frequency windows
ENSEMBLE_RECENT_WINDOWS = [20, 50, 100]

# Candidate n-gram windows
ENSEMBLE_NGRAM_WINDOW = 50


# ============================================================
# OUTPUT FILES
# ============================================================

OUTPUTS = {
    "invalid": "invalid_sequences.csv",
    "backtest": "ensemble_walk_forward_predictions.csv",
    "comparison": "ensemble_model_comparison.csv",
    "position": "ensemble_position_accuracy.csv",
    "weights": "ensemble_weights_by_position.csv",
    "periods": "ensemble_period_performance.csv",
    "distribution": "ensemble_prediction_distribution.csv",
    "next": "next_17_ensemble_prediction.csv",
    "model": "logistic_ensemble_model.pkl",
}


# ============================================================
# OUTCOME NAMES
# ============================================================

OUTCOME_NAMES = {
    0: "Draw",
    1: "Home",
    2: "Away",
}


# ============================================================
# SEQUENCE VALIDATION
# ============================================================

def normalize_sequence(value):

    if pd.isna(value):
        return None

    value = str(value).strip()

    if len(value) != SEQ_LEN:
        return None

    if not all(char in "012" for char in value):
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

df["clean_sequence"] = df[COLUMN].apply(
    normalize_sequence
)

valid_df = df[
    df["clean_sequence"].notna()
].copy()

invalid_df = df[
    df["clean_sequence"].isna()
].copy()

print(f"Original rows: {len(df)}")
print(f"Valid 17-outcome sequences: {len(valid_df)}")
print(f"Invalid sequences: {len(invalid_df)}")


# ============================================================
# SAVE INVALID
# ============================================================

if len(invalid_df) > 0:

    invalid_df.to_csv(
        OUTPUTS["invalid"],
        index=False
    )

    print(
        f"Invalid rows saved to "
        f"{OUTPUTS['invalid']}"
    )


# ============================================================
# CHRONOLOGICAL ORDER
# ============================================================
#
# CSV:
# TOP    = newest
# BOTTOM = oldest
#
# Therefore reverse.
# ============================================================

sequences = list(
    reversed(
        valid_df["clean_sequence"].tolist()
    )
)

if len(sequences) <= INITIAL_TRAIN_SIZE:

    raise ValueError(
        f"Need more than {INITIAL_TRAIN_SIZE} "
        f"valid sequences."
    )

print()
print("Chronological order:")
print(f"Oldest: {sequences[0]}")
print(f"Latest: {sequences[-1]}")


# ============================================================
# MATRIX
# ============================================================

X = np.array(
    [
        [int(char) for char in sequence]
        for sequence in sequences
    ],
    dtype=int
)

print()
print(f"Sequence matrix: {X.shape}")


# ============================================================
# OVERALL FREQUENCY
# ============================================================

print()
print("=" * 70)
print("OVERALL OUTCOME FREQUENCY")
print("=" * 70)

all_values = X.flatten()

overall_counts = Counter(all_values)

for outcome in [0, 1, 2]:

    count = overall_counts[outcome]

    percentage = (
        count / len(all_values) * 100
    )

    print(
        f"{outcome} = "
        f"{OUTCOME_NAMES[outcome]:5s} : "
        f"{count:5d} "
        f"({percentage:.2f}%)"
    )


# ============================================================
# UTILITY
# ============================================================

def normalize_probabilities(scores):

    """
    Convert dictionary of scores into
    probabilities that sum to 1.
    """

    result = np.array([
        scores.get(0, 0.0),
        scores.get(1, 0.0),
        scores.get(2, 0.0)
    ], dtype=float)

    total = result.sum()

    if total <= 0:

        return np.array(
            [1 / 3, 1 / 3, 1 / 3]
        )

    return result / total


# ============================================================
# POSITION FREQUENCY PROBABILITY
# ============================================================

def position_frequency_proba(
    train,
    position
):

    values = train[:, position]

    counts = Counter(values)

    total = len(values)

    probabilities = np.array([
        counts.get(0, 0) / total,
        counts.get(1, 0) / total,
        counts.get(2, 0) / total
    ])

    return probabilities


# ============================================================
# RECENT FREQUENCY PROBABILITY
# ============================================================

def recent_frequency_proba(
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

    total = len(values)

    return np.array([
        counts.get(0, 0) / total,
        counts.get(1, 0) / total,
        counts.get(2, 0) / total
    ])


# ============================================================
# MARKOV PROBABILITY
# ============================================================

def markov_proba(
    train,
    position
):

    if position == 0:

        return position_frequency_proba(
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

    if latest_previous not in transitions:

        return position_frequency_proba(
            train,
            position
        )

    counts = transitions[
        latest_previous
    ]

    return normalize_probabilities(
        counts
    )


# ============================================================
# N-GRAM PROBABILITY
# ============================================================

def ngram_proba(
    train,
    position,
    order,
    window=None
):

    if position < order:

        return position_frequency_proba(
            train,
            position
        )

    if window is not None:

        window = min(
            window,
            len(train)
        )

        data = train[-window:]

    else:

        data = train

    model = defaultdict(
        Counter
    )

    for row in data:

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
        for x in data[
            -1,
            position - order:
            position
        ]
    )

    if latest_context not in model:

        return position_frequency_proba(
            data,
            position
        )

    return normalize_probabilities(
        model[
            latest_context
        ]
    )


# ============================================================
# LOGISTIC REGRESSION FEATURES
# ============================================================

def build_logistic_dataset(
    train,
    position
):

    """
    Build supervised examples.

    Features:

        previous 1 outcome
        previous 2 outcomes
        previous 3 outcomes
        previous 4 outcomes

    Target:

        current position outcome
    """

    rows = []
    targets = []

    MIN_CONTEXT = 4

    if len(train) <= MIN_CONTEXT:

        return None, None

    for i in range(
        MIN_CONTEXT,
        len(train)
    ):

        row = train[i]

        features = []

        # Previous outcomes at this position
        for lag in range(
            1,
            MIN_CONTEXT + 1
        ):

            features.append(
                int(
                    train[
                        i - lag,
                        position
                    ]
                )
            )

        # Previous positions from current sequence
        # if available
        for lag in range(
            1,
            min(position, 4) + 1
        ):

            features.append(
                int(
                    row[
                        position - lag
                    ]
                )
            )

        rows.append(
            features
        )

        targets.append(
            int(
                row[position]
            )
        )

    return (
        np.array(rows),
        np.array(targets)
    )


# ============================================================
# LOGISTIC REGRESSION PROBABILITY
# ============================================================

def logistic_proba(
    train,
    position
):

    X_train, y_train = (
        build_logistic_dataset(
            train,
            position
        )
    )

    if X_train is None:

        return position_frequency_proba(
            train,
            position
        )

    if len(X_train) < MIN_LOGISTIC_TRAIN:

        return position_frequency_proba(
            train,
            position
        )

    unique_classes = np.unique(
        y_train
    )

    if len(unique_classes) < 2:

        return position_frequency_proba(
            train,
            position
        )

    try:

        model = LogisticRegression(
            multi_class="multinomial",
            max_iter=1000,
            C=0.5
        )

        model.fit(
            X_train,
            y_train
        )

        # Build features for the next prediction

        features = []

        for lag in range(
            1,
            5
        ):

            features.append(
                int(
                    train[
                        -lag,
                        position
                    ]
                )
            )

        for lag in range(
            1,
            min(position, 4) + 1
        ):

            features.append(
                int(
                    train[
                        -1,
                        position - lag
                    ]
                )
            )

        latest_features = np.array(
            [features]
        )

        probabilities = (
            model.predict_proba(
                latest_features
            )[0]
        )

        result = np.zeros(3)

        for class_value, probability in zip(
            model.classes_,
            probabilities
        ):

            result[
                int(class_value)
            ] = probability

        return result

    except Exception:

        return position_frequency_proba(
            train,
            position
        )


# ============================================================
# GET ALL COMPONENT PROBABILITIES
# ============================================================

def get_component_probabilities(
    train,
    position
):

    component_probabilities = {}

    # --------------------------------------------------------
    # RECENT FREQUENCY
    # --------------------------------------------------------

    recent_predictions = []

    for window in (
        ENSEMBLE_RECENT_WINDOWS
    ):

        recent_predictions.append(
            recent_frequency_proba(
                train,
                position,
                window
            )
        )

    component_probabilities[
        "recent_frequency"
    ] = np.mean(
        recent_predictions,
        axis=0
    )

    # --------------------------------------------------------
    # MARKOV
    # --------------------------------------------------------

    component_probabilities[
        "markov"
    ] = markov_proba(
        train,
        position
    )

    # --------------------------------------------------------
    # N-GRAMS
    # --------------------------------------------------------

    for order in NGRAM_ORDERS:

        component_probabilities[
            f"ngram_{order}"
        ] = ngram_proba(
            train,
            position,
            order,
            ENSEMBLE_NGRAM_WINDOW
        )

    # --------------------------------------------------------
    # LOGISTIC
    # --------------------------------------------------------

    component_probabilities[
        "logistic"
    ] = logistic_proba(
        train,
        position
    )

    return component_probabilities


# ============================================================
# ENSEMBLE PREDICTION
# ============================================================

def ensemble_predict(
    train,
    position,
    weights=None
):

    probabilities = (
        get_component_probabilities(
            train,
            position
        )
    )

    if weights is None:

        weights = {
            component: 1.0
            for component in COMPONENTS
        }

    final_probability = np.zeros(
        3
    )

    total_weight = 0.0

    for component in COMPONENTS:

        probability = probabilities[
            component
        ]

        weight = weights.get(
            component,
            0.0
        )

        final_probability += (
            probability
            *
            weight
        )

        total_weight += weight

    if total_weight <= 0:

        final_probability = (
            np.ones(3)
            /
            3
        )

    else:

        final_probability /= (
            total_weight
        )

    prediction = int(
        np.argmax(
            final_probability
        )
    )

    return (
        prediction,
        final_probability,
        probabilities
    )


# ============================================================
# FIND BEST ENSEMBLE WEIGHTS
# ============================================================

def choose_ensemble_weights(
    train,
    position
):

    """
    Leakage-safe inner validation.

    Candidate weight configurations are tested
    only against historical data inside `train`.
    """

    n = len(train)

    if n < 60:

        return {
            component: 1.0
            for component in COMPONENTS
        }

    validation_size = max(
        15,
        int(
            n *
            VALIDATION_FRACTION
        )
    )

    validation_start = (
        n
        -
        validation_size
    )

    # --------------------------------------------------------
    # WEIGHT CONFIGURATIONS
    # --------------------------------------------------------

    weight_configs = {

        "equal": {
            "recent_frequency": 1.0,
            "markov": 1.0,
            "ngram_2": 1.0,
            "ngram_3": 1.0,
            "ngram_4": 1.0,
            "logistic": 1.0,
        },

        "logistic_heavy": {
            "recent_frequency": 1.0,
            "markov": 1.0,
            "ngram_2": 1.0,
            "ngram_3": 1.0,
            "ngram_4": 1.0,
            "logistic": 2.0,
        },

        "recent_heavy": {
            "recent_frequency": 2.0,
            "markov": 1.0,
            "ngram_2": 1.0,
            "ngram_3": 1.0,
            "ngram_4": 1.0,
            "logistic": 1.0,
        },

        "markov_heavy": {
            "recent_frequency": 1.0,
            "markov": 2.0,
            "ngram_2": 1.0,
            "ngram_3": 1.0,
            "ngram_4": 1.0,
            "logistic": 1.0,
        },

        "ngram_heavy": {
            "recent_frequency": 1.0,
            "markov": 1.0,
            "ngram_2": 2.0,
            "ngram_3": 2.0,
            "ngram_4": 2.0,
            "logistic": 1.0,
        },

        "simple": {
            "recent_frequency": 2.0,
            "markov": 2.0,
            "ngram_2": 1.0,
            "ngram_3": 1.0,
            "ngram_4": 1.0,
            "logistic": 1.0,
        },

        "logistic_recent": {
            "recent_frequency": 2.0,
            "markov": 1.0,
            "ngram_2": 1.0,
            "ngram_3": 1.0,
            "ngram_4": 1.0,
            "logistic": 2.0,
        },

        "markov_logistic": {
            "recent_frequency": 1.0,
            "markov": 2.0,
            "ngram_2": 1.0,
            "ngram_3": 1.0,
            "ngram_4": 1.0,
            "logistic": 2.0,
        }
    }

    scores = {}

    for name, weights in weight_configs.items():

        correct = 0
        total = 0

        for index in range(
            validation_start,
            n
        ):

            inner_train = train[:index]

            actual = int(
                train[
                    index,
                    position
                ]
            )

            prediction, _, _ = (
                ensemble_predict(
                    inner_train,
                    position,
                    weights
                )
            )

            if prediction == actual:

                correct += 1

            total += 1

        scores[name] = (
            correct / total
            if total > 0
            else 0
        )

    best_name = max(
        scores,
        key=scores.get
    )

    return (
        weight_configs[best_name],
        best_name,
        scores
    )


# ============================================================
# LOAD DATA COMPLETE
# ============================================================

print()
print("=" * 70)
print("ENSEMBLE CONFIGURATION")
print("=" * 70)

print(
    "Components:"
)

for component in COMPONENTS:

    print(
        f"  - {component}"
    )


# ============================================================
# OUTER WALK-FORWARD BACKTEST
# ============================================================

print()
print("=" * 70)
print("NESTED LEAKAGE-FREE ENSEMBLE BACKTEST")
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

ensemble_correct = 0
ensemble_total = 0

position_correct = Counter()
position_total = Counter()

exact_matches = 0

correct_distribution = Counter()

weight_selection_count = Counter()

period_records = []


# ============================================================
# OUTER LOOP
# ============================================================

for test_index in range(
    INITIAL_TRAIN_SIZE,
    len(X)
):

    train = X[:test_index]

    actual = X[test_index]

    actual_sequence = "".join(
        map(str, actual)
    )

    row = {
        "historical_index":
            test_index,

        "actual_sequence":
            actual_sequence
    }

    predictions = []

    position_details = []

    # --------------------------------------------------------
    # EACH POSITION
    # --------------------------------------------------------

    for position in range(
        SEQ_LEN
    ):

        # -----------------------------------------------
        # INNER MODEL SELECTION
        # -----------------------------------------------

        weights, weight_name, _ = (
            choose_ensemble_weights(
                train,
                position
            )
        )

        weight_selection_count[
            weight_name
        ] += 1

        # -----------------------------------------------
        # OUTER PREDICTION
        # -----------------------------------------------

        prediction, probability, components = (
            ensemble_predict(
                train,
                position,
                weights
            )
        )

        predictions.append(
            prediction
        )

        actual_value = int(
            actual[position]
        )

        position_total[
            position
        ] += 1

        ensemble_total += 1

        if prediction == actual_value:

            position_correct[
                position
            ] += 1

            ensemble_correct += 1

        position_details.append({

            "position":
                position + 1,

            "prediction":
                prediction,

            "actual":
                actual_value,

            "correct":
                prediction == actual_value,

            "weight_config":
                weight_name,

            "draw_probability":
                probability[0],

            "home_probability":
                probability[1],

            "away_probability":
                probability[2]
        })

        # Save probability information
        row[
            f"position_{position + 1}_draw_prob"
        ] = probability[0]

        row[
            f"position_{position + 1}_home_prob"
        ] = probability[1]

        row[
            f"position_{position + 1}_away_prob"
        ] = probability[2]

        row[
            f"position_{position + 1}_model"
        ] = weight_name

        row[
            f"position_{position + 1}_prediction"
        ] = prediction

        row[
            f"position_{position + 1}_actual"
        ] = actual_value

    # --------------------------------------------------------
    # COMPLETE SEQUENCE
    # --------------------------------------------------------

    prediction_sequence = "".join(
        map(str, predictions)
    )

    correct_positions = int(
        np.sum(
            np.array(predictions)
            ==
            actual
        )
    )

    row[
        "ensemble_prediction"
    ] = prediction_sequence

    row[
        "correct_positions"
    ] = correct_positions

    row[
        "sequence_accuracy"
    ] = (
        correct_positions
        /
        SEQ_LEN
    )

    correct_distribution[
        correct_positions
    ] += 1

    if correct_positions == SEQ_LEN:

        exact_matches += 1

    backtest_rows.append(
        row
    )

    # --------------------------------------------------------
    # PROGRESS
    # --------------------------------------------------------

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
# BACKTEST DATAFRAME
# ============================================================

backtest_df = pd.DataFrame(
    backtest_rows
)

backtest_df.to_csv(
    OUTPUTS["backtest"],
    index=False
)


# ============================================================
# OVERALL RESULTS
# ============================================================

ensemble_accuracy = (
    ensemble_correct
    /
    ensemble_total
)

average_correct = (
    backtest_df[
        "correct_positions"
    ].mean()
)


print()
print("=" * 70)
print("ENSEMBLE OUT-OF-SAMPLE RESULTS")
print("=" * 70)

print(
    f"Accuracy: "
    f"{ensemble_accuracy * 100:.2f}%"
)

print(
    f"Average correct: "
    f"{average_correct:.2f}/17"
)

print(
    f"Exact 17/17: "
    f"{exact_matches}"
)


# ============================================================
# POSITION ACCURACY
# ============================================================

print()
print("=" * 70)
print("ENSEMBLE POSITION ACCURACY")
print("=" * 70)

position_rows = []

for position in range(
    SEQ_LEN
):

    accuracy = (
        position_correct[position]
        /
        position_total[position]
    )

    position_rows.append({

        "position":
            position + 1,

        "correct":
            position_correct[position],

        "total":
            position_total[position],

        "accuracy":
            accuracy,

        "accuracy_percent":
            accuracy * 100
    })

    print(
        f"Position "
        f"{position + 1:2d}: "
        f"{position_correct[position]:3d}/"
        f"{position_total[position]:3d} = "
        f"{accuracy * 100:.2f}%"
    )


position_df = pd.DataFrame(
    position_rows
)

position_df.to_csv(
    OUTPUTS["position"],
    index=False
)


# ============================================================
# WEIGHT CONFIGURATION USAGE
# ============================================================

print()
print("=" * 70)
print("ENSEMBLE WEIGHT CONFIGURATION USAGE")
print("=" * 70)

for name, count in sorted(
    weight_selection_count.items(),
    key=lambda x: x[1],
    reverse=True
):

    print(
        f"{name:20s}: "
        f"{count}"
    )


# ============================================================
# SAVE WEIGHT USAGE
# ============================================================

weight_rows = []

for name, count in weight_selection_count.items():

    weight_rows.append({

        "weight_configuration":
            name,

        "times_selected":
            count
    })

pd.DataFrame(
    weight_rows
).to_csv(
    OUTPUTS["weights"],
    index=False
)


# ============================================================
# CORRECT POSITION DISTRIBUTION
# ============================================================

print()
print("=" * 70)
print("ENSEMBLE CORRECT-POSITION DISTRIBUTION")
print("=" * 70)

distribution_rows = []

total_sequences = len(
    backtest_df
)

for correct_positions in range(
    SEQ_LEN + 1
):

    count = correct_distribution.get(
        correct_positions,
        0
    )

    percentage = (
        count
        /
        total_sequences
        *
        100
    )

    distribution_rows.append({

        "correct_positions":
            correct_positions,

        "sequences":
            count,

        "percentage":
            percentage
    })

    if count > 0:

        print(
            f"{correct_positions:2d}/17 : "
            f"{count:3d} "
            f"({percentage:.2f}%)"
        )


pd.DataFrame(
    distribution_rows
).to_csv(
    OUTPUTS["distribution"],
    index=False
)


# ============================================================
# THRESHOLD PERFORMANCE
# ============================================================

print()
print("=" * 70)
print("ENSEMBLE THRESHOLD PERFORMANCE")
print("=" * 70)

for threshold in range(
    5,
    18
):

    count = sum(
        value
        for correct, value
        in correct_distribution.items()
        if correct >= threshold
    )

    percentage = (
        count
        /
        total_sequences
        *
        100
    )

    print(
        f"{threshold:2d}+/17 : "
        f"{count:3d} "
        f"({percentage:.2f}%)"
    )


# ============================================================
# CHRONOLOGICAL PERFORMANCE
# ============================================================

print()
print("=" * 70)
print("CHRONOLOGICAL ENSEMBLE PERFORMANCE")
print("=" * 70)

period_rows = []

test_count = len(
    backtest_df
)

period_size = max(
    1,
    test_count // 5
)

for period in range(5):

    start = (
        period *
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

    period_data = (
        backtest_df.iloc[
            start:end
        ]
    )

    if len(period_data) == 0:

        continue

    total_correct = (
        period_data[
            "correct_positions"
        ].sum()
    )

    total_possible = (
        len(period_data)
        *
        SEQ_LEN
    )

    accuracy = (
        total_correct
        /
        total_possible
    )

    exact = (
        period_data[
            "correct_positions"
        ]
        ==
        SEQ_LEN
    ).sum()

    average = (
        period_data[
            "correct_positions"
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
            average,

        "exact_17":
            exact
    })

    print(
        f"Period {period + 1}: "
        f"{len(period_data)} sequences | "
        f"{accuracy * 100:.2f}% | "
        f"{average:.2f}/17 | "
        f"exact={exact}"
    )


period_df = pd.DataFrame(
    period_rows
)

period_df.to_csv(
    OUTPUTS["periods"],
    index=False
)


# ============================================================
# FINAL TRAINING
# ============================================================

print()
print("=" * 70)
print("FINAL ENSEMBLE TRAINING")
print("=" * 70)

final_predictions = []
final_details = []
final_weights = {}


for position in range(
    SEQ_LEN
):

    # --------------------------------------------------------
    # Choose weights using ALL historical data
    # --------------------------------------------------------

    weights, weight_name, validation_scores = (
        choose_ensemble_weights(
            X,
            position
        )
    )

    final_weights[
        position
    ] = {
        "configuration":
            weight_name,

        "weights":
            weights,

        "validation_scores":
            validation_scores
    }

    # --------------------------------------------------------
    # Predict future sequence
    # --------------------------------------------------------

    prediction, probability, components = (
        ensemble_predict(
            X,
            position,
            weights
        )
    )

    final_predictions.append(
        prediction
    )

    final_details.append({

        "position":
            position + 1,

        "prediction":
            prediction,

        "outcome":
            OUTCOME_NAMES[prediction],

        "probability_draw":
            probability[0],

        "probability_home":
            probability[1],

        "probability_away":
            probability[2],

        "selected_configuration":
            weight_name,

        "recent_frequency_probability":
            components[
                "recent_frequency"
            ][prediction],

        "markov_probability":
            components[
                "markov"
            ][prediction],

        "ngram_2_probability":
            components[
                "ngram_2"
            ][prediction],

        "ngram_3_probability":
            components[
                "ngram_3"
            ][prediction],

        "ngram_4_probability":
            components[
                "ngram_4"
            ][prediction],

        "logistic_probability":
            components[
                "logistic"
            ][prediction]
    })

    print(
        f"Position "
        f"{position + 1:2d}: "
        f"{prediction} = "
        f"{OUTCOME_NAMES[prediction]:5s} | "
        f"{weight_name:20s} | "
        f"D={probability[0]:.3f} "
        f"H={probability[1]:.3f} "
        f"A={probability[2]:.3f}"
    )


# ============================================================
# FINAL SEQUENCE
# ============================================================

next_sequence = "".join(
    map(str, final_predictions)
)


print()
print("=" * 70)
print("FINAL NEXT 17-OUTCOME ENSEMBLE PREDICTION")
print("=" * 70)

print()
print(next_sequence)

print()

for detail in final_details:

    print(
        f"{detail['position']:2d}. "
        f"{detail['prediction']} = "
        f"{detail['outcome']:5s} "
        f"| D={detail['probability_draw']:.3f} "
        f"H={detail['probability_home']:.3f} "
        f"A={detail['probability_away']:.3f}"
    )


# ============================================================
# SAVE NEXT PREDICTION
# ============================================================

next_df = pd.DataFrame(
    final_details
)

next_df.to_csv(
    OUTPUTS["next"],
    index=False
)


# ============================================================
# SAVE MODEL PACKAGE
# ============================================================

model_package = {

    "model_type":
        "nested_probability_ensemble",

    "components":
        COMPONENTS,

    "sequence_length":
        SEQ_LEN,

    "initial_train_size":
        INITIAL_TRAIN_SIZE,

    "recent_windows":
        RECENT_WINDOWS,

    "ngram_orders":
        NGRAM_ORDERS,

    "ensemble_recent_windows":
        ENSEMBLE_RECENT_WINDOWS,

    "ensemble_ngram_window":
        ENSEMBLE_NGRAM_WINDOW,

    "validation_fraction":
        VALIDATION_FRACTION,

    "historical_sequences":
        sequences,

    "historical_matrix":
        X,

    "final_weights":
        final_weights,

    "next_prediction":
        next_sequence,

    "outcome_mapping":
        OUTCOME_NAMES,

    "backtest_accuracy":
        ensemble_accuracy,

    "backtest_average_correct":
        average_correct,

    "backtest_exact_17":
        exact_matches,

    "evaluation_method":
        "nested_expanding_walk_forward"
}


with open(
    OUTPUTS["model"],
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
    f"Nested ensemble accuracy: "
    f"{ensemble_accuracy * 100:.2f}%"
)

print(
    f"Average correct per sequence: "
    f"{average_correct:.2f}/17"
)

print(
    f"Exact 17/17 matches: "
    f"{exact_matches}"
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

for number, filename in enumerate(
    OUTPUTS.values(),
    start=1
):

    print(
        f"{number}. {filename}"
    )

print()
print("=" * 70)
print("DONE")
print("=" * 70)

