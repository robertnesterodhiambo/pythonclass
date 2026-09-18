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
    # Building the Digital Twin
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A farm you cannot measure is a farm you cannot automate. This week you build the **logic layer** of Maji Ndogo's Digital Twin — the code that counts what has been planted, decides when a tractor needs fuel, drives a machine down a row until it meets an obstacle, and keeps every farm's harvest on record. Conditionals, loops, comprehensions, sets, and nested dictionaries: the moving parts that turn a static model of the land into one that can reason about itself.
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
    - You may only use tools introduced up to this week: variables and data types, conditionals, loops, comprehensions, and the built-in data structures (lists, tuples, sets, dictionaries). The function definitions are provided for you — you only fill in the bodies.
    - The use of StackOverflow, Google, and other online resources is permitted. The use of Generative AI tools — including ChatGPT, Claude, Copilot, and others — is also allowed and encouraged as a learning partner. However, the code you submit must reflect your own understanding. Copying a fellow student's code is a breach of the honor code. [Read the honor code here](https://drive.google.com/file/d/1atFOPUQRLz5slb4Q1ASXh8QQfKyXVqrw/preview). Submitting code you do not understand is also a breach.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Three days after the ministry meeting, Sanaa takes you to the land itself.

    You walk the northern plot with her and two engineers from the automation team. The field stretches two hundred meters in every direction — wheat stubble, red soil, a rusted irrigation pipe running along the western edge. One of the engineers points at a tractor parked near the gate. "That machine needs to know where it is," she says. "What it has and hasn't covered. Right now it doesn't know anything — it just moves when someone pushes a button."

    The plan, Sanaa explains on the drive back, is to build a **Digital Twin** of Maji Ndogo's farms: a live, programmable model that mirrors the physical reality. Last week you turned a notepad into clean records. This week you give those records *behaviour* — logic that makes decisions, loops that do the repetitive work, and structures that hold a whole region's worth of farms. No libraries, no databases. Just Python deciding, counting, and remembering.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 1: Read the fuel gauge

    Before a tractor sets off, the system checks its fuel. The decision is a classic **conditional**: the same input (a fuel level) produces different outcomes depending on which range it falls into.

    ### Task

    Complete `fuel_status(fuel_level, fuel_capacity)`. Compute the fraction of the tank that is full (`fuel_level / fuel_capacity`) and return a status string using these rules, checked in order:

    | Condition | Return |
    |---|---|
    | `fuel_level` is exactly `0` | `'Empty'` |
    | fraction is **less than 0.25** | `'Low'` |
    | fraction is **less than 1.0** | `'OK'` |
    | otherwise (tank full or over-full) | `'Full'` |

    > ⚠️ Do not change the function name `fuel_status`.

    ### Expected outputs

    **Input 1:** `fuel_status(10, 60)` → `'Low'`  *(fraction ≈ 0.17)*

    **Input 2:** `fuel_status(60, 60)` → `'Full'`  *(fraction = 1.0)*
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def fuel_status(fuel_level, fuel_capacity):
        fraction = fuel_level / fuel_capacity

        if fuel_level == 0:
            return 'Empty'
        elif fraction < 0.25:
            return 'Low'
        elif fraction < 1.0:
            return 'OK'
        else:
            return 'Full'
        return
    ### END FUNCTION
    return (fuel_status,)


@app.cell
def _(fuel_status):
    # input 1
    fuel_status(10, 60)
    return


@app.cell
def _(fuel_status):
    # input 2
    fuel_status(60, 60)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 2: Count what is planted

    A field in the Digital Twin is a grid — a **list of lists** — where `0` is bare soil and `1` is a planted cell. To report progress, the system needs to count every planted cell across every row. That means stepping through the grid with **nested loops**: the outer loop over rows, the inner loop over the cells in each row.

    ### Task

    Complete `count_planted_cells(field)`. Return the total number of cells equal to `1`. It must work for any grid size, including an empty field.

    > ⚠️ Do not change the function name `count_planted_cells`.

    ### Expected outputs

    **Input 1:** `count_planted_cells([[1, 0, 1], [0, 1, 0]])` → `3`

    **Input 2:** `count_planted_cells([[0, 0], [0, 0]])` → `0`
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def count_planted_cells(field):
        count = 0

        for row in field:
            for cell in row:
                if cell == 1:
                    count += 1

        return count
    ### END FUNCTION
    return (count_planted_cells,)


