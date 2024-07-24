# gui.py

import tkinter as tk
from tkinter import filedialog, messagebox
import file_operations as fo
import os
import string

class FileManagerApp:
    def __init__(self, root):
        self.root = root
        root.title("Simple File Manager")
        root.geometry("800x600")  # Kezdő méret beállítása

        # Háttérszín beállítása
        root.configure(bg="#2E2E2E")

        # Üdvözlő képernyő megjelenítése
        self.show_welcome_screen()

    def show_welcome_screen(self):
        """Üdvözlő képernyő megjelenítése."""
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Welcome")
        welcome_window.geometry("400x300")
        welcome_window.configure(bg="#2E2E2E")

        tk.Label(welcome_window, text="Welcome to Simple File Manager", font=("Arial", 16, "bold"), bg="#2E2E2E", fg="#FFFFFF").pack(pady=20)
        tk.Label(welcome_window, text="This application allows you to manage your files and directories easily.", wraplength=300, bg="#2E2E2E", fg="#DDDDDD").pack(pady=10)
        tk.Label(welcome_window, text="Framework by FK-Development", bg="#2E2E2E", fg="#AAAAAA").pack(pady=5)

        tk.Button(welcome_window, text="Continue", command=self.close_welcome_screen, bg="#4B4B4B", fg="#FFFFFF").pack(pady=20)

        # Az üdvözlő képernyő lezárása
        self.welcome_window = welcome_window

    def close_welcome_screen(self):
        """Az üdvözlő képernyő bezárása és a fő alkalmazás megjelenítése."""
        self.welcome_window.destroy()
        self.setup_main_ui()

    def setup_main_ui(self):
        """A fő alkalmazás felületének beállítása."""
        # Fő keret
        self.main_frame = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg="#2E2E2E")
        self.main_frame.pack(expand=1, fill=tk.BOTH)

        # Oldalsó menü keret
        self.sidebar = tk.Frame(self.main_frame, width=200, bg="#1F1F1F")
        self.sidebar.pack_propagate(False)
        self.main_frame.add(self.sidebar, stretch="never")

        # Fájl- és mappaböngésző keret
        self.file_frame = tk.Frame(self.main_frame, bg="#2E2E2E")
        self.file_frame.pack(expand=1, fill=tk.BOTH)
        self.main_frame.add(self.file_frame, stretch="always")

        # Menü
        self.menu = tk.Menu(self.root, bg="#2E2E2E", fg="#FFFFFF")
        self.root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, bg="#2E2E2E", fg="#FFFFFF")
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Create File", command=self.create_file)
        self.file_menu.add_command(label="Create Directory", command=self.create_directory)
        self.file_menu.add_command(label="Delete File", command=self.delete_file)
        self.file_menu.add_command(label="Delete Directory", command=self.delete_directory)
        self.file_menu.add_command(label="Rename", command=self.rename_file)
        self.file_menu.add_command(label="Copy", command=self.copy_file)
        self.file_menu.add_command(label="Search", command=self.search_text)
        self.file_menu.add_command(label="Preview", command=self.preview_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # Oldalsó menü tartalom
        self.create_sidebar()

        # Fájl- és mappaböngésző nézet
        self.file_listbox = tk.Listbox(self.file_frame, selectmode=tk.SINGLE, bg="#1F1F1F", fg="#FFFFFF", highlightbackground="#3C3C3C", highlightcolor="#3C3C3C")
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=5, pady=5)

        # Görgetősáv
        self.scrollbar = tk.Scrollbar(self.file_frame, orient=tk.VERTICAL, command=self.file_listbox.yview, bg="#2E2E2E", troughcolor="#1F1F1F")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=self.scrollbar.set)

        self.current_directory = os.path.expanduser("~")  # Kezdőkönyvtár a felhasználói könyvtár
        self.update_file_list()

        self.file_listbox.bind('<Double-1>', self.on_file_select)

    def create_sidebar(self):
        """Létrehozza az oldalsó menüt."""
        tk.Label(self.sidebar, text="Quick Access", bg="#1F1F1F", fg="#FFFFFF", font=("Arial", 12, "bold")).pack(pady=10)

        self.sidebar_buttons = {
            "Home": os.path.expanduser("~"),
            "Desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
            "Documents": os.path.join(os.path.expanduser("~"), "Documents"),
            "Downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
            "This PC": None,  # Hely a lemezek számára
        }

        for name, path in self.sidebar_buttons.items():
            button = tk.Button(self.sidebar, text=name, command=lambda p=path: self.change_directory(p), bg="#3C3C3C", fg="#FFFFFF", relief=tk.FLAT)
            button.pack(fill=tk.X, padx=10, pady=5)

        # Hozzáadjuk a lemezeket
        self.add_drives()

    def add_drives(self):
        """Lemezek hozzáadása a 'This PC' alá."""
        if os.name == 'nt':  # Windows rendszeren
            drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
            for drive in drives:
                button = tk.Button(self.sidebar, text=drive, command=lambda d=drive: self.change_directory(d), bg="#3C3C3C", fg="#FFFFFF", relief=tk.FLAT)
                button.pack(fill=tk.X, padx=10, pady=5)
        else:
            messagebox.showinfo("Info", "Drive listing is only supported on Windows.")

    def change_directory(self, path):
        """Navigál a megadott könyvtárba."""
        if os.path.isdir(path):
            self.current_directory = path
            self.update_file_list()

    def update_file_list(self):
        """Frissíti a fájlok és könyvtárak listáját."""
        self.file_listbox.delete(0, tk.END)
        try:
            items = fo.list_files_and_dirs(self.current_directory)
            for item in items:
                self.file_listbox.insert(tk.END, item)
        except Exception as e:
            messagebox.showerror("Hiba", str(e))

    def on_file_select(self, event):
        """Kiválasztott fájl vagy könyvtár kezelése."""
        selection = self.file_listbox.curselection()
        if not selection:
            return

        selected_item = self.file_listbox.get(selection[0])
        full_path = os.path.join(self.current_directory, selected_item)

        if os.path.isdir(full_path):
            self.current_directory = full_path
            self.update_file_list()
        else:
            self.open_file(full_path)

    def open_file(self, filepath=None):
        if not filepath:
            filepath = filedialog.askopenfilename()
        if filepath:
            try:
                with open(filepath, 'r') as file:
                    content = file.read()
                self.show_file_content(content, filepath)
            except Exception as e:
                messagebox.showerror("Hiba", str(e))

    def show_file_content(self, content, filepath):
        preview_window = tk.Toplevel(self.root)
        preview_window.title("File Preview")
        preview_window.configure(bg="#2E2E2E")

        tk.Label(preview_window, text=filepath, font=("Arial", 12, "bold"), bg="#2E2E2E", fg="#FFFFFF").pack(pady=5)
        text_area = tk.Text(preview_window, wrap=tk.WORD, bg="#1F1F1F", fg="#FFFFFF", highlightbackground="#3C3C3C", highlightcolor="#3C3C3C")
        text_area.pack(expand=1, fill=tk.BOTH)
        text_area.insert(tk.END, content)
        text_area.config(state=tk.DISABLED)

    def save_file(self):
        if self.current_file:
            with open(self.current_file, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END))
        else:
            filepath = filedialog.asksaveasfilename()
            if filepath:
                with open(filepath, 'w') as file:
                    file.write(self.text_area.get(1.0, tk.END))
                self.current_file = filepath

    def create_file(self):
        filepath = filedialog.asksaveasfilename()
        if filepath:
            try:
                fo.create_file(filepath)
                messagebox.showinfo("Siker", f"{filepath} létrehozva")
                self.update_file_list()
            except Exception as e:
                messagebox.showerror("Hiba", str(e))

    def delete_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            try:
                fo.delete_file(filepath)
                messagebox.showinfo("Siker", f"{filepath} törölve")
                self.update_file_list()
            except Exception as e:
                messagebox.showerror("Hiba", str(e))

    def rename_file(self):
        old_filepath = filedialog.askopenfilename()
        if old_filepath:
            new_filepath = filedialog.asksaveasfilename()
            if new_filepath:
                try:
                    fo.rename_file(old_filepath, new_filepath)
                    messagebox.showinfo("Siker", f"{old_filepath} átnevezve {new_filepath}-re")
                    self.update_file_list()
                except Exception as e:
                    messagebox.showerror("Hiba", str(e))

    def copy_file(self):
        source = filedialog.askopenfilename()
        if source:
            destination = filedialog.asksaveasfilename()
            if destination:
                try:
                    fo.copy_file(source, destination)
                    messagebox.showinfo("Siker", f"{source} másolva {destination}-re")
                    self.update_file_list()
                except Exception as e:
                    messagebox.showerror("Hiba", str(e))

    def search_text(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search")
        search_window.configure(bg="#2E2E2E")

        tk.Label(search_window, text="Search:", bg="#2E2E2E", fg="#FFFFFF").pack(side=tk.LEFT, padx=5)
        search_entry = tk.Entry(search_window, bg="#1F1F1F", fg="#FFFFFF")
        search_entry.pack(side=tk.LEFT, padx=5)

        def search():
            search_term = search_entry.get()
            if search_term:
                content = self.text_area.get(1.0, tk.END)
                start_idx = content.find(search_term)
                if start_idx != -1:
                    end_idx = start_idx + len(search_term)
                    self.text_area.tag_add('highlight', f"1.0 + {start_idx} chars", f"1.0 + {end_idx} chars")
                    self.text_area.tag_config('highlight', background='yellow')
                else:
                    messagebox.showinfo("Search", "Term not found")

        tk.Button(search_window, text="Search", command=search, bg="#4B4B4B", fg="#FFFFFF").pack(side=tk.LEFT, padx=5)

    def preview_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            try:
                with open(filepath, 'r') as file:
                    content = file.read()
                self.show_file_content(content, filepath)
            except Exception as e:
                messagebox.showerror("Hiba", str(e))

    def create_directory(self):
        directory_path = filedialog.askdirectory()
        if directory_path:
            try:
                fo.create_directory(directory_path)
                messagebox.showinfo("Siker", f"{directory_path} létrehozva")
                self.update_file_list()
            except Exception as e:
                messagebox.showerror("Hiba", str(e))

    def delete_directory(self):
        directory_path = filedialog.askdirectory()
        if directory_path:
            try:
                fo.delete_directory(directory_path)
                messagebox.showinfo("Siker", f"{directory_path} törölve")
                self.update_file_list()
            except Exception as e:
                messagebox.showerror("Hiba", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()
