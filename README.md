# hrpt
Ham Radio Programming Toolkit

I have several ham radio VHF/UHF radios. It would be great if they all
used the same programming software.
[CHIRP](https://chirpmyradio.com/projects/chirp/wiki/Home) is the natural answer,
it's free and it supports a bunch of radios. But it doesn't support all radios, and
there are some minor differences in the CHIRP import and export file format
depending on the radio it's connected to.

I've had people email me a "CHIRP file that you can import", and have it be
an Excel spreadsheet, which when then had to export to a CSV, and when I
imported it into chirp it complained about some of the frequencies or
settings.

I want a way to keep a single list of frequencies for radios with 999
memories, and then have a tool that would create a file I could immediately
import into CHIRP that was connected to my Kenwood TH-D75, and another file
that I could import into CHIRP that was connected to the Wouxun KG-UV9PX, and
another file that I could import into ADMS-16, the software from Yaesu used to
program the FTM-500DR.

I tried making a big spreadsheet to do this, but I ran into a bunch of limitations.
I'm a better programmer than I am a spreadsheet wizard, so I decided to build
some software which can:

* Parse the key information for a set of VHF/UHF memories stored in several
  different formats (including CHIRP and a generic Excel version)
* Translate that information into one of more output formats that can be
  imported into programming software and sent to a radio with no additional
  fiddling or hand-tweaking


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
