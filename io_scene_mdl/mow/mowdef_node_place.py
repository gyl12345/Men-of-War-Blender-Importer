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

from mowdef import MOWDEF
from mowdef_node import MOWDEF_NODE
from mowdef_node_game_entity import MOWDEF_NODE_GAME_ENTITY

class MOWDEF_NODE_PLACE(MOWDEF_NODE):
	def __init__(self, parent):
		self.bone_name = None
		self.mowdefs = []

		super(MOWDEF_NODE_PLACE, self).__init__(parent)

	def load_data(self):
		game_entity_name = None

		# Split the parameters of this bone into two possible components
		tokens = self.data.split()[1:]

		i = 0
		for token in tokens:
			# Check if this is a valid attribute
			if token[0] != '"':
				break

			# Check if it is a bone name
			if i == 0:
				# Get the bone name
				self.bone_name = token[1:-1]
			# Check if it is another MOWDEF object
			elif i > 0:
				# Get the MOWDEF object name
				game_entity_name = token[1:-1]

				# Check if we have a bone name and a game entity name
				if self.bone_name and game_entity_name:
					# Build a complete filepath to the .DEF file
					filename = self.path + game_entity_name + '\\' + game_entity_name + '.def'
					print(filename)
					# Load the .DEF file of the game entity
					self.mowdefs.append(MOWDEF(filename))

			# Increment our attribute counter
			i += 1

		super(MOWDEF_NODE_PLACE, self).load_data()

	def build_blender_scene(self, blender_context, use_animations):
		super(MOWDEF_NODE_PLACE, self).build_blender_scene(blender_context, use_animations)

		import bpy

		# Get the bone
		if self.bone_name and len(self.mowdefs) > 0:
			bone_blender_object = bpy.data.objects[self.bone_name]

		# Process each MOWDEF object
		for mowdef in self.mowdefs:
			game_entity_blender_object = None

			# Let the MOWDEF object build its blender scene first
			mowdef.build_blender_scene(blender_context, use_animations)

			# Get the root blender object from the MOWDEF object
			game_entity_blender_object = mowdef.blender_get_root_object()

			# Check if we have found the root blender object of the MOWDEF
			if game_entity_blender_object and bone_blender_object:
				# Make it the child of its defined parent bone
				game_entity_blender_object.parent = bone_blender_object