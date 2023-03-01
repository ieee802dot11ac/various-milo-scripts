#!/usr/bin/python
# thanks to https://github.com/PikminGuts92/re-notes/blob/master/raw_notes/milo/amp/info_tex.txt
# also thanks to https://learn.microsoft.com/en-us/windows/win32/direct3ddds/dds-header for being super fuckin simple lmao
import sys

# no structs :despair:

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


class HMXTexture:
    def SaveAsDDS(self, outPath):
        inFile = open(self.path, "rb")
        outFile = open(outPath, "wb")

        size = inFile.seek(0, 2)
        inFile.seek(self.ddsOffset, 0)

        outFile.write(self.BuildDDSHeader(self.width[0], self.height[0], self.version[0]))

        # xbox amp. imagine. anyways we don't need to shuffle it lol
        while (inFile.tell() < size):
            buf = inFile.read(1)
            outFile.write(buf)

        inFile.close()
        outFile.close()
        return

    def __init__(self, path):
        if not os.path.isfile(path):
            return
            
        self.path = path
        with open(self.path, "rb") as file:
            self.SetHeaderInfo(file.read(32))
        return

    def SetHeaderInfo(self, data):
        self.version = struct.unpack_from("<i", data, 2)
        self.width = struct.unpack_from("<h", data, 7)
        self.height = struct.unpack_from("<h", data, 9)
        self.ddsOffset = 32;
        return

    def BuildDDSHeader(self, width, height, version):
        if (version == 8): # DXT1
            v = bytes([ 0x44, 0x58, 0x54, 0x31])
        elif (version == 32): # ATI2
            v = bytes([ 0x41, 0x54, 0x49, 0x32])
        else: # DXT5
            v = bytes([ 0x44, 0x58, 0x54, 0x35])

        h = struct.pack("<I", height)
        w = struct.pack("<I", width)

        dds = bytes([
            0x44, 0x44, 0x53, 0x20, 0x7C, 0x00, 0x00, 0x00, 0x07, 0x10, 0x0A, 0x00, h[0], h[1], h[2], h[3],
            w[0], w[1], w[2], w[3], 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00,
            0x04, 0x00, 0x00, 0x00, v[0], v[1], v[2], v[3], 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
                ])
        return dds # thanks cisco :gradientpeek:

# 0500 0000 is magic number, blame hmx for it
# next 12 bytes are width, then height, then bpp (either 4 or 8, 4 will be multiplied by flat 16)
