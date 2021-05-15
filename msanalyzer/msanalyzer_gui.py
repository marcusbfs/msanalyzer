import json
import os
import pathlib
import re
import sys
import threading
import time
import tkinter
from tkinter import font
from typing import List, Tuple, TypedDict

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import NullFormatter  # useful for `logit` scale

from . import msanalyzer

matplotlib.use("TkAgg")


class ConfigDict(TypedDict):
    theme: str
    font: str
    font_size: int


import PySimpleGUI as sg

from . import icons_gui
from .models.SizeDistributionModelsFactory import available_models

script_folder = pathlib.Path(__file__).parent.absolute()
config_file: str = os.path.join(script_folder, "config_msanalyzer.cfg")

root = tkinter.Tk()
fonts = list(font.families())
fonts.extend(["Helvetica"])
fonts.sort()
root.destroy()

DEFAULT_SETTINGS: ConfigDict = {
    "theme": "DarkAmber",
    "font": "Helvetica",
    "font_size": 16,
}

##################### Load/Save Settings File #####################
def save_settings(settings_file: str, settings: ConfigDict) -> None:
    with open(settings_file, "w") as f:
        json.dump(settings, f)


def load_settings(settings_file: str, default_settings: ConfigDict) -> ConfigDict:
    settings: ConfigDict
    try:
        with open(settings_file, "r") as f:
            settings = json.load(f)
    except Exception as e:
        print("Creating default config file...")
        settings = default_settings
        save_settings(settings_file, settings)
    return settings


CURRENT_SETTINGS: ConfigDict = load_settings(config_file, DEFAULT_SETTINGS)

cf_theme: str = CURRENT_SETTINGS["theme"]
cf_font: str = CURRENT_SETTINGS["font"]
cf_font_size: int = int(CURRENT_SETTINGS["font_size"])

sg.theme(cf_theme)
sg.set_options(font=(cf_font, cf_font_size))

fig_canvas_agg: FigureCanvasTkAgg = None
fig_model_canvas_agg: FigureCanvasTkAgg = None


def delete_figure_agg(figure_agg: FigureCanvasTkAgg) -> None:
    figure_agg.get_tk_widget().forget()
    plt.close("all")


def draw_figure(canvas: tkinter.Canvas, figure: plt.figure) -> FigureCanvasTkAgg:
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


def long_function_thread(window: sg.Window, cmd_args: List[str]) -> None:
    msanalyzer.main(cmd_args)
    window.write_event_value("-THREAD DONE-", "")


def long_function() -> None:
    threading.Thread(
        target=long_function_thread, args=(window, cmd_args), daemon=True
    ).start()


def zerosSpin(
    key: str = "",
    min_val: int = 1,
    max_val: int = 50,
    size: Tuple[int, int] = (4, 1),
    default_val: int = 1,
) -> sg.Spin:
    return sg.Spin(
        values=[i for i in range(min_val, max_val + 1)],
        initial_value=default_val,
        key=key,
        size=size,
        enable_events=True,
        readonly=True,
        text_color="black",
    )


def create_settings_window(settings: ConfigDict) -> sg.Window:
    sg.theme(settings["theme"])

    def TextLabel(text: str) -> sg.Text:
        return sg.Text(text + ":", justification="r", size=(15, 1))

    layout = [
        [
            sg.Text(
                "Configurações",
            )
        ],
        [
            sg.T("Tema: "),
            sg.Combo(
                sg.theme_list(), default_value=cf_theme, k="theme#combo", readonly=True
            ),
        ],
        [
            sg.T("Fonte: "),
            sg.Combo(fonts, default_value=cf_font, k="font#combo", readonly=True),
        ],
        [
            sg.T("Tamanho da fonte: "),
            sg.Spin(
                values=[i for i in range(10, 51)],
                initial_value=int(cf_font_size),
                size=(5, 1),
                k="font_size",
                readonly=True,
            ),
        ],
        [sg.Button("Salvar", k="save_config"), sg.Button("Sair", k="sair_config")],
    ]

    window = sg.Window("Configurações", layout, keep_on_top=True, finalize=True)

    return window


python_exe = os.path.join(os.path.dirname(sys.executable), "python.exe")
pythonw_exe = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
script_path = pathlib.Path(__file__).parent.absolute()
msanalyzer_py = os.path.join(script_path, "msanalyzer.py")

xps_file: str = ""
output_dir: str = ""
output_basename: str = ""
t0: float = time.time()
single_file_mode: bool = True
time_progress_bar_to_exit_sec: float = 2.0

