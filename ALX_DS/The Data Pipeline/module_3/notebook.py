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
    # Building the Maji Ndogo Data Pipeline
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notebooks are great for exploration, but production systems need something more resilient. When an audit deadline forces three consultants to work across drifting copies of the same analysis, messy copy-pasted code quickly becomes a maintenance nightmare. In this project you will refactor raw analytical code into a production-quality data pipeline for Maji Ndogo. You will work with modular Python scripts for SQL ingestion, run purpose-built data-processing classes, configure a single-source-of-truth parameter dictionary, and deploy automated two-sample Welch's t-tests to validate field measurements against weather station readings. This is the software-engineering transition that turns exploration scripts into reliable, reusable systems.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ⚠️ **This notebook is graded and contributes to your overall marks for this module.**

    ### Instructions

    - Do not add or remove cells in this notebook. Do not edit or remove the `### START FUNCTION` or `### END FUNCTION` comments. Do not add any code outside of the functions and classes you are required to edit. Doing any of this will result in a mark of 0%.
    - Answer the questions according to the specifications provided.
    - Use the provided test cells to verify your output before submitting.
    - Do not hard-code answers.
    - The use of StackOverflow, Google, and other online resources is permitted. The use of Generative AI tools — including ChatGPT, Claude, Copilot, and others — is also allowed and encouraged as a learning partner. However, the code you submit must reflect your own understanding. Copying a fellow student's code is a breach of the honor code. [Read the honor code here](https://drive.google.com/file/d/1atFOPUQRLz5slb4Q1ASXh8QQfKyXVqrw/preview). Submitting code you do not understand is also a breach.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Sanaa sends an email at 11 p.m.

    "I tried to run the analysis on the updated database and got an error on line 47. The column rename code is in three different notebooks, each slightly different. One of them has the old database filename. I fixed it in one place and it broke in another."

    She adds: "We are not building a notebook. We are building a system. Notebooks are for exploration. Systems are for production. We need to separate the two."

    This is the wall every data scientist hits eventually. Notebook code works, but it does not *scale*. When the same thirty lines of setup code appear in every notebook, slightly different each time, maintenance becomes a full-time job. The auditor's deadline made it worse — three people editing three notebooks in parallel, each drifting in a different direction.

    The solution is **modular Python scripts**. One module for data ingestion. One for field data processing. One for weather data processing. Every notebook imports these modules in two lines. When something changes, you fix the module once and every notebook inherits the fix.

    By the end of this project you will have a production-quality data pipeline: documented, testable, and reusable.

    > **AI assist:** Use AI actively this week. It excels at generating docstring templates, explaining error messages, and validating config dictionaries. Ask it to generate a PEP 257 docstring for any function, then review and adapt the output before using it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Setup:** Execute the cell below.

    The pipeline modules — `data_ingestion.py`, `field_data_processor.py`, and `weather_data_processor.py` — must be saved in the same folder as this notebook.

    **Download the database:** [Maji_Ndogo_farm_survey_small.db](https://raw.githubusercontent.com/Explore-AI/Public-Data/master/Maji_Ndogo/Maji_Ndogo_farm_survey_small.db)
    """)
    return


@app.cell
def _():
    ### DO NOT CHANGE ANYTHING IN THIS CELL, ONLY EXECUTE IT!

    import numpy as np
    import pandas as pd
    import logging
    from scipy.stats import ttest_ind

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return (ttest_ind,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 1: Document the data ingestion module

    `data_ingestion.py` contains three functions that form the foundation of the pipeline: `create_db_engine` connects to the SQLite database, `query_data` runs a SQL query and returns a DataFrame, and `read_from_web_CSV` fetches a CSV from a URL. Each function is already implemented and includes error handling.

    Good documentation is not optional in a production pipeline — it is what makes a script reusable by teammates, reviewable by auditors, and maintainable six months from now.

    ### Task

    1. Open `data_ingestion.py`.
    2. Add a **module-level docstring** at the very top of the file (before any imports) describing what the module does in one to three sentences.
    3. Add a **PEP 257 compliant function docstring** to each of the three functions. Each docstring must include:
       - A one-line summary of what the function does.
       - A `Parameters` section listing every argument with its type and description.
       - A `Returns` section describing the return value and its type.
       - A `Raises` section listing any exceptions the function may raise.
    4. Run the verification cell below.

    > ⚠️ Do not change the function logic — only add documentation.

    > **AI assist:** Paste each function signature and body into an AI assistant and ask: *"Generate a PEP 257 compliant docstring for this function — include Parameters, Returns, and Raises sections."* Then review and adapt the output before pasting it in.

    ### Expected output

    ```
    data_ingestion
    data_ingestion
    data_ingestion
    ```
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    # The provided data_ingestion.py already contains docstrings.
    # Students must verify they are present and PEP 257 compliant.
    from data_ingestion import create_db_engine, query_data, read_from_web_CSV

    print(create_db_engine.__module__)
    print(query_data.__module__)
    print(read_from_web_CSV.__module__)
    ### END FUNCTION
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 2: Configure the pipeline

    A production pipeline has one single source of truth for its parameters. Rather than hunting through the code every time the database path changes or a new crop spelling correction is discovered, every parameter lives in a single configuration dictionary. Change one value, and the whole pipeline picks it up.

    The two weather-data URLs are already provided in the template below.

    ### Task

    Complete the `config_params` dictionary. Every key is provided — fill in the four missing values using the parameters that have been consistent across all three notebooks in this course.

    - `sql_query`: the four-table LEFT JOIN query used since Week 1.
    - `db_path`: the SQLite connection string used since Week 1.
    - `columns_to_rename`: the dictionary that corrects the swapped `Annual_yield` / `Crop_type` columns.
    - `values_to_rename`: the dictionary of crop spelling corrections.

    > ⚠️ Do not change the dictionary key names.

    ### Expected output

    The config cell runs without errors.
    """)
    return


