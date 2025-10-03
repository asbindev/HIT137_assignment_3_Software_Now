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
