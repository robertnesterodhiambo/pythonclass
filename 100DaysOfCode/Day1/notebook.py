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
    # Farm harvest management
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It's 6:47 a.m., the minister's meeting is at eight, and a notepad of harvest figures needs to become numbers a ministry can trust. Your first job in Maji Ndogo: turn two test fields' worth of scribbles into a clean season record — harvest, costs, revenue, and profit — using nothing but Python's raw building blocks.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **This challenge is graded.** It tests your mastery of Python fundamentals: data types, operators, strings, string formatting, and core data structures (lists, tuples, sets, dictionaries).

    ### Instructions

    - Do not add or remove cells in this notebook.
    - Do not edit or remove the `### START FUNCTION` or `### END FUNCTION` comments.
    - Do not add any code outside of the functions you are required to complete.
    - Answer the questions according to the specifications provided.
    - You will only use tools introduced this week: variables, data types, type casting, operators, strings, string formatting, and the core data structures (lists, tuples, sets, dictionaries). No loops, conditionals, or functions yet — those come later.
    - The use of StackOverflow, Google, Generative AI tools, and any other online resources is permitted. Use AI to help you understand — not to shortcut the thinking. [Read the honor code here](https://drive.google.com/file/d/1atFOPUQRLz5slb4Q1ASXh8QQfKyXVqrw/preview).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You did not expect your first day at the Maji Ndogo Ministry of Agriculture to involve a spreadsheet crisis, but here you are.

    Sanaa, the ministry's data team lead, meets you at the door with a coffee and a problem. "Our field teams submitted harvest numbers this morning," she says, sliding a notepad across the table. "Two test fields — wheat and potato. I need the total harvest, the cost, the revenue, and the profit before the minister's meeting at eight. Finance needs it in code, not a napkin — our programmer takes over next week and has to understand every number."

    You open your laptop. It is 6:47 a.m.

    ---

    **Welcome to Maji Ndogo.**

    Maji Ndogo is a region of about 5,654 smallholder farms spread across highlands, river plains, and dry plateaus. Tea and coffee grow in the cool upper elevations; wheat, potato, cassava, maize, rice, and banana dominate the warmer lowlands. Farming is the economic backbone of the region — and it is in trouble. Yields vary wildly from field to field with no clear explanation. Some plots are contaminated. Others are underperforming despite good soil. The Ministry has launched an initiative to fix this with data science, and you have just been hired as the consultant.

    This first task is deliberately simple. No databases, no libraries, no functions yet — just the raw building blocks of Python. By the end you will have turned a notepad into a clean, readable season record: exactly the kind of artifact a ministry can trust — and the foundation everything later builds on.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 1: Total harvest

    Sanaa's notepad shows two entries:

    - **Field 18442 (wheat):** 2,050 kg harvested this season
    - **Field 52711 (potato):** 3,600 kg harvested this season

    ### Task

    Complete the function `calculate_total_harvest` that takes two harvest values (wheat and potato) and returns their sum.

    ### Expected output

    ```
    5650
    ```
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def calculate_total_harvest(wheat_kg, potato_kg):
        """
        Calculate the total harvest from wheat and potato fields.

        Parameters
        ----------
        wheat_kg : int or float
            Kilograms of wheat harvested.
        potato_kg : int or float
            Kilograms of potato harvested.

        Returns
        -------
        int or float
            Total harvest in kilograms.
        """
        return wheat_kg + potato_kg
    ### END FUNCTION

    # Test
    print(calculate_total_harvest(2050, 3600))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 2: Total expenses

    Running both fields this season cost:

    - Seeds: $650
    - Labour: $3,070

    ### Task

    Complete the function `calculate_total_expenses` that takes seed and labour costs and returns their sum.

    ### Expected output

    ```
    3720
    ```
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def calculate_total_expenses(seed_cost, labour_cost):
        """
        Calculate the total expenses from seeds and labour.

        Parameters
        ----------
        seed_cost : int or float
            Cost of seeds in dollars.
        labour_cost : int or float
            Cost of labour in dollars.

        Returns
        -------
        int or float
            Total expenses in dollars.
        """
        return seed_cost + labour_cost
    ### END FUNCTION

    # Test
    print(calculate_total_expenses(650, 3070))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 3: Total revenue

    Market prices this season:

    - Wheat: $2.00 per kg
    - Potato: $1.40 per kg

    ### Task

    Complete the function `calculate_revenue` that takes harvest quantities and prices, then returns total revenue.

    ### Expected output

    ```
    9140.0
    ```
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def calculate_revenue(wheat_kg, potato_kg, wheat_price, potato_price):
        """
        Calculate total revenue from wheat and potato sales.

        Parameters
        ----------
        wheat_kg : int or float
            Kilograms of wheat harvested.
        potato_kg : int or float
            Kilograms of potato harvested.
        wheat_price : int or float
            Price per kilogram of wheat in dollars.
        potato_price : int or float
            Price per kilogram of potato in dollars.

        Returns
        -------
        float
            Total revenue in dollars.
        """
        return wheat_kg * wheat_price + potato_kg * potato_price
    ### END FUNCTION

    # Test
    print(calculate_revenue(2050, 3600, 2, 1.4))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 4: Profit

    ### Task

    Complete the function `calculate_profit` that takes revenue and expenses and returns net profit.

    ### Expected output

    ```
    5420.0
    ```
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def calculate_profit(revenue, expenses):
        """
        Calculate net profit from revenue and expenses.

        Parameters
        ----------
        revenue : int or float
            Total revenue in dollars.
        expenses : int or float
            Total expenses in dollars.

        Returns
        -------
        float
            Net profit in dollars.
        """
        return revenue - expenses
    ### END FUNCTION

    # Test
    print(calculate_profit(9140.0, 3720))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 5: Clean crop names

    Field data comes in messy: `"  WhEaT  "` with random spacing and case. Clean it up.

    ### Task

    Complete the function `clean_crop_name` that takes a raw crop string and returns it cleaned (stripped and lowercased).

    ### Expected output

    ```
    wheat
    ```
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def clean_crop_name(raw_crop):
        """
        Clean a crop name by stripping whitespace and converting to lowercase.

        Parameters
        ----------
        raw_crop : str
            Raw crop name with possible whitespace and mixed case.

        Returns
        -------
        str
            Cleaned crop name (stripped and lowercased).
        """
        return raw_crop.strip().lower()
    ### END FUNCTION

    # Test
    print(clean_crop_name("  WhEaT  "))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 6: Season summary with formatting

    Sanaa needs a readable summary for Finance. Format harvest, revenue, and profit with proper currency and precision.

    ### Task

    Complete the function `format_season_summary` that creates a formatted multi-line summary string. It must include total harvest, revenue (with 2 decimal places and comma separators), profit (with 2 decimal places and comma separators), and profit margin as a percentage.

    ### Expected output (first line of the string)

    ```
    Season summary — Maji Ndogo test fields
    Total harvest: 5650 kg
    Total revenue: $9,140.00
    Total profit: $5,420.00
    Profit margin: 59.3%
    ```
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def format_season_summary(total_harvest, revenue, profit):
        """
        Format a season summary with harvest, revenue, profit, and margin.

        Parameters
        ----------
        total_harvest : int
            Total harvest in kilograms.
        revenue : float
            Total revenue in dollars.
        profit : float
            Total profit in dollars.

        Returns
        -------
        str
            Multi-line formatted summary string.
        """
        return  f"""Season summary — Maji Ndogo test fields
    Total harvest: {total_harvest} kg
    Total revenue: ${revenue:,.2f}
    Total profit: ${profit:,.2f}
    Profit margin: {(profit / revenue) * 100:.1f}%"""
    ### END FUNCTION

    # Test
    print(format_season_summary(5650, 9140.0, 5420.0))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 7: List operations on harvest data

    As more fields report in, organize their harvests in a list. Extract specific records, find the largest, and rank them.

    ### Task

    Complete the function `analyze_field_harvests` that:
    - Takes a list of harvests.
    - Appends 2400 (maize) to the list.
    - Returns a dictionary with keys: `all_harvests`, `first_two`, `largest`, `total`, `ranked`.

    ### Expected output (repr of return dict)

    ```
    {'all_harvests': [2050, 3600, 1875, 2400], 'first_two': [2050, 3600], 'largest': 3600, 'total': 9925, 'ranked': [1875, 2050, 2400, 3600]}
    ```
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def analyze_field_harvests(harvests):
        """
        Analyze field harvest data using list operations.

        Parameters
        ----------
        harvests : list
            Initial list of harvest values in kilograms.

        Returns
        -------
        dict
            Dictionary with keys: all_harvests, first_two, largest, total, ranked.
        """
        harvests.append(2400)
        all_harvests = harvests.copy()
        first_two = harvests[:2]
        largest = max(harvests)
        total = sum(harvests)
        ranked = sorted(harvests, reverse=True)

        return {
            "all_harvests": all_harvests,
            "first_two": first_two,
            "largest": largest,
            "total": total,
            "ranked": ranked
        }
    ### END FUNCTION
    _result = analyze_field_harvests([2050, 3600, 1875])
    # Test
    print(_result)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 8: Tuple unpacking for field records

    Create an immutable field record and unpack it.

    ### Task

    Complete the function `create_field_record` that takes a field ID, crop, and harvest amount, creates a tuple, and returns it unpacked as three separate values.

    ### Expected output

    ```
    18442 wheat 2050
    ```
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def create_field_record(field_id, crop, harvest_kg):
        """
        Create a field record as a tuple and return unpacked values.

        Parameters
        ----------
        field_id : int
            Unique field identifier.
        crop : str
            Crop type.
        harvest_kg : int
            Harvest in kilograms.

        Returns
        -------
        tuple
            Tuple of (field_id, crop, harvest_kg).
        """
        return (field_id, crop, harvest_kg)
    ### END FUNCTION

    # Test
    record = create_field_record(18442, "wheat", 2050)
    field_id, crop, harvest_kg = record
    print(field_id, crop, harvest_kg)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 9: Count unique crops with sets

    How many distinct crops are in today's log?

    ### Task

    Complete the function `count_unique_crops` that takes a list of crop names and returns the count of unique crops.

    ### Expected output

    ```
    3
    ```
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def count_unique_crops(crops_logged):
        """
        Count the number of unique crops in a list.

        Parameters
        ----------
        crops_logged : list
            List of crop names (may contain duplicates).

        Returns
        -------
        int
            Number of unique crops.
        """
        return len(set(crops_logged))
    ### END FUNCTION

    # Test
    crops = ["wheat", "potato", "cassava", "wheat", "potato"]
    print(count_unique_crops(crops))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 10: Dictionary lookups

    Look up harvest by field ID and count the records.

    ### Task

    Complete the function `lookup_field_harvest` that:
    - Takes a dictionary mapping field IDs to harvests.
    - Takes a field ID to look up.
    - Returns a tuple: (harvest_value, total_fields_on_record).

    ### Expected output

    ```
    (2050, 3)
    ```
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def lookup_field_harvest(harvest_dict, field_id):
        """
        Look up harvest for a field and return harvest with field count.

        Parameters
        ----------
        harvest_dict : dict
            Dictionary mapping field IDs to harvest values.
        field_id : int
            Field ID to look up.

        Returns
        -------
        tuple
            (harvest_value, number_of_fields).
        """
        return (harvest_dict.get(field_id, 0), len(harvest_dict))
    ### END FUNCTION
    harvest_by_field = {18442: 2050, 52711: 3600, 60013: 1875}
    # Test
    _result = lookup_field_harvest(harvest_by_field, 18442)
    print(_result)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Wrapping up

    Sanaa looks over the screen. "That's more than I asked for — and exactly what I'll need next." She forwards the summary to Finance before the meeting starts.

    You started with a notepad and ended with a clean, readable season record: totals and profit, the right data types, tidy crop names, a formatted summary, and the same numbers organised four different ways — a list, a tuple, a set, and a dictionary. Every one of these is a tool you'll lean on for the rest of the project.

    This is where it begins — not with algorithms or neural networks, but with the discipline of expressing a real-world question in code that anyone can read, run, and trust. Save this notebook — you'll want these building blocks close at hand for what's coming.

    Make sure every cell produces the expected output before you move on.
    """)
    return


@app.cell
def cell_readiness():
    import inspect as _inspect
    import ast as _ast
    _spec = {'analyze_field_harvests': {'expected_params': ['harvests']}, 'calculate_profit': {'expected_params': ['revenue', 'expenses']}, 'calculate_revenue': {'expected_params': ['wheat_kg', 'potato_kg', 'wheat_price', 'potato_price']}, 'calculate_total_expenses': {'expected_params': ['seed_cost', 'labour_cost']}, 'calculate_total_harvest': {'expected_params': ['wheat_kg', 'potato_kg']}, 'clean_crop_name': {'expected_params': ['raw_crop']}, 'count_unique_crops': {'expected_params': ['crops_logged']}, 'create_field_record': {'expected_params': ['field_id', 'crop', 'harvest_kg']}, 'format_season_summary': {'expected_params': ['total_harvest', 'revenue', 'profit']}, 'lookup_field_harvest': {'expected_params': ['harvest_dict', 'field_id']}}
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
