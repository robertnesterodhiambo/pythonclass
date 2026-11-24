import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <div align="center" style=" font-size: 80%; text-align: center; margin: 0 auto">
    <img src="https://raw.githubusercontent.com/Explore-AI/Pictures/refs/heads/master/Python-Notebook-Banners/Code_challenge.png"  style="display: block; margin-left: auto; margin-right: auto;";/>
    </div>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Understanding the Yield — Part A
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Data validation is complete; now it's time to predict. To help farmers plan ahead, the Ministry needs models that forecast crop yield. In this project, you build the foundation of supervised machine learning using scikit-learn to fit simple linear regressions. You will calculate Pearson correlation coefficients, isolate rainfall drivers using Least Squares, implement an 80/20 train-test split, and run residual diagnostics to validate model assumptions. It is the exact predictive baseline that the rest of the regression work builds on.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **This challenge is not graded.** It is here to build your footing before the graded work begins.

    ### Instructions

    - Do not add or remove cells in this notebook.
    - Answer the questions according to the specifications provided.
    - Use the provided **Expected output** blocks and test cells to verify your work before continuing.
    - Use the tools introduced in this course: pandas, NumPy, scikit-learn, statsmodels, and Matplotlib — for simple and multiple linear regression, model evaluation (R², MAE, MSE, RMSE), regularisation, and model persistence.
    - The use of StackOverflow, Google, Generative AI tools, and any other online resources is permitted. Use AI to help you understand — not to shortcut the thinking. [Read the honor code here](https://drive.google.com/file/d/1atFOPUQRLz5slb4Q1ASXh8QQfKyXVqrw/preview).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The Ministry of Agriculture's audit concluded with a clear message: the field data is sound, the weather stations are calibrated, and the pipeline is production-ready. Now comes the harder question.

    Sanaa drops a printout on your desk — a summary of the Maji Ndogo farm survey. "We can validate the data all we like," she says. "But what the farmers actually need is a prediction. If I can tell a maize farmer in Kilimani that his expected yield next season is 4.2 tonnes per hectare, he can plan accordingly. If I can tell the ministry which environmental factors drive yield the most, they can direct investment."

    She taps the printout. "We have weather readings, soil measurements, plot sizes, and three seasons of yield records. Build me a model."

    This is where data science becomes machine learning. You are not just describing what happened — you are learning from it to predict what will happen next. In Part A, you will work with a single predictor at a time: the simplest possible model, but the essential foundation. By the end of this notebook you will have:

    - Visualized and quantified linear relationships between individual farm features and crop yield.
    - Fit your first regression model using the Least Squares method in scikit-learn.
    - Evaluated model performance using R-squared, MAE, MSE, and RMSE.
    - Used a train-test split to confirm that performance generalizes to unseen fields.
    - Diagnosed model assumptions through residual analysis.

    > **AI assist:** This module introduces the full supervised learning workflow for the first time. Use an AI assistant as a thinking partner. Good prompts to try: *"Explain the intuition behind R-squared in plain language — what does 0.03 actually mean?"* *"What is the difference between MAE and RMSE and when would you prefer one over the other?"*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Data Setup

    ### Data Dictionary

    The dataset is loaded directly from the Maji Ndogo farm survey database — the same source used throughout the programme. Each row represents one field.

    **Target variable**
    - `Standard_yield`: The normalized crop yield score for each field, ranging from 0 to 1. This is what we are predicting.

    **Environmental features**
    - `Rainfall`: Annual rainfall in mm (Float).
    - `Ave_temps`: Average temperature in degrees Celsius (Float).
    - `Elevation`: Field elevation above sea level in meters (Float).
    - `Slope`: Slope of the land in degrees (Float).

    **Soil features**
    - `Soil_fertility`: Normalized fertility index, 0–1 (Float).
    - `pH`: Soil pH level (Float).
    - `Pollution_level`: Normalized pollution index, 0–1 (Float).

    **Farm features**
    - `Plot_size`: Field area in hectares (Float).
    - `Crop_type`: Type of crop grown (String — categorical).
    - `Location`: Province where the field is located (String — categorical).
    - `Annual_yield`: Raw annual yield in tonnes (Float).

    **Setup:** Run the cell below to load the data before attempting any challenge.

    **The database is bundled with this notebook** as `Maji_Ndogo_farm_survey_small.db` — the setup cell below reads it directly, offline. You do not need to download anything.
    """)
    return


@app.cell
def _():
    import sqlite3
    import pandas as pd
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')  # headless rendering for test environments
    import matplotlib.pyplot as plt
    from scipy.stats import pearsonr
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
    from sklearn.model_selection import train_test_split

    # Load the Maji Ndogo farm survey from the SQLite database
    conn = sqlite3.connect('Maji_Ndogo_farm_survey_small.db')
    sql_query = """
    SELECT *
    FROM geographic_features
    LEFT JOIN weather_features USING (Field_ID)
    LEFT JOIN soil_and_crop_features USING (Field_ID)
    LEFT JOIN farm_management_features USING (Field_ID)
    """
    df = pd.read_sql_query(sql_query, conn)
    conn.close()

    # Standard cleaning pipeline from earlier in the programme
    df.rename(columns={'Annual_yield': 'Crop_type_Temp', 'Crop_type': 'Annual_yield'}, inplace=True)
    df.rename(columns={'Crop_type_Temp': 'Crop_type'}, inplace=True)
    df['Elevation'] = df['Elevation'].abs()
    corrections = {'cassaval': 'cassava', 'wheatn': 'wheat', 'teaa': 'tea'}
    df['Crop_type'] = df['Crop_type'].apply(lambda c: corrections.get(c.strip(), c.strip()))
    df = df.dropna()

    print(f'Shape: {df.shape}')
    print(df[['Rainfall', 'Ave_temps', 'Standard_yield']].head())
    return (
        LinearRegression,
        df,
        mean_absolute_error,
        mean_squared_error,
        np,
        pearsonr,
        plt,
        r2_score,
        train_test_split,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Challenge 1: Visualizing the Relationship

    Every predictive model starts with a question: *Is there even a relationship to model?*

    Before fitting any line, we need to look at the data. We have many features, but let's begin with `Ave_temps` — average temperature across the field's growing season. Temperature directly affects crop growth rates, photosynthesis efficiency, and evapotranspiration. It's a logical first candidate.

    ### Task
     Create a function named `temp_yield_correlation` that:
    - Takes a DataFrame and the names of the temperature column and the yield column as parameters.
    - Generates a scatter plot visualizing the relationship between the two variables, with axis labels and a title.
    - Calculates the Pearson correlation coefficient between them.
    - Returns the Pearson correlation coefficient as a float.

    **Note:**
    - Use `matplotlib` for plotting.
    - Use `scipy.stats.pearsonr` or `numpy.corrcoef` for the correlation coefficient.
    - Ensure your function returns the Pearson correlation coefficient as a float.

    ### Expected Output
    ```
    Correlation: 0.006785950289020154
    ```
    """)
    return


