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

import os

from mowdef_node import MOWDEF_NODE

class MOWDEF:
	def __init__(self, filename):
		self.data = None
		self.root_node = None

		# Create the root node with no parent
		self.root_node = MOWDEF_NODE.create_node_from_type('root', None)

		# Add the path information to the root node
		self.root_node.path = os.path.dirname(filename) + '\\'

		# Open the file and load its content into our self.data attribute
		self.open_file(filename)

		# Let the root node parse the file content
		self.root_node.parse_def_node(self.data)

		# Load data files (.mdl, etc)
		self.root_node.load_data()

	def print_type(self):
		self.root_node.print_type()

	def blender_get_root_object(self):
		game_entity_node = self.root_node.get_game_entity_node()
		if game_entity_node:
			extension_node = game_entity_node.get_extension_node()
			if extension_node:
				return extension_node.blender_get_root_object()

		return None

	def open_file(self, filename):
		if filename == None or os.path.splitext(filename)[1][1:].strip() != "def":
			raise Exception("Invalid file %s" % filename)

		# Encode filename to filesystem encoding
		filename = os.fsencode(filename)

		# Open MDL file
		f = open(filename, 'r')

		# Read all lines of the MDL file
		lines = f.readlines()

		# Close file
		f.close()

		# Build data string
		for line in lines:
			# Get rid of leading and trailing spaces and line feeds
			line = line.lstrip().rstrip()

			# Ignore empty lines
			if not line:
				continue

			# Ignore comment lines
			if line[0] == ';':
				continue

			# Concatenate line to data string
			if self.data == None:
				self.data = line
			else:
				self.data += ' ' + line

		# Get length of the data string		
		length = len(self.data)

		bracket_counter = 0
		i = 0

		# Check if we are consistent (number of '{'s must match number of '}'s)
		while i < length:
			if self.data[i] == '{':
				bracket_counter += 1
			if self.data[i] == '}':
				bracket_counter -= 1
			i += 1

		# Open bracket counter should be zero
		if bracket_counter != 0:
			raise Exception("Number of '{'s doesn't match number of '}'s in file")

		# First and last character of our data string should now be a '{' and a '}' respectively
		if self.data[0] != '{' or self.data[-1] != '}':
			raise Exception("First is not a { or last character is not a }")

	def build_blender_scene(self, blender_context, use_animations):
		print("Building Blender scene")
		# Build blender armature (bones)
		#self.root_node.build_blender_armature(blender_context)
		# Build blender data first (meshes, objects, ...)
		self.root_node.build_blender_data(blender_context)
		# Build blender scene (link object hierarchy, link to scene, ...)
		self.root_node.build_blender_scene(blender_context, use_animations)
		# Check if we should load the animations
		if use_animations:
			# Animations start at 0
			blender_context.scene.frame_start = 0
			# Set current animation frame start
			blender_context.scene.frame_current = 0
			# Build blender animation
			self.root_node.build_blender_animation(blender_context)
			# Set the current frame position as the animation end
			blender_context.scene.frame_end = blender_context.scene.frame_current
			# Set current animation frame at the beginning
			blender_context.scene.frame_current = 0
		print("Finished building Blender scene")