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
    # Understanding the Shortfall — Part B
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A single-variable baseline isn’t enough; now it's time to see the whole picture. To help grid operators manage supply, the Ministry needs models that process national weather patterns simultaneously. In this project, you build your first Multiple Linear Regression (MLR) model using scikit-learn to handle multi-city inputs. You will isolate redundant weather drivers using Variance Inflation Factors (VIF), implement an 80/20 train-test split, run Durbin-Watson diagnostics to check time-series independence, and plot residuals to test for homoscedasticity. It is the exact diagnostic checkpoint that scales the work from simple baselines to multi-variable models.
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
    The government of Spain has reviewed your Part A findings. They appreciate the honesty — simple linear regression using a single predictor explained only about 3% of the variance in the energy shortfall. But they need more than an honest baseline. They need a model that the grid operators can actually use.

    Your contact at the Ministry of Energy puts it plainly: "Temperature drops in Madrid on the same day it drops in Seville. Wind picks up along the coast while the interior stays still. These patterns are what drive the shortfall. We need your model to see all of it at once."

    This is exactly what **Multiple Linear Regression (MLR)** is built for. Instead of fitting one line through one predictor, MLR fits a hyperplane through many predictors simultaneously — letting the model separate the contribution of each city's weather while accounting for the others.

    But more predictors come with new responsibilities. When predictors are too similar to each other — a condition called **multicollinearity** — the model's coefficients become unreliable and interpretations break down. And because Spain's energy data is a time series recorded every three hours, we must check that residuals are not autocorrelated, which would violate the independence assumption of linear regression.

    By the end of this notebook you will have:

    - Fit your first MLR model using scikit-learn with five simultaneous predictors.
    - Diagnosed multicollinearity using the Variance Inflation Factor (VIF).
    - Applied the train-test split to evaluate out-of-sample performance.
    - Tested residual independence using the Durbin-Watson statistic.
    - Assessed homoscedasticity by plotting residuals against fitted values.

    > **AI assist:** This module introduces MLR diagnostics that can feel abstract. Good prompts: *"Explain the Variance Inflation Factor in plain language — what does a VIF of 9,000 actually mean for a regression model?"* *"What is the Durbin-Watson test checking, and why does it matter for time-series regression data?"*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Data Setup

    ### Data Dictionary

    The dataset contains 3-hourly weather readings from five Spanish cities — Madrid, Seville, Valencia, Bilbao, and Barcelona — alongside the corresponding energy shortfall.

    **Target variable**
    - `load_shortfall_3h`: The shortfall between fossil fuel and renewable energy generation over 3 hours (Float). This is what we are predicting.

    **Weather features (per city)**
    - `{city}_temp`: Average temperature in Kelvin (Float).
    - `{city}_humidity`: Relative humidity as a percentage (Float).
    - `{city}_wind_speed`: Wind speed in m/s (Float).
    - `{city}_pressure`: Atmospheric pressure in hPa (Float, except `Seville_pressure` which is categorical string).
    - `{city}_clouds_all`: Cloud coverage as a percentage (Float).

    **Columns requiring preprocessing**
    - `Valencia_wind_deg`: Encoded as string levels (`level_1` through `level_10`) — extract the numeric value.
    - `Seville_pressure`: Encoded as strings (`sp1` through `sp25`) — extract the numeric value.
    - `Valencia_pressure`: Contains approximately 2,000 missing values — rows will be dropped.

    **Setup:** Run the cell below to load and prepare the data before attempting any challenge.
    """)
    return


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')  # headless rendering for test environments
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
    from sklearn.model_selection import train_test_split
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    from statsmodels.stats.stattools import durbin_watson
    import statsmodels.api as sm
    import warnings
    warnings.filterwarnings('ignore')

    file_path = 'df_train.csv'  # Replace with your file path
    df_raw = pd.read_csv(file_path, index_col=0)

    # Preprocess: extract numeric values from categorical-encoded columns, drop nulls
    df = df_raw.copy()
    df = df.drop(columns=['time'], errors='ignore')
    df['Valencia_wind_deg'] = df['Valencia_wind_deg'].str.extract(r'(\d+)').astype(float)
    df['Seville_pressure']  = df['Seville_pressure'].str.extract(r'(\d+)').astype(float)
    df = df.dropna()

    print(df.shape)
    print(df.head())
    return (
        LinearRegression,
        df,
        durbin_watson,
        mean_squared_error,
        np,
        pd,
        plt,
        r2_score,
        train_test_split,
        variance_inflation_factor,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Challenge 1: Fitting a Multiple Linear Regression Model

    Temperature is recorded across all five cities in our dataset. Rather than choosing just one city's temperature as we did in Part A, we can bring all five in simultaneously. This allows the model to learn the *combined* influence of temperature conditions across Spain — Madrid's continental climate, Seville's heat, the coastal moderation in Barcelona.

    ### Task
    Create a function named `fit_temperature_mlr` that:
    - Takes a DataFrame as input.
    - Uses the following five features as predictors: `Madrid_temp`, `Seville_temp`, `Valencia_temp`, `Bilbao_temp`, `Barcelona_temp`.
    - Fits a multiple linear regression model on the **full dataset**.
    - Returns a tuple `(model, r2, rmse)` containing the fitted model object, R-squared on the full dataset, and RMSE on the full dataset.

    **Note:**
    - Use `LinearRegression` from `sklearn.linear_model`.
    - Return format: `(model, r2, rmse)`.

    ### Expected Output
    ```
    R-squared: 0.06820610764408985
    RMSE: 5091.726004672317
    Coefficients: {'Madrid_temp': np.float64(121.5574), 'Seville_temp': np.float64(-78.9912), 'Valencia_temp': np.float64(-6.8158), 'Bilbao_temp': np.float64(29.1241), 'Barcelona_temp': np.float64(113.1248)}
    ```
    """)
    return


