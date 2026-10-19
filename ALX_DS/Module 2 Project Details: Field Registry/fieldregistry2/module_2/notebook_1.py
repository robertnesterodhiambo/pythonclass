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
    # Modeling the Field Registry
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A dictionary will let you set a field's pollution level to 7,000 and never complain. That is fine for a throwaway script and dangerous for a system five engineers will build on. As international consultants assisting Maji Ndogo's agricultural registry modernization initiative, you will retire the loose dictionaries and model the survey data using robust object-oriented programming (OOP). You will design a base `Field` class that validates its own data, crop-specific subclasses that price their own harvest, an abstract base that prevents structural inconsistencies, and a unified `FieldRegistry` class that aggregates vital metrics across thousands of records cleanly. Encapsulation, inheritance, polymorphism, and abstraction will be applied directly to real survey data using professional standards. A genuine asset to demonstrate enterprise data practices.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ⚠️ **This challenge is graded and contributes to your overall marks for this module.**

    ### Instructions

    - Do not add or remove cells in this notebook. Do not edit or remove the `### START FUNCTION` or `### END FUNCTION` comments. Do not add any code outside of the functions and classes you are required to edit. Doing any of this will result in a mark of 0%.
    - Answer the questions according to the specifications provided.
    - Use the provided test cells to verify your output before submitting.
    - Do not hard-code answers.
    - Write to a professional standard: PEP 8 `snake_case` names, and a PEP 257 docstring on every class and method.
    - The use of online resources is permitted. The use of Generative AI tools is also allowed and encouraged as a learning partner. However, the code you submit must reflect your own understanding. Copying a fellow student's code is a breach of the honor code. [Read the honor code here](https://drive.google.com/file/d/1atFOPUQRLz5slb4Q1ASXh8QQfKyXVqrw/preview). Submitting code you do not understand is also a breach.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The Auditing Engine is running and the search functions are fast. But Sanaa calls you into her office with a whiteboard already covered in red marker.

    "Here's the problem," she says, drawing a box labeled `dict`. "Every field record is a dictionary. Nothing stops anyone from setting `Pollution_level` to 7,000. Nothing ensures `Plot_size` is always there. Nothing groups the behavior that belongs with the data." She draws a line through the box. "A dictionary is fine for one-off scripts. We are building a system that five other engineers will build on top of. Loose data breaks systems."

    She turns to you. "We need to redesign."

    This is where **object-oriented programming** comes in. Instead of passing dictionaries around and hoping everyone handles them consistently, we define a class — a blueprint that declares what every field *has* (attributes) and what every field *can do* (methods). The blueprint enforces structure. Other code can trust it.

    By the end of this session you will have built the **Maji Ndogo Field Registry**: a set of Python classes that model the survey data with proper validation, inheritance, and polymorphism — the kind of code that professional engineering teams actually build on.
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

    connection = sqlite3.connect('Maji_Ndogo_farm_survey_small.db')
    cursor = connection.cursor()
    rows = cursor.execute(
        """SELECT Field_ID, Pollution_level, Plot_size, Crop_type, Annual_yield, Standard_yield
           FROM farm_management_features"""
    ).fetchall()
    connection.close()

    field_data = []
    for field_id, pollution, plot_size, yield_value, crop_name, standard in rows:
        # Note: the source columns 'Crop_type' and 'Annual_yield' were swapped
        # during export, so we swap them back as we build each record.
        field_data.append({
            'Field_ID': int(field_id),
            'Pollution_level': round(pollution, 2),
            'Plot_size': round(plot_size, 1),
            'Crop_type': crop_name.strip(),
            'Annual_yield': round(yield_value, 2),
            'Standard_yield': round(standard, 2),
        })

    print(f"Loaded {len(field_data)} field survey records.")
    print("First record:", field_data[0])
    return (field_data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 1: The `Field` class

    A class is a blueprint. Define it once, and every field in the survey can become an object.

    Sensors also malfunction. A reading of `7.5` on a 0–1 scale is physically impossible. **Encapsulation** lets a class control its own data: a `@property` with a setter intercepts every write and enforces the valid range. A field's identity and its self-protection belong to the same blueprint, so you build both here.

    ### Task

    Complete the class `Field`:
    - `__init__` must accept `field_id`, `plot_size`, `standard_yield`, and `pollution_level` (**defaulting to `0.0`** — a field with no reading is treated as clean), storing each as an instance attribute with the same PEP 8 `snake_case` name.
    - `describe()` must **return** (not print) the string: `'Field {field_id}: {plot_size} Ha (standard yield {standard_yield})'`
    - `calculate_yield()` must **return** `round(plot_size * standard_yield, 2)`.
    - Back `pollution_level` with a `@property` and a private attribute `_pollution_level`. The setter must raise a `ValueError` with the message `'Pollution level must be between 0 and 1.'` if the value falls outside `[0, 1]`.
    - Add a class docstring and a docstring for each method.

    > ⚠️ Do not change the class or method names.

    ### Expected outputs

    **Input 1:** `f = Field(39924, 3.4, 0.65); f.describe()` → `'Field 39924: 3.4 Ha (standard yield 0.65)'`

    **Input 2:** `Field(39924, 3.4, 0.65).calculate_yield()` → `2.21`

    **Input 3:** `Field(40734, 1.3, 0.58, 0.09).pollution_level` → `0.09`

    **Input 4:**
    ```python
    try:
        Field(40734, 1.3, 0.58, 7.5)
    except ValueError as e:
        print(e)
    ```
    `Pollution level must be between 0 and 1.`
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    class Field:
        """Represents a surveyed field with validated pollution monitoring."""

        def __init__(self, field_id, plot_size, standard_yield, pollution_level=0.0):
            # Insert your code here
            return

        @property
        def pollution_level(self):
            # Insert your code here
            return

        @pollution_level.setter
        def pollution_level(self, value):
            # Insert your code here
            return

        def describe(self):
            # Insert your code here
            return

        def calculate_yield(self):
            # Insert your code here
            return
    ### END FUNCTION
    return (Field,)


@app.cell
def _(Field):
    f = Field(39924, 3.4, 0.65)
    f.describe()
    return


@app.cell
def _(Field):
    Field(39924, 3.4, 0.65).calculate_yield()
    return


@app.cell
def _(Field):
    Field(40734, 1.3, 0.58, 0.09).pollution_level
    return


@app.cell
def _(Field):
    try:
        Field(40734, 1.3, 0.58, 7.5)
    except ValueError as e:
        print(e)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 2: Inheritance — crop-specific subclasses

    Tea, coffee, and wheat each sell at a different price per ton. **Inheritance** lets us create specialized subclasses that extend `Field` with crop-specific behavior without rewriting the shared logic. Because each subclass implements the same method names, code can call `describe()` or `projected_revenue()` on any of them without knowing which crop it is — that is **polymorphism**.

    ### Task

    Create three subclasses of `Field`: `TeaField` ($1,180/ton), `CoffeeField` ($2,400/ton), `WheatField` ($320/ton). Each must:
    - Store the price as a class attribute `PRICE_PER_TON`.
    - Override `describe()` to prefix with the crop name (e.g. `'Tea field 39924: ...'`).
    - Add a method `projected_revenue()` returning `round(calculate_yield() * PRICE_PER_TON, 2)`.
    - Include a class docstring.

    > ⚠️ Do not change the class or method names.

    ### Expected outputs

    **Input 1:** `TeaField(39924, 3.4, 0.65, 0.36).describe()` → `'Tea field 39924: 3.4 Ha (standard yield 0.65)'`

    **Input 2:** `TeaField(39924, 3.4, 0.65, 0.36).projected_revenue()` → `2607.8`
    """)
    return


@app.cell
def _(Field):
    ### START FUNCTION
    class TeaField(Field):
        """Tea crop field."""
        PRICE_PER_TON = 1180

        def describe(self):
            # Insert your code here
            return

        def projected_revenue(self):
            # Insert your code here
            return

    class CoffeeField(Field):
        """Coffee crop field."""
        PRICE_PER_TON = 2400

        def describe(self):
            # Insert your code here
            return

        def projected_revenue(self):
            # Insert your code here
            return

    class WheatField(Field):
        """Wheat crop field."""
        PRICE_PER_TON = 320

        def describe(self):
            # Insert your code here
            return

        def projected_revenue(self):
            # Insert your code here
            return
    ### END FUNCTION
    return (TeaField,)


@app.cell
def _(TeaField):
    TeaField(39924, 3.4, 0.65, 0.36).describe()
    return


@app.cell
def _(TeaField):
    TeaField(39924, 3.4, 0.65, 0.36).projected_revenue()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 3: Abstraction — an abstract base class

    Nothing prevents a developer from creating a plain `AbstractCropField` object when they should have used a concrete subclass. **Abstraction** via an abstract base class (ABC) makes that impossible — the class cannot be instantiated until its abstract methods are implemented.

    ### Task

    Create `AbstractCropField(ABC)` with:
    - `__init__` accepting `field_id`, `plot_size`, and `standard_yield`.
    - An abstract method `crop_name()` — every concrete subclass must implement it.
    - `calculate_yield()` returning `round(plot_size * standard_yield, 2)`.
    - A class docstring.

    Then create `MaizeField(AbstractCropField)` implementing `crop_name()` to return `'maize'`.

    > ⚠️ Do not change the class or method names.

    ### Expected outputs

    **Input 1:** instantiating the abstract base directly raises a `TypeError` (the exact message wording depends on your Python version):
    ```python
    try:
        AbstractCropField(41964, 4.1, 0.55)
    except TypeError as e:
        print(e)
    ```
    `Can't instantiate abstract class AbstractCropField without an implementation for abstract method 'crop_name'`

    **Input 2:** `MaizeField(41964, 4.1, 0.55).crop_name()` → `'maize'`

    **Input 3:** `MaizeField(41964, 4.1, 0.55).calculate_yield()` → `2.25`
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    from abc import ABC, abstractmethod

    class AbstractCropField(ABC):
        """Abstract base - every concrete crop field must implement crop_name()."""

        def __init__(self, field_id, plot_size, standard_yield):
            # Insert your code here
            return

        @abstractmethod
        def crop_name(self):
            # Insert your code here
            pass

        def calculate_yield(self):
            # Insert your code here
            return

    class MaizeField(AbstractCropField):
        """Concrete maize field."""

        def crop_name(self):
            # Insert your code here
            return
    ### END FUNCTION
    return AbstractCropField, MaizeField


@app.cell
def _(AbstractCropField):
    try:
        AbstractCropField(41964, 4.1, 0.55)
    except TypeError as e:
        print(e)
    return


@app.cell
def _(MaizeField):
    MaizeField(41964, 4.1, 0.55).crop_name()
    return


@app.cell
def _(MaizeField):
    MaizeField(41964, 4.1, 0.55).calculate_yield()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 4: The `build_field` factory

    The survey hands you raw dictionaries. Something has to decide which class each record becomes, and that decision belongs in one place rather than scattered across every caller. A **factory function** takes a record and hands back the right object.

    ### Task

    Complete `build_field(record)`:
    - Accept a raw survey record dictionary.
    - Return the correct `TeaField`, `CoffeeField`, or `WheatField` object based on `Crop_type` (case-insensitive).
    - Return `None` for any crop not in the pricing catalog.
    - Include a docstring.

    > ⚠️ Do not change the function name.

    ### Expected outputs

    **Input 1:**
    ```python
    tea_record = {'Field_ID': 39924, 'Plot_size': 3.4, 'Standard_yield': 0.65,
                  'Crop_type': 'tea', 'Pollution_level': 0.36}
    type(build_field(tea_record)).__name__
    ```
    → `'TeaField'`

    **Input 2:**
    ```python
    cassava_record = {'Field_ID': 41964, 'Plot_size': 4.1, 'Standard_yield': 0.55,
                      'Crop_type': 'cassava', 'Pollution_level': 0.2}
    build_field(cassava_record)
    ```
    → `None`
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    def build_field(record):
        # Insert your code here
        return
    ### END FUNCTION
    return (build_field,)


@app.cell
def _(build_field):
    # input 1
    tea_record = {'Field_ID': 39924, 'Plot_size': 3.4, 'Standard_yield': 0.65,
                  'Crop_type': 'tea', 'Pollution_level': 0.36}
    type(build_field(tea_record)).__name__
    return


@app.cell
def _(build_field):
    # input 2
    cassava_record = {'Field_ID': 41964, 'Plot_size': 4.1, 'Standard_yield': 0.55,
                      'Crop_type': 'cassava', 'Pollution_level': 0.2}
    build_field(cassava_record)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Challenge 5: The `FieldRegistry`

    Now bring it together. The registry aggregates every priced field, calling the same method names on each one regardless of crop. That shared interface is polymorphism doing the real work.

    ### Task

    Complete the `FieldRegistry` class:
    - Accept a list of raw records in `__init__`, use `build_field()` to build `self.fields` (excluding `None` values).
    - `size()` → number of priced fields.
    - `total_projected_yield()` → sum of all `calculate_yield()` values, rounded to 2 dp.
    - `total_projected_revenue()` → sum of all `projected_revenue()` values, rounded to 2 dp.
    - Include a class docstring and method docstrings.

    > ⚠️ Do not change the class or method names.

    ### Expected outputs (on the full 5,654-record survey)

    **Input 1:** `registry = FieldRegistry(field_data); registry.size()` → `2840`

    **Input 2:** `registry.total_projected_yield()` → `6103.59`

    **Input 3:** `registry.total_projected_revenue()` → `6412228.0`
    """)
    return


