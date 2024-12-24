```
                                                 _    _           _ 
                                                | |  | |         (_)
  ___ _ __   __ ___      ___ __  _ __   ___  ___| | _| |__   ___  _ 
 / __| '_ \ / _` \ \ /\ / / '_ \| '_ \ / _ \/ _ \ |/ / '_ \ / _ \| |
 \__ \ |_) | (_| |\ V  V /| | | | |_) |  __/  __/   <| |_) | (_) | |
 |___/ .__/ \__,_| \_/\_/ |_| |_| .__/ \___|\___|_|\_\_.__/ \___/|_|
     | |                        | |                                 
     |_|                        |_|                                 
```
# OpenCC SRT Converter

This repository provides a Docker image for converting SRT (SubRip Subtitle) files from Simplified Chinese to Traditional Chinese using the OpenCC library.

## Table of Contents

- [OpenCC SRT Converter](#opencc-srt-converter)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Docker Image tag](#docker-image-tag)
    - [Tag: `basic`](#tag-basic)
    - [Tag: `latest`](#tag-latest)
  - [Docker Image Usage](#docker-image-usage)
  - [Docker Compose Setup](#docker-compose-setup)
  - [Building the Image](#building-the-image)
  - [Credits](#credits)
  - [License](#license)

## Overview

The OpenCC SRT Converter utilizes the OpenCC library to perform translation of SRT files from Simplified Chinese to Traditional Chinese using the OpenCC library. It includes basic features such as reading SRT files, performing translations, and backing up original files. It will read from `/media` and search for any `.srt` in all directory including subfolder. After the inital deployment, all the original srt will be store at `/data` according to its origianl folder structure. A `translation_log.json` will be store at `/data`. Starting from second deployment, the program will compare the metadata of file with the same name as in the log, if all metadata are the same, the file will not be processed again.

## Docker Image tag

### Tag: `basic`
This version of the image provides core functionality. This version only uses CRC64 and **does not** implement SHA-256 checksum validation or a cleanup function.

### Tag: `latest`
The latest version of the image also include SHA-256 checksum validation to ensure file integrity during processing. Additionally, it introduces a cleanup function for removing duplicate SRT files which occur when using Jellyfin opensubtitle plugin to run `download all missing subtitles`.

## Docker Image Usage

To use the OpenCC SRT Converter Docker image, follow these steps:

1. **Pull the Docker Image**:
   You can pull the latest version of the image from Docker Hub with the following command:
    
```docker pull spawnpeekboi/opencc-srt-converter```    
    
2. **Run the Docker Container**:
Use the following command to run the converter. Replace `/path/to/media` with the path to your directory containing SRT files and `/path/to/data` with your desired backup/log directory:

```docker run --rm -v /path/to/media:/media -v /path/to/data:/data spawnpeekboi/opencc-srt-converter```

For using `tag:latest`

```docker run --rm -e do_jellyfin_cleanup=true -v /path/to/media:/media -v /path/to/data:/data spawnpeekboi/opencc-srt-converter```
    
## Docker Compose Setup

You can also use Docker Compose to simplify running the OpenCC SRT Converter. Below is an example `docker-compose.yml` file you can use:

```
version: '3.8'

services:
  opencc-srt-converter:
    volumes:
      - /path/to/media:/media    # path to your jellyfin library
      - /path/to/data:/data      # path to store config, metadata and backup original .srt file
    environment:
      - do_jellyfin_cleanup=true # Set to true or false as needed
```

## Building the Image

If you want to build the Docker image from source, you can do so by cloning this repository and running the following command in the project directory:

```docker build -t opencc-srt-converter .```

## Credits

This project uses [OpenCC](https://github.com/BYVoid/OpenCC) for converting Simplified Chinese to Traditional Chinese. 

Published on Dockerhub at [https://hub.docker.com/r/spawnpeekboi/opencc-srt-converter](https://hub.docker.com/r/spawnpeekboi/opencc-srt-converter)  
Published on GitHub at [https://github.com/spawnpeekboi/opencc-srt-converter](https://github.com/spawnpeekboi/opencc-srt-converter)

## License

This project is licensed under the Apache License 2.0. You may obtain a copy of this license at [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0). See the LICENSE file for more details.
