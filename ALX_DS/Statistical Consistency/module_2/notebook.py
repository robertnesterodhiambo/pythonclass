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
    # Validating Maji Ndogo's Statistical Consistency
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Guessing a tolerance window isn’t science; it’s a liability. When an audit hinges on whether a 2% variance is a data flaw or natural noise, guessing leaves a budget exposed. In this project, you will use inferential statistics to defend Maji Ndogo's data. You will calculate sample metrics with Bessel's correction, map the Central Limit Theorem, construct 95% confidence intervals, and write an automated one-sample t-test script. It is exactly the kind of rigorous statistical proof required to ensure data credibility for international agricultural audits.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ⚠️ **This challenge is graded and contributes to your overall marks for this module.**

    ### Instructions

    - Write your code only in the cells marked `# your code here` and inside the provided function markers. Do not edit or remove the `### START FUNCTION` or `### END FUNCTION` comments. Do not add any code outside of the functions you are required to edit. Doing any of this will result in a mark of 0%.
    - Answer the questions according to the specifications provided.
    - Use the provided test cells to verify your output before submitting.
    - Do not hard-code answers — your functions must work on unseen inputs.
    - The use of StackOverflow, Google, and other online resources is permitted. The use of Generative AI tools — including ChatGPT, Claude, Copilot, and others — is also allowed and encouraged as a learning partner. However, the code you submit must reflect your own understanding. Copying a fellow student's code is a breach of the honor code. [Read the honor code here](https://drive.google.com/file/d/1atFOPUQRLz5slb4Q1ASXh8QQfKyXVqrw/preview). Submitting code you do not understand is also a breach.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Sanaa calls you in at 7 a.m. She has been up since four.

    "I have been thinking about that comparison," she says. "True: 7, False: 8. The tolerance I used was 1.5%. But why 1.5%? I made that number up." She draws a circle on the whiteboard. "What if the measurements are naturally noisy? What if a 2% difference between a sensor and a field reading is completely normal given how spread out the data is? We would be flagging perfectly good data as a problem."

    She looks at you. "We need to stop guessing and start using statistics."

    That is the shift this week. Instead of asking "is this within a tolerance window I invented?", you will ask the question the scientific way: *Could the difference between our field measurements and the weather station readings be explained by random variation alone?*

    The tools you will use — population metrics, the Central Limit Theorem, confidence intervals, and hypothesis testing — form the backbone of inferential statistics. By the end of this notebook, you will have a defensible, statistically grounded answer for the auditor.

    > **AI assist:** This week introduces several statistical concepts that build on each other. Use an AI assistant as a thinking partner throughout. Good prompts to try: *"Why does sample variance divide by n-1 instead of n? Explain the intuition without just giving me the formula."* *"What does a 95% confidence interval actually mean? Challenge me on the common misinterpretation."*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Setup:** Execute the cell below before starting.

    **Download:** [Maji_Ndogo_farm_survey_small.db](https://raw.githubusercontent.com/Explore-AI/Public-Data/master/Maji_Ndogo/Maji_Ndogo_farm_survey_small.db)
    """)
    return


@app.cell
def _():
    ### DO NOT CHANGE ANYTHING IN THIS CELL, ONLY EXECUTE IT!

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from scipy import stats
    from sqlalchemy import create_engine, text

    engine = create_engine('sqlite:///Maji_Ndogo_farm_survey_small.db')
    sql_query = """
    SELECT *
    FROM geographic_features
    LEFT JOIN weather_features USING (Field_ID)
    LEFT JOIN soil_and_crop_features USING (Field_ID)
    LEFT JOIN farm_management_features USING (Field_ID)
    """
    with engine.connect() as connection:
        MD_agric_df = pd.read_sql_query(text(sql_query), connection)

    MD_agric_df.rename(columns={'Annual_yield': 'Crop_type_Temp', 'Crop_type': 'Annual_yield'}, inplace=True)
    MD_agric_df.rename(columns={'Crop_type_Temp': 'Crop_type'}, inplace=True)
    MD_agric_df['Elevation'] = MD_agric_df['Elevation'].abs()
    corrections = {'cassaval': 'cassava', 'wheatn': 'wheat', 'teaa': 'tea'}
    MD_agric_df['Crop_type'] = MD_agric_df['Crop_type'].apply(
        lambda crop: corrections.get(crop.strip(), crop.strip())
    )

    weather_station_mapping_df = pd.read_csv(
        'Weather_data_field_mapping.csv'
    )
    MD_agric_df = MD_agric_df.merge(weather_station_mapping_df, on='Field_ID', how='left')
    MD_agric_df = MD_agric_df.drop(columns='Unnamed: 0', errors='ignore')
    print(f'Loaded: {MD_agric_df.shape[0]} rows x {MD_agric_df.shape[1]} columns')
    return MD_agric_df, np, plt, stats


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 1: Sample vs. population metrics

    Our 5,654 field records are the **population** — every farm in the survey. Any subset we analyze is a **sample**. The variance formula changes depending on whether you are describing the population or estimating it from a sample: population variance divides by `n`; sample variance divides by `n-1` (Bessel's correction, which removes bias in the estimate).

    ### Task

    1. Calculate the population mean and variance of `Standard_yield` using `ddof=0`.
    2. Call `np.random.seed(42)` on the first line of the cell, then draw a random
       sample of 50 fields using the `.sample()` method.
    3. Calculate the sample mean and variance of that sample using `ddof=1`.
    4. Print all four values, formatted as shown below.

    ### Expected output

    ```
    Population mean: 0.5344
    Population variance: 0.012498
    Sample mean (n=50): 0.5305
    Sample variance (ddof=1): 0.010990
    ```
    """)
    return