@app.cell
def _(LinearRegression, mean_squared_error, np, r2_score):
    ### START FUNCTION
    def fit_temperature_mlr(df):
        temp_cols = ['Madrid_temp', 'Seville_temp', 'Valencia_temp',
                     'Bilbao_temp', 'Barcelona_temp']
        X = df[temp_cols]
        y = df['load_shortfall_3h']

        # Fit on the full dataset
        model = LinearRegression()
        model.fit(X, y)
        predictions = model.predict(X)

        r2 = r2_score(y, predictions)
        rmse = np.sqrt(mean_squared_error(y, predictions))
        return model, r2, rmse
    ### END FUNCTION
    return (fit_temperature_mlr,)


@app.cell
def _(df, fit_temperature_mlr):
    # Input:
    model, _r2, _rmse = fit_temperature_mlr(df)
    print(f'R-squared: {_r2}')
    print(f'RMSE: {_rmse}')
    print(f"Coefficients: {dict(zip(['Madrid_temp', 'Seville_temp', 'Valencia_temp', 'Bilbao_temp', 'Barcelona_temp'], model.coef_.round(4)))}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Compare this R-squared to Part A's single-predictor model (~0.028 for humidity). Adding four more temperature predictors improved the fit — but modestly. Five predictors, and we have barely doubled the explanatory power. This is a warning sign: the five city temperatures may be measuring the same underlying phenomenon — Spain's national weather pattern — just from different vantage points. We will investigate this next.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Challenge 2: Diagnosing Multicollinearity with VIF

    Before trusting any coefficient in an MLR model, we need to check for **multicollinearity** — the condition where two or more predictors are highly correlated with each other. When predictors move together, the model cannot isolate each one's individual contribution, and coefficients become statistically unstable.

    The **Variance Inflation Factor (VIF)** measures this directly. For each predictor, VIF answers: "How much larger is the variance of this coefficient than it would be if this predictor were uncorrelated with all the others?"

    **Rules of thumb:**
    - VIF < 5: Low multicollinearity — acceptable.
    - VIF 5–10: Moderate — worth monitoring.
    - VIF > 10: High — the predictor is likely redundant.

    ### Task
    Create a function named `calculate_vif` that:
    - Takes a DataFrame and a list of feature column names as input.
    - Calculates the VIF for each feature.
    - Returns a DataFrame with columns `feature` and `VIF`, sorted by VIF in descending order with the index reset.

    **Note:** Use `variance_inflation_factor` from `statsmodels.stats.outliers_influence`.

    ### Expected Output
    ```
              feature           VIF
    0   Valencia_temp  14491.975682
    1  Barcelona_temp  12796.330493
    2    Seville_temp   9105.434827
    3     Bilbao_temp   8624.932391
    4     Madrid_temp   7006.728704
    ```
    """)
    return


@app.cell
def _(pd, variance_inflation_factor):
    ### START FUNCTION
    def calculate_vif(df, feature_cols):
        X = df[feature_cols].values

        vif_data = pd.DataFrame({
            'feature': feature_cols,
            'VIF': [variance_inflation_factor(X, i) for i in range(X.shape[1])]
        })
        return vif_data.sort_values('VIF', ascending=False).reset_index(drop=True)
    ### END FUNCTION
    return (calculate_vif,)


@app.cell
def _(calculate_vif, df):
    # Input:
    temp_features = ['Madrid_temp', 'Seville_temp', 'Valencia_temp', 'Bilbao_temp', 'Barcelona_temp']
    vif_df = calculate_vif(df, temp_features)
    print(vif_df)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    VIF values in the thousands confirm that the five temperature columns are essentially measuring the same thing: Spain's nationwide temperature pattern. Temperature in Madrid and Seville rise and fall together — so the model cannot assign a stable coefficient to either. In Module 3, variable selection will help us choose the most informative, least redundant predictors and reduce this multicollinearity to acceptable levels.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Challenge 3: Train-Test Split and Performance Evaluation

    Fitting and evaluating on the same data, as we did in Challenge 1, can give an overly optimistic view of performance. A model that has seen every training example can fit those points closely, but then fail when it encounters new data it has never seen.

    The train-test split gives us an honest estimate: train on 80%, evaluate on the held-out 20%. If test performance is close to training performance, the model is generalizing. If test performance is dramatically worse, the model is overfitting.

    ### Task
    Create a function named `mlr_train_test_evaluate` that:
    - Takes a DataFrame as input.
    - Uses `Madrid_temp`, `Seville_temp`, `Valencia_temp`, `Bilbao_temp`, `Barcelona_temp` as predictors and `load_shortfall_3h` as the target.
    - Splits the data with `test_size=0.2` and `random_state=42`.
    - Trains on the training set, evaluates on the test set.
    - Returns `(r2, rmse), (predictions, y_test)`.

    **Note:** The second tuple `(predictions, y_test)` will be used directly in Challenges 4 and 5.

    ### Expected Output
    ```
    Test R-squared: 0.07184913973567075
    Test RMSE: 5098.7257157969025
    ```
    """)
    return


