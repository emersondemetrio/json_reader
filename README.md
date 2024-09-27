# Python JSON editor

Use this tool to read/update a json file.

```bash

python app.py file.json

[Available properties]

Code: 1 | outer_1 = value 1
Code: 2 | outer_2 = 2
Code: 3 | outer_3.inner_1.deep_inner_1 = 1
Code: 4 | outer_3.inner_1.deep_inner_2 = we would save


EXIT = 0, q, Q

Enter a code to edit: 1
Editing value for 'outer_1'

Value (press enter to finish): [1,2,3]
JSON updated successfully.
[Available properties]

Code: 1 | outer_1 = [1,2,3]
Code: 2 | outer_2 = 2
Code: 3 | outer_3.inner_1.deep_inner_1 = 1
Code: 4 | outer_3.inner_1.deep_inner_2 = we would save
```