@app.cell
def _(MD_agric_df, np):
    np.random.seed(42)

    # Calculate the population mean
    population_mean = MD_agric_df['Standard_yield'].mean()

    # Calculate population variance (ddof=0 divides by n)
    population_variance = MD_agric_df['Standard_yield'].var(ddof=0)

    # Draw a random sample of 50 fields
    sample = MD_agric_df['Standard_yield'].sample(n=50)

    # Calculate the sample mean
    sample_mean = sample.mean()

    # Calculate sample variance (ddof=1 divides by n-1)
    sample_variance = sample.var(ddof=1)

    # Print the results in the required format
    print(f"Population mean: {population_mean:.4f}")
    print(f"Population variance: {population_variance:.6f}")
    print(f"Sample mean (n=50): {sample_mean:.4f}")
    print(f"Sample variance (ddof=1): {sample_variance:.6f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 2: The Central Limit Theorem

    A single sample mean wobbles around the true population mean. The Central Limit Theorem (CLT) says: take enough samples, and the distribution of those sample means will be approximately normal — centered on the population mean — regardless of what the original data looks like.

    This is why we can use statistical tests on real-world data that is not normally distributed: the test statistics are based on sample means, not the raw data.

    ### Task

    1. Call `np.random.seed(42)` on the first line of the cell, then draw 1,000 samples of 30 fields each using the `.sample()` method
    2. Compute the mean `Standard_yield` of each sample and store results in a list called `sample_means`.
    3. Plot a histogram of `sample_means` with a title and axis labels.
    4. Print the mean of the sample means, their standard deviation, and the theoretical standard error (`population_std / sqrt(30)`).

    ### Expected output

    ```
    Mean of sample means: 0.5343
    Std of sample means: 0.0207
    Theoretical standard error: 0.0204
    ```
    """)
    return


@app.cell
def _(MD_agric_df, np, plt):
    np.random.seed(42)

    def calculate_sample_means():
        # Store the means of the 1,000 samples
        sample_means = []

        # Draw 1,000 samples of 30 fields each
        for i in range(1000):
            current_sample = MD_agric_df['Standard_yield'].sample(n=30)

            # Calculate the mean of the current sample
            sample_means.append(current_sample.mean())

        return sample_means


    # Calculate the sample means
    sample_means = calculate_sample_means()

    # Calculate the population standard deviation
    population_std = MD_agric_df['Standard_yield'].std(ddof=0)

    # Calculate the theoretical standard error
    theoretical_se = population_std / np.sqrt(30)

    # Plot the histogram
    plt.figure(figsize=(10, 6))
    plt.hist(sample_means, bins=30, edgecolor='black')
    plt.title('Distribution of Sample Means (Central Limit Theorem)')
    plt.xlabel('Sample Mean of Standard_yield')
    plt.ylabel('Frequency')
    plt.show()

    # Print the results
    print(f"Mean of sample means: {np.mean(sample_means):.4f}")
    print(f"Std of sample means: {np.std(sample_means, ddof=1):.4f}")
    print(f"Theoretical standard error: {theoretical_se:.4f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 3: Confidence intervals

    A **95% confidence interval** gives a range: if we repeated this survey many times and built a CI each time, 95% of those intervals would contain the true population mean. It does **not** mean there is a 95% probability that the true mean lies in this particular interval — the true mean either is or is not in there.

    SciPy syntax: `stats.t.interval(confidence, df, loc=mean, scale=sem)` — where `sem` is `stats.sem(data)` and `df` is `len(data) - 1`.

    ### Task

    1. Calculate the 95% CI for the mean `Standard_yield` across all 5,654 fields.
    2. Calculate the 95% CI for `Rainfall` in fields assigned to **weather station 0** only.
    3. Print both results as shown below.
    4. State in a comment whether the station's published mean of **1,575.95 mm** falls inside or outside the second CI.

    ### Expected output

    ```
    Mean yield: 0.5344, 95% CI: (0.5315, 0.5373)
    n: 1375, Mean rainfall: 1522.89 mm, 95% CI: (1499.83, 1545.96)
    ```
    """)
    return


