# KiCad Resistor Symbol Generator

This Python script generates KiCad symbol files (.kicad_sym) for resistors based on data from a CSV file. It's designed to streamline the process of creating custom resistor symbols for use in KiCad electronic design automation (EDA) software.

## Features

- Generates KiCad symbol files from CSV data
- Customizable for different resistor properties
- Creates a standardized resistor symbol with configurable properties
- Handles multiple resistors in a single CSV file

## Requirements

- Python 3.x
- No external libraries required (uses only Python standard library)

## Usage

1. Prepare your CSV file with resistor data (see `resistor.csv` for example format).
2. Run the script:

   ```
   python kicad_resistor_symbol_generator.py
   ```

3. The script will generate a `RESISTORS_DATA_BASE.kicad_sym` file in the same directory.

## CSV File Format

The input CSV file should have the following headers:

- Symbol Name
- Reference
- Value
- Footprint
- Datasheet
- Description
- Manufacturer
- MPN
- Tolerance
- Voltage Rating

Each row in the CSV represents a different resistor.

## Adding as a Submodule

To add this repository as a submodule to your existing project, follow these steps:

1. Open a terminal and navigate to your project's root directory.
2. Run the following command to add the KiCAD Symbol Generator as a submodule:

   ```
   git submodule add https://github.com/ionutms/KiCAD_Symbol_Generator.git
   ```

3. Commit the changes to your project:

   ```
   git commit -m "Add KiCAD Symbol Generator as submodule"
   ```

4. Push the changes to your remote repository:

   ```
   git push origin main
   ```

To update the submodule in the future, use:

```
git submodule update --remote KiCAD_Symbol_Generator
```

To clone a project that includes this submodule, use:

```
git clone --recursive https://github.com/ionutms/KiCAD_Symbol_Generator.git
```

Or, if you've already cloned the project without the `--recursive` flag:

```
git submodule init
git submodule update
```

## Removing the Submodule

If you need to remove the KiCAD Symbol Generator submodule from your project, follow these steps:

1. Run the `deinit` command to unregister the submodule:

   ```
   git submodule deinit -f KiCAD_Symbol_Generator
   ```

2. Remove the submodule from the Git cache:

   ```
   rm -rf .git/modules/KiCAD_Symbol_Generator
   ```

3. Remove the submodule from the working tree:

   ```
   git rm -f KiCAD_Symbol_Generator
   ```

4. Commit the changes:

   ```
   git commit -m "Removed KiCAD Symbol Generator submodule"
   ```

5. Push the changes to your remote repository:

   ```
   git push origin main
   ```

After completing these steps, the KiCAD Symbol Generator submodule will be completely removed from your project.