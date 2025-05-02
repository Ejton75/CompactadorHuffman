import os
import heapq
import pickle
from collections import defaultdict
from math import ceil

class HuffmanCompressor:
    def __init__(self):
        self.codes = {}
        self.reverse_mapping = {}
    
    def _make_frequency_dict(self, text):
        frequency = defaultdict(int)
        for character in text:
            frequency[character] += 1
        return frequency    

    def _build_huffman_tree(self, frequency):
        heap = [[weight, [char, ""]] for char, weight in frequency.items()]
        heapq.heapify(heap)
        
        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
        
        return heap[0]        

    def _make_codes(self, huffman_tree):
        codes = {}
        for pair in huffman_tree[1:]:
            char, code = pair
            codes[char] = code
        return codes

    def _get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    def _pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        encoded_text += '0' * extra_padding
        padded_info = "{0:08b}".format(extra_padding)
        return padded_info + encoded_text

    def _get_byte_array(self, padded_encoded_text):
        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b

    def compress(self, input_path):
        filename, file_extension = os.path.splitext(input_path)
        output_path = filename + ".bin"

        with open(input_path, 'r+') as file, open(output_path, 'wb') as output:
            text = file.read()
            text = text.rstrip()

            frequency = self._make_frequency_dict(text)
            huffman_tree = self._build_huffman_tree(frequency)
            self.codes = self._make_codes(huffman_tree)
            encoded_text = self._get_encoded_text(text)
            padded_encoded_text = self._pad_encoded_text(encoded_text)
            byte_array = self._get_byte_array(padded_encoded_text)

            # Salva os dados necessários para descompactação
            output.write(pickle.dumps((frequency, byte_array)))
        
        print(f"Arquivo compactado salvo como: {output_path}")
        return output_path

    def _remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)
        padded_encoded_text = padded_encoded_text[8:] 
        encoded_text = padded_encoded_text[:-1*extra_padding]
        return encoded_text

    def _decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text

    def decompress(self, input_path):
        filename, file_extension = os.path.splitext(input_path)
        output_path = filename + "_decompressed.txt"

        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            frequency, byte_array = pickle.loads(file.read())

            # Reconstrói a árvore
            huffman_tree = self._build_huffman_tree(frequency)
            self.codes = self._make_codes(huffman_tree)
            self.reverse_mapping = {v: k for k, v in self.codes.items()}

            # Reconverte bytes para bits
            bit_string = ""
            for byte in byte_array:
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits

            encoded_text = self._remove_padding(bit_string)
            decompressed_text = self._decode_text(encoded_text)
            
            output.write(decompressed_text)
        
        print(f"Arquivo descompactado salvo como: {output_path}")
        return output_path

    def print_huffman_tree(self, node=None, prefix="", is_left=True):
        if node is None:
            node = self._build_huffman_tree(self._make_frequency_dict(""))
        
        if isinstance(node[0], int):
            print(f"{'│   ' * (len(prefix)//4)}{'├── ' if is_left else '└── '}{node[0]}")
            for pair in node[1:]:
                char, code = pair
                print(f"{'│   ' * (len(prefix)//4)}{'├── ' if is_left else '└── '}{char}: {code}")
        else:
            print("Árvore não disponível. Execute a compactação primeiro.")

