import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, simpledialog

def convert_rgb_to_cmyk(r, g, b):
    r, g, b = [x / 255.0 for x in (r, g, b)]
    k = min(1.0 - x for x in (r, g, b))
    if k == 1.0:
        return 0, 0, 0, 100
    c = (1 - r - k) / (1 - k)
    m = (1 - g - k) / (1 - k)
    y = (1 - b - k) / (1 - k)
    return round(c * 100), round(m * 100), round(y * 100), round(k * 100)

class CustomCopyDialog(simpledialog.Dialog):
    def body(self, master):
        self.choice = tk.StringVar()
        tk.Radiobutton(master, text="HEX", variable=self.choice, value="HEX").grid(row=0, sticky=tk.W)
        tk.Radiobutton(master, text="RGB", variable=self.choice, value="RGB").grid(row=1, sticky=tk.W)
        tk.Radiobutton(master, text="CMYK", variable=self.choice, value="CMYK").grid(row=2, sticky=tk.W)
        return None  # No initial focus

    def apply(self):
        self.result = self.choice.get()

class ColorCodeConverterGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Color Code Converter")
        self.geometry("550x400")
        self.last_selected_color = None
        self.initialize_components()

    def initialize_components(self):
        titleLabel = tk.Label(self, text="Color Code Converter")
        titleLabel.place(x=200, y=10)

        colorPickerButton = tk.Button(self, text="Choose Color", command=self.choose_color)
        colorPickerButton.place(x=20, y=50)

        self.outputTextArea = tk.Text(self, height=10, width=60)
        self.outputTextArea.place(x=20, y=90)

        clearButton = tk.Button(self, text="Clear", command=lambda: self.outputTextArea.delete(1.0, tk.END))
        clearButton.place(x=20, y=250)

        copyButton = tk.Button(self, text="Copy", command=self.copy_to_clipboard)
        copyButton.place(x=110, y=250)

        loadButton = tk.Button(self, text="Load", command=self.load_color_code)
        loadButton.place(x=200, y=250)

        saveButton = tk.Button(self, text="Save", command=self.save_color_code)
        saveButton.place(x=290, y=250)

        exitButton = tk.Button(self, text="Exit", command=self.quit)
        exitButton.place(x=380, y=250)

    def choose_color(self):
        color = colorchooser.askcolor(title="Pick a Color")[0]
        if color:
            self.last_selected_color = color
            self.update_color_output(color)

    def update_color_output(self, color):
        r, g, b = (int(x) for x in color)
        hex_code = f"#{r:02x}{g:02x}{b:02x}".upper()
        rgb = f"RGB({r}, {g}, {b})"
        cmyk = "CMYK({}%, {}%, {}%, {}%)".format(*convert_rgb_to_cmyk(r, g, b))
        self.outputTextArea.delete(1.0, tk.END)
        self.outputTextArea.insert(tk.END, f"HEX: {hex_code}\n{rgb}\n{cmyk}")

    def copy_to_clipboard(self):
        if self.last_selected_color:
            dialog = CustomCopyDialog(self)
            choice = dialog.result

            r, g, b = (int(x) for x in self.last_selected_color)
            text_to_copy = ""
            if choice == "HEX":
                text_to_copy = f"#{r:02x}{g:02x}{b:02x}".upper()
            elif choice == "RGB":
                text_to_copy = f"RGB({r}, {g}, {b})"
            elif choice == "CMYK":
                text_to_copy = "CMYK({}%, {}%, {}%, {}%)".format(*convert_rgb_to_cmyk(r, g, b))

            if text_to_copy:
                self.clipboard_clear()
                self.clipboard_append(text_to_copy)
                messagebox.showinfo("Copied", f"{choice} code copied to clipboard.")

    def load_color_code(self):
        file_path = filedialog.askopenfilename(title="Load Color Code", filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    self.outputTextArea.delete(1.0, tk.END)
                    self.outputTextArea.insert(tk.END, file.read())
            except Exception as e:
                messagebox.showerror("Load Error", f"Error loading the color code: {e}")

    def save_color_code(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(self.outputTextArea.get(1.0, tk.END))
            except Exception as e:
                messagebox.showerror("Save Error", f"Error saving the color code: {e}")

if __name__ == "__main__":
    app = ColorCodeConverterGUI()
    app.mainloop()
