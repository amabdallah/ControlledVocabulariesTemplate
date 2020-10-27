# CVsTemplate

Is a template application to create a controlled vocabulary web-server powered by python/django. This project was adapted from the source code of the controlled vocabulary registry for the Observations Data Model 2 (ODM2) https://github.com/ODM2/ODM2ControlledVocabularies

# What's the difference?

This repository has a simplified folder structure and configuration, using the same pattern to load variables from a json file with some new parameters. But the main asset is the use of the file `cv_models.json` to declare the models that will be loaded into the system on runtime. The following files have been modified to allow these changes: 

* cvservices/models.py
* cvinterface/controlled_vocabularies.py
* cvservices/api.py

Now the `cvservices` module has two commands to load and reset the tables declared on `cv_models.json`, these commands locations are:

* cvservices/management/commands/reset_db.py
* cvservices/management/commands/populate_db.py

Note: The `units` tables and references have been dropped just for convenience on this project

# How it works?

The files mentioned in the section above follow these steps to load in runtime the data they need about the models: 

1. Read the `cv_models.json` file. If the file is not present then throw an exception and stop execution
2. For each model found, its name is replaced into the respective template. The model names are written differently in some sections of the template, so in some cases utility functions are used to change them. The result of this step is a huge string variable with the corresponding declaration of the models read from `cv_models.json`.
3. In this step the string variables are executed as actual code

The result is that you can centralize the model declaration writing all the model names and descriptions in `cv_models.json`, then all the modules that require to know the model names will read this file and create the proper code from the given templates

Adding or removing models will be easier this way than making these same changes by hand on all the required files, several times if you need to add or remove many tables. Also this approach is way less prone to human typing errors

But this scheme also has its own limitations; the models declared here must be homogeneus, no additional fields on specific models are supported and the format to write the models should be followed strictly

# Format and considerations for the file cv_models.json

The `cv_models.json` is a dictionary that contains models that will be loaded by the application. To avoid unknown erros or misbehavior, it is encouraged that you follow this conventions for every item: 

```
{
    "name": "CamelCaseName",
    "description" : "To be added."
},
```

The name parameter should be written in [camel case](https://en.wikipedia.org/wiki/Camel_case)

Currently it's not supported that the description parameter contains sub-strings, so it's encouraged to look for an alternative to quotes or highlightings. Please see the examples below

This are supported descriptions

```
"description" : "This table is based on the [vw_CDSS_NetAmts] view."
```

```
"description" : "This table is based on the reported water quality of the resource in question."
```

and this is a not supported description

```
"description" : 'A term for describing types of Methods associated with recording or generating data values to attributes. Example method types are like "expert opinion", "field procedure", "model simulation".'
```