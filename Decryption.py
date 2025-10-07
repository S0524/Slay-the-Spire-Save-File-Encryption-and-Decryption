import base64
import os
import json

def xor_with_key(data: bytes, key: bytes) -> bytes:
    return bytes(data[i] ^ key[i % len(key)] for i in range(len(data)))

def decode(encoded_string: str, key: str) -> str:
    base64_decoded = base64.b64decode(encoded_string)
    decrypted_bytes = xor_with_key(base64_decoded, key.encode('utf-8'))
    return decrypted_bytes.decode('utf-8')

def modify_save_data(save_dict: dict) -> dict:
    save_dict['gold'] = 9999
    save_dict['red'] = 10
    save_dict['max_health'] = 99
    save_dict['current_health'] = 99
    
    required_relics = {"Molten Egg 2", "Toxic Egg 2", "Frozen Egg 2"}
    
    if 'relics' in save_dict:
        current_relics = set(save_dict['relics'])
        missing_relics = required_relics - current_relics
        save_dict['relics'].extend(missing_relics)
    else:
        save_dict['relics'] = list(required_relics)
    
    if 'uncommon_relics' in save_dict:
        save_dict['uncommon_relics'] = [relic for relic in save_dict['uncommon_relics'] if relic not in required_relics]
    
    cards_to_remove = {
        "AscendersBane", "CurseOfTheBell", "Necronomicurse", "Pride", 
        "Clumsy", "Decay", "Doubt", "Injury", "Normality", "Pain", 
        "Parasite", "Regret", "Shame", "Writhe"
    }
    
    if 'cards' in save_dict:
        for card in save_dict['cards']:
            card['upgrades'] = 1
        save_dict['cards'] = [card for card in save_dict['cards'] if card['id'] not in cards_to_remove]
    
    return save_dict

def process_save_file(autosave_file, key):
    output_file = f"{os.path.splitext(autosave_file)[0]}.json"

    if not os.path.exists(autosave_file):
        print(f"文件 {autosave_file} 不存在")
        return

    try:
        with open(autosave_file, 'r') as file:
            encrypted_save = file.read().strip()
    except IOError as e:
        print(f"读取文件 {autosave_file} 失败: {e}")
        return

    try:
        decrypted_save = decode(encrypted_save, key)
        save_dict = json.loads(decrypted_save)
    except Exception as e:
        print(f"解密或解析存档 {autosave_file} 失败: {e}")
        return

    try:
        modified_save_dict = modify_save_data(save_dict)
        modified_save = json.dumps(modified_save_dict, indent=4)
    except Exception as e:
        print(f"修改存档数据 {autosave_file} 失败: {e}")
        return

    try:
        with open(output_file, 'w') as file:
            file.write(modified_save)
        print(f"修改后的存档内容已保存为 {output_file}")
    except IOError as e:
        print(f"保存文件 {output_file} 失败: {e}")
        return

if __name__ == "__main__":
    key = "key"
    characters = ["IRONCLAD", "DEFECT", "THESILENT", "VAGABOND", "WATCHER"]

    for character in characters:
        autosave_file = f"{character}.autosave"
        process_save_file(autosave_file, key)