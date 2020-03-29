# config_reader.py
I made [this](https://www.github.com/pawnlord/config_reader) but in python  
  
## usage
It has all the same functionallity as the other one, just with different syntax 
**How to Use**
```
cfg = config("example.cfg") 
# constructor syntax
# config(fieldname, eol='\n', field_begin='[', field_end=']')

# to read FIELD1, do
field1 = cfg.get_field("FIELD1")

# to get a value MIN in that field
# Remember, this will return a double list of strings
# this is so you get all values with the name MIN 
# if there are duplicates
cfg.get_val(field1, "MIN")

# if you want one, use either
cfg.get_first_val(field1, "MIN")
cfg.get_last_val(field1, "MIN")

# if you do not want to get the field first, use dir variants
# dir stands for direct
cfg.dir_get_val("FIELD1", "MIN")
cfg.dir_get_first_val("FIELD1", "MIN")
cfg.dir_get_last_val("FIELD1", "MIN")
```