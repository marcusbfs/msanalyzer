# msanalyzer

Analyze XPS report files generated by Mastersizer 2000.

## Aplicativo web (PT-BR)

O _msanalyzer_ possui uma versão mais simples em formato de _aplicativo web_. Deste modo, é extremamente fácil usar o programa.

Basta acessar o site [msanalyzer.netlify.app](https://msanalyzer.netlify.app/) e utilizar! Não é necessário nenhum tipo de instalação.

Qualquer dúvida sobre a utilização do site, por favor, entre em contato.

## Interface gráfica (PT-BR)

Para usar a interface gráfica, baixe o arquivo _msanalyzer_gui_win64.zip_ disponível na [página de releases](https://github.com/marcusbfs/msanalyzer/releases) e descompacte-o.

Dentro da pasta descompactada, haverá um arquivo chamado _msanalyzer_gui.exe_. Execute-o para iniciar o programa.

_Obs: Ao abrir o executável pela primeira vez, pode ser que o programa demore para iniciar. Isto é normal: o interpretador do Python precisa ser descompactado; este procedimento não deve demorar mais que 20 segundos. Apenas espere e não se preocupe :)_

Qualquer dúvida sobre a utilização do programa, sugestões de melhoria ou desejo de colaborar com o código, sinta-se a vontade para entrar em contato!

### Seleção e visualização de modelos

[![Models](https://raw.githubusercontent.com/marcusbfs/msanalyzer/master/images/models_tab.png)](https://raw.githubusercontent.com/marcusbfs/msanalyzer/master/images/models_tab.png)

### Gráfico de um único arquivo

[![Models](https://raw.githubusercontent.com/marcusbfs/msanalyzer/master/images/plot_tab.png)](https://raw.githubusercontent.com/marcusbfs/msanalyzer/master/images/plot_tab.png)

### Gráfico de vários arquivos

[![Models](https://raw.githubusercontent.com/marcusbfs/msanalyzer/master/images/multiplots_tab.png)](https://raw.githubusercontent.com/marcusbfs/msanalyzer/master/images/multiplots_tab.png)

### Janela principal

[![Options](https://raw.githubusercontent.com/marcusbfs/msanalyzer/master/images/options_gui.png)](https://raw.githubusercontent.com/marcusbfs/msanalyzer/master/images/options_gui.png)

## Command line interface

The easiest way to use **msanalyzer** is to download the .exe file on [release pages](https://github.com/marcusbfs/msanalyzer/releases).
After downloading it, put the XPS report in the same folder as the EXE. Rename the XPS to "ms_input.xps" and double-click "msanalyzer.exe".

This will create a directory called "mastersizer_output" with the following files:

- output_curve_data.xlsx: diameter, volume fraction and cumulative volume fraction data in a Excel file;
- output_curves.svg: Plot of volume fraction and cumulative volume fraction data (example below);
  [![RRB fitted model](https://raw.githubusercontent.com/marcusbfs/msanalyzer/master/output_example/output_curves.png)](https://raw.githubusercontent.com/marcusbfs/msanalyzer/master/output_example/output_curves.png)
- output_curve_data.txt: diameter, volume fraction and cumulative volume fraction data in a TXT file;
- output_RRB_model_parameters.txt: RRB model parameters fitted to input data;
- output_RRB_model.svg: Cumulative volume fraction plot of data and RRB fitted model (example below).
  [![RRB fitted model](https://raw.githubusercontent.com/marcusbfs/msanalyzer/master/output_example/output_RRB_model.png)](https://raw.githubusercontent.com/marcusbfs/msanalyzer/master/output_example/output_RRB_model.png)

This program can also be used from command line with several options. Inside CMD or PowerShell, enter

```
./msanalyzer.exe --help
```

to see the available options.

### dev install

To get a development enviroment running, do the following:

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

Feel free to contribute anyway you want to :)

## Authors

- **Marcus Bruno Fernandes Silva** - *marcusbfs@gmail.com*

## License

This project is licensed under the MIT License - see the [LICENSE.rst](LICENSE.rst) file for details
