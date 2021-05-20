#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function
import os
import sys 
import argparse 
import time
import subprocess
import signal
import tempfile
import re
import locale
from tqdm import tqdm
import queue



# This part is a modified version of ffpb made by:
# Copyright (c) 2017-2021 Martin Larralde <martin.larralde@ens-paris-saclay.fr>

unicode = str

class ProgressNotifier(object):

    _DURATION_RX = re.compile(b"Duration: (\d{2}):(\d{2}):(\d{2})\.\d{2}")
    _PROGRESS_RX = re.compile(b"time=(\d{2}):(\d{2}):(\d{2})\.\d{2}")
    _SOURCE_RX = re.compile(b"from '(.*)':")
    _FPS_RX = re.compile(b"(\d{2}\.\d{2}|\d{2}) fps")

    @staticmethod
    def _seconds(hours, minutes, seconds):
        return (int(hours) * 60 + int(minutes)) * 60 + int(seconds)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.pbar is not None:
            self.pbar.close()

    def __init__(self, file=None, encoding=None, tqdm=tqdm):
        self.lines = []
        self.line_acc = bytearray()
        self.duration = None
        self.source = None
        self.started = False
        self.pbar = None
        self.fps = None
        self.file = file or sys.stderr
        self.encoding = encoding or locale.getpreferredencoding() or 'UTF-8'
        self.tqdm = tqdm

    def __call__(self, char, stdin = None):
        if isinstance(char, unicode):
            char = char.encode('ascii')
        if char in b"\r\n":
            line = self.newline()
            if self.duration is None:
                self.duration = self.get_duration(line)
            if self.source is None:
                self.source = self.get_source(line)
            if self.fps is None:
                self.fps = self.get_fps(line)
            self.progress(line)
        else:
            self.line_acc.extend(char)
            if self.line_acc[-6:] == bytearray(b"[y/N] "):
                print(self.line_acc.decode(self.encoding), end="", file=self.file)
                self.file.flush()
                if stdin:
                    stdin.put(input() + "\n")
                self.newline()

    def newline(self):
        line = bytes(self.line_acc)
        self.lines.append(line)
        self.line_acc = bytearray()
        return line

    def get_fps(self, line):
        search = self._FPS_RX.search(line)
        if search is not None:
            return round(float(search.group(1)))
        return None

    def get_duration(self, line):
        search = self._DURATION_RX.search(line)
        if search is not None:
            return self._seconds(*search.groups())
        return None

    def get_source(self, line):
        search = self._SOURCE_RX.search(line)
        if search is not None:
            return os.path.basename(search.group(1).decode(self.encoding))
        return None

    def progress(self, line):
        search = self._PROGRESS_RX.search(line)
        if search is not None:

            total = self.duration
            current = self._seconds(*search.groups())
            unit = " seconds"

            if self.fps is not None:
                unit = " frames"
                current *= self.fps
                if total:
                    total *= self.fps

            if self.pbar is None:
                self.pbar = self.tqdm(
                    desc=self.source,
                    file=self.file,
                    total=total,
                    dynamic_ncols=True,
                    unit=unit,
                    ncols=0,
                    ascii=os.name=="nt",  # windows cmd has problems with unicode
                )

            self.pbar.update(current - self.pbar.n)

def ffprogress(argv=None, stream=sys.stderr, encoding=None, tqdm=tqdm):
    argv = argv or sys.argv[1:]

    try:
        with ProgressNotifier(file=stream, encoding=encoding, tqdm=tqdm) as notifier:

            cmd = ["ffmpeg"] + argv
            p = subprocess.Popen(cmd, stderr=subprocess.PIPE)

            while True:
                out = p.stderr.read(1)
                if out == b"" and p.poll() != None:
                    break
                if out != b"":
                    notifier(out)

    except KeyboardInterrupt:
        print("Exiting.", file=stream)
        return signal.SIGINT + 128  # POSIX standard

    except Exception as err:
        print("Unexpected exception:", err, file=stream)
        return 1

    else:
        if p.returncode != 0:
            print(notifier.lines[-1].decode(notifier.encoding), file=stream)
        return p.returncode









