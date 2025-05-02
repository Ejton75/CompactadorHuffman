import heapq
from collections import defaultdict, deque

class LZ77Compressor:
    """Implementação do algoritmo LZ77 para pré-compressão"""
    
    def __init__(self, window_size=20, lookahead_buffer=15):
        self.window_size = window_size
        self.lookahead_buffer = lookahead_buffer
    
    def compress(self, text):
        output = []
        i = 0
        window = deque(maxlen=self.window_size)
        
        while i < len(text):
            match = self._find_longest_match(window, text[i:i+self.lookahead_buffer])
            if match:
                offset, length = match
                output.append((offset, length, text[i+length]))
                window.extend(text[i:i+length+1])
                i += length + 1
            else:
                output.append((0, 0, text[i]))
                window.append(text[i])
                i += 1
        return output
    
    def _find_longest_match(self, window, lookahead):
        best_offset, best_length = 0, 0
        buffer = ''.join(window)
        
        for length in range(1, len(lookahead)+1):
            substring = lookahead[:length]
            offset = buffer.rfind(substring)
            
            if offset != -1 and length > best_length:
                best_offset = len(buffer) - offset
                best_length = length
        
        return (best_offset, best_length) if best_length > 0 else None

class ImprovedHuffmanCompressor(HuffmanCompressor):
    """Combina LZ77 com Huffman para melhor compressão"""
    
    def __init__(self):
        super().__init__()
        self.lz77 = LZ77Compressor()
    
    def compress(self, input_path):
        # Primeiro aplica LZ77
        with open(input_path, 'r') as f:
            text = f.read()
        
        lz77_compressed = self.lz77.compress(text)
        serialized = str(lz77_compressed).encode('utf-8')
        
        # Depois aplica Huffman
        frequency = self._make_frequency_dict(serialized)
        huffman_tree = self._build_huffman_tree(frequency)
        self.codes = self._make_codes(huffman_tree)
        encoded_text = self._get_encoded_text(serialized)
        
        # Salva os dados
        output_path = input_path + '.hzlz'
        with open(output_path, 'wb') as f:
            pickle.dump({
                'frequency': frequency,
                'encoded_data': self._pad_encoded_text(encoded_text)
            }, f)
        
        return output_path