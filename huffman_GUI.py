import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import os
import math
from huffman import HuffmanCompressor
from huffman_lz77 import ImprovedHuffmanCompressor

class HuffmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compactador Huffman")
        self.root.geometry("800x600")
        
        self.file_path = None
        self.compressed_path = None
        self.huffman_compressor = HuffmanCompressor()
        self.improved_compressor = ImprovedHuffmanCompressor()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(main_frame, text="Compactador de Arquivos", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Frame de seleção de arquivo
        file_frame = tk.LabelFrame(main_frame, text="Seleção de Arquivo", padx=10, pady=10)
        file_frame.pack(fill=tk.X, pady=10)
        
        self.file_label = tk.Label(file_frame, text="Nenhum arquivo selecionado", wraplength=600)
        self.file_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_btn = tk.Button(file_frame, text="Selecionar Arquivo", command=self.select_file)
        browse_btn.pack(side=tk.RIGHT, padx=5)
        
        # Frame de opções de compactação
        compress_frame = tk.LabelFrame(main_frame, text="Opções de Compactação", padx=10, pady=10)
        compress_frame.pack(fill=tk.X, pady=10)
        
        huffman_btn = tk.Button(compress_frame, text="Compactar com Huffman", command=self.compress_huffman)
        huffman_btn.pack(side=tk.LEFT, padx=5)
        
        improved_btn = tk.Button(compress_frame, text="Compactar com Huffman+LZ77", command=self.compress_improved)
        improved_btn.pack(side=tk.LEFT, padx=5)
        
        decompress_btn = tk.Button(compress_frame, text="Descompactar", command=self.decompress)
        decompress_btn.pack(side=tk.LEFT, padx=5)
        
        # Frame de visualização
        view_frame = tk.LabelFrame(main_frame, text="Visualização", padx=10, pady=10)
        view_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.notebook = ttk.Notebook(view_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Aba de conteúdo do arquivo
        self.file_content_tab = tk.Frame(self.notebook)
        self.notebook.add(self.file_content_tab, text="Conteúdo do Arquivo")
        
        self.file_content_text = tk.Text(self.file_content_tab, wrap=tk.WORD)
        self.file_content_text.pack(fill=tk.BOTH, expand=True)
        
        # Aba de árvore de Huffman
        self.tree_tab = tk.Frame(self.notebook)
        self.notebook.add(self.tree_tab, text="Árvore de Huffman")
        
        self.tree_text = tk.Text(self.tree_tab, wrap=tk.WORD)
        self.tree_text.pack(fill=tk.BOTH, expand=True)
        
        # Aba de taxa de compactação
        self.ratio_tab = tk.Frame(self.notebook)
        self.notebook.add(self.ratio_tab, text="Taxa de Compactação")
        
        self.ratio_text = tk.Text(self.ratio_tab, wrap=tk.WORD)
        self.ratio_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto")
        status_bar = tk.Label(main_frame, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X)
    
    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if self.file_path:
            self.file_label.config(text=self.file_path)
            self.show_file_content()
            self.status_var.set(f"Arquivo selecionado: {os.path.basename(self.file_path)}")
    
    def show_file_content(self):
        if not self.file_path:
            return
            
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.file_content_text.delete(1.0, tk.END)
                self.file_content_text.insert(tk.END, content)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível ler o arquivo: {str(e)}")
    
    def compress_huffman(self):
        if not self.file_path:
            messagebox.showwarning("Aviso", "Selecione um arquivo primeiro")
            return
            
        try:
            self.compressed_path = self.huffman_compressor.compress(self.file_path)
            self.show_compression_ratio("Huffman")
            self.show_huffman_tree()
            messagebox.showinfo("Sucesso", f"Arquivo compactado com sucesso: {self.compressed_path}")
            self.status_var.set(f"Compactação Huffman concluída: {os.path.basename(self.compressed_path)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na compactação: {str(e)}")
            self.status_var.set("Erro na compactação")
    
    def compress_improved(self):
        if not self.file_path:
            messagebox.showwarning("Aviso", "Selecione um arquivo primeiro")
            return
            
        try:
            self.compressed_path = self.improved_compressor.compress(self.file_path)
            self.show_compression_ratio("Huffman + LZ77")
            self.show_huffman_tree()
            messagebox.showinfo("Sucesso", f"Arquivo compactado com sucesso: {self.compressed_path}")
            self.status_var.set(f"Compactação Huffman+LZ77 concluída: {os.path.basename(self.compressed_path)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na compactação: {str(e)}")
            self.status_var.set("Erro na compactação")
    
    def decompress(self):
        if not self.file_path:
            messagebox.showwarning("Aviso", "Selecione um arquivo compactado primeiro")
            return
            
        try:
            if self.file_path.endswith('.bin'):
                decompressed_path = self.huffman_compressor.decompress(self.file_path)
            elif self.file_path.endswith('.hzlz'):
                decompressed_path = self.improved_compressor.decompress(self.file_path)
            else:
                messagebox.showerror("Erro", "Tipo de arquivo compactado não reconhecido")
                return
                
            self.file_path = decompressed_path
            self.file_label.config(text=decompressed_path)
            self.show_file_content()
            messagebox.showinfo("Sucesso", f"Arquivo descompactado com sucesso: {decompressed_path}")
            self.status_var.set(f"Descompactação concluída: {os.path.basename(decompressed_path)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na descompactação: {str(e)}")
            self.status_var.set("Erro na descompactação")
    
    def show_huffman_tree(self):
        if hasattr(self.huffman_compressor, 'codes') and self.huffman_compressor.codes:
            self.tree_text.delete(1.0, tk.END)
            
            # Mostra os códigos de Huffman
            self.tree_text.insert(tk.END, "Códigos de Huffman:\n")
            for char, code in self.huffman_compressor.codes.items():
                display_char = char if ord(char) >= 32 and ord(char) <= 126 else f"ASCII {ord(char)}"
                self.tree_text.insert(tk.END, f"{display_char}: {code}\n")
            
            # Tenta mostrar a árvore (simplificada)
            self.tree_text.insert(tk.END, "\nEstrutura da Árvore (simplificada):\n")
            try:
                self.huffman_compressor.print_huffman_tree()
                # Nota: A implementação atual de print_huffman_tree imprime no console, não na GUI
                # Podemos melhorar isso no futuro
                self.tree_text.insert(tk.END, "Verifique o console para a visualização da árvore.")
            except Exception as e:
                self.tree_text.insert(tk.END, f"Não foi possível exibir a árvore: {str(e)}")
        else:
            self.tree_text.delete(1.0, tk.END)
            self.tree_text.insert(tk.END, "Execute a compactação primeiro para gerar a árvore.")
    
    def show_compression_ratio(self, method):
        if not self.file_path or not self.compressed_path:
            return
            
        original_size = os.path.getsize(self.file_path)
        compressed_size = os.path.getsize(self.compressed_path)
        ratio = (1 - (compressed_size / original_size)) * 100
        
        self.ratio_text.delete(1.0, tk.END)
        self.ratio_text.insert(tk.END, f"Método de compactação: {method}\n\n")
        self.ratio_text.insert(tk.END, f"Tamanho original: {original_size} bytes\n")
        self.ratio_text.insert(tk.END, f"Tamanho compactado: {compressed_size} bytes\n")
        self.ratio_text.insert(tk.END, f"Taxa de compactação: {ratio:.2f}%\n\n")
        
        # Explicação da taxa de compactação
        self.ratio_text.insert(tk.END, "Explicação:\n")
        self.ratio_text.insert(tk.END, "A taxa de compactação mostra quanto o arquivo foi reduzido em relação ao original.\n")
        self.ratio_text.insert(tk.END, "Quanto maior a porcentagem, melhor a compactação.\n")
        self.ratio_text.insert(tk.END, f"O método {method} conseguiu reduzir o arquivo em {ratio:.2f}%.\n")
        
        if method == "Huffman + LZ77":
            self.ratio_text.insert(tk.END, "\nA combinação de LZ77 com Huffman geralmente oferece melhores resultados,\n")
            self.ratio_text.insert(tk.END, "pois o LZ77 explora repetições no texto antes da codificação de Huffman.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanGUI(root)
    root.mainloop()