@app.cell
def _(pearsonr, plt):
    ### START FUNCTION
    def temp_yield_correlation(df, temp_col, yield_col):
        # Scatter plot of temperature vs yield
        plt.figure(figsize=(8, 5))
        plt.scatter(df[temp_col], df[yield_col], alpha=0.5)
        plt.xlabel('Average Temperature (°C)')
        plt.ylabel('Standard Yield')
        plt.title('Average Temperature vs Standard Yield')
        plt.show()

        # Pearson correlation coefficient
        corr, _p_value = pearsonr(df[temp_col], df[yield_col])
        return float(corr)
    ### END FUNCTION
    return (temp_yield_correlation,)


@app.cell
def _(df, temp_yield_correlation):
    # Input:
    correlation = temp_yield_correlation(df, 'Ave_temps', 'Standard_yield')
    print(f'Correlation: {correlation}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The near-zero correlation confirms that average temperature alone has almost no linear relationship with normalized yield in Maji Ndogo. This makes agronomic sense — temperature variation across the survey area is modest compared to the large variation in rainfall and soil conditions. The feature is not useless, but it will not anchor a simple linear model on its own.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Challenge 2: Rainfall as a Predictor

    Let's shift focus to `Rainfall`. Annual rainfall is one of the most cited drivers of agricultural yield — too little and crops wither, too much and roots drown. If any single feature should predict yield, rainfall is the best candidate in this dataset.

    ### Task
     Create a function named `rainfall_yield_relationship` that:
    - Takes a DataFrame and the names of the rainfall column and the yield column as parameters.
    - Generates a scatter plot visualizing the relationship and overlays the fitted regression line.
    - Fits a simple linear regression model using scikit-learn's `LinearRegression`.
    - Returns the slope and intercept of the fitted model as a tuple `(slope, intercept)`.

    **Note:**
    - Use `matplotlib` for plotting.
    - Use `sklearn.linear_model.LinearRegression` for modeling.
    - Plot the regression line in red on top of the scatter plot.

    ### Expected Output
    ```
    Slope: 8.77309700148857e-06
    Intercept: 0.5238603528299144
    ```
    """)
    return


@app.cell
def _(LinearRegression, plt):
    ### START FUNCTION
    def rainfall_yield_relationship(df, rainfall_col, yield_col):
        X = df[[rainfall_col]]
        y = df[yield_col]

        # Fit simple linear regression (Least Squares)
        model = LinearRegression()
        model.fit(X, y)

        # Scatter plot with the fitted line in red
        plt.figure(figsize=(8, 5))
        plt.scatter(X, y, alpha=0.5)
        plt.plot(X, model.predict(X), color='red')
        plt.xlabel('Rainfall (mm)')
        plt.ylabel('Standard Yield')
        plt.title('Rainfall vs Standard Yield with Regression Line')
        plt.show()

        return model.coef_[0], model.intercept_
    ### END FUNCTION
    return (rainfall_yield_relationship,)


@app.cell
def _(df, rainfall_yield_relationship):
    # Input:
    slope_intercept = rainfall_yield_relationship(df, 'Rainfall', 'Standard_yield')
    print('Slope:', slope_intercept[0])
    print('Intercept:', slope_intercept[1])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The slope is positive but very small — higher rainfall is weakly associated with higher yield, consistent with agricultural intuition. The shallow slope and wide scatter tell us that rainfall explains very little of the variation in yield on its own. That is the honest baseline: the signal is real, but single-predictor linear regression is too simple a lens for this data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Challenge 3: Evaluating Rainfall's Predictive Power

    A regression line can always be drawn through data. The question is whether that line is *useful*. Let's measure how well rainfall predicts yield using four performance metrics:

    - **R-squared (R²)**: The proportion of variance in yield explained by rainfall. Ranges from 0 (no explanatory power) to 1 (perfect).
    - **MAE**: Mean Absolute Error — average magnitude of prediction errors, in the same units as yield.
    - **MSE**: Mean Squared Error — penalizes large errors more heavily than MAE.
    - **RMSE**: Root Mean Squared Error — the square root of MSE, in the same units as yield.

    ### Task
     Create a function named `evaluate_rainfall_model` that:
    - Takes a DataFrame as input.
    - Trains a simple linear regression model using `Rainfall` as the predictor and `Standard_yield` as the target, on the **entire dataset**.
    - Calculates R-squared, MAE, MSE, and RMSE.
    - Returns a tuple `(r2, mae, mse, rmse)`.

    ### Expected Output
    ```
    Evaluation Metrics:
    R-squared: 0.0015379401175150686
    MAE: 0.08766959364573583
    MSE: 0.012479116464950486
    RMSE: 0.11170996582646728
    ```
    """)
    return