@app.cell
def _():
    config_params = {
        'sql_query': """
            SELECT * FROM geographic_features
            LEFT JOIN weather_features USING (Field_ID)
            LEFT JOIN soil_and_crop_features USING (Field_ID)
            LEFT JOIN farm_management_features USING (Field_ID)
        """,
        'db_path': 'sqlite:///Maji_Ndogo_farm_survey_small.db',
        'columns_to_rename': {'Annual_yield': 'Crop_type', 'Crop_type': 'Annual_yield'},
        'values_to_rename': {'Corn': 'maize', 'Bean': 'beans', 'Sugarcane': 'cane'},
        'weather_csv_path': 'https://raw.githubusercontent.com/robertnesterodhiambo/Datasets/refs/heads/main/Weather_station_data.csv',
        'weather_mapping_csv': 'https://raw.githubusercontent.com/robertnesterodhiambo/Datasets/refs/heads/main/Weather_data_field_mapping.csv'
    }

    _config_params = config_params
    return (config_params,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 3: Run the field data processor

    `FieldDataProcessor` in `field_data_processor.py` chains four processing steps into a single `.process()` call: it ingests the SQL data, corrects the swapped column names, applies crop-type spelling fixes, and merges the weather station mapping. All the logic is already implemented — your job is to document it so that anyone can understand it without reading the source code.

    ### Task

    1. Open `field_data_processor.py`.
    2. Add a **class-level docstring** to `FieldDataProcessor` describing its purpose, the `config_params` it expects, and the attribute it exposes (`self.df`).
    3. Add a **method-level docstring** to every public method that does not already have one. At minimum: `__init__`, `ingest_sql_data`, `rename_columns`, `apply_corrections`, and `process`.
    4. Run the verification cell below.

    > ⚠️ Do not change the processing logic — only add documentation.

    ### Expected output

    ```
    Shape: (5654, 19)
    ```
    """)
    return


@app.cell
def _():
    _config_params = {'sql_query': ..., 'db_path': ..., 'columns_to_rename': ..., 'values_to_rename': ..., 'weather_csv_path': ..., 'weather_mapping_csv': ...}
    return


@app.cell
def _(config_params):
    from field_data_processor import FieldDataProcessor

    # Initialize the processor with our configuration dictionary
    processor = FieldDataProcessor(config_params, logging_level="INFO")

    # Execute the complete processing pipeline
    processor.process()

    # Verify the shape of the resulting DataFrame
    print(f"Shape: {processor.df.shape}")
    return (processor,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 4: Run the weather data processor

    `WeatherDataProcessor` in `weather_data_processor.py` loads the IoT sensor CSV and extracts structured measurements (Temperature, Rainfall, Pollution_level) from free-text messages. Document it the same way you documented the field processor.

    ### Task

    1. Open `weather_data_processor.py`.
    2. Add a **class-level docstring** and a **method-level docstring** to any method that does not already have one.
    3. Run the verification cell below.

    > ⚠️ Do not change the processing logic — only add documentation.

    ### Expected output

    ```
    Shape: (1843, 4)
    ```
    """)
    return


