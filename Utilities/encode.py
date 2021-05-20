#!/usr/bin/env python
# coding: utf-8
import os, sys, argparse, time, subprocess, signal
import ffpb


parser = argparse.ArgumentParser(prog='encoder.py', formatter_class=argparse.ArgumentDefaultsHelpFormatter, description='Reduce video size with FFmpeg')
parser.add_argument('input', type=str, help='Input file')
parser.add_argument('size', type=int, help='Desired output size in MB')
parser.add_argument('-f', default='mkv', help='Output format (mp4, mkv, etc)', metavar='format')
parser.add_argument('-p', type=str, default='medium', help='libx264 encoder preset', metavar='preset')
parser.add_argument('-e', choices=["cpu", "gpu"], default='cpu', help='Use cpu or gpu for encoding (NVIDIA only)')
parser.add_argument('-o', type=str, help='Output file', metavar='output')

class style():
    green = '\033[1m\033[32m'
    yellow = '\033[1m\033[93m'
    blue = '\033[1m\033[34m'
    white = '\033[1m\033[37m'
    red = '\033[1m\033[31m'
    reset = '\033[0m'

def remove_ffmpeg_remains():
    try:
        os.remove("ffmpeg2pass-0.log")
        os.remove("ffmpeg2pass-0.log.mbtree")
    except:
        pass
    try:
        os.remove("ffmpeg2pass-0.log.temp")
        os.remove("ffmpeg2pass-0.log.mbtree.temp")
    except:
        pass

if __name__ == '__main__':
    os.system("") #Because Windows is stupid and doesn't like ANSI colors
    args = parser.parse_args()
    def signal_handler(signal, frame):
        remove_ffmpeg_remains()
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
        print(e.output.decode('utf-8'))
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

def filepath(file):
    return os.path.abspath(file)

def outfile(filename):
    if args.o == None:
        return filepath(filename) + '-' + get_size_notation(args.size) + '.' + args.f
    else:
        return args.o


def do_conversion():
    if os.path.isdir(args.input):
        if args.o != None:
            print(style.red + 'Syntax Error: "-o" argument must not be used when converting entire directories' + style.reset)
            sys.exit(1)
        file = [entry.path for entry in os.scandir(args.input) if entry.is_file()]
    elif os.path.isfile(args.input):
        file = [args.input]
        if args.o != None:
            print(style.yellow + 'WARNING: ' + style.white + 'using "-o" will override the "-f" argument' + style.reset)
    
    for filename in file:
        
        arg_list = ['-hide_banner', '-y', '-i', filename, '-c:v', get_encoder(), '-preset', args.p, '-b:v', calculate_bitrate(filename, args.size), '-an', '-pass', '1', '-f', 'matroska', os.devnull]
        arg_pass = ['-hide_banner', '-y', '-i', filename, '-c:v', get_encoder(), '-preset', args.p, '-b:v', calculate_bitrate(filename, args.size), '-map', '0', '-c:a', 'copy', '-pass', '2', outfile(filename)]
        
        print_slow((style.white + 'Input file: ' + style.reset + filepath(filename)), 0.5)
        print_slow((style.white + 'Output File: ' + style.reset + outfile(filename)), 0.5)
        print_slow((style.white + 'Desired final file size: ' + style.reset + '~' + get_size_notation(args.size)), 0.5)
        print_slow((style.white + 'FFmpeg will use the ' + style.blue + get_encoder() + style.white + ' encoder' + style.reset), 0.5)
        print_slow((style.white + 'Expected video bitrate will be: ' + style.reset + '~' + calculate_bitrate(filename, args.size)), 0.5)
        print_slow(style.blue + 'Audio bitrate will remain as-is\n' + style.reset, 0.5)
        
        
        print_slow('Running 1st pass...', 0.5)
        ffpb.main(argv=arg_list)

        print('\nRunning 2nd pass...')
        ffpb.main(argv=arg_pass)
        
        print('\nCleaning up...')
        remove_ffmpeg_remains()
    time.sleep(0.5)
    print(style.green + 'Done' + style.reset)
    exit(0)

do_conversion()


