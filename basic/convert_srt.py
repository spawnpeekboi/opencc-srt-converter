"""
Copyright 2024 spawnpeekboi

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import opencc
import os
import re
import shutil
import json
from datetime import datetime
import zlib

"""
                                                 _    _           _ 
                                                | |  | |         (_)
  ___ _ __   __ ___      ___ __  _ __   ___  ___| | _| |__   ___  _ 
 / __| '_ \ / _` \ \ /\ / / '_ \| '_ \ / _ \/ _ \ |/ / '_ \ / _ \| |
 \__ \ |_) | (_| |\ V  V /| | | | |_) |  __/  __/   <| |_) | (_) | |
 |___/ .__/ \__,_| \_/\_/ |_| |_| .__/ \___|\___|_|\_\_.__/ \___/|_|
     | |                        | |                                 
     |_|                        |_|                                 
"""
# Published on Dockerhub at https://hub.docker.com/r/spawnpeekboi/opencc-srt-converter
# Published on Github at https://github.com/spawnpeekboi/opencc-srt-converter

# Library Copyright Notices:
# - OpenCC: (c) BYVoid. Licensed under MIT License. See https://github.com/BYVoid/OpenCC
# - Python Standard Libraries: Various licenses apply; see Python documentation for details.

def calculate_checksum(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    return format(zlib.crc32(data) & 0xFFFFFFFF, '08x')

def convert_srt(input_file, output_file):
    print(f'Starting translation for {input_file}...')
    converter = opencc.OpenCC('s2hk')
    
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            if re.match(r'^\d+$', line.strip()) or line.strip() == '':
                outfile.write(line)  # Write timestamps and empty lines unchanged.
            else:
                outfile.write(converter.convert(line))  # Convert and write translated lines.
    
    print(f'Translated SRT saved to {output_file}')

def backup_srt(input_file, backup_folder):
    relative_path = os.path.relpath(os.path.dirname(input_file), input_directory)
    backup_path = os.path.join(backup_folder, relative_path)
    os.makedirs(backup_path, exist_ok=True)

    original_output_file = os.path.join(backup_path, os.path.basename(input_file))
    print(f'Backing up {input_file} to {original_output_file}...')
    
    shutil.copy2(input_file, original_output_file)  # Copy the original SRT file to the backup location.
    return original_output_file

def update_translation_log(file_info, log_path):
    data = []
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as log_file:
            data = json.load(log_file)  # Load existing log data.
    
    data.append(file_info)  # Append new file information to the log.
    
    with open(log_path, 'w', encoding='utf-8') as log_file:
        json.dump(data, log_file, indent=4)  # Write updated log data back to file.

def is_already_translated(file_info, log_path):
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as log_file:
            data = json.load(log_file)
            for entry in data:
                if (entry['file_name'] == file_info['file_name'] and
                    entry['modified_date'] == file_info['modified_date'] and
                    entry['file_path'] == file_info['file_path'] and
                    entry['checksum'] == file_info['checksum']):
                    return True  # Return True if a matching entry is found.
    return False  # Return False if no match is found.

def scan_and_process(input_directory, output_directory):
    print("Scanning for .srt files...")
    
    log_path = '/data/translation_log.json'
    
    for root, _, files in os.walk(input_directory):  # Walk through the input directory.
        for file in files:
            if file.endswith('.srt'):  # Process only SRT files.
                input_file = os.path.join(root, file)

                modification_time = datetime.fromtimestamp(os.path.getmtime(input_file)).isoformat()
                checksum = calculate_checksum(input_file)  # Calculate checksum of the input SRT file.

                temp_file_info = {
                    "file_name": file,
                    "modified_date": modification_time,
                    "file_path": input_file,
                    "checksum": checksum
                }

                if is_already_translated(temp_file_info, log_path):  # Check if this file has already been translated.
                    print(f'File already logged as translated: {input_file}')
                    continue  # Skip processing if already translated.

                backed_up_file = backup_srt(input_file, output_directory)  # Backup the original SRT file.
                translated_output_file = os.path.join(root, f'traditional_{file}')  # Define output path for translated SRT.
                
                convert_srt(input_file, translated_output_file)  # Convert the SRT file to Traditional Chinese.
                
                print(f'Replacing original SRT {input_file} with translated version.')
                shutil.move(translated_output_file, input_file)  # Replace original SRT with the translated version.

                translated_modification_time = datetime.fromtimestamp(os.path.getmtime(input_file)).isoformat()
                translated_checksum = calculate_checksum(input_file)  # Calculate checksum of the newly translated SRT.

                final_file_info = {
                    "file_name": os.path.basename(input_file),
                    "modified_date": translated_modification_time,
                    "file_path": input_file,
                    "checksum": translated_checksum
                }

                update_translation_log(final_file_info, log_path)  # Update the translation log with new metadata.

    print("All SRT found are being processed.")

if __name__ == '__main__':
    print("opencc-srt-converter starting")
    
    input_directory = '/media'  # Directory where original SRT files are located.
    output_directory = '/data/old_srt'  # Directory where backups will be stored.
    
    print("opencc-srt-converter has started")  
    
    scan_and_process(input_directory, output_directory)  # Start scanning and processing SRT files.
    
    print("The container will be terminated now.")