options_layout = [
    [
        sg.Col(
            [[sg.Text(text="Diretório de saída:")], [sg.Text(text="Nome de saída:")]]
        ),
        sg.Col(
            [
                [
                    sg.Input(
                        default_text="./msanalyzer_output", key="output_path##input"
                    )
                ],
                [sg.InputText(key="basename##input")],
            ]
        ),
        sg.Col(
            [
                [
                    sg.FolderBrowse(button_text="...", target="output_path##input"),
                    sg.Button(
                        button_text="Abrir diretório", key="open_output_dir##button"
                    ),
                ]
            ],
            vertical_alignment="top",
        ),
    ],
    [
        sg.Checkbox(
            "Gráficos em escala logarítimica",
            default=True,
            key="logscale##checkbox",
        )
    ],
]

input_xps_layout = [
    [
        sg.Text("Arquivo(s) XPS:", justification="left"),
        sg.Input(
            enable_events=True,
            key="input##xps",
        ),
        sg.FilesBrowse(
            button_text="...",
            file_types=(("XPS files", "*.xps"),),
            tooltip="Atalho: ctrl-o",
        ),
        sg.Button(
            "Abrir arquivo", key="openxps##button", tooltip="Abre XPS selecionado"
        ),
    ],
]

advanced_options_layout = [
    [
        sg.Text(
            text="Tipo de média:",
            tooltip="O manual do MasterSizer recomenda a utilização da média geométrica.",
        ),
        sg.Radio(text="Geométrica", group_id=1, default=True, key="media_geo##radio"),
        sg.Radio(text="Aritimética", group_id=1),
    ],
    [sg.HorizontalSeparator()],
    [
        sg.Checkbox(
            "Não colocar legenda nos gráficos de múltiplos arquivos",
            default=False,
            key="nomultiplolabel",
        )
    ],
    [sg.HorizontalSeparator()],
    [
        sg.Col(
            [[sg.Text(text="Zeros à esquerda: ")], [sg.Text(text="Zeros à direita:  ")]]
        ),
        sg.Col(
            [[zerosSpin("first_zeros##spin")], [zerosSpin("last_zeros##spin")]],
            element_justification="left",
        ),
    ],
    [sg.HorizontalSeparator()],
    [sg.B("Opções do aplicativo", k="app_config##button")],
    [sg.HorizontalSeparator()],
]


tab_plot_layout = [
    [sg.T("", k="plot_text", size=(70, 1), justification="left")],
    [sg.HorizontalSeparator()],
    [sg.Canvas(k="canvas")],
]

layout_principal = [
    [
        sg.Frame(
            "",
            input_xps_layout,
            tooltip="Selecione um arquivos para fazer a análise isolada e mais detalhada (com modelos tipo RRB).\nSelecione dois ou mais arquivos XPS para comparar os gráficos.",
            key="input_xps##frame",
            vertical_alignment="top",
        )
    ],
    [
        sg.Frame(
            "Opções", options_layout, key="options##frame", vertical_alignment="top"
        )
    ],
    [sg.HorizontalSeparator()],
    [
        sg.Checkbox(
            'Ir para aba "Output" automaticamente',
            default=True,
            key="go_out##check",
        )
    ],
]

output_layout = [
    [sg.Output(key="out##output", echo_stdout_stderr=True)],
]

tab_models_layout = [
    [
        sg.T("Modelo: "),
        sg.Combo(
            available_models,
            default_value="RRB",
            k="model##combo",
            size=(15, 1),
            readonly=True,
            enable_events=True,
        ),
    ],
    [sg.HorizontalSeparator()],
    [sg.T("", k="model_name_text", size=(70, 1), justification="left")],
    [sg.HorizontalSeparator()],
    [sg.Canvas(k="model##canvas")],
    [sg.HorizontalSeparator()],
    [
        sg.B("Ranking dos modelos", k="models_rank##button"),
        sg.T("", size=(5, 1)),
        sg.B("Dados do modelo", k="open_model_data##button"),
    ],
]

layout = [
    [
        sg.Column(
            [
                [
                    sg.TabGroup(
                        [
                            [
                                sg.Tab(
                                    "Principal",
                                    layout_principal,
                                    key="principal##tab",
                                ),
                                sg.Tab("Opções avançadas", advanced_options_layout),
                                sg.Tab("Plot", tab_plot_layout, key="plot##tab"),
                                sg.Tab("Modelos", tab_models_layout, key="models##tab"),
                                sg.Tab("Output", output_layout, key="output##tab"),
                            ]
                        ],
                        key="main##tabgroup",
                    )
                ],
                [
                    sg.Button(button_text="Executar", tooltip="Atalho: ctrl-r"),
                ],
                [
                    sg.Progress(
                        100,
                        key="exec##progress",
                        orientation="horizontal",
                        size=(20, 20),
                        visible=True,
                    )
                ],
                [
                    sg.StatusBar(
                        "", k="status##text", justification="right", size=(20, 1)
                    )
                ],
            ],
            scrollable=False,
            key="main##col",
            vertical_alignment="top",
            element_justification="left",
        )
    ]
]

