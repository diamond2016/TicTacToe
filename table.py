# import things
from flask_table2 import Table, Col
from markupsafe import Markup

# Declare your table
class GameGrid(Table):
   col1 = Col('Col1')
   col2 = Col('Col2')
   col3 = Col('Col3')

# Get some objects
class Item(object):
    def __init__(self, val1, val2, val3):
        self.col1 = val1
        self.col2 = val2
        self.col3 = val3

items = [Item('X','O','X'), 
         Item('','O',''), 
         Item('X','','O')]

# Or, more likely, load items from your database with something like
# items = ItemModel.query.all()  # Commented out since ItemModel is not defined

# Populate the table
table = GameGrid(items)

# Print the html
print(table.__html__())
# or just {{ table }} from within a Jinja template