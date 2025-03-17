# mador-adom-016



## Add your plug-in:
under "/plugins/<your-plug-in>/..." add your plug-in files. 
```
│   <your-plug-in>.py
│   schema.json
│   __init__.py
```
### .py
The .py file must follow the next instructions:
 * make sure you log every operation using the logger which is a must argument for every main
```python
def main(arg1: str, arg2: int, logger):
    """
    Plugin's main function. Receives arguments as named parameters via kwargs.
    """
    logger.info(msg)
    func()
    return ...

def func():
    """
    Side function. It performs some calculation/operation/etc... to serve the main function. 
    """
    ...
```

### Schema
The schema must follow the next instructions:
```
{
    "fields": [
        {"name": "<field-name1>"},
        {"name": "<field-name2>"}
    ]
}
```
