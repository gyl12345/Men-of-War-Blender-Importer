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

"""
This script imports Men of War MDL files to Blender.

Usage:
Run this script from "File->Import" menu and then load the desired MDL file.
Note: All dependent files have to be in the same path as the MDL file (texture, animation, ...)
"""

import os, sys, inspect
import time
import bpy
import mathutils

# Add our current folder to sys.path
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

# Add the "mow" subfolder to sys.path
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"mow")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from mdl import MDL

def load(operator, context, **keywords):
    time_main = time.time()

    filepath = keywords['filepath']

	# Get rid of all existing objects in the scene
    for obj in bpy.context.scene.objects:
        obj.select = obj.type == 'MESH' or obj.type == 'EMPTY'
    bpy.ops.object.delete()

    mdl = MDL(filepath)

    mdl.build_blender_scene(context, keywords['use_animations'])

    mdl.print_type()

    time_new = time.time()

    print("finished importing: %r in %.4f sec." % (filepath, (time_new - time_main)))
    return {'FINISHED'}
