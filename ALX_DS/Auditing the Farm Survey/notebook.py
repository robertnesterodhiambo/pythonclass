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
    # Auditing the Farm Survey
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A working answer is not the same as a usable one. When a survey grows from 5,654 fields toward a million, the gap between `O(n)` and `O(log n)` is the gap between an inspector getting her reading and missing her window. In this project you build an **auditing engine** for the Maji Ndogo farm survey: linear and binary search to find a field, a recursive merge sort to rank the harvest, lambda-powered `map` and `filter` to flag and project, and the Big O vocabulary to say precisely why each choice scales. It is exactly the kind of efficiency-minded work on real data that belongs in a data-science portfolio.
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
    - Do not hard-code answers — your functions must work on unseen inputs.
    - The use of StackOverflow, Google, and other online resources is permitted. The use of Generative AI tools — including ChatGPT, Claude, Copilot, and others — is also allowed and encouraged as a learning partner. However, the code you submit must reflect your own understanding. Copying a fellow student's code is a breach of the honor code. [Read the honor code here](https://drive.google.com/file/d/1atFOPUQRLz5slb4Q1ASXh8QQfKyXVqrw/preview). Submitting code you do not understand is also a breach.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The radio crackles at 2:14 p.m.

    "Field 672. Pollution level. Now."

    The inspector is standing in the middle of a potato field in the Sokoto lowlands with a clipboard and a deadline. Her truck's satellite link is down. She needs the pollution reading for that specific field — out of 5,654 records — in under ten seconds, or she misses her reporting window and the entire audit gets rescheduled.

    On your laptop, you have the farm survey database. You have Python. You have a list of 5,654 dictionaries.

    You also have a problem: the code you have right now loops through every single record from the first to the last, checking each one. On this dataset, that takes less than a second. But Maji Ndogo's ambition is to grow this system to cover one million farms across the region within five years. At that scale, the same loop takes minutes. The inspector does not have minutes.

    **This is the challenge of algorithmic efficiency.** The question is not just "does this code work?" — it is "does this code work *fast enough* when the data is ten times larger? A hundred times larger? A million records?" The Big O notation you are about to learn is the vocabulary for answering that question precisely.
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

    import sqlite3

    # Connect to the Maji Ndogo farm survey database.
    # Make sure the .db file is in the same folder as this notebook.
    connection = sqlite3.connect('Maji_Ndogo_farm_survey_small.db')
    cursor = connection.cursor()

    cursor.execute(
        """SELECT Field_ID, Pollution_level, Plot_size, Annual_yield, Crop_type, Standard_yield
           FROM farm_management_features"""
    )

    # The Crop_type and Annual_yield labels were swapped when the survey was digitised,
    # so we swap them back while building our list of field records.
    field_records = []
    for row in cursor.fetchall():
        field_records.append({
            'Field_ID': row[0],
            'Pollution_level': round(row[1], 4),
            'Plot_size': row[2],
            'Crop_type': row[3],                # stored under 'Annual_yield' in the database
            'Annual_yield': round(row[4], 4),   # stored under 'Crop_type' in the database
            'Standard_yield': round(row[5], 4),
        })

    connection.close()

    print(f"Loaded {len(field_records)} field records.")
    return (field_records,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The expected outputs for each challenge use a five-record sample. Execute the cell below to create it.
    """)
    return


@app.cell
def _():
    ### DO NOT CHANGE ANYTHING IN THIS CELL, ONLY EXECUTE IT!

    maji_ndogo_sample = [
        {'Field_ID': 40734, 'Pollution_level': 0.0853, 'Plot_size': 1.3, 'Crop_type': 'cassava', 'Annual_yield': 0.7514, 'Standard_yield': 0.578},
        {'Field_ID': 30629, 'Pollution_level': 0.3997, 'Plot_size': 2.2, 'Crop_type': 'cassava', 'Annual_yield': 1.0699, 'Standard_yield': 0.4863},
        {'Field_ID': 39924, 'Pollution_level': 0.358, 'Plot_size': 3.4, 'Crop_type': 'tea', 'Annual_yield': 2.2088, 'Standard_yield': 0.6496},
        {'Field_ID': 5754, 'Pollution_level': 0.2867, 'Plot_size': 2.4, 'Crop_type': 'cassava', 'Annual_yield': 1.2776, 'Standard_yield': 0.5323},
        {'Field_ID': 14146, 'Pollution_level': 0.0432, 'Plot_size': 1.5, 'Crop_type': 'wheat', 'Annual_yield': 0.8326, 'Standard_yield': 0.5551}
    ]
    return (maji_ndogo_sample,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 1: Linear search

    The survey records are stored in the order the teams submitted them — no sorting, no index. When an inspector calls in a `Field_ID`, we start at record one and check every record until we find a match. This is a **linear search**: `O(n)` — in the worst case, it inspects every record.

    ### Task

    Complete `linear_search_field(field_list, target_id)`. It must:
    - Iterate through `field_list`.
    - Return the `Pollution_level` of the first record whose `Field_ID` matches `target_id`.
    - Return `None` if no match is found.

    > ⚠️ Do not change the function name `linear_search_field`.

    ### Expected outputs

    **Input 1:** `linear_search_field(maji_ndogo_sample, 39924)` → `0.358`

    **Input 2:** `print(linear_search_field(maji_ndogo_sample, 99999))` → `None`
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def linear_search_field(field_list, target_id):
        # Insert your code here
        for field in field_list:
            if field['Field_ID'] == target_id:
                return field['Pollution_level']
        return
    ### END FUNCTION
    return (linear_search_field,)


@app.cell
def _(linear_search_field, maji_ndogo_sample):
    linear_search_field(maji_ndogo_sample, 39924)
    return


@app.cell
def _(linear_search_field, maji_ndogo_sample):
    print(linear_search_field(maji_ndogo_sample, 99999))
    return


@app.cell
def _(field_records, linear_search_field):
    # On the full 5,654-record survey:
    linear_search_field(field_records, 672)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 2: Binary search

    If the records are **sorted by `Field_ID`**, we can do much better. Jump to the middle record. Is the target ID higher or lower? Discard half the list. Repeat. This is a **binary search**: `O(log n)` — at one million records, it takes roughly 20 comparisons instead of one million.

    The cost: the data must be sorted first.

    ### Task

    Complete `binary_search_yield(sorted_field_list, target_id)`. Assume the input is already sorted by `Field_ID` in ascending order. Return the `Annual_yield` of the matching record, or `None` if not found.

    > ⚠️ Do not change the function name `binary_search_yield`.

    ### Expected outputs

    **Input 1:**
    ```python
    sorted_sample = sorted(maji_ndogo_sample, key=lambda f: f['Field_ID'])
    binary_search_yield(sorted_sample, 30629)
    ```
    `1.0699`

    **Input 2:**
    ```python
    sorted_sample = sorted(maji_ndogo_sample, key=lambda f: f['Field_ID'])
    print(binary_search_yield(sorted_sample, 11111))
    ```
    `None`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Note**: lambda is explained in Challenge 4 — here it just tells sorted() what value to sort by.
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def binary_search_yield(sorted_field_list, target_id):
        # Insert your code here
        left = 0
        right = len(sorted_field_list) - 1

        while left <= right:
            mid = (left + right) // 2
            field = sorted_field_list[mid]

            if field['Field_ID'] == target_id:
                return field['Annual_yield']
            elif field['Field_ID'] < target_id:
                left = mid + 1
            else:
                right = mid - 1
        return
    ### END FUNCTION
    return (binary_search_yield,)


@app.cell
def _(binary_search_yield, maji_ndogo_sample):
    _sorted_sample = sorted(maji_ndogo_sample, key=lambda f: f['Field_ID'])
    binary_search_yield(_sorted_sample, 30629)
    return


@app.cell
def _(binary_search_yield, maji_ndogo_sample):
    _sorted_sample = sorted(maji_ndogo_sample, key=lambda f: f['Field_ID'])
    print(binary_search_yield(_sorted_sample, 11111))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 3: Merge sort

    Binary search needs sorted data. We need a sorter. Bubble sort is `O(n²)`: double the records, quadruple the work. **Merge sort** is `O(n log n)`: it splits the list in half, sorts each half **recursively**, then merges the two sorted halves.

    Pseudocode:
    ```
    merge_sort(list):
        if len(list) <= 1: return list
        mid   = len(list) // 2
        left  = merge_sort(list[:mid])
        right = merge_sort(list[mid:])
        return merge(left, right)
    ```

    ### Task

    Complete `merge_sort_yields(field_list)` and the helper `merge(left, right)`. Sort records into **descending** order of `Annual_yield` (highest yield first). `merge_sort_yields` must be recursive and must call `merge`.

    > ⚠️ Do not change either function name.

    ### Expected outputs

    **Input 1:** `merge_sort_yields(maji_ndogo_sample)` →
    ```
    [{'Field_ID': 39924, 'Pollution_level': 0.358, 'Plot_size': 3.4, 'Crop_type': 'tea', 'Annual_yield': 2.2088, 'Standard_yield': 0.6496},
     {'Field_ID': 5754, 'Pollution_level': 0.2867, 'Plot_size': 2.4, 'Crop_type': 'cassava', 'Annual_yield': 1.2776, 'Standard_yield': 0.5323},
     {'Field_ID': 30629, 'Pollution_level': 0.3997, 'Plot_size': 2.2, 'Crop_type': 'cassava', 'Annual_yield': 1.0699, 'Standard_yield': 0.4863},
     {'Field_ID': 14146, 'Pollution_level': 0.0432, 'Plot_size': 1.5, 'Crop_type': 'wheat', 'Annual_yield': 0.8326, 'Standard_yield': 0.5551},
     {'Field_ID': 40734, 'Pollution_level': 0.0853, 'Plot_size': 1.3, 'Crop_type': 'cassava', 'Annual_yield': 0.7514, 'Standard_yield': 0.578}]
    ```

    **Input 2:** `[f['Annual_yield'] for f in merge_sort_yields(maji_ndogo_sample)[:3]]` → `[2.2088, 1.2776, 1.0699]`
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def merge_sort_yields(field_list):
        if len(field_list) <= 1:
            return field_list

        mid = len(field_list) // 2

        left = merge_sort_yields(field_list[:mid])
        right = merge_sort_yields(field_list[mid:])

        return merge(left, right)


    def merge(left, right):
        sorted_list = []
        i = 0
        j = 0

        while i < len(left) and j < len(right):
            if left[i]['Annual_yield'] >= right[j]['Annual_yield']:
                sorted_list.append(left[i])
                i += 1
            else:
                sorted_list.append(right[j])
                j += 1

        while i < len(left):
            sorted_list.append(left[i])
            i += 1

        while j < len(right):
            sorted_list.append(right[j])
            j += 1

        return sorted_list
    ### END FUNCTION
    return (merge_sort_yields,)


@app.cell
def _(maji_ndogo_sample, merge_sort_yields):
    merge_sort_yields(maji_ndogo_sample)
    return


@app.cell
def _(maji_ndogo_sample, merge_sort_yields):
    [f['Annual_yield'] for f in merge_sort_yields(maji_ndogo_sample)[:3]]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 4: Lambda and filter — flagging polluted fields

    Any field above a pollution threshold needs an inspection visit, and the list must update as thresholds change. Python's `filter()` with a `lambda` makes this one readable line.

    ### Task

    Complete `identify_high_pollution(field_list, threshold)`. Use `filter()` and a `lambda` to return only the records whose `Pollution_level` is **strictly greater than** `threshold`. Return the result as a list.

    > ⚠️ Do not change the function name `identify_high_pollution`.

    ### Expected outputs

    **Input 1:** `identify_high_pollution(maji_ndogo_sample, 0.3)` →
    ```python
    [{'Field_ID': 30629, 'Pollution_level': 0.3997, 'Plot_size': 2.2, 'Crop_type': 'cassava', 'Annual_yield': 1.0699, 'Standard_yield': 0.4863},
     {'Field_ID': 39924, 'Pollution_level': 0.358, 'Plot_size': 3.4, 'Crop_type': 'tea', 'Annual_yield': 2.2088, 'Standard_yield': 0.6496}]
    ```

    **Input 2:** `identify_high_pollution(maji_ndogo_sample, 0.5)` → `[]`
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def identify_high_pollution(field_list, threshold):
        return list(filter(lambda field: field['Pollution_level'] > threshold, field_list))
    ### END FUNCTION
    return (identify_high_pollution,)


@app.cell
def _(identify_high_pollution, maji_ndogo_sample):
    identify_high_pollution(maji_ndogo_sample, 0.3)
    return


@app.cell
def _(identify_high_pollution, maji_ndogo_sample):
    identify_high_pollution(maji_ndogo_sample, 0.5)
    return


@app.cell
def _(field_records, identify_high_pollution):
    # On the full survey: how many fields exceed a 0.9 pollution level?
    len(identify_high_pollution(field_records, 0.9))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 5: Lambda and map — projecting harvests

    If `filter()` decides which items to *keep*, `map()` transforms *every* item. The Ministry of Agriculture wants a quick harvest projection for each field: `Plot_size` × `Standard_yield`, rounded to 2 decimal places.

    ### Task

    Complete `project_harvests(field_list)`. Use `map()` and a `lambda` to compute each field's projected yield (`Plot_size * Standard_yield`, rounded to 2 decimals). Return the result as a list.

    > ⚠️ Do not change the function name `project_harvests`.

    ### Expected outputs

    **Input 1:** `project_harvests(maji_ndogo_sample)` → `[0.75, 1.07, 2.21, 1.28, 0.83]`

    **Input 2:** `project_harvests(maji_ndogo_sample[2:4])` → `[2.21, 1.28]`
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def project_harvests(field_list):
        return list(map(lambda field: round(field['Plot_size'] * field['Standard_yield'], 2), field_list))
    ### END FUNCTION
    return (project_harvests,)


@app.cell
def _(maji_ndogo_sample, project_harvests):
    project_harvests(maji_ndogo_sample)
    return


@app.cell
def _(maji_ndogo_sample, project_harvests):
    project_harvests(maji_ndogo_sample[2:4])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Wrapping up

    The auditing engine is complete. Six functions: find any field by ID two different ways, rank the harvest with a recursive sort, flag the polluted land, project production, and name the computational cost of each approach — all in code that stays fast as the survey grows.

    That last point is the real deliverable. Anyone can write a loop that works on 5,654 records. Writing code whose cost you can *predict and defend* as the data heads toward a million records is what separates a script from an engine — and it is the third asset in your Maji Ndogo portfolio.

    Make sure every function runs without errors and matches the expected outputs before submitting.
    """)
    return


@app.cell
def cell_readiness():
    import inspect as _inspect
    import ast as _ast
    _spec = {'binary_search_yield': {'expected_params': ['sorted_field_list', 'target_id']}, 'identify_high_pollution': {'expected_params': ['field_list', 'threshold']}, 'linear_search_field': {'expected_params': ['field_list', 'target_id']}, 'merge': {'expected_params': ['left', 'right']}, 'merge_sort_yields': {'expected_params': ['field_list']}, 'project_harvests': {'expected_params': ['field_list']}}
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


if __name__ == "__main__":
    app.run()