@app.cell
def _(LinearRegression, mean_absolute_error, mean_squared_error, np, r2_score):
    ### START FUNCTION
    def evaluate_rainfall_model(df):
        X = df[['Rainfall']]
        y = df['Standard_yield']

        # Train and predict on the entire dataset
        model = LinearRegression()
        model.fit(X, y)
        predictions = model.predict(X)

        r2 = r2_score(y, predictions)
        mae = mean_absolute_error(y, predictions)
        mse = mean_squared_error(y, predictions)
        rmse = np.sqrt(mse)
        return r2, mae, mse, rmse
    ### END FUNCTION
    return (evaluate_rainfall_model,)


@app.cell
def _(df, evaluate_rainfall_model):
    # Input:
    _evaluation_metrics = evaluate_rainfall_model(df)
    print(f'Evaluation Metrics:\nR-squared: {_evaluation_metrics[0]}\nMAE: {_evaluation_metrics[1]}\nMSE: {_evaluation_metrics[2]}\nRMSE: {_evaluation_metrics[3]}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    An R-squared of 0.00154 means rainfall explains less than 0.2% of the variance in normalized yield — a very weak model. The RMSE of about 0.11 on a 0-to-1 scale means our predictions can be off by 11 percentage points of normalized yield on average. This is our honest starting baseline. The signal is detectable, but a single predictor is nowhere near enough for production use. Module 2 brings in the full feature set.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Challenge 4: The Train-Test Split

    So far we have trained and evaluated our model on the same data. That is like a teacher grading students on the questions they practiced — it tells us how well the model memorized the training data, not how well it will predict yields for fields it has never seen.

    The **train-test split** fixes this. We hold out a random 20% of the data, train on the remaining 80%, and evaluate only on the held-out set. If performance is similar to the full-data evaluation, our model is generalizing — not just memorizing.

    ### Task
    Create a function named `train_test_split_evaluate` that:
    - Takes in the DataFrame.
    - Separates it into features (`X`) using `Rainfall` and target (`y`) using `Standard_yield`.
    - Splits the data into training and testing sets using `test_size=0.2` and `random_state=42`.
    - Trains a simple linear regression model on the training set.
    - Evaluates the model on the test set, calculating R-squared, MAE, MSE, and RMSE.
    - Returns `(r2, mae, mse, rmse), (predictions, y_test)`.

    **Note:** The second tuple `(predictions, y_test)` will be used in Challenge 5.

    ### Expected Output
    ```
    Evaluation Metrics on Test Set:
    R-squared: 4.80629092007856e-05
    MAE: 0.08998991387920033
    MSE: 0.01332478573926128
    RMSE: 0.11543303573614132
    ```
    """)
    return


@app.cell
def _(
    LinearRegression,
    mean_absolute_error,
    mean_squared_error,
    np,
    r2_score,
    train_test_split,
):
    ### START FUNCTION
    def train_test_split_evaluate(df):
        X = df[['Rainfall']]
        y = df['Standard_yield']

        # 80/20 split, reproducible
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = LinearRegression()
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        r2 = r2_score(y_test, predictions)
        mae = mean_absolute_error(y_test, predictions)
        mse = mean_squared_error(y_test, predictions)
        rmse = np.sqrt(mse)
        return (r2, mae, mse, rmse), (predictions, y_test)
    ### END FUNCTION
    return (train_test_split_evaluate,)


@app.cell
def _(df, train_test_split_evaluate):
    # Input:
    _evaluation_metrics, (_predictions, _y_test) = train_test_split_evaluate(df)
    print(f'Evaluation Metrics on Test Set:\nR-squared: {_evaluation_metrics[0]}\nMAE: {_evaluation_metrics[1]}\nMSE: {_evaluation_metrics[2]}\nRMSE: {_evaluation_metrics[3]}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The test-set performance is very close to the full-dataset performance from Challenge 3 — a sign that our model is consistently weak rather than overfitting. When train and test performance are similar, the model is learning something genuine, even if what it has learned is of limited usefulness. This consistency also tells us that the 80% training sample is representative of the full population of fields.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Challenge 5: Diagnosing Model Fit Through Residual Analysis

    Our metrics give us a high-level picture. Residual analysis gives us the X-ray. **Residuals** are the differences between actual yield values and our model's predictions:

    ```
    residual = actual_yield - predicted_yield
    ```

    A well-specified linear regression model should produce residuals that:
    1. Are **roughly normally distributed** — a bell curve centered near zero.
    2. Have a **mean close to zero** — meaning the model is not systematically over- or under-predicting.
    3. Do not fan out or curve — no systematic pattern suggesting a non-linear relationship.

    ### Task
    Create a function named `analyze_model_residuals` that:
    - Uses `predictions` and `y_test` from Challenge 4 to calculate residuals (`y_test - predictions`).
    - Plots the residuals as a histogram with a vertical line at zero, axis labels, and a title.
    - Calculates the mean and standard deviation of the residuals.
    - Returns `(mean_residual, std_residual)`.

    ### Expected Output
    ```
    Mean residual: 0.007188033196518129
    Std of residuals: 0.11520901838843622
    ```
    """)
    return


