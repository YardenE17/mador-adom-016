# mador-adom-016



## Add your plug-in:
under "/plugins/<your-plug-in>/..." add your plug-in files. 
```
│   <your-plug-in>.py
│   schema.json
│   __init__.py
```

The schema must follow the next instructions:
```
{
    "fields": [
        {"name": "<field-name>"}
    ]
}
```