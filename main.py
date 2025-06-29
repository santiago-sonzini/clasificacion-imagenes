import os
import shutil
import re
from tkinter import Tk, Label, Button, Entry, StringVar, filedialog, messagebox, Frame, font
from tkinter import ttk
from PIL import Image, ImageTk

class ImageRenamer:
    def __init__(self):
        self.setup_folders()
        self.setup_images()
        self.setup_gui()
        self.current_index = 0
        self.history = []
        
    def setup_folders(self):
        self.INPUT_FOLDER = filedialog.askdirectory(title="Selecciona la carpeta de imágenes")
        if not self.INPUT_FOLDER:
            exit()
            
        self.OUTPUT_FOLDER = "salida"
        self.RENAMED_FOLDER = os.path.join(self.OUTPUT_FOLDER, "renombradas")
        self.DISCARDED_FOLDER = os.path.join(self.OUTPUT_FOLDER, "descartadas")
        self.PENDING_FOLDER = os.path.join(self.OUTPUT_FOLDER, "pendientes")
        
        os.makedirs(self.RENAMED_FOLDER, exist_ok=True)
        os.makedirs(self.DISCARDED_FOLDER, exist_ok=True)
        os.makedirs(self.PENDING_FOLDER, exist_ok=True)
    
    def natural_sort_key(self, filename):
        """Sort filenames naturally (0, 1, 2, 10, 11 instead of 0, 1, 10, 11, 2)"""
        return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', filename)]
    
    def setup_images(self):
        valid_exts = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff']
        all_files = [f for f in os.listdir(self.INPUT_FOLDER) 
                    if os.path.splitext(f)[1].lower() in valid_exts]
        
        # Sort using natural sorting to handle numeric names properly
        self.image_files = sorted(all_files, key=self.natural_sort_key)
        
        if not self.image_files:
            messagebox.showerror("Error", "No se encontraron imágenes en la carpeta seleccionada.")
            exit()
    
    def setup_gui(self):
        self.root = Tk()
        self.root.title("🖼️ Renombrador de Imágenes")
        self.root.geometry("800x900")
        self.root.configure(bg='#f0f0f0')
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container
        main_frame = Frame(self.root, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Header
        header_frame = Frame(main_frame, bg='#f0f0f0')
        header_frame.pack(fill='x', pady=(0, 20))
        
        title_font = font.Font(family="Arial", size=16, weight="bold")
        title_label = Label(header_frame, text="🖼️ Renombrador de Imágenes", 
                           font=title_font, bg='#f0f0f0', fg='#333')
        title_label.pack()
        
        # Counter
        self.counter_label = Label(header_frame, text="", font=("Arial", 12), 
                                  bg='#f0f0f0', fg='#666')
        self.counter_label.pack(pady=(5, 0))
        
        # Image display
        image_frame = Frame(main_frame, bg='white', relief='raised', bd=2)
        image_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        self.img_label = Label(image_frame, bg='white', text="Cargando imagen...", 
                              font=("Arial", 14), fg='#999')
        self.img_label.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Controls frame
        controls_frame = Frame(main_frame, bg='#f0f0f0')
        controls_frame.pack(fill='x')
        
        # Name input
        name_frame = Frame(controls_frame, bg='#f0f0f0')
        name_frame.pack(fill='x', pady=(0, 15))
        
        Label(name_frame, text="Nuevo nombre:", font=("Arial", 11, "bold"), 
              bg='#f0f0f0', fg='#333').pack(anchor='w')
        
        self.name_var = StringVar()
        self.name_entry = Entry(name_frame, textvariable=self.name_var, 
                               font=("Arial", 12), width=50, relief='flat', bd=5)
        self.name_entry.pack(fill='x', pady=(5, 0), ipady=8)
        
        # Buttons frame
        buttons_frame = Frame(controls_frame, bg='#f0f0f0')
        buttons_frame.pack(fill='x', pady=(0, 15))
        
        # Main action buttons
        btn_frame1 = Frame(buttons_frame, bg='#f0f0f0')
        btn_frame1.pack(fill='x', pady=(0, 10))
        
        self.create_button(btn_frame1, "✅ Renombrar", self.rename_image, '#4CAF50', 'white', 0)
        self.create_button(btn_frame1, "🗑️ Descartar", self.discard_image, '#F44336', 'white', 1)
        self.create_button(btn_frame1, "⏳ Para después", self.leave_for_later, '#FF9800', 'white', 2)
        
        # Navigation buttons
        btn_frame2 = Frame(buttons_frame, bg='#f0f0f0')
        btn_frame2.pack(fill='x')
        
        self.create_button(btn_frame2, "← Volver", self.go_back, '#2196F3', 'white', 0)
        
        # Go to image frame
        goto_frame = Frame(btn_frame2, bg='#f0f0f0')
        goto_frame.grid(row=0, column=1, padx=10, sticky='ew')
        
        self.go_to_var = StringVar()
        self.go_to_entry = Entry(goto_frame, textvariable=self.go_to_var, 
                                font=("Arial", 10), width=8, justify='center')
        self.go_to_entry.pack(side='left', padx=(0, 5))
        
        goto_btn = Button(goto_frame, text="Ir a #", command=self.go_to_image,
                         bg='#9C27B0', fg='white', font=("Arial", 10, "bold"),
                         relief='flat', padx=15, pady=5)
        goto_btn.pack(side='left')
        
        btn_frame2.columnconfigure(1, weight=1)
        
        # Keyboard shortcuts info
        info_frame = Frame(controls_frame, bg='#f0f0f0')
        info_frame.pack(fill='x', pady=(10, 0))
        
        shortcuts_text = "Atajos: Enter=Renombrar • ←→=Navegar • Cmd+D=Descartar"
        Label(info_frame, text=shortcuts_text, font=("Arial", 9), 
              bg='#f0f0f0', fg='#666').pack()
        
        # Bind keyboard shortcuts
        self.root.bind("<Return>", lambda e: self.rename_image())
        self.root.bind("<Left>", lambda e: self.go_back())
        self.root.bind("<Right>", lambda e: self.rename_image())
        self.root.bind("<Command-d>", lambda e: self.discard_image())  # macOS
        self.root.bind("<Control-d>", lambda e: self.discard_image())  # Windows/Linux
        
        # Focus on name entry
        self.name_entry.focus_set()
    
    def create_button(self, parent, text, command, bg_color, fg_color, column):
        btn = Button(parent, text=text, command=command,
                    bg=bg_color, fg=fg_color, font=("Arial", 11, "bold"),
                    relief='flat', padx=20, pady=10, cursor='hand2')
        btn.grid(row=0, column=column, padx=5, sticky='ew')
        parent.columnconfigure(column, weight=1)
        return btn
    
    def load_image(self, index):
        if 0 <= index < len(self.image_files):
            img_path = os.path.join(self.INPUT_FOLDER, self.image_files[index])
            
            try:
                img = Image.open(img_path)
                
                # Handle transparency
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    if img.mode == 'RGBA':
                        background.paste(img, mask=img.split()[-1])
                    else:
                        background.paste(img, mask=img.split()[-1])
                    img = background
                else:
                    img = img.convert("RGB")
                
                # Resize maintaining aspect ratio
                img.thumbnail((700, 500), Image.Resampling.LANCZOS)
                tk_img = ImageTk.PhotoImage(img)
                
                self.img_label.config(image=tk_img, text="")
                self.img_label.image = tk_img
                
                # Update counter with current filename
                current_file = self.image_files[index]
                self.counter_label.config(
                    text=f"Imagen {index + 1} de {len(self.image_files)} • {current_file}"
                )
                self.name_var.set("")
                
            except Exception as e:
                self.img_label.config(image='', text=f"Error al cargar imagen:\n{str(e)}")
                self.counter_label.config(text=f"Error en imagen {index + 1}")
    
    def move_and_next(self, target_folder, new_name=None):
        if self.current_index >= len(self.image_files):
            return
        
        filename = self.image_files[self.current_index]
        src = os.path.join(self.INPUT_FOLDER, filename)
        
        if new_name:
            new_filename = new_name + os.path.splitext(filename)[1]
            dst = os.path.join(target_folder, new_filename)
            
            if os.path.exists(dst):
                confirm = messagebox.askyesno(
                    "Confirmación", 
                    f"El nombre '{new_name}' ya existe. ¿Deseas sobrescribirlo?"
                )
                if not confirm:
                    return
        else:
            dst = os.path.join(target_folder, filename)
        
        try:
            shutil.copy2(src, dst)
            self.history.append((self.current_index, filename))
            self.current_index += 1
            self.show_current()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mover el archivo:\n{str(e)}")
    
    def rename_image(self):
        name = self.name_var.get().strip()
        if name:
            self.move_and_next(self.RENAMED_FOLDER, new_name=name)
        else:
            messagebox.showwarning("Advertencia", "Por favor ingresa un nombre para la imagen.")
    
    def discard_image(self):
        self.move_and_next(self.DISCARDED_FOLDER)
    
    def leave_for_later(self):
        self.move_and_next(self.PENDING_FOLDER)
    
    def go_back(self):
        if self.history:
            last_index, last_file = self.history.pop()
            self.current_index = last_index
            self.show_current()
        else:
            messagebox.showinfo("Información", "No hay más imágenes anteriores.")
    
    def show_current(self):
        if self.current_index < len(self.image_files):
            self.load_image(self.current_index)
            self.name_entry.focus_set()
        else:
            self.img_label.config(image='', text="🎉 ¡Has terminado todas las imágenes!\n\nRevisa las carpetas de salida.")
            self.counter_label.config(text="Procesamiento completado")
            self.name_entry.config(state='disabled')
    
    def go_to_image(self):
        try:
            index = int(self.go_to_var.get()) - 1
            if 0 <= index < len(self.image_files):
                self.current_index = index
                self.show_current()
                self.go_to_var.set("")
            else:
                messagebox.showerror("Error", f"Número fuera de rango (1-{len(self.image_files)}).")
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un número válido.")
    
    def run(self):
        self.show_current()
        self.root.mainloop()

if __name__ == "__main__":
    app = ImageRenamer()
    app.run()