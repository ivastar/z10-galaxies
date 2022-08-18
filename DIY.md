## Make your own THINGS list

You don't like my galaxies? You want to make a list of your own favourite things? Make your own list. Here's how.

1. Import this repository. Go [here](https://github.com/new/import) and paste https://github.com/ivastar/z10-galaxies in the URL box. Don't fork it because then your list will be forever connected to this one which is completely unnecessary.

2. What properties would you want your things to have?  Edit the `thing` properties in the `list.yaml`. You should have some required properties marked as `group: Default`. You can specify their `kind` if you want to verify that the data type is correct (currently only checking `string`, `int` and `float`).

3. Delete all my things and make some of your own. Run the test locally (run `pytest` in the repo directory) to validate your things.

4. There are 3 files you need to edit to make the website work.
- First edit `docs/config.yml` to change which entries from the list you would like displayed in the table. My table only displays a handful of columns. If your list has few properties, you can display all the columns. Change the `columns` list. The `columns_title` list specifies your preferred column headings. They can be the same or different from the `columns` list.
- Then edit the `src/website/generate.py` file. In the `generate_table_line` you need to specify what your list entries would look like in HTML format. I've gone a bit overboard by including links and asymetric errorbars. If you want just to display all the columns on your list, something as simple as this would do it:

```
def generate_table_line(thing: dict = {}, columns: list = []):

    table_line = []
    table_line.append(f'<tr><th scope="row">thing[columns[0]]["value"]</th>')
    for col in columns[1:]:
        table_line.append(f'<td>{thing[col]["value"]}</td>')

    table_line.append('</tr>')
    return ''.join(table_line)

```

- Finally, edit the  `src/website/theme/index.html` file. This is the base file for your website, you can edit the footer and header.

5. Test your site. If you added any dependancies to your `generate.py` file, do add them in the appropriate section of the `setup.cfg` file. You can install the repository as a python package from the directory of the `setup.cfg` file:

`pip install -e .`

Now in the `docs/` directory you can generate the site via the `make html` command. View your site at `_build/html/index.html`

6. Edit the bells and whistles. The JS functions of the site are primarily from the [DataTables](https://datatables.net/) library. If you want to turn off the search boxes, change the export functions, etc. look at the documentation there. The user-defined functions are in `src/website/theme/assets/js`, specifically `search-table.js` and `sort-table.js`.

7. Setup GitHub pages.
