# Element Concentration Plotter

A Python desktop application for visualizing element concentration data from Excel files.

The tool reads `.xls` and `.xlsx` files, uses the first column as sample identifiers, and plots all remaining columns as elements or analytical parameters. Each sample is displayed as a separate colored line on a logarithmic Y-axis.

## Features

* Graphical Excel file selection
* Supports `.xls` and `.xlsx` files
* Automatically detects plotted elements from Excel column headers
* Uses the first column as sample ID
* Plots each sample as a separate colored line
* Connects data points with lines
* Skips missing, invalid, zero, or negative values
* Supports comma-based decimal values, such as `0,25`
* Uses a logarithmic Y-axis
* Automatically scales the Y-axis based on the data
* Adds one order of magnitude below and above the data range
* Allows loading a new Excel file from the menu bar
* Saves figures as PNG, PDF, or SVG
* Automatically saves a PNG output next to the source Excel file

## Use Case

This tool is designed for quick visualization of geochemical, environmental, laboratory, or analytical datasets where multiple samples are measured across the same set of elements or parameters.

Typical use cases include:

* Geochemical element concentration plots
* Soil, rock, sediment, or water sample comparison
* Laboratory result checking
* Multi-sample concentration profile visualization
* Log-scale plotting of datasets with wide value ranges

## Input Excel Format

The Excel file must contain a header row.

The first column must contain the sample ID or sample number.

All remaining columns are treated as elements or analytical parameters and are plotted on the X-axis.

Example:

| Sample ID | Mo   | Cu | Pb  | Zn | Fe   | As  |
| --------- | ---- | -- | --- | -- | ---- | --- |
| 1         | 0.12 | 15 | 3.2 | 45 | 1200 | 5.4 |
| 2         | 0.20 | 18 |     | 50 | 1500 | 7.1 |
| 3         |      | 11 | 2.1 |    | 980  | 4.8 |

In this example:

* `Sample ID` is used for the legend
* `Mo`, `Cu`, `Pb`, `Zn`, `Fe`, and `As` are plotted on the X-axis
* each row is plotted as a separate line

## Data Handling

The application automatically prepares the Excel data before plotting.

It converts numeric values and also supports comma decimal notation.

For example:

```text
0,25
```

is interpreted as:

```text
0.25
```

The following values are ignored:

* empty cells
* non-numeric values
* zero values
* negative values

Zero and negative values are excluded because they cannot be displayed on a logarithmic axis.

## Missing Values

Missing values are not plotted.

If a value is missing within a sample line, the line is interrupted at that point. The line continues from the next valid value.

This prevents misleading interpolation across missing analytical results.

## Y-Axis Scaling

The Y-axis uses a logarithmic scale.

The axis range is calculated automatically from the positive numeric values in the dataset:

```text
Y minimum = minimum positive value / 10
Y maximum = maximum positive value × 10
```

This gives the plot one order of magnitude of visual margin below and above the actual data range.

Example:

```text
Minimum positive value = 0.001
Maximum positive value = 2000
```

The resulting Y-axis range will be:

```text
0.0001 – 20000
```

## User Interface

The application runs in a graphical desktop window.

When started, it opens a file selection dialog. After selecting an Excel file, the plot is generated automatically.

The menu bar contains the following options:

```text
File
├── Select new file
├── Save figure
└── Exit
```

Selecting a new file updates the plot in the same application window without restarting the program.

## Output

The generated figure is displayed in the application window.

A PNG file is automatically saved next to the selected Excel file.

The output filename format is:

```text
original_excel_filename_diagram.png
```

Example:

```text
data.xlsx
```

creates:

```text
data_diagram.png
```

Figures can also be saved manually from the menu in the following formats:

* PNG
* PDF
* SVG

## Installation

Python 3.9 or newer is recommended.

Install the required Python packages:

```bash
pip install pandas matplotlib numpy openpyxl xlrd
```

On Linux, `tkinter` may need to be installed separately:

```bash
sudo apt install python3-tk
```

On Windows, `tkinter` is usually included with the standard Python installation.

## Running the Application

Run the script from a terminal:

```bash
python element_concentration_plotter.py
```

Then:

1. Select an Excel file.
2. The application reads the table.
3. The plot is generated.
4. The figure is displayed.
5. A PNG copy is saved automatically.

## Example Workflow

1. Prepare an Excel file with sample IDs in the first column.
2. Add element or parameter names as column headers.
3. Fill in the concentration values.
4. Run the application.
5. Select the Excel file.
6. Review the logarithmic plot.
7. Load another file from the menu if needed.
8. Save the figure as PNG, PDF, or SVG.

## Limitations

* The first worksheet is read by default.
* The table must contain a header row.
* The first column must contain sample IDs.
* Zero and negative values are not displayed.
* Very large numbers of samples may make the legend crowded.
* Very large numbers of elements may make the X-axis labels crowded.

## Error Handling

The application displays an error message if:

* the selected file cannot be read
* the Excel file contains fewer than two columns
* no valid element or parameter columns are found
* no positive numeric values are available for plotting
* the file cannot be processed

## Project Goal

The goal of this project is to provide a simple graphical tool for quickly plotting element concentration data from Excel files without manual column configuration.

The application automatically uses the Excel header row to determine the plotted elements, making it suitable for datasets where the measured element list may vary between files.

## AI Assistance Disclosure

This project was created with assistance from artificial intelligence.

Code structure, documentation, and README content were developed with the help of OpenAI ChatGPT, using the GPT-5.5 Thinking model. The final implementation, testing, and responsibility for the project remain with the repository maintainer.
