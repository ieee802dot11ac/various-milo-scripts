#!/usr/bin/python
# thanks to https://github.com/PikminGuts92/re-notes/blob/master/raw_notes/milo/amp/info_tex.txt
# also thanks to https://learn.microsoft.com/en-us/windows/win32/direct3ddds/dds-header for being super fuckin simple lmao
import sys
from dataclasses import dataclass
import numpy

# no structs :despair:
@dataclass
class DDSHeader:
    magic: numpy.uint32 = 0x44445320
    dwSize: numpy.uint32 = 124
    dwFlags: numpy.uint32 = 0x1007
    dwHeight: numpy.uint32 = 0
    dwWidth: numpy.uint32 = 0
    dwPitchOrLinearSize: numpy.uint32 = 0
    dwDepth: numpy.uint32 = 0
    dwMipMapCount: numpy.uint32 = 0
    dwReserved1_1: numpy.uint32 = 0
    dwReserved1_2: numpy.uint32 = 0
    dwReserved1_3: numpy.uint32 = 0
    dwReserved1_4: numpy.uint32 = 0
    dwReserved1_5: numpy.uint32 = 0
    dwReserved1_6: numpy.uint32 = 0
    dwReserved1_7: numpy.uint32 = 0
    dwReserved1_8: numpy.uint32 = 0
    dwReserved1_9: numpy.uint32 = 0
    dwReserved1_10: numpy.uint32 = 0
    dwReserved1_11: numpy.uint32 = 0
    ddspf: numpy.uint32 = 0 # actually 32 bytes wide but hush, this is temp
    dwCaps: numpy.uint32 = 0x1000

dds_hdr = new DDSHeader;

try:
    working_file = open(sys.argv[1],mode='rb').read()
    result_file = open(sys.argv[2],mode='wb')
except:
    print("either of: no filename(s), no file/bad perms. are you sure you typed it right? aborting...")
    sys.exit()

if (not (sys.argv[1].lower().endswith('.bmp'))):
    print("not a .bmp! aborting...")
    sys.exit()

if (working_file[0] != 0x05):
    print("bad file! only accepts .bmps ripped from Amplitude (2003) .rnd archives. un-gzipped .bmps are untested. aborting...")
    sys.exit()

# 0500 0000 is magic number, blame hmx for it
# next 12 bytes are width, then height, then bpp (either 4 or 8, 4 will be multiplied by flat 16)

image_width = working_file[4]
print(image_width)
dds_hdr.dwWidth = image_width
dds_hdr.dwPitchOrLinearSize = (image_width*8+7)/8