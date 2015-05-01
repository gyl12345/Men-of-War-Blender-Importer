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

import ntpath
from mdl_node import MDL_NODE

class MDL_NODE_DIFFUSE1(MDL_NODE):
	blender_images = {}

	def __init__(self, parent):
		self.texturename = None
		self.filename = None
		self.blender_image = None
		super(MDL_NODE_DIFFUSE1, self).__init__(parent)

	def load_data(self):
		# Get texture name
		self.texturename = self.data.split()[1][1:-1]
		print("Texturename:", self.texturename)
		# Get rid of any path information that might exist
		if self.texturename[0] == '$':
			self.texturename = self.texturename[1:]
			print("Texturename:", self.texturename)
			path, self.texturename = ntpath.split(self.texturename)
			print("Texturename:", path, self.texturename)

		self.texturename += ".dds"
		print("Texturename:", self.texturename)
		# Build filename path
		self.filename = self.path + self.texturename

	def build_blender_data(self, blender_context):
		from bpy_extras.image_utils import load_image

		# Check if image was already loaded
		if self.texturename not in self.blender_images:
			print("Loading texture:", self.texturename, self.filename)
			# Load and create a new Blender image object
			self.blender_images[self.texturename] = load_image(self.filename)