# Ferrah's Python Utilities!!

This is my humble collection of random Python stuff that I made over time...
They might not be useful for much, but feel free to use the as you like!


# Main ones

These are my main scripts. They are more complex and usually were made to accomplish a simple task(s)

## Encoder

Located [here](https://github.com/DatCrazyDelphox/python_stuff/blob/main/Utilities/encode.py), this is a simple python 3.x script that uses ffmpeg to re-encode your video files to a specific file size and format.

### Installation
Encoder needs two dependencies: 
- **FFmpeg** - Install it with your system's package manager (already bundled with the windows release zip)
-  [ffpb](https://github.com/althonos/ffpb), which can be installed with `python -m pip install ffpb`

### Usage
Encoder takes an `input` video file and the desired output `size` as arguments.

<code>usage: encoder.py [-h] [-f format] [-p preset] [-e {cpu,gpu}] input size</code>

## BME280 Data logger

This project is now made in Rust and can be found [here](https://github.com/DatCrazyDelphox/rpi-bme280-logger)
