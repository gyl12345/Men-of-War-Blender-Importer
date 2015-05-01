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
from mdl_node_box import MDL_NODE_BOX
from mdl_node_cylinder import MDL_NODE_CYLINDER
from mdl_node_matrix34 import MDL_NODE_MATRIX34
from mdl_node_position import MDL_NODE_POSITION
from mdl_node_polyhedron import MDL_NODE_POLYHEDRON

class MDL_NODE_VOLUME(MDL_NODE):
	def __init__(self, parent):
		self.bone_name = None
		self.volume_name = None
		self.blender_object_name = None
		super(MDL_NODE_VOLUME, self).__init__(parent)

	def select_layer(self, layer):
		return tuple(i == layer for i in range(0, 20))

	def get_blender_object(self):
		import bpy

		if self.blender_object_name:
			return bpy.data.objects[self.blender_object_name]
		else:
			return None

	def load_data(self):
		# Get volume name
		self.volume_name = self.data.split()[1][1:-1]

		# Check if we haven't found the volume name
		if self.volume_name == None:
			# Set a dummy name
			self.volume_name = '<unknown>'

		# Append a '_vol' to the volume name to distinguish its mesh from regular VolumeView meshes
		self.volume_name = self.volume_name + '_vol'

		super(MDL_NODE_VOLUME, self).load_data()

	def build_blender_data(self, blender_context):
		from mdl_node_bone import MDL_NODE_BONE
		import bpy
		import mathutils

		super(MDL_NODE_VOLUME, self).build_blender_data(blender_context)

		box_node = None
		bone_node = None
		cylinder_node = None
		matrix34_node = None
		position_node = None
		polyhedron_node = None

		blender_mesh = None
		blender_object = None

		# Search for important child nodes
		for node in self.nodes:
			if type(node) == MDL_NODE_BOX:
				box_node = node
			elif type(node) == MDL_NODE_BONE:
				bone_node = node
			elif type(node) == MDL_NODE_CYLINDER:
				cylinder_node = node
			elif type(node) == MDL_NODE_MATRIX34:
				matrix34_node = node
			elif type(node) == MDL_NODE_POSITION:
				position_node = node
			elif type(node) == MDL_NODE_POLYHEDRON:
				polyhedron_node = node

		# If we found a polyhedron node, get the blender mesh from it
		if polyhedron_node:
			blender_mesh = polyhedron_node.blender_mesh

			# Create a new object with the name of this volume and (if available) a mesh
			blender_object = bpy.data.objects.new(self.volume_name, blender_mesh)

		# If we found a box node, get the blender object name from it
		if box_node:
			blender_object = bpy.data.objects[box_node.blender_object_name]

		# If we found a cylinder node, get the blender object name from it
		if cylinder_node:
			blender_object = bpy.data.objects[cylinder_node.blender_object_name]

		if blender_object:
			self.blender_object_name = blender_object.name

			# If we have position data, set objects location
			if position_node:
				pass
				blender_object.location = position_node.position

			# If we have orientation data, set objects orientation
			# if orientation_node:
			# 	pass
				#blender_object.scale = (orientation_node.orientation[0][0], orientation_node.orientation[1][1], orientation_node.orientation[2][2])
				#blender_object.rotation_quaternion = mathutils.Matrix(orientation_node.orientation).to_3x3().to_quaternion()

			# If we have a matrix34 node, set objects orientation and location from it
			if matrix34_node:
				pass
				blender_object.matrix_local = matrix34_node.orientation
				blender_object.location = matrix34_node.position
				blender_object.scale = (1.0, 1.0, 1.0)
				
				# blender_object.rotation_quaternion = mathutils.Matrix(matrix34_node.orientation).to_3x3().to_quaternion()
				# blender_object.matrix_world = matrix34_node.matrix_4x4

		# Check if we have a child bone node
		if bone_node:
			# Make the the bone our parent
			self.bone_name = bone_node.bone_name

	def build_blender_scene(self, blender_context):
		import bpy

		blender_object = self.get_blender_object()

		# Make the volume the child of the parent bone
		if blender_object and self.bone_name:
			blender_object.parent = bpy.data.objects[self.bone_name]

		# Don't do anything if we don't have a blender object
		if blender_object == None:
			return

		# Link our blender object to the scene
		try:
			blender_context.scene.objects.link(blender_object)
		except (RuntimeError):
			pass
		#blender_context.scene.objects.link(blender_object)

		# Show volume objects on a separate layer
		blender_object.layers = self.select_layer(1)

		super(MDL_NODE_VOLUME, self).build_blender_scene(blender_context)