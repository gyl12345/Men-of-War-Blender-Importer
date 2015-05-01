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

class MDL_NODE_BOX(MDL_NODE):
	def __init__(self, parent):
		self.dimension = None
		self.blender_object_name = None
		super(MDL_NODE_BOX, self).__init__(parent)

	def load_data(self):
		# Explode the box values into separate strings
		values = self.data.split()
		# Assert that all 3 dimensions are present (including the Box tag)
		if len(values) != 4:
			raise Exception("Box data incomplete")

		self.dimension = ( float(values[1]), float(values[2]), float(values[3]) )

		super(MDL_NODE_BOX, self).load_data()

	def build_blender_data(self, blender_context):
		from mdl_node_volume import MDL_NODE_VOLUME
		import bpy

		super(MDL_NODE_BOX, self).build_blender_data(blender_context)

		volume_name = None

		parent_node = self.parent

		# Get parents volume name
		while True:
			# Check if we found a volume node
			if type(parent_node) == MDL_NODE_VOLUME:
				volume_name = parent_node.volume_name
				break
			# Check if we reached the root node without finding a volume node
			elif parent_node == None:
				raise Exception("No parent volume node found")
			# Otherwise get the next parent
			else:
				parent_node = parent_node.parent

		# Create a primitive cube
		bpy.ops.mesh.primitive_cube_add()
		# Get object reference
		obj = bpy.context.object
		# Rename the object
		obj.name = volume_name
		# Resize the cube to the desired shape
		obj.delta_scale[0] = self.dimension[0] / 2
		obj.delta_scale[1] = self.dimension[1] / 2
		obj.delta_scale[2] = self.dimension[2] / 2
		# Keep the name of the blender object
		self.blender_object_name = obj.name
		# Deselect any selected object
		bpy.ops.object.select_all(action='DESELECT')
		# Unlink this object from the scene for now (this will be done later by our parent node)
		bpy.context.scene.objects.unlink(bpy.context.scene.objects[self.blender_object_name])