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
    <img src="https://raw.githubusercontent.com/Explore-AI/Pictures/master/Python-Notebook-Banners/Exercise.png"  style="display: block; margin-left: auto; margin-right: auto;";/>
    </div>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Exercise: Dictionaries
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In this exercise, we'll be exploring problems involving dictionaries – how to create, manipulate, and use their characteristics to create efficient code.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Learning objectives

    Following this exercise, we will:
    - Understand how to create dictionaries.
    - Be able to manipulate the key-value pairs using assignment and slicing.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercises
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 1

    1. Create a dictionary called `tree` with the following key-value pairs: <br>
    - `tree_type – Pepper-bark tree`
    - `age – 15`
    - `family – Canellaceae`
    """)
    return


@app.cell
def _():
    # insert code here
    tree = {"tree_type": "Pepper-back tree", "Age": 15, "family": "Canellaceae"}
    return (tree,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    2. Print the value associated with the key `age`.
    """)
    return


@app.cell
def _(tree):
    # insert code here
    print(tree["Age"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    3. When we created this dictionary in the first step, we accidentally left out one of the information categories, namely 'kingdom'. Fortunately, dictionaries are mutable, and we can add a new key-value pair to the dictionary: `kingdom – Plantae`. Do this in the code cell below.
    """)
    return


@app.cell
def _():
    # insert code here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    4. We have found that people are no longer interested in one of the key-value pairs in our dictionary. Remove the `family` key-value pair from the dictionary.
    """)
    return


@app.cell
def _():
    # insert code here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    5. Update the dictionary by changing the `tree_type` key to `Wild Cinnamon`.
    """)
    return


@app.cell
def _():
    # insert code here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    6. Extract the keys and values from our `tree` dictionary, and store the values in two separate lists, `key_list` and `value_list`.
    """)
    return


@app.cell
def _():
    # insert code here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    7. Extract the key-value pairs from our `tree` dictionary in tuples, and store the values in a single list, `item_list`.
    """)
    return


@app.cell
def _():
    # insert code here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2

    1. We have been provided with a basic nested dictionary containing African tree species. We have just received more detailed information on these trees and need to add it to this nested dictionary. Use the code provided as a starting point, adding in the extra information where required.
    """)
    return


@app.cell
def _():
    # basic dictionary provided 
    african_trees = {
        "Baobab": {
            "common_name": "Baobab",
            "scientific_name": "Adansonia",
        },
        "Acacia": {
            "common_name": "Acacia",
            "scientific_name": "Acacia",
        }
    }
    print(african_trees)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **New information**

    Baobab:
    - country – Zimbabwe
    - average_height – 25

    Acacia:
    - country – South Africa
    - average_height – 15

    **Hint**:
    - Print the dictionary to view the current structure.
    - Use the keys to access the Baobab and Acacia dictionaries and append the additional information.
    - The new keys will be `country` and `average_height`.
    """)
    return


@app.cell
def _():
    # insert code here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Solutions
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 1

    1. Create a dictionary called `tree` with the following key-value pairs: <br>
    - `tree_type – Pepper-bark tree`
    - `age – 15`
    - `family – Canellaceae`
    """)
    return


@app.cell
def _():
    # insert code here

    # option 1
    tree = {"tree_type":"Pepper-bark tree", "age":15, "family":"Canellaceae"}
    print(tree)

    # option 2
    tree = dict(tree_type="Pepper-bark tree", age=15, family="Canellaceae")
    print(tree)
    return (tree,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here we have shown two different ways of initialising our dictionary – the first with the curly brackets, the second using the built-in `dict()` function. Note that when we use the `dict()` function, **the keys are automatically recognised without the need to place them in quotes**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <br>

    2. Print the value associated with the key `age`.
    """)
    return


@app.cell
def _(tree):
    # insert code here

    print(f"Age: {tree['age']}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <br>

    3. When we created this dictionary in the first step, we accidentally left out one of the information categories, namely 'kingdom'. Fortunately, dictionaries are mutable, and we can add a new key-value pair to the dictionary: `kingdom – Plantae`. Do this in the code cell below.
    """)
    return


@app.cell
def _(tree):
    # insert code here

    # option 1 – assigning directly to key
    tree["kingdom"] = "Plantae"
    print(tree)
    return