# Create the Window
window = sg.Window(
    "MSanalyzer - Interface gráfica",
    layout,
    return_keyboard_events=True,
    titlebar_icon=icons_gui.main_icon,
    icon=icons_gui.main_icon,
)
window.Resizable = True
window.finalize()

progress_bar: sg.Progress = window["exec##progress"]
out_text: sg.Output = window["out##output"]
tabgroup: sg.TabGroup = window["main##tabgroup"]
input_xps_frame: sg.Frame = window["input_xps##frame"]
options_frame: sg.Frame = window["options##frame"]
exec_button: sg.Button = window["Executar"]
model_canvas: sg.Canvas = window["model##canvas"]
tab_models: sg.Tab = window["models##tab"]
tab_plot: sg.Tab = window["plot##tab"]

out_text.expand(expand_x=True, expand_y=True)
tabgroup.expand(expand_x=True, expand_y=True)
input_xps_frame.expand(expand_x=True)
options_frame.expand(expand_x=True)
window["input##xps"].expand(expand_x=True)
window["output_path##input"].expand(expand_x=True)
window["basename##input"].expand(expand_x=True)
window["main##col"].expand(expand_x=True, expand_y=True)
window["canvas"].expand(expand_x=True, expand_y=True)
model_canvas.expand(expand_x=True, expand_y=True)

window.set_min_size((1080, 400))

progress_bar.update(0, visible=False)

can_clear_status: bool = True

tab_models.update(disabled=True)

