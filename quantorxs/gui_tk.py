import tkinter as tk
from tkinter.filedialog import askdirectory
from subprocess import call


def main():
    def run(*args, **kwargs):
        print(directory.get())
        call(["quantorxs",
             "--directory", directory.get(),
             "--results_directory", T.get("1.0",'end-1c'),
             "--fig_format", formats[v.get()][0].lower(),
             "--demo"]
             )

    def update_directory():
        directory.set(askdirectory())
        print(directory.get())

    root = tk.Tk()
    root.title("QUANTORXS GUI")
    demo = tk.BooleanVar()
    directory = tk.StringVar("")
    results_directory_label = tk.Label(root, text="Results directory")
    results_directory_label.grid(row=1, column=0)
    T = tk.Text(root, height=1, width=30)
    T.insert(tk.END, "QUANTORXS results")
    T.grid(row=1, column=1)
    tk.Checkbutton(root, text="Demo", variable=demo).grid(row=2, sticky=tk.W)

    directory_button = tk.Button(root,
                       text="Choose data directory",
                       # fg="red",
                       command=update_directory,
                       )
    directory_button.grid(row=0, sticky=tk.W)
    directory_txt = tk.Label(root, textvariable=directory)
    directory_txt.grid(row=0, column=1)
    quit_button = tk.Button(root,
                       text="QUIT",
                       # fg="red",
                       command=quit)
    # quit_button.pack(side="left")
    run_button = tk.Button(root,
                       text="RUN",
                       # fg="red",
                       command=run)

    v = tk.IntVar()
    v.set(1)  # initializing the choice, i.e. Python

    formats = [
        ("SVG",1),
        ("PDF",2),
        ("PNG",3),
    ]

    def ShowChoice():
        print(v.get())

    tk.Label(root,
             text="Choose the figures format",
             justify = tk.LEFT,
             padx = 20).grid(row=3)
    i = 4
    for val, format_ in enumerate(formats):
        tk.Radiobutton(root,
                      text=format_,
                      padx = 20,
                      variable=v,
                      command=ShowChoice,
                      value=val).grid(row=i)
        i += 1


    run_button.grid(row=i + 1, column=0,sticky=tk.W)
    quit_button.grid(row=i + 1, column=1,sticky=tk.W)

    root.mainloop()
