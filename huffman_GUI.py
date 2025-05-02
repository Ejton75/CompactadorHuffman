import tkinter as tk
from tkinter import filedialog, messagebox
from huffman import HuffmanCompressor

class HuffmanGUI:
    def __init__(self, root):
        self.root = root
        self.compressor = HuffmanCompressor()
        self.setup_ui()
    
    def setup_ui(self):
        self.root.title("Compactador Huffman")
        
        # Frame principal
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack()
        
        # Botões
        tk.Button(frame, text="Compactar Arquivo", 
                 command=self.compress_file).grid(row=0, column=0, pady=5)
        tk.Button(frame, text="Descompactar Arquivo",
                 command=self.decompress_file).grid(row=1, column=0, pady=5)
        
        # Status
        self.status = tk.StringVar()
        self.status.set("Pronto")
        tk.Label(frame, textvariable=self.status).grid(row=2, column=0)
    
    def compress_file(self):
        input_path = filedialog.askopenfilename(title="Selecione o arquivo para compactar")
        if not input_path:
            return
        
        self.status.set("Compactando...")
        self.root.update()
        
        try:
            output_path = self.compressor.compress(input_path)
            messagebox.showinfo("Sucesso", f"Arquivo compactado:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            self.status.set("Pronto")
    
    def decompress_file(self):
        input_path = filedialog.askopenfilename(title="Selecione o arquivo para descompactar")
        if not input_path:
            return
        
        self.status.set("Descompactando...")
        self.root.update()
        
        try:
            output_path = self.compressor.decompress(input_path)
            messagebox.showinfo("Sucesso", f"Arquivo descompactado:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            self.status.set("Pronto")

if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanGUI(root)
    root.mainloop()