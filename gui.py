import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading

class AppGUI:
    def __init__(self, model_manager, oop_demo):
        self.model_manager = model_manager
        self.oop_demo = oop_demo

        self.root = tk.Tk()
        self.root.title('HIT137 - Assignment 3 (Group)')
        self.root.geometry('900x700')
        self.create_widgets()


    def create_widgets(self):
        # Top frame: Input selection
        top = ttk.Frame(self.root, padding=10)
        top.pack(fill='x')

        ttk.Label(top, text='Select Input Type:').grid(row=0, column=0, sticky='w')
        self.input_type = tk.StringVar(value='text')
        ttk.Combobox(top, textvariable=self.input_type, values=['text', 'image'], state='readonly').grid(row=0, column=1, sticky='w')

        ttk.Label(top, text='Enter Text / Choose Image:').grid(row=1, column=0, sticky='w', pady=(8,0))
        self.input_text = tk.Text(top, height=4, width=60)
        self.input_text.grid(row=2, column=0, columnspan=3, sticky='w')

        self.choose_img_btn = ttk.Button(top, text='Select Image...', command=self.select_image)
        self.choose_img_btn.grid(row=1, column=1, sticky='w', padx=(6,0))

        # Model selection
        ttk.Label(top, text='Select Model:').grid(row=3, column=0, sticky='w', pady=(12,0))
        self.model_var = tk.StringVar(value='text-generation')
        ttk.Combobox(top, textvariable=self.model_var, values=['text-generation (gpt2)', 'image-classification (google/vit-base-patch16-224)'], state='readonly').grid(row=3, column=1, sticky='w')

        # Run button
        self.run_btn = ttk.Button(top, text='Run Model', command=self.run_model_thread)
        self.run_btn.grid(row=3, column=2, sticky='e', padx=(10,0))

        # Output frame
        out_frame = ttk.LabelFrame(self.root, text='Model Output', padding=10)
        out_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.output_text = tk.Text(out_frame, height=12)
        self.output_text.pack(fill='both', expand=True)

        # Right frame: image preview + OOP explanation + model info
        right_frame = ttk.Frame(self.root, padding=10)
        right_frame.pack(fill='x')

        # Image preview
        self.preview_label = ttk.Label(right_frame, text='No image selected', anchor='center')
        self.preview_label.pack(fill='both')

        # Tabs for OOP and Model Info
        tabs = ttk.Notebook(self.root)
        tabs.pack(fill='both', expand=True, padx=10, pady=10)

        self.oop_tab = ttk.Frame(tabs)
        self.model_info_tab = ttk.Frame(tabs)

        tabs.add(self.oop_tab, text='OOP Explanation')
        tabs.add(self.model_info_tab, text='Model Info')

        self.oop_text = tk.Text(self.oop_tab, wrap='word')
        self.oop_text.pack(fill='both', expand=True)
        self.oop_text.insert('1.0', self.oop_demo.explain_all())

        self.model_info_text = tk.Text(self.model_info_tab, wrap='word')
        self.model_info_text.pack(fill='both', expand=True)
        self.model_info_text.insert('1.0', self.model_manager.get_models_info())

       #selecting image for image classification

    def select_image(self):
        try:
            filepath = filedialog.askopenfilename(filetypes=[('Image files', '*.png;*.jpg;*.jpeg;*.bmp;*.gif')])
            if not filepath:
                return
            img = Image.open(filepath)
            img.thumbnail((300,300))
            self._last_image = img.copy()
            img_tk = ImageTk.PhotoImage(img)
            self.preview_label.configure(image=img_tk, text='')
            self.preview_label.image = img_tk
        except Exception as e:
            messagebox.showerror('Image Error', f'Could not open image: {e}')

    def run_model_thread(self):
        t = threading.Thread(target=self.run_model)
        t.daemon = True
        t.start()

    def run_model(self):
        self.run_btn.config(state='disabled')
        self.output_text.delete('1.0', 'end')
        input_type = self.input_type.get()
        selected_model = self.model_var.get()

        try:
            if input_type == 'text':
                text = self.input_text.get('1.0', 'end').strip()
                if not text:
                    raise ValueError('Text input is empty. Please provide valid input.')
                if 'text-generation' in selected_model:
                    out = self.model_manager.generate_text(text)
                    if not isinstance(out, str):
                        raise TypeError('Model did not return valid text output.')
                    self.output_text.insert('end', out)
                else:
                    raise ValueError('Selected model is not compatible with text input.')

            elif input_type == 'image':
                if not hasattr(self, '_last_image') or self._last_image is None:
                    raise ValueError('No image selected. Please select an image file first.')
                if 'image-classification' in selected_model:
                    out = self.model_manager.classify_image(self._last_image)
                    if not isinstance(out, str):
                        raise TypeError('Model did not return valid classification output.')
                    self.output_text.insert('end', out)
                else:
                    raise ValueError('Selected model is not compatible with image input.')


            else:
                raise ValueError('Unsupported input type selected.')

        except ValueError as ve:
            messagebox.showwarning('Validation Error', str(ve))
            self.output_text.insert('end', f'Validation Error: {ve}')
        except TypeError as te:
            messagebox.showerror('Type Error', str(te))
            self.output_text.insert('end', f'Type Error: {te}')
        except Exception as e:
            messagebox.showerror('Runtime Error', str(e))
            self.output_text.insert('end', f'Unexpected Error: {e}')
        finally:
            self.run_btn.config(state='normal')

    def run(self):
        self.root.mainloop()