button_text = f'Dados do modelo {"RRB"}'
window["open_model_data##button"].update(text=button_text)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read(timeout=333)

    if (
        event == sg.WIN_CLOSED or event == "Cancel" or event == None
    ):  # if user closes window or clicks cancel
        break
    if event == "Executar":

        xps_file = os.path.abspath(values["input##xps"]).split(";")
        # check mode
        if len(xps_file) == 1:
            single_file_mode = True
        else:
            single_file_mode = False

        # check if file(s) exists

        go_on: bool = True

        for f in xps_file:
            if not os.path.isfile(f):
                confirm = sg.PopupOK(
                    f'Arquivo "{f}" não existe"', title="Erro no arquivo XPS"
                )
                go_on = False

        if go_on:
            can_clear_status = False
            exec_button.update(disabled=True)

            if values["go_out##check"]:
                window["output##tab"].select()

            cmd_args = []

            progress_bar.update(5, visible=True)
            window.Element("status##text").Update("Computando...")
            window.refresh()

            if single_file_mode:

                xps_file = xps_file[0]

                cmd_args.append(xps_file)

            else:
                cmd_args.append("-M")
                for f in xps_file:
                    cmd_args.append(f)

                if not values["nomultiplolabel"]:
                    cmd_args.append("--multi-labels")
                    for f in xps_file:
                        basename = os.path.splitext(os.path.basename(f))[0]
                        cmd_args.append(basename)
                else:
                    cmd_args.append("--multi-no-labels")

            progress_bar.update(30)
            window.refresh()

            output_dir = os.path.abspath(values["output_path##input"])
            output_basename = values["basename##input"]
            media = "geo" if values["media_geo##radio"] else "ari"

            # -o
            if output_basename[-1] != "_":
                output_basename = output_basename + "_"
            cmd_args.append("--output_basename")
            cmd_args.append(output_basename)

            # -d
            cmd_args.append("--output_dir")
            cmd_args.append(output_dir)

            # -m
            cmd_args.append("--diameter_mean")
            cmd_args.append(media)

            # -f
            cmd_args.append("--first_zeros")
            cmd_args.append(str(values["first_zeros##spin"]))

            # -l
            cmd_args.append("--last_zeros")
            cmd_args.append(str(values["last_zeros##spin"]))

            # -s
            if values["logscale##checkbox"]:
                cmd_args.append("--log-scale")

            progress_bar.update(60)
            window.refresh()

            cmd_args.append("--info")

            # clear current output
            out_text.update("")
            # long_function()
            msanalyzer.main(_args=cmd_args)
            progress_bar.update(80)
            window.refresh()
            window.write_event_value("-THREAD DONE-", "")

    if event == "-THREAD DONE-":
        window.Element("status##text").Update("Pronto!")
        progress_bar.update(100)
        t0 = time.time()
        if values["go_out##check"]:
            window["principal##tab"].select()
        can_clear_status = True
        exec_button.update(disabled=False)
        window.refresh()

        # plot
        if msanalyzer.fig:
            # clear canvas
            window["canvas"].tk_canvas.delete("all")
            if fig_canvas_agg:
                delete_figure_agg(fig_canvas_agg)
            # plot
            fig_canvas_agg = draw_figure(window["canvas"].TKCanvas, msanalyzer.fig)
            # set name
            file_name = "Arquivo: " + os.path.basename(values["input##xps"])
            # window['plot_text'].set_size((len(file_name),1))
            window["plot_text"].update(file_name)

        if single_file_mode:
            # Display models
            if len(msanalyzer.models_figs) > 0:
                tab_models.update(disabled=False)
                model_canvas.tk_canvas.delete("all")
                if fig_model_canvas_agg:
                    delete_figure_agg(fig_model_canvas_agg)
                curr_model_label = values["model##combo"]
                fig_model_canvas_agg = draw_figure(
                    model_canvas.TKCanvas, msanalyzer.models_figs[curr_model_label]
                )
                # set name
                file_name = "Arquivo: " + os.path.basename(values["input##xps"])
                window["model_name_text"].update(file_name)
        else:
            tab_models.update(disabled=True)

    if event == "models_rank##button":
        output_dir = os.path.abspath(values["output_path##input"])
        rank_data_file = os.path.join(output_dir, "best_models_ranking.txt")
        if os.path.isfile(rank_data_file):
            os.startfile(rank_data_file)

    if event == "open_model_data##button":
        output_dir = os.path.abspath(values["output_path##input"])
        base_file = output_basename = values["basename##input"]
        model_name = values["model##combo"]
        out_file = model_name + "_" + base_file + "_model_parameters.txt"
        model_data_file = os.path.join(output_dir, out_file)

        if os.path.isfile(model_data_file):
            os.startfile(model_data_file)

    if event == "input##xps":

        xps_file = os.path.abspath(values["input##xps"]).split(";")
        # check mode
        if len(xps_file) == 1:
            single_file_mode = True

            xps_file = os.path.abspath(xps_file[0])
            output_basename = os.path.splitext(os.path.basename(xps_file))[0]
            output_dir = os.path.join(
                os.path.dirname(xps_file), output_basename + "_output"
            )
            window.Element("input##xps").Update(xps_file)
            window.Element("output_path##input").Update(output_dir)
            window.Element("basename##input").Update(output_basename)
        else:
            single_file_mode = False
            output_basename = "multifiles"
            output_dir = os.path.join(
                os.path.dirname(xps_file[0]), "multifiles" + "_output"
            )
            window.Element("output_path##input").Update(output_dir)
            window.Element("basename##input").Update(output_basename)

    if event == "open_output_dir##button":
        output_dir = os.path.abspath(values["output_path##input"])
        if os.path.isdir(output_dir):
            os.startfile(output_dir)

    if event == "r:82":  # ctrl-r
        # Mudar para tab
        window["Executar"].click()

    if event == "o:79":  # ctrl-o
        window["Selecionar"].click()

    if event == "openxps##button":
        xps_file = os.path.abspath(values["input##xps"])
        if os.path.isfile(xps_file):
            os.startfile(xps_file)
        else:
            confirm = sg.PopupOK(
                f'Arquivo "{xps_file}" não existe"', title="Erro no arquivo XPS"
            )
            continue

    if event == "model##combo":
        model = values[event]

        # update plot
        if len(msanalyzer.models_figs) > 0:
            model_canvas.tk_canvas.delete("all")
            if fig_model_canvas_agg:
                delete_figure_agg(fig_model_canvas_agg)
            fig_model_canvas_agg = draw_figure(
                model_canvas.TKCanvas, msanalyzer.models_figs[model]
            )

        # update button
        button_text = f"Dados do modelo {model}"
        window["open_model_data##button"].update(text=button_text)

    if event == "app_config##button":
        event, values = create_settings_window(CURRENT_SETTINGS).read(close=True)
        if event == "save_config":
            try:
                CURRENT_SETTINGS["theme"] = str(values["theme#combo"])
                CURRENT_SETTINGS["font"] = str(values["font#combo"])
                CURRENT_SETTINGS["font_size"] = int(values["font_size"])

                save_settings(config_file, CURRENT_SETTINGS)
                window["status##text"].update("Salvo! É necessário reiniciar o app!")
            except:
                window["status##text"].update("Erro ao salvar configurações!")

            can_clear_status = True
            t0 = time.time()
            window.refresh()

    if event in ("first_zeros##spin", "last_zeros##spin"):
        window.FindElement(event).Update(int(re.sub(r"[^0-9]", "", str(values[event]))))

    window["plot##tab"].update(disabled=False if msanalyzer.fig else True)

    if can_clear_status:
        if (time.time() - t0) >= time_progress_bar_to_exit_sec:
            window.Element("status##text").Update("")
            progress_bar.update(0, visible=False)


window.close()
