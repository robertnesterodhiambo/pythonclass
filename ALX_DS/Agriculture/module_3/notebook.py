import marimo

__generated_with = "0.24.0"
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
    # Understanding Maji Ndogo's Agriculture
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The Minister wants a planting recommendation by Friday morning, and the answer is sitting in a database nobody can question fast enough. This week you turn four raw survey tables into a single **Pandas** DataFrame and interrogate it: which crop thrives in the highlands, which soils are most productive, and exactly which fields meet every condition for a strong harvest. Loading and joining SQL tables, cleaning the messy real-world entries, then grouping, filtering, sorting, and querying your way to an answer — the core data-analysis loop, on real data, delivered against a deadline. The closing piece of your Maji Ndogo engagement, and the one the Minister will actually read.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ⚠️ **This challenge is graded and contributes to your overall marks for this module.**

    ### Instructions

    - Do not add or remove cells in this notebook. Do not edit or remove the `### START FUNCTION` or `### END FUNCTION` comments. Do not add any code outside of the functions you are required to edit. Doing any of this will result in a mark of 0%.
    - Answer the questions according to the specifications provided.
    - Use the provided test cells to verify your output before submitting.
    - Do not hard-code answers.
    - The use of StackOverflow, Google, and other online resources is permitted. The use of Generative AI tools — including ChatGPT, Claude, Copilot, and others — is also allowed and encouraged as a learning partner. However, the code you submit must reflect your own understanding. Copying a fellow student's code is a breach of the honor code. [Read the honor code here](https://drive.google.com/file/d/1atFOPUQRLz5slb4Q1ASXh8QQfKyXVqrw/preview). Submitting code you do not understand is also a breach.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Sanaa's phone rings on Thursday afternoon.

    "The Minister needs a crop recommendation for the northern highland plots by Friday morning," the assistant says. "Specifically: which crop performs best up there, what soil types are most productive, and which fields should be prioritized for the next planting cycle."

    Sanaa puts the phone down and looks at you. "We have the data. We have the Field Registry. What we do not have is a fast way to ask it questions."

    That changes today. The tools you need are already installed: **Pandas** turns the farm survey database into a structured DataFrame that you can filter, group, sort, and transform with single lines of code. The analysis that takes an afternoon with raw Python takes twenty minutes with Pandas.

    The Ministry is waiting.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Setup:** Execute the cell below.

    **Download:** [Maji_Ndogo_farm_survey_small.db](https://raw.githubusercontent.com/Explore-AI/Public-Data/master/Maji_Ndogo/Maji_Ndogo_farm_survey_small.db) — save it in the same folder as this notebook before running.
    """)
    return


@app.cell
def _():
    ### DO NOT CHANGE ANYTHING IN THIS CELL, ONLY EXECUTE IT!

    import pandas as pd
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

    # Wrangling: the 'Crop_type' and 'Annual_yield' labels were swapped on export, so swap them back;
    # elevations were stored with the wrong sign; and a few crop names were misspelt.
    MD_agric_df.rename(columns={'Annual_yield': 'Crop_type_Temp', 'Crop_type': 'Annual_yield'}, inplace=True)
    MD_agric_df.rename(columns={'Crop_type_Temp': 'Crop_type'}, inplace=True)
    MD_agric_df['Elevation'] = MD_agric_df['Elevation'].abs()
    corrections = {'cassaval': 'cassava', 'wheatn': 'wheat', 'teaa': 'tea'}
    MD_agric_df['Crop_type'] = MD_agric_df['Crop_type'].apply(
        lambda crop: corrections.get(crop.strip(), crop.strip())
    )
    print(f'Loaded: {MD_agric_df.shape[0]} rows × {MD_agric_df.shape[1]} columns')
    return (MD_agric_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Data dictionary

    **Geographic features**
    | Column | Description | Type |
    |--------|-------------|------|
    | Field_ID | Unique identifier for each field | BigInt |
    | Elevation | Elevation above sea level in meters | Float |
    | Latitude / Longitude | Geographic coordinates in degrees | Float |
    | Location | Province the field is in | Text |
    | Slope | Slope of the land in degrees | Float |

    **Weather features**
    | Column | Description | Type |
    |--------|-------------|------|
    | Rainfall | Annual rainfall in mm | Float |
    | Min_temperature_C | Average minimum temperature in °C | Float |
    | Max_temperature_C | Average maximum temperature in °C | Float |
    | Ave_temps | Average temperature in °C — mean of Min and Max | Float |

    **Soil features**
    | Column | Description | Type |
    |--------|-------------|------|
    | Soil_fertility | Normalized fertility index, 0–1 | Float |
    | Soil_type | Categorical soil classification | Text |
    | pH | Soil pH level | Float |

    **Farm management features**
    | Column | Description | Type |
    |--------|-------------|------|
    | Pollution_level | Normalized pollution index, 0–1 | Float |
    | Plot_size | Field area in hectares | Float |
    | Crop_type | Type of crop grown | Text |
    | Annual_yield | Total annual yield in tonnes | Float |
    | Standard_yield | Normalized yield score, 0–1 | Float |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 1: Crop distribution

    Before recommending where to plant, we need to understand where crops currently grow and what conditions they share. For a given crop type, the average rainfall and average elevation immediately tells us whether it is a highland or lowland species.

    ### Task

    Complete `explore_crop_distribution(df, crop_filter)`. It must filter the DataFrame to rows where `Crop_type` matches `crop_filter`, then return a **tuple** of `(mean Rainfall, mean Elevation)` as plain Python floats.

    > ⚠️ Do not change the function name `explore_crop_distribution`.

    ### Expected output

    **Input 1:** `explore_crop_distribution(MD_agric_df, 'tea')` → `(1534.5079956188388, 775.208667535597)`

    **Input 2:** `explore_crop_distribution(MD_agric_df, 'wheat')` → `(1010.2859910581222, 595.8384148002981)`
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def explore_crop_distribution(df, crop_filter):
        # Insert your code here
        crop_df = df[df['Crop_type'] == crop_filter]

        mean_rainfall = float(crop_df['Rainfall'].mean())
        mean_elevation = float(crop_df['Elevation'].mean())

        return (mean_rainfall, mean_elevation)
    ### END FUNCTION
    return (explore_crop_distribution,)


@app.cell
def _(MD_agric_df, explore_crop_distribution):
    explore_crop_distribution(MD_agric_df, 'tea')
    return


@app.cell
def _(MD_agric_df, explore_crop_distribution):
    explore_crop_distribution(MD_agric_df, 'wheat')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 2: Soil fertility by type

    Soil type is one of the strongest predictors of crop success.

    ### Task

    Complete `analyse_soil_fertility(df)`. It must group the DataFrame by `Soil_type`, calculate the mean `Soil_fertility` per group, and return the result as a **Pandas Series**.

    > ⚠️ Do not change the function name `analyse_soil_fertility`.

    ### Expected output

    ```
    Soil_type
    Loamy       0.585868
    Peaty       0.604882
    Rocky       0.582368
    Sandy       0.595669
    Silt        0.652654
    Volcanic    0.648894
    Name: Soil_fertility, dtype: float64
    ```
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def analyse_soil_fertility(df):
        # Insert your code here
        soil_fertility = df.groupby('Soil_type')['Soil_fertility'].mean()
        return soil_fertility
    ### END FUNCTION
    return (analyse_soil_fertility,)


@app.cell
def _(MD_agric_df, analyse_soil_fertility):
    analyse_soil_fertility(MD_agric_df)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 3: Climate and geography by crop

    For every crop type, we need the average elevation, minimum temperature, maximum temperature, and rainfall.

    ### Task

    Complete `climate_geography_influence(df, column)`. It must group the DataFrame by `column`, calculate the mean of `Elevation`, `Min_temperature_C`, `Max_temperature_C`, and `Rainfall` — **in that order** — and return the result as a **DataFrame**.

    > ⚠️ Do not change the function name `climate_geography_influence`.

    ### Expected output

    ```
                 Elevation  Min_temperature_C  Max_temperature_C    Rainfall
    Crop_type
    banana      487.973572          -5.354344          31.988152  1659.905687
    cassava     682.903008          -3.992113          30.902381  1210.543006
    coffee      647.047734          -4.028007          30.855189  1527.265074
    maize       680.596982          -4.497995          30.576692   681.010276
    potato      696.313917          -4.375334          30.300608   660.289064
    rice        352.858053          -6.610566          32.727170  1632.382642
    tea         775.208668          -2.862651          29.950383  1534.507996
    wheat       595.838415          -4.968107          30.973845  1010.285991
    ```
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def climate_geography_influence(df, column):
        # Insert your code here
        columns = [
            'Elevation',
            'Min_temperature_C',
            'Max_temperature_C',
            'Rainfall'
        ]

        result = df.groupby(column)[columns].mean()
        return result
    ### END FUNCTION
    return (climate_geography_influence,)


@app.cell
def _(MD_agric_df, climate_geography_influence):
    climate_geography_influence(MD_agric_df, 'Crop_type')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 4: Top-performing crop

    Time to identify Maji Ndogo's single best-performing crop — the one with the most fields exceeding the average `Standard_yield`.

    **Hint:** After grouping, the labels of the grouping column can be accessed with `.index`. For example:
    ```python
    grouped_df = MD_agric_df.groupby('Soil_type').mean(numeric_only=True).sort_values('Elevation', ascending=False)
    print(grouped_df.index[0])
    ```

    ### Task

    Complete `find_ideal_fields(df)`. It must:
    1. Filter to fields with an above-average `Standard_yield`.
    2. Group by `Crop_type` and count records per group.
    3. Sort to put the highest count first.
    4. Return the `Crop_type` name at index 0 as a **string**.

    > ⚠️ Do not change the function name `find_ideal_fields`.

    ### Expected output

    **Input 1:** `type(find_ideal_fields(MD_agric_df))` → `<class 'str'>`

    **Input 2:** `print('Top-performing crop:', find_ideal_fields(MD_agric_df))` → `Top-performing crop: tea`
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def find_ideal_fields(df):
        # Insert your code here
        average_yield = df['Standard_yield'].mean()

        ideal_fields = df[df['Standard_yield'] > average_yield]

        crop_counts = ideal_fields.groupby('Crop_type').size()

        crop_counts = crop_counts.sort_values(ascending=False)

        return str(crop_counts.index[0])
    ### END FUNCTION
    return (find_ideal_fields,)


@app.cell
def _(MD_agric_df, find_ideal_fields):
    type(find_ideal_fields(MD_agric_df))
    return


@app.cell
def _(MD_agric_df, find_ideal_fields):
    print('Top-performing crop:', find_ideal_fields(MD_agric_df))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 5: Ideal growing conditions

    Given a crop type, return only the fields that meet all four quality criteria simultaneously. This is a natural fit for the `.query()` method, which reads almost like the sentence above — though a boolean mask works just as well.

    ### Task

    Complete `find_good_conditions(df, crop_type)`. Filter to rows where:
    1. `Crop_type` matches `crop_type`.
    2. `Standard_yield` is above that crop's own mean `Standard_yield`.
    3. `Ave_temps` is between 12 and 15 (inclusive).
    4. `Pollution_level` is below 0.0001.

    Return the filtered **DataFrame**.

    > 📌 `Ave_temps` is pre-computed in the database as the average of `Min_temperature_C` and `Max_temperature_C`.

    > ⚠️ Do not change the function name `find_good_conditions`.

    ### Expected output

    **Input 1:** `find_good_conditions(MD_agric_df, 'tea').shape` → `(14, 18)`
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def find_good_conditions(df, crop_type):
        # Insert your code here
        crop_df = df[df['Crop_type'] == crop_type]

        average_yield = crop_df['Standard_yield'].mean()

        good_fields = crop_df[
            (crop_df['Standard_yield'] > average_yield) &
            (crop_df['Ave_temps'] >= 12) &
            (crop_df['Ave_temps'] <= 15) &
            (crop_df['Pollution_level'] < 0.0001)
        ]

        return good_fields
    ### END FUNCTION
    return (find_good_conditions,)


@app.cell
def _(MD_agric_df, find_good_conditions):
    find_good_conditions(MD_agric_df, 'tea').shape
    return


@app.cell
def _(MD_agric_df, find_good_conditions, find_ideal_fields):
    find_good_conditions(MD_agric_df, find_ideal_fields(MD_agric_df)).head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Wrapping up

    Five functions. Together they answer the questions the Ministry put on the table:

    1. What conditions define each crop? → `explore_crop_distribution` and `climate_geography_influence`
    2. Which soil types are most productive? → `analyse_soil_fertility`
    3. Which crop performs best and under what precise conditions? → `find_ideal_fields` and `find_good_conditions`

    The recommendation writes itself: **tea**, in the cool, clean, high-elevation plots of the northern highlands. And the work behind it — joining four tables, cleaning the data, then grouping, filtering, sorting, and querying — is the everyday loop of a working data analyst. Across this course you went from raw algorithms to objects to a real Pandas analysis delivered on a deadline, proof you can take a question from a decision-maker and return an answer they can act on.

    Make sure all cells run without errors before submitting. The Ministry meeting is at eight.

    — Sanaa 🌾
    """)
    return


@app.cell
def cell_readiness():
    import inspect as _inspect
    import ast as _ast
    _spec = {'analyse_soil_fertility': {'expected_params': ['df']}, 'climate_geography_influence': {'expected_params': ['df', 'column']}, 'explore_crop_distribution': {'expected_params': ['df', 'crop_filter']}, 'find_good_conditions': {'expected_params': ['df', 'crop_type']}, 'find_ideal_fields': {'expected_params': ['df']}}
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