@app.cell
def _(count_planted_cells):
    # input 1
    count_planted_cells([[1, 0, 1], [0, 1, 0]])
    return


@app.cell
def _(count_planted_cells):
    # input 2
    count_planted_cells([[0, 0], [0, 0]])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 3: Drive the tractor down a row

    Now the machine moves. A row is a list of cells: `0` is soil to plant, `1` is already planted, and `-1` is an obstacle — that rusted irrigation pipe. The tractor starts at index `0` and drives **left to right**, planting each cell as it goes, until it reaches an obstacle, at which point it must stop. It never plants the obstacle or anything beyond it.

    This is a natural fit for a **`while` loop** with a `break`: keep advancing until the obstacle (or the end of the row) stops you.

    ### Task

    Complete `drive_and_plant(row)`. Move from index `0` rightward; set each cell you reach to `1`; the moment you reach a cell equal to `-1`, stop. Return the updated row. Cells already equal to `1` simply stay `1`.

    > ⚠️ Do not change the function name `drive_and_plant`.

    ### Expected outputs

    **Input 1:** `drive_and_plant([0, 1, 0, -1, 0])` → `[1, 1, 1, -1, 0]`  *(stops at the pipe)*

    **Input 2:** `drive_and_plant([0, 0, 0, 0])` → `[1, 1, 1, 1]`  *(clear run to the end)*
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def drive_and_plant(row):
        index = 0

        while index < len(row):
            if row[index] == -1:
                break

            row[index] = 1
            index += 1

        return row
    ### END FUNCTION
    return (drive_and_plant,)


@app.cell
def _(drive_and_plant):
    # input 1
    drive_and_plant([0, 1, 0, -1, 0])
    return


@app.cell
def _(drive_and_plant):
    # input 2
    drive_and_plant([0, 0, 0, 0])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 4: Total fleet power

    The fleet is a **list of dictionaries** — one dictionary per vehicle. To report the combined power of everything in the yard, iterate the list with a **`for` loop** and add up each vehicle's `horsepower`.

    ### Task

    Complete `total_horsepower(fleet)`. Return the sum of the `'horsepower'` value across every vehicle. An empty fleet returns `0`.

    > ⚠️ Do not change the function name `total_horsepower`.

    ### Expected outputs

    **Input 1:**
    ```python
    fleet = [
        {'model': 'TX-1300', 'colour': 'Green', 'horsepower': 150, 'fuel_capacity': 60},
        {'model': 'RX-850',  'colour': 'Red',   'horsepower': 120, 'fuel_capacity': 45},
        {'model': 'SX-750',  'colour': 'White', 'horsepower': 180, 'fuel_capacity': 80},
    ]
    total_horsepower(fleet)
    ```
    `450`

    **Input 2:** `total_horsepower([])` → `0`
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def total_horsepower(fleet):
        total = 0

        for vehicle in fleet:
            total += vehicle['horsepower']

        return total
    ### END FUNCTION
    return (total_horsepower,)


@app.cell
def _(total_horsepower):
    # input 1
    fleet = [
        {'model': 'TX-1300', 'colour': 'Green', 'horsepower': 150, 'fuel_capacity': 60},
        {'model': 'RX-850',  'colour': 'Red',   'horsepower': 120, 'fuel_capacity': 45},
        {'model': 'SX-750',  'colour': 'White', 'horsepower': 180, 'fuel_capacity': 80},
    ]
    total_horsepower(fleet)
    return


