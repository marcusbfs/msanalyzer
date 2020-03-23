# msanalyzer

Analyze XPS report files generated from Mastersizer 2000.

## Getting Started

The easiest way to use msanalyzer is to download the .exe on release pages.
After downloading it, put the XPS report in the same folder as the EXE. Rename the XPS to "ms_input.xps" and double-click "msanalyzer.exe".

This will create a "mastersizer_output" directory with the following files:
- output_curve_data.xlsx: diameter, volume fraction and cumulative volume fraction data in a Excel file;
- output_curves.svg: Plots of volume fraction and cumulative volume fraction data;
[![RRB fitted model](https://raw.githubusercontent.com/marcusbfs/msanalyzer/output_example/output_curves.svg)](https://raw.githubusercontent.com/marcusbfs/msanalyzer/output_example/output_curves.svg)
- output_curve_data.txt: diameter, volume fraction and cumulative volume fraction data in a TXT file;
- output_RRB_model_parameters.txt: RRB model parameters fitted to input data;
- output_RRB_model.svg: Cumulative volume fraction plot of data and RRB fitted model.
[![RRB fitted model](https://raw.githubusercontent.com/marcusbfs/msanalyzer/output_example/output_RRB_model.svg)](https://raw.githubusercontent.com/marcusbfs/msanalyzer/output_example/output_RRB_model.svg)

The program can also be used from command line with several options. Insided CMD or PowerShell, use

```
./msanalyzer.exe --help
```

to see the available options.

### Installing

To get a development env running, do the following:

1 - Clone the repo

```
git clone https://github.com/marcusbfs/msanalyzer.git
```

2 - Create a virtual environment and activate it

```
python -m venv msanalyzer_venv
.\msanalyzer_venv\Script\activate.bat
```

3 - Download requirements files

```
pip install -r requirements.txt
```

4 - Run a test

```
python msanalyzer.py ms_input.xps
```

## Contributing

Feel free to contribute anyway you feel like :)

## Authors

* **Marcus Bruno Fernandes Silva** - *marcusbfs@gmail.com*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details