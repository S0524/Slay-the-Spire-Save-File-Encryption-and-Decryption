import base64
import os
import json

def xor_with_key(data: bytes, key: bytes) -> bytes:
    return bytes(data[i] ^ key[i % len(key)] for i in range(len(data)))

def decode(encoded_string: str, key: str) -> str:
    base64_decoded = base64.b64decode(encoded_string)
    decrypted_bytes = xor_with_key(base64_decoded, key.encode('utf-8'))
    return decrypted_bytes.decode('utf-8')

def encode(original_string: str, key: str) -> str:
    xor_encrypted = xor_with_key(original_string.encode('utf-8'), key.encode('utf-8'))
    base64_encoded = base64.b64encode(xor_encrypted)
    return base64_encoded.decode('utf-8')

def process_file(character_name: str, key: str):
    input_file = f"{character_name}.json"
    output_file = f"{character_name}.autosave"

    if not os.path.exists(input_file):
        print(f"文件 {input_file} 不存在")
        return

    with open(input_file, 'r') as file:
        decrypted_save = file.read().strip()

    try:
        save_dict = json.loads(decrypted_save)
        json_string = json.dumps(save_dict)
        encrypted_save = encode(json_string, key)
        with open(output_file, 'w') as file:
            file.write(encrypted_save)
        print(f"加密后的存档内容已保存为 {output_file}")
    except Exception as e:
        print(f"加密或保存失败: {e}")

if __name__ == "__main__":
    key = "key"
    characters = ["Defect", "TheSilent", "Vagabond", "Watcher"]

    for character in characters:
        process_file(character, key)