@app.cell
def _(total_horsepower):
    # input 2
    total_horsepower([])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 5: Which machines are running low?

    Before a long shift, dispatch wants the models of every vehicle whose tank is smaller than some threshold. A **list comprehension** expresses this in one readable line: build a list of models, filtered by a condition.

    ### Task

    Complete `low_fuel_models(fleet, threshold)`. Return a list of the `'model'` values for every vehicle whose `'fuel_capacity'` is **strictly less than** `threshold`, keeping the original fleet order. Use a list comprehension.

    > ⚠️ Do not change the function name `low_fuel_models`.

    ### Expected outputs

    Using the same `fleet` as Challenge 4 (capacities 60, 45, 80):

    **Input 1:** `low_fuel_models(fleet, 50)` → `['RX-850']`

    **Input 2:** `low_fuel_models(fleet, 70)` → `['TX-1300', 'RX-850']`
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def low_fuel_models(fleet, threshold):
        return [vehicle['model'] for vehicle in fleet if
                vehicle['fuel_capacity'] < threshold]
        return
    ### END FUNCTION
    return (low_fuel_models,)


@app.cell
def _(low_fuel_models):
    # input 1
    fleet_1 = [{'model': 'TX-1300', 'colour': 'Green', 'horsepower': 150, 'fuel_capacity': 60}, {'model': 'RX-850', 'colour': 'Red', 'horsepower': 120, 'fuel_capacity': 45}, {'model': 'SX-750', 'colour': 'White', 'horsepower': 180, 'fuel_capacity': 80}]
    low_fuel_models(fleet_1, 50)
    return (fleet_1,)


@app.cell
def _(fleet_1, low_fuel_models):
    # input 2
    low_fuel_models(fleet_1, 70)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 6: Revenue for every crop

    Last week you priced two crops by hand. Now the model holds many crops at once: one dictionary of harvest weights and one of prices. A **dictionary comprehension** turns them into a revenue figure for each crop in a single expression.

    ### Task

    Complete `revenue_by_crop(harvest_kg, price_per_kg)`. Both arguments are dictionaries keyed by crop name. Return a new dictionary mapping each crop in `harvest_kg` to its revenue (`kilograms × price`). You may assume every crop in `harvest_kg` also appears in `price_per_kg`. Use a dictionary comprehension.

    > ⚠️ Do not change the function name `revenue_by_crop`.

    ### Expected outputs

    **Input 1:**
    ```python
    revenue_by_crop({'wheat': 2050, 'potato': 3600}, {'wheat': 2, 'potato': 1.4})
    ```
    `{'wheat': 4100, 'potato': 5040.0}`

    **Input 2:**
    ```python
    revenue_by_crop({'maize': 2400}, {'maize': 1.5, 'rice': 2})
    ```
    `{'maize': 3600.0}`
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def revenue_by_crop(harvest_kg, price_per_kg):
        return {crop: harvest_kg[crop] * price_per_kg[crop] for crop in harvest_kg}
    ### END FUNCTION
    return (revenue_by_crop,)


@app.cell
def _(revenue_by_crop):
    # input 1
    revenue_by_crop({'wheat': 2050, 'potato': 3600}, {'wheat': 2, 'potato': 1.4})
    return


@app.cell
def _(revenue_by_crop):
    # input 2
    revenue_by_crop({'maize': 2400}, {'maize': 1.5, 'rice': 2})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 7: Compare two farms' crop plans

    Two neighbouring farms send in the crops they intend to plant. The lists are messy — free text with repeats. **Sets** answer the planning questions cleanly: what both farms grow (**intersection**), what only the first grows (**difference**), and the full catalogue across both (**union**) — with duplicates removed automatically.

    ### Task

    Complete `compare_crop_plans(farm_a_crops, farm_b_crops)`. Both arguments are lists of crop-name strings (possibly with duplicates). Return a dictionary with exactly these three keys, each a **sorted list**:

    - `'shared'`: crops grown by **both** farms.
    - `'only_in_a'`: crops grown by farm A but **not** farm B.
    - `'all_crops'`: every distinct crop across both farms.

    > ⚠️ Do not change the function name `compare_crop_plans`.

    ### Expected outputs

    **Input 1:**
    ```python
    compare_crop_plans(['wheat', 'potato', 'maize', 'wheat'], ['potato', 'rice', 'maize'])
    ```
    `{'shared': ['maize', 'potato'], 'only_in_a': ['wheat'], 'all_crops': ['maize', 'potato', 'rice', 'wheat']}`

    **Input 2:**
    ```python
    compare_crop_plans(['tea'], ['coffee'])
    ```
    `{'shared': [], 'only_in_a': ['tea'], 'all_crops': ['coffee', 'tea']}`
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def compare_crop_plans(farm_a_crops, farm_b_crops):
        a = set(farm_a_crops)
        b = set(farm_b_crops)

        return {
            'shared': sorted(a & b),
            'only_in_a': sorted(a - b),
            'all_crops': sorted(a | b)
        }
    ### END FUNCTION
    return (compare_crop_plans,)


