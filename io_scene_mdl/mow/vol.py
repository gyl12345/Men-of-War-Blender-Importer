# coding=utf-8

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Men of War MDL importer for Blender
# Script Copyright (C) by Björn Martins Paz

from __future__ import print_function

import struct

VOLMAGICK = b"EVLM"

SUPPORTED_ENTRY = [b"VERT", b"INDX", b"SIDE"]

class VOL:
    def __init__(self, path):
        self.path = path
        self.positions = []
        self.indeces = []
        self.sides = []

        self.open()

    def open(self):
        with open(self.path, "rb") as f:
            # read header
            magick, = struct.unpack("4s", f.read(4))
            if magick != VOLMAGICK:
                raise Exception("Unsupported format: %s" % magick)

            # Process entries
            while True:
                try:
                    entry, = struct.unpack("4s", f.read(4))
                except struct.error:
                    return

                print("Found entry %s at %s" % (entry, hex(f.tell())) )

                # Check if the entry is a supported one
                if not(entry in SUPPORTED_ENTRY):
                    raise Exception("Unsupported entry type: %s" % entry)
                
                if entry == SUPPORTED_ENTRY[0]: #VERT
                    # Read number of vertices
                    vertices, = struct.unpack("<I", f.read(4))
                    print("Number of vertices: %i at %s" % (vertices, hex(f.tell())))

                    # Read all vertices form the file
                    for i in range(0, vertices):
                        vx,vy,vz = struct.unpack("fff", f.read(12))
                        self.positions.append((vx,vy,vz))

                if entry == SUPPORTED_ENTRY[1]: #INDX
                    # Read number of indices
                    indices, = struct.unpack("<I", f.read(4))
                    print("Number of indices: %i at %s" % (indices, hex(f.tell())))

                    # Read all indices from the file
                    for i in range(0, int(indices/3)):
                        i0,i1,i2 = struct.unpack("<HHH", f.read(6))
                        self.indeces.append((i0,i1,i2))

                if entry == SUPPORTED_ENTRY[2]: #SIDE
                    # Read number of sides
                    sides, = struct.unpack("<I", f.read(4))
                    print("Number of sides: %i at %s" % (indices, hex(f.tell())))

                    # Read all sides from the file
                    for i in range(0, sides):
                        side = struct.unpack("<B", f.read(1))
                        self.sides.append((side))