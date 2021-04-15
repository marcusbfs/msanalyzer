import os
import sys
import pathlib
import subprocess
import time
import re
import icons_gui

import PySimpleGUI as sg

sg.theme("DarkAmber")  # Add a touch of color


def zerosSpin(key: str = "", min_val: int = 1, max_val: int = 50, size=(4, 1)):
    return sg.Spin(
        values=[i for i in range(min_val, max_val + 1)],
        initial_value=min_val,
        key=key,
        size=size,
        enable_events=True,
        readonly=True,
        text_color="black",
    )


def main():

    python_exe = os.path.join(os.path.dirname(sys.executable), "python.exe")
    pythonw_exe = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
    script_path = pathlib.Path(__file__).parent.absolute()
    msanalyzer_py = os.path.join(script_path, "msanalyzer.py")

    xps_file: str = ""
    output_dir: str = ""
    output_basename: str = ""
    t0: float = time.time()
    single_file_mode: bool = True
    time_progress_bar_to_exit_sec: float = 1.5

    sg.set_options(font=("Helvetica", 16))

    options_layout = [
        [
            sg.Text(text="Diretório de saída:"),
            sg.Input(default_text="./msanalyzer_output", key="output_path##input"),
            sg.FolderBrowse(button_text="Selecionar",),
            sg.Button(button_text="Abrir diretório", key="open_output_dir##button"),
        ],
        [sg.Text(text="Nome de saída:"), sg.InputText(key="basename##input")],
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
            sg.Text("Arquivo(s) XPS:"),
            sg.Input(enable_events=True, key="input##xps"),
            sg.FilesBrowse(
                button_text="Selecionar",
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
            sg.Radio(
                text="Geométrica", group_id=1, default=True, key="media_geo##radio"
            ),
            sg.Radio(text="Aritimética", group_id=1),
        ],
        [
            sg.Checkbox(
                "Não colocar legenda nos gráficos de múltiplos arquivos",
                default=False,
                key="nomultiplolabel",
            )
        ],
        [sg.Text(text="Zeros à esquerda: "), zerosSpin("first_zeros##spin")],
        [sg.Text(text="Zeros à direita:  "), zerosSpin("last_zeros##spin"),],
    ]

    layout_principal = [
        [
            sg.Frame(
                "",
                input_xps_layout,
                tooltip="Selecione um arquivos para fazer a análise isolada e mais detalhada (com modelos tipo RRB).\nSelecione dois ou mais arquivos XPS para comparar os gráficos.",
            )
        ],
        [sg.Frame("Opções", options_layout)],
        [sg.HorizontalSeparator()],
        [
            sg.Checkbox(
                'Ir para aba "Output" depois de executado',
                default=False,
                key="go_out##check",
            )
        ],
        [
            sg.Button(button_text="Executar", tooltip="Atalho: ctrl-r"),
            sg.Text(text="", key="status##text", size=(20, 1)),
        ],
        [
            sg.Progress(
                100,
                key="exec##progress",
                orientation="horizontal",
                size=(20, 20),
                visible=False,
            )
        ],
    ]

    output_layout = [
        [sg.Multiline("", auto_refresh=True, key="out##multiline", disabled=True)]
    ]

    layout = [
        [
            sg.TabGroup(
                [
                    [
                        sg.Tab("Principal", layout_principal, key="principal##tab"),
                        sg.Tab("Opções avançadas", advanced_options_layout),
                        sg.Tab("Output", output_layout, key="output##tab"),
                    ]
                ],
                key="main##tabgroup",
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
    window.Size = (1100, 600)

    progress_bar: sg.Progress = window["exec##progress"]
    out_text: sg.Multiline = window["out##multiline"]
    tabgroup: sg.Trabgroup = window["main##tabgroup"]

    out_text.expand(expand_x=True, expand_y=True)
    tabgroup.expand(expand_x=True, expand_y=True)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read(timeout=333)

        # event, values = window.read()
        # print("-------------------\n", event, values, "\n---------------")

        if (
            event == sg.WIN_CLOSED or event == "Cancel" or event == None
        ):  # if user closes window or clicks cancel
            break
        elif event == "Executar":

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

                cmd = [python_exe, msanalyzer_py]

                progress_bar.update(5, visible=True)
                window.Element("status##text").Update("Computando...")
                window.refresh()

                if single_file_mode:

                    xps_file = xps_file[0]

                    cmd.append(xps_file)

                    # -l
                    cmd.append("--last_zeros")
                    cmd.append(str(values["last_zeros##spin"]))

                    # -s
                    if values["logscale##checkbox"]:
                        cmd.append("--log-scale")

                else:
                    cmd.append("-M")
                    for f in xps_file:
                        cmd.append(f)

                    if not values["nomultiplolabel"]:
                        cmd.append("--multi-labels")
                        for f in xps_file:
                            basename = os.path.splitext(os.path.basename(f))[0]
                            cmd.append(basename)
                    else:
                        cmd.append("--multi-no-labels")

                progress_bar.update(30)
                window.refresh()

                output_dir = os.path.abspath(values["output_path##input"])
                output_basename = values["basename##input"]
                media = "geo" if values["media_geo##radio"] else "ari"

                # -o
                if output_basename[-1] != "_":
                    output_basename = output_basename + "_"
                cmd.append("--output_basename")
                cmd.append(output_basename)

                # -d
                cmd.append("--output_dir")
                cmd.append(output_dir)

                # -m
                cmd.append("--diameter_mean")
                cmd.append(media)

                # -f
                cmd.append("--first_zeros")
                cmd.append(str(values["first_zeros##spin"]))

                progress_bar.update(60)
                window.refresh()

                cmd.append("--info")

                # run command
                out = subprocess.check_output(
                    cmd, shell=True, stderr=subprocess.STDOUT
                ).decode("utf-8")

                progress_bar.update(80)
                window.refresh()

                # send output
                out_text.update(disabled=False)
                out_text.update(value=out)
                out_text.update(disabled=True)

                window.Element("status##text").Update("Pronto!")
                progress_bar.update(100)
                t0 = time.time()

                if values["go_out##check"]:
                    window["output##tab"].select()

                window.refresh()

        elif event == "input##xps":

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

        elif event == "open_output_dir##button":
            output_dir = os.path.abspath(values["output_path##input"])
            if os.path.isdir(output_dir):
                os.startfile(output_dir)

        elif event == "r:82":  # ctrl-r
            # Mudar para tab
            window["principal##tab"].select()
            window["Executar"].click()

        elif event == "o:79":  # ctrl-o
            window["Selecionar"].click()

        elif event == "openxps##button":
            xps_file = os.path.abspath(values["input##xps"])
            if os.path.isfile(xps_file):
                os.startfile(xps_file)
            else:
                confirm = sg.PopupOK(
                    f'Arquivo "{xps_file}" não existe"', title="Erro no arquivo XPS"
                )
                continue

        elif event in ("first_zeros##spin", "last_zeros##spin"):
            window.FindElement(event).Update(
                int(re.sub(r"[^0-9]", "", str(values[event])))
            )

        if progress_bar.visible:
            if (time.time() - t0) >= time_progress_bar_to_exit_sec:
                window.Element("status##text").Update("")
                progress_bar.update(0, visible=False)

    window.close()


if __name__ == "__main__":
    main()