@app.cell
def _(MD_agric_df, stats):
    # 95% CI for Standard_yield (all fields):
    # your code here


    # Calculate the 95% confidence interval for Standard_yield
    yield_data = MD_agric_df['Standard_yield']

    yield_mean = yield_data.mean()
    yield_sem = stats.sem(yield_data)
    yield_df = len(yield_data) - 1

    yield_ci = stats.t.interval(
        0.95,
        df=yield_df,
        loc=yield_mean,
        scale=yield_sem
    )

    return yield_ci, yield_mean


@app.cell
def _(MD_agric_df, stats, yield_ci, yield_mean):

    # 95% CI for Rainfall near station 0:
    # your code here


    # Filter fields assigned to weather station 0
    station_0_data = MD_agric_df.loc[
        MD_agric_df['Weather_station'] == 0, 'Rainfall'
    ]

    # Calculate the rainfall statistics for station 0
    rainfall_mean = station_0_data.mean()
    rainfall_sem = stats.sem(station_0_data)
    rainfall_df = len(station_0_data) - 1

    rainfall_ci = stats.t.interval(
        0.95,
        df=rainfall_df,
        loc=rainfall_mean,
        scale=rainfall_sem
    )


    # Print the results
    print(f"Mean yield: {yield_mean:.4f}, 95% CI: ({yield_ci[0]:.4f}, {yield_ci[1]:.4f})")
    print(f"n: {len(station_0_data)}, Mean rainfall: {rainfall_mean:.2f} mm, "
          f"95% CI: ({rainfall_ci[0]:.2f}, {rainfall_ci[1]:.2f})")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 4: One-sample t-test

    The confidence interval showed the station's published rainfall mean sits outside our field data's 95% CI. But a CI only tells us the range for our mean — it does not directly test whether the station value is plausible. For that, we use a hypothesis test.

    **H₀:** The true mean rainfall near station 0 equals 1,575.95 mm — any difference is random noise.
    **H₁:** The true mean is different from 1,575.95 mm.

    We reject H₀ if the p-value is below α = 0.05. A small p-value means: "if H₀ were true, the probability of seeing data this extreme by chance is less than 5%."

    ### Task

    1. Run `stats.ttest_1samp()` on the `Rainfall` data for fields near station 0, tested against the reference value `1575.95`. Print the t-statistic, p-value (5 decimal places), and your conclusion.
    2. Repeat for **average temperature** (`Ave_temps`), tested against the station reference mean of `13.4039`. Print those results too.

    ### Expected output

    **Rainfall:**
    ```
    T-statistic: -4.51238, P-value: 0.00001
    Reject H₀ — rainfall discrepancy is statistically significant.
    ```

    **Temperature:**
    ```
    T-statistic: -0.48144, P-value: 0.63028
    Fail to reject H₀ — temperature difference is consistent with random noise.
    ```
    """)
    return


@app.cell
def _(MD_agric_df, stats):
    # Rainfall t-test for station 0:
    # Filter rainfall measurements for weather station 0
    station_0_rainfall = MD_agric_df.loc[
        MD_agric_df['Weather_station'] == 0, 'Rainfall'
    ]

    # Perform one-sample t-test against the published mean
    rainfall_test = stats.ttest_1samp(
        station_0_rainfall,
        popmean=1575.95
    )

    # Print the t-statistic and p-value
    print(f"T-statistic: {rainfall_test.statistic:.5f}, P-value: {rainfall_test.pvalue:.5f}")

    # Interpret the result at a 5% significance level
    if rainfall_test.pvalue < 0.05:
        print("Reject H₀ — rainfall discrepancy is statistically significant.")
    else:
        print("Fail to reject H₀ — rainfall difference is consistent with random noise.")
    return


@app.cell
def _(MD_agric_df, stats):
    # Temperature t-test for station 0:
    # Filter average temperature measurements for weather station 0
    station_0_temperature = MD_agric_df.loc[
        MD_agric_df['Weather_station'] == 0, 'Ave_temps'
    ]

    # Perform one-sample t-test against the published mean
    temperature_test = stats.ttest_1samp(
        station_0_temperature,
        popmean=13.4039
    )

    # Print the t-statistic and p-value
    print(f"T-statistic: {temperature_test.statistic:.5f}, P-value: {temperature_test.pvalue:.5f}")

    # Interpret the result at a 5% significance level
    if temperature_test.pvalue < 0.05:
        print("Reject H₀ — temperature discrepancy is statistically significant.")
    else:
        print("Fail to reject H₀ — temperature difference is consistent with random noise.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 5: All stations — systematic testing

    Station 0's rainfall is a problem. But what about the other four stations? Running the test one station at a time is tedious and error-prone. We need a function that systematizes the process.

    ### Task

    Complete `rainfall_ttest_results(df, station_means, alpha=0.05)`. The function must:
    - Accept a DataFrame, a dictionary of `{station_id: reference_rainfall_mean}`, and a significance level.
    - Loop over every station in `station_means`.
    - Run a one-sample t-test on the field `Rainfall` for each station against its reference mean.
    - Print one line per station showing the station ID, p-value, and whether H₀ was rejected.
    - Include a docstring.

    > ⚠️ Do not change the function name `rainfall_ttest_results`.

    ### Expected output

    ```
    Significant difference in Rainfall at Station 0 (P-value: 0.00001 ≤ 0.05). H₀ rejected.
    No significant difference in Rainfall at Station 1 (P-value: 0.06741 > 0.05). H₀ not rejected.
    Significant difference in Rainfall at Station 2 (P-value: 0.00542 ≤ 0.05). H₀ rejected.
    Significant difference in Rainfall at Station 3 (P-value: 0.00549 ≤ 0.05). H₀ rejected.
    Significant difference in Rainfall at Station 4 (P-value: 0.00064 ≤ 0.05). H₀ rejected.
    ```
    """)
    return


