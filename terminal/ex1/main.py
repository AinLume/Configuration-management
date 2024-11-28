import zipfile
import yaml
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, filedialog


class ShellEmulator:
    def __init__(self, config_file):
        self.load_config(config_file)
        self.current_path = Path("/")
        self.username = self.config.get("username", "user")
        self.hostname = self.config.get("hostname", "host")
        self.fs_archive = None
        self.load_filesystem()

    def load_config(self, config_file):
        with open(config_file, "r") as file:
            self.config = yaml.safe_load(file)

    def load_filesystem(self):
        zip_path = self.config.get("fs_path", "")
        if not zip_path or not Path(zip_path).exists():
            raise FileNotFoundError("Файл виртуальной файловой системы не найден.")
        self.fs_archive = zipfile.ZipFile(zip_path, "r")

    def list_dir(self, path):
        path = str(path).lstrip("/")
        if path and not path.endswith("/"):
            path += "/"
        return sorted(
            {
                entry[len(path):].split("/", 1)[0]
                for entry in self.fs_archive.namelist()
                if entry.startswith(path) and entry != path
            }
        )

    def ls(self):
        try:
            items = self.list_dir(self.current_path)
            return "\n".join(items)
        except Exception as e:
            return f"Ошибка: {str(e)}"

    def cd(self, args):
        if not args:
            return "Ошибка: отсутствует аргумент для cd."

        target_path = (self.current_path / args[0]).resolve()
        target_path_str = str(target_path).lstrip("/") + "/"

        if not any(entry.startswith(target_path_str) for entry in self.fs_archive.namelist()):
            return f"Ошибка: путь {args[0]} не найден."

        self.current_path = target_path
        return ""


    def uniq(self, args):
        if not args:
            return "Ошибка: отсутствует аргумент для uniq."

        file_path = str(self.current_path / args[0]).lstrip("/")
        if file_path not in self.fs_archive.namelist():
            return f"Ошибка: файл {args[0]} не найден."

        with self.fs_archive.open(file_path) as file:
            lines = file.read().decode("utf-8").splitlines()

        uniq_lines = sorted(set(lines))
        return "\n".join(uniq_lines)

    def run_command(self, command):
        parts = command.strip().split()
        if not parts:
            return ""

        cmd = parts[0]
        args = parts[1:]

        if cmd == "ls":
            return self.ls()
        elif cmd == "cd":
            return self.cd(args)
        elif cmd == "exit":
            exit(0)
        elif cmd == "uniq":
            return self.uniq(args)
        elif cmd == "whoami":
            return self.username
        else:
            return f"Команда {cmd} не найдена."


class ShellGUI:
    def __init__(self, emulator):
        self.emulator = emulator
        self.window = tk.Tk()
        self.window.title("Shell Emulator")
        self.output = tk.Text(self.window, wrap=tk.WORD, state=tk.DISABLED, height=20, width=80)
        self.output.pack(padx=10, pady=10)
        self.input_field = tk.Entry(self.window, width=80)
        self.input_field.pack(padx=10, pady=10)
        self.input_field.bind("<Return>", self.execute_command)

    def execute_command(self, event):
        command = self.input_field.get()
        if command:
            prompt = f"{self.emulator.username}@{self.emulator.hostname}:{self.emulator.current_path}$ {command}\n"
            result = self.emulator.run_command(command)
            self.append_output(prompt + (result or "") + "\n")
            self.input_field.delete(0, tk.END)

    def append_output(self, text):
        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, text)
        self.output.config(state=tk.DISABLED)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    config_file = filedialog.askopenfilename(title="Выберите конфигурационный файл", filetypes=[("YAML files", "*.yaml")])
    if not config_file:
        messagebox.showerror("Ошибка", "Конфигурационный файл не выбран.")
        exit(1)

    try:
        emulator = ShellEmulator(config_file)
        gui = ShellGUI(emulator)
        gui.run()
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))