@app.cell
def _(np, plt):
    ### START FUNCTION
    def analyze_model_residuals(predictions, y_test):
        # residual = actual - predicted
        residuals = y_test - predictions

        # Histogram with a vertical line at zero
        plt.figure(figsize=(8, 5))
        plt.hist(residuals, bins=30, edgecolor='black', alpha=0.7)
        plt.axvline(x=0, color='red', linestyle='--')
        plt.xlabel('Residual (actual - predicted)')
        plt.ylabel('Frequency')
        plt.title('Distribution of Residuals')
        plt.show()

        mean_residual = float(np.mean(residuals))
        std_residual = float(np.std(residuals))
        return mean_residual, std_residual
    ### END FUNCTION
    return (analyze_model_residuals,)


@app.cell
def _(analyze_model_residuals, df, train_test_split_evaluate):
    # Re-run Challenge 4 to get predictions and y_test
    _evaluation_metrics, (_predictions, _y_test) = train_test_split_evaluate(df)
    mean_residual, std_residual = analyze_model_residuals(_predictions, _y_test)
    print(f'Mean residual: {mean_residual}')
    print(f'Std of residuals: {std_residual}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The near-zero mean residual tells us the model has no systematic bias. The standard deviation is similar to the RMSE from Challenge 4 — as expected, since RMSE is the square root of mean squared residual. If the histogram is roughly bell-shaped and symmetric around zero, linear regression is a defensible framework for this data, even at this low R-squared. The scatter confirms that we need more predictors, but the *framework* is sound.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Wrapping up

    You have built and evaluated your first machine learning model on the Maji Ndogo farm survey data. This is Part A of a three-part modeling arc:

    | Part | Scope | Status |
    |---|---|---|
    | **Part A (this notebook)** | Single-predictor simple linear regression | ✅ Complete |
    | **Part B (Module 2)** | Multiple linear regression with feature selection | Upcoming |
    | **Part C (Module 3)** | Regularization (Ridge & LASSO) and model persistence | Upcoming |

    ### What you learned this module

    - **Pearson correlation** measures the *strength* and *direction* of a linear relationship — not causation.
    - **Simple linear regression** finds the line that minimizes the sum of squared residuals (Least Squares).
    - **R-squared** tells you how much variance your model explains. An R-squared near zero means the single predictor is not enough — but a detectable signal means it is worth keeping.
    - **The train-test split** simulates real-world generalization. Similar train and test performance means no overfitting.
    - **Residual analysis** is the X-ray: if residuals are symmetric around zero with no pattern, the linear framework is appropriate.

    Sanaa's next question: "Can we do better with more predictors?" In Module 2, we will bring in the full feature set and use Multiple Linear Regression to close the gap.

    — Sanaa 🌾
    """)
    return


@app.cell
def cell_readiness():
    import inspect as _inspect
    import ast as _ast
    _spec = {'analyze_model_residuals': {'expected_params': ['predictions', 'y_test']}, 'evaluate_rainfall_model': {'expected_params': ['df']}, 'rainfall_yield_relationship': {'expected_params': ['df', 'rainfall_col', 'yield_col']}, 'temp_yield_correlation': {'expected_params': ['df', 'temp_col', 'yield_col']}, 'train_test_split_evaluate': {'expected_params': ['df']}}
    _msgs = []
    _missing = 0
    _stubs = 0
    _mismatches = 0
    for _name, _checks in _spec.items():
        try:
            _fn = eval(_name)
        except NameError:
            _msgs.append(f"❌ `{_name}` — not defined yet")
            _missing += 1
            continue
        if not callable(_fn):
            _msgs.append(f"❌ `{_name}` — exists but is not callable")
            _missing += 1
            continue
        try:
            _sig = _inspect.signature(_fn)
            _actual_params = list(_sig.parameters.keys())
        except (ValueError, TypeError):
            _msgs.append(f"✓ `{_name}` — defined (signature unavailable)")
            continue
        _expected = _checks.get("expected_params")
        if _expected and _actual_params != _expected:
            _msgs.append(
                f"⚠️ `{_name}` — parameter mismatch: expected {_expected}, got {_actual_params}"
            )
            _mismatches += 1
            continue
        # AST check — flag empty stubs (function body is just `pass` or `return None`)
        _is_stub = False
        try:
            import textwrap as _textwrap
            _src = _textwrap.dedent(_inspect.getsource(_fn))
            _tree = _ast.parse(_src)
            _body = _tree.body[0].body if _tree.body else []
            # Strip any leading docstring (an Expr with a Constant str)
            _real_body = [
                _stmt for _stmt in _body
                if not (
                    isinstance(_stmt, _ast.Expr)
                    and isinstance(_stmt.value, _ast.Constant)
                    and isinstance(_stmt.value.value, str)
                )
            ]
            _is_stub = (
                not _real_body
                or (
                    len(_real_body) == 1
                    and (
                        isinstance(_real_body[0], _ast.Pass)
                        or (isinstance(_real_body[0], _ast.Return) and _real_body[0].value is None)
                    )
                )
            )
        except (OSError, TypeError, SyntaxError, IndexError):
            pass  # source unavailable; skip stub check
        if _is_stub:
            _msgs.append(
                f"⚠️ `{_name}` — body looks empty (just `pass` or bare `return`). Did you implement it?"
            )
            _stubs += 1
            continue
        _msgs.append(f"✓ `{_name}` — defined with parameters {_actual_params}")
    print("Readiness check:")
    for _m in _msgs:
        print(f"  {_m}")
    print()
    if _missing == len(_spec):
        print("It looks like none of the required functions are defined yet.")
        print("Click 'Run all cells' (the ▶▶ button at the top of the page),")
        print("or run each function-defining cell individually first.")
    elif _missing > 0:
        print(f"{_missing} function(s) not yet defined — run the cells that define them and re-run this check.")
    elif _stubs > 0 or _mismatches > 0:
        print(f"Some functions need fixing before submitting ({_stubs} stub(s), {_mismatches} signature mismatch(es)).")
    else:
        print("All required functions are present and ready. You can submit.")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
