# hrpt
Ham Radio Programming Tool


## Contributing

Create a python environment by
```
$ pyenv install 3.12.2
$ pyenv virtualenv -p python3.12 3.12.2 hrpt-3.12
$ echp "hrpt-3.12" > .python-version
```

## Test Files

There are a number of test files in tests/input_files and tests/output_files.
These files have the following naming convention:

    {dataset_name}-{schema}{-variant}.{format}

The various portions of the file name have the following definitions:

* dataset_name - an arbitrary name to represent a set of memories
* schema - the structure of the data, for example CHIRP or ADMS-16
* variant - some schemas have different variations, like CHIRP, which
  has a slightly different structure and values for each radio it can
  program
* format - the file format the schema is expressed in. For example, the
  same schema and variant can be saved as a Comma Seperated Value file or
  and Excel file. Generally the rendered output is in a single format which
  can be natively read by the desired programming software. Input files can
  often be read in several different formats.

Files with the same dataset name go together. For example there is a dataset
called `mem1000` which is stored in a files in `tests/input_files` as
`mem1000-CHIRP.csv`. The filename indicates that files in in the CHIRP format.

There are some automated tests that convert that file to various formats, and
compare the test output with static files in `tests/output_files`, for example
`mem1000-ADMS16.csv`. The files in `tests/output_files` are manually tested to
ensure they can be programmed into their respective radios.

These files serve as a sort of integration test to validate that any changes to
the software can still produce files that can successfully be used on a radio.


## TODO

- consider an input format from an excel file using openpyxl
-