parser = argparse.ArgumentParser(prog='encoder.py', formatter_class=argparse.ArgumentDefaultsHelpFormatter, description='Reduce video size with FFmpeg')
parser.add_argument('input', type=str, help='Input file')
parser.add_argument('size', type=int, help='Desired output size in MB')
parser.add_argument('-f', default='mkv', help='Output format (mp4, mkv, etc)', metavar='format')
parser.add_argument('-p', type=str, default='medium', help='libx264 encoder preset', metavar='preset')
parser.add_argument('-e', choices=["cpu", "gpu"], default='cpu', help='Use cpu or gpu for encoding (NVIDIA only)')
parser.add_argument('-o', type=str, help='Output file', metavar='output')

class style():
    green = '\033[1m\033[32m'
    magenta = '\033[1m\033[35m'
    yellow = '\033[1m\033[93m'
    blue = '\033[1m\033[34m'
    white = '\033[1m\033[37m'
    red = '\033[1m\033[31m'
    reset = '\033[0m'

if __name__ == '__main__':
    os.system("") #Because Windows is stupid and doesn't like ANSI colors
    args = parser.parse_args()
    def signal_handler(signal, frame):
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)


def print_slow(text, duration):
    print('\n' + str(text))
    time.sleep(duration)

def get_encoder():
    if args.e == 'cpu':
        return 'libx264'
    elif args.e == 'gpu':
        return 'h264_nvenc'

def calculate_bitrate(filename, size):
    try:
        proc = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filename],check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(style.red + '\nffprobe error:\n' + style.reset + e.output.decode('utf-8'))
        sys.exit(1)

        
    duration = float(proc.stdout.decode('utf-8'))
         
    exp_br = int(float(size) * 1024 * 1024 * 8 / duration / 1000)
    final_br = exp_br - (exp_br * 0.020)
    text_br = str(final_br) + 'k'
        
    return text_br

def get_size_notation(size):
    fltsize = int(size)
    if fltsize >= 1024:
        realsize = str(float(fltsize / 1024)) + 'GB'
    else:
        realsize = str(size) + 'MB'
    return str(realsize)

def outfile(filename):
    if args.o == None:
        return os.path.abspath(filename) + '-' + get_size_notation(args.size) + '.' + args.f
    else:
        return os.path.abspath(args.o)

def do_conversion():
    if os.path.isdir(args.input):
        if args.o != None:
            print(style.red + 'Syntax Error: "-o" argument must not be used when converting entire directories' + style.reset)
            sys.exit(1)
        mov = [entry.path for entry in os.scandir(args.input) if entry.is_file()]
    elif os.path.isfile(args.input):
        mov = [args.input]
        if args.o != None:
            print(style.yellow + 'WARNING: ' + style.white + 'Using "-o" will override the "-f" argument' + style.reset)
    
    for filename in mov:
        
        arg_list = ['-hide_banner', '-y', '-i', filename, '-c:v', get_encoder(), '-preset', args.p, '-b:v', calculate_bitrate(filename, args.size), '-an', '-pass', '1', '-f', 'matroska', os.devnull]
        arg_pass = ['-hide_banner', '-y', '-i', filename, '-c:v', get_encoder(), '-preset', args.p, '-b:v', calculate_bitrate(filename, args.size), '-map', '0', '-c:a', 'copy', '-pass', '2', outfile(filename)]
        
        print_slow((style.white + 'Input file: ' + style.reset + os.path.abspath(filename)), 0.5)
        print_slow((style.white + 'Output File: ' + style.reset + outfile(filename)), 0.5)
        print_slow((style.white + 'Desired final file size: ' + style.reset + '~' + get_size_notation(args.size)), 0.5)
        print_slow((style.white + 'FFmpeg will use the ' + style.blue + get_encoder() + style.white + ' encoder ' + style.white + 'with the ' + style.magenta + args.p + style.white + ' preset' + style.reset), 0.5)
        print_slow((style.white + 'Expected video bitrate will be: ' + style.reset + '~' + calculate_bitrate(filename, args.size)), 0.5)
        print_slow(style.blue + 'Audio bitrate will remain as-is\n' + style.reset, 0.5)
        
        tmp = tempfile.TemporaryDirectory()
        os.chdir(tmp.name)

        print_slow('Running ' + style.green + '1st' + style.reset + ' pass...', 0.5)
        ffprogress(argv=arg_list)

        print_slow('\nRunning ' + style.green + '2nd' + style.reset + ' pass...', 0.5)
        ffprogress(argv=arg_pass)
        
        print_slow(style.white + 'Cleaning up...' + style.reset, 0.5)
    time.sleep(0.5)
    print(style.green + 'Done' + style.reset)
    sys.exit(0)

do_conversion()