@app.cell
def _(stats):
    # Reference rainfall means for each weather station
    station_rainfall_means = {
        0: 1575.953750,
        1: 577.383910,
        2: 1690.955324,
        3: 905.191397,
        4: 1200.183505,
    }

    ### START FUNCTION
    def rainfall_ttest_results(df, station_means, alpha=0.05):
        # Loop through each station and its reference rainfall mean
        for station_id, reference_mean in station_means.items():

            # Select rainfall measurements belonging to the current station
            station_rainfall = df.loc[
                df['Weather_station'] == station_id, 'Rainfall'
            ]

            # Perform a one-sample t-test
            test_result = stats.ttest_1samp(
                station_rainfall,
                popmean=reference_mean
            )

            # Extract the p-value
            p_value = test_result.pvalue

            # Check whether the result is statistically significant
            if p_value < alpha:
                print(
                    f"Significant difference in Rainfall at Station {station_id} "
                    f"(P-value: {p_value:.5f} ≤ {alpha}). H₀ rejected."
                )
            else:
                print(
                    f"No significant difference in Rainfall at Station {station_id} "
                    f"(P-value: {p_value:.5f} > {alpha}). H₀ not rejected."
                )

        return
    ### END FUNCTION
    return rainfall_ttest_results, station_rainfall_means


@app.cell
def _(MD_agric_df, rainfall_ttest_results, station_rainfall_means):
    rainfall_ttest_results(MD_agric_df, station_rainfall_means)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 6: Type I and Type II errors — written reflection

    Every hypothesis test can be wrong in two ways:

    - A **Type I error** rejects a null hypothesis that is actually true — a false alarm. α = 0.05 is the per-test probability of this happening.
    - A **Type II error** fails to reject a null hypothesis that is actually false — a miss. The probability depends on sample size and effect size.

    ### Task

    Answer the two questions below in the markdown cell provided.

    1. Our tests found statistically significant rainfall discrepancies at 4 of 5 stations. Is it plausible that all four rejections are Type I errors? Explain your reasoning using the α value.
    2. What would you examine next to determine whether each discrepancy is a data quality problem or a genuine physical difference between the station location and the surrounding fields?

    > **AI assist:** *"I ran hypothesis tests on agricultural field data and found significant discrepancies at 4 of 5 weather stations. Challenge my reasoning on whether this is consistent with Type I errors at α = 0.05."*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Your response:**

    1.

    2.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Wrap up

    The statistical toolkit is complete. You have moved from "does this fall within a tolerance window I invented?" to "is this difference too large to explain by chance?" — which is exactly the question the auditor needs answered.

    The verdict: rainfall discrepancies at 4 of 5 stations are statistically significant. Temperature, by contrast, checks out. The audit now has a specific, evidence-based claim to investigate rather than a vague concern about data quality.

    Before submitting:
    - The graded function `rainfall_ttest_results` must include a docstring.
    - All cells must run without errors from top to bottom.
    - Your written reflection in Challenge 6 must be completed.
    """)
    return


@app.cell
def cell_readiness():
    import inspect as _inspect
    import ast as _ast
    _spec = {'rainfall_ttest_results': {'expected_params': ['df', 'station_means', 'alpha']}}
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
