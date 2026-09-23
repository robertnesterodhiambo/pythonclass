import marimo

__generated_with = "0.23.6+alx.1"
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
    # Tractor Traversal
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Last week the farm could *reason*; this week it *moves on its own*. You'll write the path-planning **functions** that sweep a tractor across any field without wasting a metre — and turn the loose logic of earlier weeks into clean, reusable functions with default arguments, variable inputs, and multiple return values. That is the difference between code that runs once and code a team can build on. The project closes with the step that makes three weeks of work shareable and safe: putting the whole thing under **version control**.
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
    - You may use everything introduced across this module: variables and data types, conditionals, loops, comprehensions, the built-in data structures, and — the focus of this week — functions, including default arguments, `*args`, and `**kwargs`.
    - The use of StackOverflow, Google, and other online resources is permitted. The use of Generative AI tools — including ChatGPT, Claude, Copilot, and others — is also allowed and encouraged as a learning partner. However, the code you submit must reflect your own understanding. Copying a fellow student's code is a breach of the honor code. [Read the honor code here](https://drive.google.com/file/d/1atFOPUQRLz5slb4Q1ASXh8QQfKyXVqrw/preview). Submitting code you do not understand is also a breach.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It happens on a Tuesday afternoon, three weeks into the pilot.

    One of the test tractors completes its first row, turns to begin the second — and drives straight back the way it came. Then it does it again. And again. By the time the operator kills the engine, the tractor has ploughed a perfectly tidy strip down the middle of the field and left the rest untouched.

    The hardware is fine. The soil sensors are fine. The issue is the path-planning algorithm. Nobody wrote one.

    That is the problem you are being asked to solve today. How does a tractor move so that it covers every cell of a field exactly once, wastes as little fuel as possible on turns, and does it the same way every single time regardless of the field's dimensions?

    The answer, it turns out, is not complicated once you know the right pattern. Farmers have been doing it for centuries with ox-drawn ploughs. They call it the **boustrophedon sweep**: left to right on the first pass, right to left on the second, alternating until the whole field is done. No backtracking. No missed rows. Maximum efficiency.

    This week you'll build it the right way — not as one long script, but as small, named **functions** that each do one job and can be reused, tested, and trusted. Your job is to code it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 1: Standard sweep

    The simplest traversal strategy: the tractor starts at `(row=0, col=0)` and visits every cell left to right, then moves to the next row and starts from the left again — like reading a page of text.

    The field is a list of lists. Each cell is identified by its `(row, col)` position: `row` is the index into the outer list, `col` is the index into the inner list.

    ### Task

    Complete `tractor_movement_standard(field)`. It must **return** a list of `(row, col)` tuples covering every cell in the field in left-to-right, top-to-bottom order. It must work for any field size, including irregular and empty fields.

    > ⚠️ Do not change the function name `tractor_movement_standard`.

    ### Expected outputs

    **Input 1:** the 10×5 `field_standard` → `[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), ... , (9, 4)]`

    **Input 2:** the irregular `field_wide` (row 0 has 15 columns, row 1 has 7) → `[(0, 0), ... , (0, 14), (1, 0), ... , (1, 6)]`
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def tractor_movement_standard(field):
        # Insert your code here
        return
    ### END FUNCTION
    return (tractor_movement_standard,)


@app.cell
def _(tractor_movement_standard):
    field_standard = [
        ['soil3','soil3','soil1','soil2','soil2'],
        ['soil2','soil3','soil2','soil1','soil3'],
        ['soil2','soil3','soil1','soil3','soil3'],
        ['soil3','soil2','soil3','soil3','soil2'],
        ['soil3','soil2','soil1','soil3','soil2'],
        ['soil2','soil3','soil3','soil1','soil3'],
        ['soil3','soil1','soil3','soil2','soil2'],
        ['soil2','soil1','soil2','soil2','soil1'],
        ['soil1','soil1','soil3','soil2','soil3'],
        ['soil3','soil3','soil3','soil1','soil1'],
    ]
    tractor_movement_standard(field_standard)
    return (field_standard,)