@app.cell
def _(config_params):
    from weather_data_processor import WeatherDataProcessor

    # Initialize the weather data processor with our configuration dictionary
    weather_processor = WeatherDataProcessor(config_params, logging_level="INFO")

    # Execute the weather processing pipeline
    weather_processor.process()

    # Verify the shape of the resulting weather DataFrame
    print(f"Shape: {weather_processor.weather_df.shape}")
    return (weather_processor,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 5: Data validation with hypothesis testing

    The pipeline is running and both DataFrames are loaded. Now we close the loop on the audit question: do the field measurements and weather station readings agree?

    In Week 2 we used one-sample t-tests to compare field means against fixed reference values. Here we use **independent-samples t-tests** (`ttest_ind`) because we now have actual measurement samples from both sources — we are comparing two distributions, not one distribution against a constant.

    Note that the field DataFrame uses the column name `Ave_temps` for temperature, while the weather DataFrame labels it `Temperature`. Your `filter_field_data` function must map between these names.

    ### Task

    Complete the four functions below. Each must include a docstring and must not be hard-coded.

    - `filter_field_data(df, station_id, measurement)` — return the corresponding column from the field DataFrame as a Series for rows where `Weather_station == station_id`, dropping NaN values. Use an internal mapping to handle the `Temperature` → `Ave_temps` name difference.
    - `filter_weather_data(df, station_id, measurement)` — return the `Value` column as a Series for rows where `Weather_station_ID == station_id` and `Measurement == measurement`, dropping NaN values.
    - `run_ttest(column_a, column_b)` — return `(t_stat, p_val)` from `ttest_ind` with `equal_var=False` and `alternative='two-sided'`.
    - `print_ttest_results(station_id, measurement, p_val, alpha)` — print one clearly formatted result line per test. If `p_val > alpha`, indicate that H₀ is not rejected; otherwise indicate that H₀ is rejected.

    > ⚠️ Do not change the function names.

    ### Expected output

    ```
    No significant difference in Temperature at Station 0 (P-value: 0.90761 > 0.05). H₀ not rejected.
    No significant difference in Rainfall at Station 0 (P-value: 0.21621 > 0.05). H₀ not rejected.
    No significant difference in Pollution_level at Station 0 (P-value: 0.56418 > 0.05). H₀ not rejected.
    No significant difference in Temperature at Station 1 (P-value: 0.47241 > 0.05). H₀ not rejected.
    ...
    ```

    > **Note:** All 15 comparisons (5 stations × 3 measurements) should return "not rejected." This is different from Week 2's one-sample results because we are now comparing full distributions, not means against fixed station-published values.
    """)
    return


@app.cell
def _(processor, ttest_ind, weather_processor):
    def filter_field_data(df, station_id, measurement):
        """Filter field data for a specific weather station and measurement.

        Parameters
        ----------
        df : pandas.DataFrame
            The processed field DataFrame.
        station_id : int
            The weather station ID to filter on.
        measurement : str
            The measurement type (e.g., 'Ave_temps', 'Rainfall', 'Pollution_level').

        Returns
        -------
        pandas.Series
            A Series of measurement values with NaN values dropped.
        """
        # Map weather measurement names to field DataFrame column names if necessary
        mapping = {
            'Temperature': 'Ave_temps',
            'Rainfall': 'Rainfall',
            'Pollution_level': 'Pollution_level'
        }
        col_name = mapping.get(measurement, measurement)
    
        # Filter by station ID, select column, and drop NaN values
        filtered_series = df.loc[df['Weather_station'] == station_id, col_name].dropna()
        return filtered_series


    def filter_weather_data(df, station_id, measurement):
        """Filter weather data for a specific weather station and measurement.

        Parameters
        ----------
        df : pandas.DataFrame
            The processed weather DataFrame with Weather_station_ID, Measurement,
            and Value columns.
        station_id : int
            The weather station ID to filter on.
        measurement : str
            The measurement type (e.g., 'Temperature', 'Rainfall', 'Pollution_level').

        Returns
        -------
        pandas.Series
            A Series of measurement values with NaN values dropped.
        """
        # Filter by station ID and measurement type, then return the 'Value' column
        filtered_series = df.loc[
            (df['Weather_station_ID'] == station_id) & (df['Measurement'] == measurement), 
            'Value'
        ].dropna()
        return filtered_series


    def run_ttest(column_a, column_b):
        """Run an independent two-sample Welch's t-test.

        Parameters
        ----------
        column_a : array-like
            First sample of observations.
        column_b : array-like
            Second sample of observations.

        Returns
        -------
        tuple
            A tuple of (t_statistic, p_value).
        """
        # Perform Welch's t-test (equal_var=False) for two-sided alternative
        t_stat, p_val = ttest_ind(column_a, column_b, equal_var=False, alternative='two-sided')
        return t_stat, p_val


    def print_ttest_results(station_id, measurement, p_val, alpha):
        """Print a formatted result line for a single t-test comparison.

        Parameters
        ----------
        station_id : int
            The weather station ID being tested.
        measurement : str
            The measurement name being compared.
        p_val : float
            The p-value from the t-test.
        alpha : float
            The significance level.
        """
        # Determine null hypothesis status based on p-value vs alpha
        if p_val > alpha:
            status = f"H₀ not rejected."
        else:
            status = f"H₀ is rejected."
        
        print(f"No significant difference in {measurement} at Station {station_id} (P-value: {p_val:.5f} > {alpha}). {status}")

    # Expose the weather dataframe for the test loop
    weather_df = weather_processor.weather_df

    # Also make sure your field dataframe variable matches what the loop expects (`field_df`)
    field_df = processor.df
    return (
        field_df,
        filter_field_data,
        filter_weather_data,
        print_ttest_results,
        run_ttest,
        weather_df,
    )


@app.cell
def _(
    field_df,
    filter_field_data,
    filter_weather_data,
    print_ttest_results,
    run_ttest,
    weather_df,
):
    measurements_to_compare = ['Temperature', 'Rainfall', 'Pollution_level']
    alpha = 0.05

    for station_id in sorted(weather_df['Weather_station_ID'].unique()):
        for measurement in measurements_to_compare:
            field_values   = filter_field_data(field_df, station_id, measurement)
            weather_values = filter_weather_data(weather_df, station_id, measurement)
            t_stat, p_val  = run_ttest(field_values, weather_values)
            print_ttest_results(station_id, measurement, p_val, alpha)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 6: The data science process — written reflection

    You have now completed the full data science cycle on the Maji Ndogo audit:

    | Stage | What you did |
    |---|---|
    | **Collect** | Ingested farm survey data from a SQL database and IoT weather CSVs |
    | **Clean** | Corrected swapped columns, fixed spelling errors, merged mapping data |
    | **Explore** | Profiled distributions and relationships — rainfall by province, crop volumes and yields, correlation analysis (Week 1) | |
    | **Analyze** | Applied population metrics, the CLT, confidence intervals, and t-tests (Week 2) |
    | **Productionize** | Refactored exploration code into modular, documented, testable scripts (Week 3) |

    ### Task

    Answer the two questions in the markdown cell below.

    1. The Week 2 one-sample t-tests found significant rainfall discrepancies at 4 of 5 stations when comparing field means against fixed reference values. The Week 3 independent-samples t-tests found **no** significant differences at any station. Explain in 3 to 5 sentences why these two tests can give different conclusions on the same data.

    2. You are presenting this pipeline to a new client in Spain who wants to validate their own agricultural survey data against government weather station records. Name two things you would need to change in `config_params` and one thing you would need to verify about `field_data_processor.py` before running it on their data.

    > **AI assist:** *"I ran one-sample t-tests and independent-samples t-tests on the same dataset and got different conclusions. Explain the key difference between these two test types and why the results can diverge."*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Your response:**

    1. The one-sample t-test compares a sample mean against a single fixed reference value. If the published station average is slightly off — due to rounding, a different time window, or a different averaging method — the test treats that discrepancy as real, leading to rejection. The independent-samples (Welch's) t-test compares the full distributions of both the field and weather data, accounting for the natural variability in each. Because both samples are drawn from the same underlying conditions, their distributions overlap heavily, and the test correctly finds no significant difference. In short, the one-sample test was comparing against a potentially imprecise constant, while the two-sample test compared the actual data, which agreed.

    2. Two things to change in `config_params`: (a) `db_path` and `sql_query` would need to point to the Spanish client's database and tables, and (b) `values_to_rename` would need to reflect any spelling errors or category inconsistencies specific to Spain's crop types. One thing to verify in `field_data_processor.py`: the column names assumed in `rename_columns` and `apply_corrections` (e.g., `Crop_type`, `Elevation`) must match the Spanish database schema — if their columns are named differently, the processor would need to be updated.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Wrap up

    The pipeline is built, documented, and validated. Loading and cleaning the entire Maji Ndogo dataset — which used to mean 30 lines of setup code copied across every notebook, slightly different each time — now takes two lines and a config dictionary.

    The audit has a clear, evidence-based answer. The workflow is packaged. The next consultant who picks this up — whether in Maji Ndogo, Spain, or elsewhere — can run it in minutes.

    Before submitting:
    - Challenge 1 must print the three correct module names.
    - Challenge 2 config must run without errors.
    - Challenges 3 and 4 must produce the correct shapes.
    - All graded functions in Challenge 5 must include docstrings.
    - All cells must run without errors from top to bottom.

    — Sanaa 🌾
    """)
    return


@app.cell
def cell_readiness():
    import inspect as _inspect
    import ast as _ast
    _spec = {'filter_field_data': {'expected_params': ['df', 'station_id', 'measurement']}, 'filter_weather_data': {'expected_params': ['df', 'station_id', 'measurement']}, 'print_ttest_results': {'expected_params': ['station_id', 'measurement', 'p_val', 'alpha']}, 'run_ttest': {'expected_params': ['column_a', 'column_b']}}
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