@app.cell
def _(LinearRegression, mean_squared_error, np, r2_score, train_test_split):
    ### START FUNCTION
    def mlr_train_test_evaluate(df):
        temp_cols = ['Madrid_temp', 'Seville_temp', 'Valencia_temp',
                     'Bilbao_temp', 'Barcelona_temp']
        X = df[temp_cols]
        y = df['load_shortfall_3h']

        # 80/20 split, reproducible
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = LinearRegression()
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        r2 = r2_score(y_test, predictions)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        return (r2, rmse), (predictions, y_test)
    ### END FUNCTION
    return (mlr_train_test_evaluate,)


@app.cell
def _(df, mlr_train_test_evaluate):
    # Input:
    (_r2, _rmse), (_predictions, _y_test) = mlr_train_test_evaluate(df)
    print(f'Test R-squared: {_r2}')
    print(f'Test RMSE: {_rmse}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The test-set performance is very close to what we saw on the full dataset in Challenge 1 — a sign that our model is not overfitting, even though it is still quite weak. When train and test performance are similar, we can trust the metrics. When test performance is dramatically worse, that gap tells us the model has memorized the training data rather than learned generalizable patterns.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Challenge 4: Checking Residual Independence — Durbin-Watson

    Our dataset is a **time series** — energy readings recorded every 3 hours over multiple years. This creates a specific risk: the error our model makes at 9 a.m. might predict the error it makes at noon. If residuals are correlated across time (**autocorrelation**), the independence assumption of linear regression is violated, and our standard errors — and therefore our p-values and confidence intervals — are unreliable.

    The **Durbin-Watson statistic** detects this. It ranges from 0 to 4:

    | Value | Interpretation |
    |---|---|
    | ~2 | No autocorrelation — independence assumption holds ✅ |
    | < 1.5 | Positive autocorrelation — model is missing a time trend |
    | > 2.5 | Negative autocorrelation — over-correction between consecutive residuals |

    ### Task
    Create a function named `check_residual_independence` that:
    - Takes `predictions` and `y_test` (from Challenge 3).
    - Calculates the residuals as `y_test - predictions`.
    - Computes and returns the Durbin-Watson statistic as a float.

    **Note:** Use `durbin_watson` from `statsmodels.stats.stattools`.

    ### Expected Output
    ```
    Durbin-Watson statistic: 1.9733091268157688
    ```
    """)
    return


@app.cell
def _(durbin_watson):
    ### START FUNCTION
    def check_residual_independence(predictions, y_test):
        # residual = actual - predicted
        residuals = y_test - predictions
        return float(durbin_watson(residuals))
    ### END FUNCTION
    return (check_residual_independence,)


@app.cell
def _(check_residual_independence, df, mlr_train_test_evaluate):
    # Input:
    (_r2, _rmse), (_predictions, _y_test) = mlr_train_test_evaluate(df)
    dw_stat = check_residual_independence(_predictions, _y_test)
    print(f'Durbin-Watson statistic: {dw_stat}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A Durbin-Watson value near 1.97 is very close to 2 — the independence assumption is not being seriously violated. Even though the energy data is a time series, after removing the temperature signal the residuals do not carry a detectable trend from one 3-hour period to the next. This is an important green light: we can proceed with standard linear regression without needing time-series corrections like ARIMA.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Challenge 5: Assessing Homoscedasticity — Residuals vs. Fitted

    The final diagnostic we need is **homoscedasticity**: the assumption that the variance of residuals is roughly constant across all predicted values. A model that is highly accurate at low predicted values but wildly off at high predicted values violates this assumption — and tells us the model structure is missing something.

    The standard check is a scatter plot of residuals against fitted values (predictions). In a well-specified model, this plot should look like a horizontal band of roughly equal scatter around the zero line, with no obvious funnel, curve, or cluster.

    ### Task
    Create a function named `plot_residuals_vs_fitted` that:
    - Takes `predictions` and `y_test` (from Challenge 3).
    - Calculates residuals as `y_test - predictions`.
    - Creates a scatter plot of residuals (y-axis) against fitted values (x-axis), with a horizontal red dashed line at zero, axis labels, and a title.
    - Returns a tuple `(mean_residual, std_residual)`.

    ### Expected Output
    ```
    Mean residual: -145.18258649860152
    Std of residuals: 5096.658311237494
    ```
    """)
    return