@app.cell
def _(tractor_movement_standard):
    field_wide = [
        ['soil3']*15,
        ['soil3']*7,
    ]
    tractor_movement_standard(field_wide)
    return (field_wide,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 2: Reverse a row

    Before implementing the boustrophedon sweep, we need a small reusable **helper function**: one that reverses a list. When the tractor finishes a row moving left to right, it traverses the next row right to left — which means reversing the column indices before it drives. Writing this as its own function is the whole point of modular code: one job, one name, reused wherever it's needed.

    ### Task

    Complete `reverse_list(input_list)`. It must **return a new list** with the elements in reverse order.

    > ⚠️ Do not change the function name `reverse_list`.

    ### Expected outputs

    **Input 1:** `reverse_list([0, 1, 2, 3, 4])` → `[4, 3, 2, 1, 0]`

    **Input 2:** `reverse_list([1, 3, 2, 0, 4])` → `[4, 0, 2, 3, 1]`
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def reverse_list(input_list):
        # Insert your code here
        return
    ### END FUNCTION
    return (reverse_list,)


@app.cell
def _(reverse_list):
    reverse_list([0, 1, 2, 3, 4])
    return


@app.cell
def _(reverse_list):
    reverse_list([1, 3, 2, 0, 4])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 3: Boustrophedon sweep

    Now put Challenges 1 and 2 together — one function **calling another**. The tractor alternates direction every row, and a **default argument** lets the caller choose which way it sets off without forcing every caller to specify it.

    ### Task

    Complete `tractor_movement_realistic(field, start_direction='right')`. The parameter `start_direction` defaults to `'right'`:

    - `start_direction='right'` (the default): row 0 goes **left → right**, row 1 goes **right → left**, alternating. Even-indexed rows go left→right; odd-indexed rows go right→left.
    - `start_direction='left'`: the pattern is flipped — even-indexed rows go right→left, odd-indexed rows go left→right.

    You **must call `reverse_list()`** inside your implementation to reverse a row's column order.

    > ⚠️ Do not change the function name `tractor_movement_realistic`.

    ### Expected outputs

    **Input 1:** `tractor_movement_realistic(field_standard)` (default direction) → `[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (1, 3), (1, 2), (1, 1), (1, 0), (2, 0), ... , (9, 0)]`

    **Input 2:** `tractor_movement_realistic([['x','x','x'], ['x','x','x']], 'left')` → `[(0, 2), (0, 1), (0, 0), (1, 0), (1, 1), (1, 2)]`
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def tractor_movement_realistic(field, start_direction='right'):
        # Insert your code here
        return
    ### END FUNCTION
    return (tractor_movement_realistic,)


@app.cell
def _(field_standard, tractor_movement_realistic):
    tractor_movement_realistic(field_standard)
    return


@app.cell
def _(tractor_movement_realistic):
    tractor_movement_realistic([['x','x','x'], ['x','x','x']], 'left')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 4: Summarise a field

    Dispatch wants a quick read on any field before sending a machine out. A single function can hand back several facts at once by **returning multiple values**, which the caller then **unpacks** into separate variables.

    ### Task

    Complete `field_summary(field)`. Return **three values, in this order**:

    1. `num_rows` — the number of rows.
    2. `total_cells` — the total number of cells across all rows (works even when rows differ in length).
    3. `is_rectangular` — `True` if every row has the same length (an empty field counts as rectangular), otherwise `False`.

    The caller will unpack the result like this: `rows, cells, rectangular = field_summary(field)`.

    > ⚠️ Do not change the function name `field_summary`.

    ### Expected outputs

    **Input 1:** `field_summary(field_standard)` → `(10, 50, True)`

    **Input 2:** `field_summary(field_wide)` → `(2, 22, False)`  *(rows of length 15 and 7)*
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def field_summary(field):
        # Insert your code here
        return
    ### END FUNCTION
    return (field_summary,)


@app.cell
def _(field_standard, field_summary):
    field_summary(field_standard)
    return


@app.cell
def _(field_summary, field_wide):
    field_summary(field_wide)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 5: Add up the fuel

    A single run burns fuel in pieces — driving each row, turning at each end, idling at the gate. Sometimes there are three figures to add, sometimes ten. A function that accepts **a variable number of positional arguments** with `*args` handles any number of segments without the caller packing them into a list first.

    ### Task

    Complete `total_fuel_used(*segment_costs)`. It must **return the sum** of however many segment costs are passed in. With no arguments at all, it returns `0`.

    > ⚠️ Do not change the function name `total_fuel_used`, and keep the `*segment_costs` parameter.

    ### Expected outputs

    **Input 1:** `total_fuel_used(2.5, 1.0, 0.5)` → `4.0`

    **Input 2:** `total_fuel_used()` → `0`
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def total_fuel_used(*segment_costs):
        # Insert your code here
        return
    ### END FUNCTION
    return (total_fuel_used,)


@app.cell
def _(total_fuel_used):
    total_fuel_used(2.5, 1.0, 0.5)
    return


@app.cell
def _(total_fuel_used):
    total_fuel_used()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 6: Log a completed trip

    When a tractor finishes, the system records the run. Every log needs a `tractor_id`, but the rest of the details vary from trip to trip — rows covered, fuel used, time taken, whatever was measured. **`**kwargs`** lets one function accept any set of named details and fold them into a single record.

    ### Task

    Complete `log_trip(tractor_id, **details)`. It must **return a dictionary** that starts with the key `'tractor_id'` (set to the value passed in) and then includes every keyword detail that was supplied.

    > ⚠️ Do not change the function name `log_trip`, and keep the `**details` parameter.

    ### Expected outputs

    **Input 1:** `log_trip('TX-1300', rows_covered=10, fuel_used=4.0)` → `{'tractor_id': 'TX-1300', 'rows_covered': 10, 'fuel_used': 4.0}`

    **Input 2:** `log_trip('RX-850')` → `{'tractor_id': 'RX-850'}`
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def log_trip(tractor_id, **details):
        # Insert your code here
        return
    ### END FUNCTION
    return (log_trip,)


@app.cell
def _(log_trip):
    log_trip('TX-1300', rows_covered=10, fuel_used=4.0)
    return


@app.cell
def _(log_trip):
    log_trip('RX-850')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Wrapping up

    The tractor traversal algorithm is complete — and, more importantly, it's built the right way. Any field, any size, covered in the most fuel-efficient pattern possible, by a handful of small functions that each do one job: one sweeps, one reverses, one composes the two, one summarises, one totals fuel from any number of segments, and one logs a trip from any set of details.

    Before submitting, check that:

    - All functions run without errors.
    - `tractor_movement_realistic` calls `reverse_list` internally and respects the `start_direction` default.
    - `field_summary` returns three values that unpack cleanly.
    - `total_fuel_used` and `log_trip` accept any number of inputs via `*args` and `**kwargs`.

    The Digital Twin is alive.
    """)
    return




# ════════════════════════════════════════════════════════════════════════
# Pre-submission readiness check
#
# This cell has NO declared dependencies — it runs even when other cells
# have not. It uses dynamic name lookup (eval + try/except) so the learner
# always gets actionable feedback, including a "run all cells first" hint
# when nothing has been defined yet.
#
# The spec below is auto-generated at conversion time from the test_suite
# (which functions pytest references) and the model solution (the canonical
# parameter names + body characteristics).
# ════════════════════════════════════════════════════════════════════════

@app.cell
def cell_readiness():
    import inspect as _inspect
    import ast as _ast
    _spec = {'field_summary': {'expected_params': ['field']}, 'log_trip': {'expected_params': ['tractor_id']}, 'reverse_list': {'expected_params': ['input_list']}, 'total_fuel_used': {'expected_params': []}, 'tractor_movement_realistic': {'expected_params': ['field', 'start_direction']}, 'tractor_movement_standard': {'expected_params': ['field']}}
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