@app.cell
def _():
    # recreating tree dictionary for illustrative purposes
    tree_1 = dict(tree_type='Pepper-bark tree', age=15, family='Canellaceae')
    new_data = {'kingdom': 'Plantae'}
    # option 2 – creating new dictionary and using update to add it
    tree_1.update(new_data)
    print(tree_1)
    return (tree_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can add new key-value pairs to the dictionary by specifying the key (`kingdom`) and its value, or create a new dictionary and use `update()` to include it in the original.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <br>

    4. We have found that people are no longer interested in one of the key-value pairs in our dictionary. Remove the `family` key-value pair from the dictionary.
    """)
    return


@app.cell
def _(tree_1):
    # insert code here
    del tree_1['family']
    # option 1
    # Using del keyword to remove the key-value pair
    print('Updated tree dict: ', tree_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can use the `del` keyword to remove the `family` key-value pair from the dictionary. If the key cannot be found, it will result in a key error.
    """)
    return


@app.cell
def _():
    # option 2
    # recreating the dict for illustrative purposes
    tree_2 = {'tree_type': 'Pepper-bark tree', 'age': 15, 'family': 'Canellaceae', 'kingdom': 'Plantae'}
    print('Original tree dict: ', tree_2)
    tree_2.pop('family')
    # Using pop() method to modify the dictionary in place
    print('Updated tree dict: ', tree_2)
    return (tree_2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can also use the `pop()` method to remove the value associated with the `family` key.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <br>

    5. Update the dictionary by changing the `tree_type` key to `Wild Cinnamon`.
    """)
    return


@app.cell
def _(tree_2):
    # insert code here
    tree_2['tree_type'] = 'Wild Cinnamon'
    print(tree_2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <br>

    6. Extract the keys and values from our `tree` dictionary, and store the values in two separate lists, `key_list` and `value_list`.
    """)
    return


@app.cell
def _(tree_2):
    # insert code here
    key_list = list(tree_2.keys())
    value_list = list(tree_2.values())
    print('Key list: ', key_list)
    print('Value list: ', value_list)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The attributes of dictionaries can be accessed with the `keys()` and `values()` methods, making it easy to extract them. These methods return `dict_keys` and `dict_values` objects, respectively. While these objects resemble lists, we can't access their elements using indexing. If you'd like to use indexing on them, it's best to convert the object to a list and access the elements from there.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <br>

    7. Extract the key-value pairs from our `tree` dictionary in tuples, and store the values in a single list, `item_list`.
    """)
    return


@app.cell
def _(tree_2):
    # insert code here
    print(type(tree_2.items()))
    item_list = list(tree_2.items())
    print(item_list)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here we extracted a `dict_items` object and converted it to a list. We can see that our `item_list` variable is a list of tuples with two elements each, containing the key-value pairs from our dictionary in each tuple.

    The `dict_items` object shares the attributes of the `dict_keys` and `dict_values` objects, meaning that while `dict_items` objects are iterable, we cannot use an index to access their elements.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <br>

    ### Exercise 2

    1. We have been provided with a basic nested dictionary containing African tree species. We have just received more detailed information on these trees and need to add it to this nested dictionary. Use the code provided as a starting point, adding in the extra information where required.
    """)
    return


@app.cell
def _():
    # basic dictionary provided 
    african_trees_1 = {'Baobab': {'common_name': 'Baobab', 'scientific_name': 'Adansonia'}, 'Acacia': {'common_name': 'Acacia', 'scientific_name': 'Acacia'}}
    print(african_trees_1)
    return (african_trees_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **New information**

    Baobab:
    - country – Zimbabwe
    - average_height – 25

    Acacia:
    - country – South Africa
    - average_height – 15

    **Hint**:
    - Print the dictionary to view the current structure.
    - Use the keys to access the Baobab and Acacia dictionaries and append the additional information.
    - The new keys will be `country` and `average_height`.
    """)
    return


@app.cell
def _(african_trees_1):
    # insert code here
    new_baobab = {'country': 'Zimbabwe', 'average_height': 25}
    african_trees_1['Baobab'].update(new_baobab)
    new_acacia = {'country': 'South Africa', 'average_height': 15}
    african_trees_1['Acacia'].update(new_acacia)
    african_trees_1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the solution we first created two new dictionaries with the additional information, and then accessed the two keys of interest, `Baobab` and `Acacia`. We then used the `update()` method to add the additional dictionaries.

    Nested dictionaries are especially useful for storing multi-level information and retaining the structure of the data. The same rules for accessing keys and values apply, making them easy to work with, despite the complex look!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    Dictionaries provide a **fast and efficient** way to work with **structured data**. In this exercise, we looked at ways of creating dictionaries, how to update them, and how to extract their attributes. Remember to look into the Python documentation to learn more about these data structures!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #

    <div align="center" style=" font-size: 80%; text-align: center; margin: 0 auto">
    <img src="https://raw.githubusercontent.com/Explore-AI/Pictures/refs/heads/master/ALX_banners/ALX_Navy.png"  style="width:140px";/>
    </div>
    """)
    return


if __name__ == "__main__":
    app.run()