@app.cell
def _(np, plt):
    ### START FUNCTION
    def plot_residuals_vs_fitted(predictions, y_test):
        # residual = actual - predicted
        residuals = y_test - predictions

        # Residuals (y) against fitted values (x), with a red dashed zero line
        plt.figure(figsize=(8, 5))
        plt.scatter(predictions, residuals, alpha=0.5)
        plt.axhline(y=0, color='red', linestyle='--')
        plt.xlabel('Fitted values (predictions)')
        plt.ylabel('Residuals')
        plt.title('Residuals vs Fitted Values')
        plt.show()

        mean_residual = float(np.mean(residuals))
        std_residual = float(np.std(residuals))
        return mean_residual, std_residual
    ### END FUNCTION
    return (plot_residuals_vs_fitted,)


@app.cell
def _(df, mlr_train_test_evaluate, plot_residuals_vs_fitted):
    # Input:
    (_r2, _rmse), (_predictions, _y_test) = mlr_train_test_evaluate(df)
    mean_res, std_res = plot_residuals_vs_fitted(_predictions, _y_test)
    print(f'Mean residual: {mean_res}')
    print(f'Std of residuals: {std_res}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What patterns do you observe in the residuals vs. fitted plot? A perfectly homoscedastic model would show a horizontal band of equal scatter. Any funneling (wider spread at higher fitted values) or curvature suggests the model is missing non-linear structure. The mean residual near zero confirms no systematic bias, but the large standard deviation (~5,000 MW·h) confirms we still have a lot of unexplained variance — more predictors and smarter feature selection are needed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Wrapping up

    Multiple Linear Regression gave us our first look at multi-predictor modeling, but this module's diagnostics told an important story about the limits of our current predictor set.

    | Diagnostic | Result | Interpretation |
    |---|---|---|
    | R-squared (5 temps) | ~0.068 | 7% of variance explained — weak but better than Part A |
    | VIF (all temps) | 7,000–14,000 | Extreme multicollinearity — predictors are redundant |
    | Durbin-Watson | ~1.97 | Residual independence holds ✅ |
    | Residuals vs. Fitted | Roughly uniform band | No obvious heteroscedasticity |

    More predictors do not automatically mean a better model. When predictors carry the same information, they compete with each other rather than complementing each other. The model's R-squared barely moved despite quadrupling the predictor count.
    """)
    return


@app.cell
def cell_readiness():
    import inspect as _inspect
    import ast as _ast
    _spec = {'calculate_vif': {'expected_params': ['df', 'feature_cols']}, 'check_residual_independence': {'expected_params': ['predictions', 'y_test']}, 'fit_temperature_mlr': {'expected_params': ['df']}, 'mlr_train_test_evaluate': {'expected_params': ['df']}, 'plot_residuals_vs_fitted': {'expected_params': ['predictions', 'y_test']}}
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