@app.cell
def _(compare_crop_plans):
    # input 1
    compare_crop_plans(['wheat', 'potato', 'maize', 'wheat'], ['potato', 'rice', 'maize'])
    return


@app.cell
def _(compare_crop_plans):
    # input 2
    compare_crop_plans(['tea'], ['coffee'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 8: The regional harvest registry

    The Digital Twin must remember every farm's harvest as the season unfolds. The natural structure is a **nested dictionary**: each farm ID maps to its own dictionary of crop → kilograms. New readings either start a fresh record or **add to** an existing one — which is exactly where a **conditional** decides between the two.

    ### Task

    Complete `record_harvest(registry, farm_id, crop, kg)`:

    1. If `farm_id` is not yet in `registry`, create an empty record for it.
    2. If that farm already has a figure for `crop`, **add** `kg` to the existing total; otherwise set it to `kg`.
    3. Return the updated registry.

    > ⚠️ Do not change the function name `record_harvest`.

    ### Expected outputs

    **Input 1:** (new farm, new crop)
    ```python
    record_harvest({}, 18442, 'wheat', 2050)
    ```
    `{18442: {'wheat': 2050}}`

    **Input 2:** (same farm and crop again — totals accumulate)
    ```python
    record_harvest({18442: {'wheat': 2050}}, 18442, 'wheat', 500)
    ```
    `{18442: {'wheat': 2550}}`
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def record_harvest(registry, farm_id, crop, kg):
        if farm_id not in registry:
            registry[farm_id] = {}

        if crop in registry[farm_id]:
            registry[farm_id][crop] += kg
        else:
            registry[farm_id][crop] = kg

        return registry
    ### END FUNCTION
    return (record_harvest,)


@app.cell
def _(record_harvest):
    # input 1
    record_harvest({}, 18442, 'wheat', 2050)
    return


@app.cell
def _(record_harvest):
    # input 2
    record_harvest({18442: {'wheat': 2050}}, 18442, 'wheat', 500)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Wrapping up

    The Digital Twin can now *reason*. It checks a fuel gauge, counts what is planted, drives a tractor down a row and stops at the pipe, sums the fleet's power, flags the machines running low, prices a whole season's crops, compares two farms' plans, and keeps a growing registry of every harvest across the region.

    Look back at what made each one work: a decision, a loop, a comprehension, a set, a nested dictionary. These are the control structures every program you write from here will lean on. Next, you'll stop writing the same logic twice and start packaging it — wrapping these behaviours into reusable, well-designed tools of your own.

    Save this notebook. Alongside last week's records, it's the second asset in your Maji Ndogo portfolio — and the first that shows you can make data *do* something.

    Make sure every cell runs without errors before submitting.
    """)
    return


@app.cell
def cell_readiness():
    import inspect as _inspect
    import ast as _ast
    _spec = {'compare_crop_plans': {'expected_params': ['farm_a_crops', 'farm_b_crops']}, 'count_planted_cells': {'expected_params': ['field']}, 'drive_and_plant': {'expected_params': ['row']}, 'fuel_status': {'expected_params': ['fuel_level', 'fuel_capacity']}, 'low_fuel_models': {'expected_params': ['fleet', 'threshold']}, 'record_harvest': {'expected_params': ['registry', 'farm_id', 'crop', 'kg']}, 'revenue_by_crop': {'expected_params': ['harvest_kg', 'price_per_kg']}, 'total_horsepower': {'expected_params': ['fleet']}}
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


app._unparsable_cell(
    r"""
    compare_crop_plans(['tea', 'coffee'], ['coffee', 'tea']) return?
    """,
    name="_"
)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
