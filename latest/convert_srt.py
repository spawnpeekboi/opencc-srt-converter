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
import hashlib

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

def backup_srt(original_file, backup_folder): # Creates a backup of the original SRT file in the specified backup folder
    relative_path = os.path.relpath(os.path.dirname(original_file), input_directory)
    backup_path = os.path.join(backup_folder, relative_path)
    os.makedirs(backup_path, exist_ok=True)

    original_output_file = os.path.join(backup_path, os.path.basename(original_file))
    print(f'Backing up {original_file} to {original_output_file}...')
    
    shutil.copy2(original_file, original_output_file)
    return original_output_file

def calculate_checksum(file_path): # Calculates and returns the SHA-256 checksum of a given file
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def cleanup_jellyfin_srt(directory): # Removes unnecessary .chi.number.srt files based on checksum comparison
    print("Cleaning up unnecessary .chi.number.srt files...")
    
    for root, _, files in os.walk(directory):
        for file in files:
            match = re.match(r'^(.*\.chi)\.(\d+)\.srt$', file)
            if match:
                base_name = match.group(1) + '.srt'
                chi_number_srt_path = os.path.join(root, file)
                corresponding_srt_path = os.path.join(root, base_name)

                if os.path.exists(corresponding_srt_path):
                    chi_number_checksum = calculate_checksum(chi_number_srt_path)
                    corresponding_checksum = calculate_checksum(corresponding_srt_path)

                    chi_number_size = os.path.getsize(chi_number_srt_path)
                    corresponding_size = os.path.getsize(corresponding_srt_path)

                    if chi_number_checksum == corresponding_checksum and chi_number_size == corresponding_size:
                        print(f'Removing {chi_number_srt_path} because it matches {corresponding_srt_path}.')
                        os.remove(chi_number_srt_path)

def convert_srt(original_file, output_file): # Translates the content of an SRT file from Simplified to Traditional Chinese
    print(f'Starting translation for {original_file}...')
    converter = opencc.OpenCC('s2hk')
    
    with open(original_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            if re.match(r'^\d+$', line.strip()) or line.strip() == '':
                outfile.write(line)
            else:
                translated_line = converter.convert(line)
                outfile.write(translated_line)
        print(f'Translated SRT saved to {output_file}')

def is_already_translated(file_info, log_path): # Checks if a file has already been translated by comparing its metadata against the log
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as log_file:
            data = json.load(log_file)
            for entry in data:
                if (entry['file_name'] == file_info['file_name'] and
                    entry['modified_date'] == file_info['modified_date'] and
                    entry['file_path'] == file_info['file_path'] and
                    entry['checksum'] == file_info['checksum']):
                    return True
    return False

def scan_and_process(input_directory, output_directory): # main process
    print("Scanning for .srt files...")
    
    log_path = '/data/translation_log.json'
    
    for root, _, files in os.walk(input_directory):
        for file in files:
            if file.endswith('.srt'):
                original_file = os.path.join(root, file)

                modification_time = datetime.fromtimestamp(os.path.getmtime(original_file)).isoformat()
                checksum = calculate_checksum(original_file)

                temp_file_info = {
                    "file_name": file,
                    "modified_date": modification_time,
                    "file_path": original_file,
                    "checksum": checksum,
                    "file_size": os.path.getsize(original_file)
                }

                if is_already_translated(temp_file_info, log_path):
                    print(f'File already logged as translated: {original_file}')
                    continue

                backed_up_file = backup_srt(original_file, output_directory)
                translated_output_file = os.path.join(root, f'traditional_{file}')
                
                convert_srt(original_file, translated_output_file)
                print(f'Replacing original SRT {original_file} with translated version.')
                shutil.move(translated_output_file, original_file)

                translated_modification_time = datetime.fromtimestamp(os.path.getmtime(original_file)).isoformat()
                translated_checksum = calculate_checksum(original_file)

                final_file_info = {
                    "file_name": os.path.basename(original_file),
                    "modified_date": translated_modification_time,
                    "file_path": original_file,
                    "checksum": translated_checksum,
                    "file_size": os.path.getsize(original_file)
                }

                update_translation_log(final_file_info, log_path)

    print("All SRT found are being processed.")

def update_translation_log(file_info, log_path): # Updates the translation log with information about processed files
    data = []
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as log_file:
            data = json.load(log_file)
    
    data.append(file_info)
    
    with open(log_path, 'w', encoding='utf-8') as log_file:
        json.dump(data, log_file, indent=4)

if __name__ == '__main__':
    print("opencc-srt-converter starting")
    
    input_directory = '/media'
    output_directory = '/data/old_srt'

    print("opencc-srt-converter has started")  
    scan_and_process(input_directory, output_directory)
    
    do_cleanup = os.getenv('do_jellyfin_cleanup', 'false').lower() == 'true'
    
    if do_cleanup:
        print("starting clean up duplicated srt")  
        cleanup_jellyfin_srt(input_directory) 
    else:
        print("Skipping cleanup of duplicated SRT files.")

    print("The container will be terminated now.")

# Library Copyright Notices:
# - OpenCC: (c) BYVoid. Licensed under MIT License. See https://github.com/BYVoid/OpenCC
# - Python Standard Libraries: Various licenses apply; see Python documentation for details.
