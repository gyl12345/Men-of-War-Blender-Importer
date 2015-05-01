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

from mdl_node import MDL_NODE
from mdl_node_file import MDL_NODE_FILE

from anm import ANM

class MDL_NODE_SEQUENCE(MDL_NODE):
	loaded_animation_files = []

	def __init__(self, parent):
		self.name = None
		self.anm = None
		super(MDL_NODE_SEQUENCE, self).__init__(parent)

	def load_data(self):
		super(MDL_NODE_SEQUENCE, self).load_data()

		filename = None

		# Get the name of this animation
		self.name = self.data.split()[1][1:-1]

		# First, try to find a child node of MDL_NODE_FILE that will tell us the animation file to use
		for node in self.nodes:
			if type(node) is MDL_NODE_FILE:
				# Get the filename
				filename = node.filename
				break

		# If there was no child node of MDL_NODE_FILE, use the sequences name to guess the animation file to use
		if filename == None:
			filename = self.path + self.name + ".anm"

		# Check if this animation file wasn't already loaded
		if filename not in self.loaded_animation_files:
			print(type(self).__name__ + " Loading file " + filename)
			# Create an Animation object and load the ANM file
			self.anm = ANM(filename)
			# Add filename into our loaded animation files
			self.loaded_animation_files.append(filename)