@app.cell
def _():
    ### START FUNCTION
    class FieldRegistry:
        """Registry of priced crop-field objects built from the survey dataset."""

        def __init__(self, records):
            # Insert your code here
            return

        def size(self):
            # Insert your code here
            return

        def total_projected_yield(self):
            # Insert your code here
            return

        def total_projected_revenue(self):
            # Insert your code here
            return
    ### END FUNCTION
    return (FieldRegistry,)


@app.cell
def _(FieldRegistry, field_data):
    registry = FieldRegistry(field_data)
    registry.size()
    return (registry,)


@app.cell
def _(registry):
    registry.total_projected_yield()
    return


@app.cell
def _(registry):
    registry.total_projected_revenue()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Wrapping up

    The Field Registry is live. Every field is now an object with validated state, crop-specific behavior, and registry analytics that scale correctly across all 5,654 records. You used all four pillars of OOP: **encapsulation** (the validated pollution property), **inheritance** (the crop subclasses), **polymorphism** (the registry calling shared method names on a mixed list), and **abstraction** (the abstract base class).

    Before submitting:

    - Every class and method carries a docstring (PEP 257), and every name is `snake_case` / `PascalCase` per PEP 8.
    - All cells run without errors from top to bottom.

    — Sanaa 🌾
    """)
    return


@app.cell
def cell_readiness():
    import inspect as _inspect
    import ast as _ast
    _spec = {'AbstractCropField': {'expected_params': []}, 'CoffeeField': {'expected_params': []}, 'Field': {'expected_params': []}, 'FieldRegistry': {'expected_params': []}, 'MaizeField': {'expected_params': []}, 'TeaField': {'expected_params': []}, 'WheatField': {'expected_params': []}, 'build_field': {'expected_params': ['record']}}
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
