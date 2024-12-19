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

- [Overview](#overview)
- [Docker Image Usage](#docker-image-usage)
- [Docker Compose Setup](#docker-compose-setup)
- [Building the Image](#building-the-image)
- [Credits](#credits)
- [License](#license)

## Overview

The OpenCC SRT Converter utilizes the OpenCC library to perform conversions between Simplified and Traditional Chinese. This Docker image encapsulates all necessary dependencies.

## Docker Image Usage

To use the OpenCC SRT Converter Docker image, follow these steps:

1. **Pull the Docker Image**:
   You can pull the latest version of the image from Docker Hub with the following command:
    
```docker pull spawnpeekboi/opencc-srt-converter```    
    
1. **Run the Docker Container**:
Use the following command to run the converter. Replace `/path/to/media` with the path to your directory containing SRT files and `/path/to/data` with your desired backup/log directory:

```docker run --rm -v /path/to/media:/media -v /path/to/data:/data spawnpeekboi/opencc-srt-converter```    
    
1. **Example Command**:
Here’s an example of running the converter with a sample directory:

```docker run --rm -v $(pwd)/srt_files:/media -v $(pwd)/backups:/data spawnpeekboi/opencc-srt-converter```    

This command will convert all SRT files in `srt_files`, back them up in `backups`, and replace them with their Traditional Chinese versions.

## Docker Compose Setup

You can also use Docker Compose to simplify running the OpenCC SRT Converter. Below is an example `docker-compose.yml` file you can use:

```
version: '3.8'

services:
  opencc-srt-converter:
    image: spawnpeekboi/opencc-srt-converter
    volumes:
      - /path/to/media:/media  # Path to your SRT files
      - /path/to/data:/data     # Path for backups and logs
    restart: unless-stopped
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
