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

from mowdef_node import MOWDEF_NODE
from mdl import MDL
import sys

class MOWDEF_NODE_EXTENSION(MOWDEF_NODE):
	def __init__(self, parent):
		self.mdl = None
		super(MOWDEF_NODE_EXTENSION, self).__init__(parent)

	def blender_get_root_object(self):
		if self.mdl:
			return self.mdl.blender_get_root_object()
		return None

	def load_data(self):
		super(MOWDEF_NODE_EXTENSION, self).load_data()

		from mowdef_node_root import MOWDEF_NODE_ROOT

		filename = None

		# Get the name of the MDL file
		filename = self.data.split()[1][1:-1]

		# Build a complete filepath to the .MDL file
		filename = self.path + filename

		print(type(self).__name__ + " Loading file " + filename)

		try:
			# Create an MDL object and load the MDL file
			self.mdl = MDL(filename)
		except:
			print(sys.exc_info()[0])

	def build_blender_scene(self, blender_context, use_animations):
		if self.mdl:
			self.mdl.build_blender_scene(blender_context, use_animations)