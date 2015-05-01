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

class MDL_NODE_SKELETON(MDL_NODE):
	def __init__(self, parent):
		self.bone_nodes = []
		self.armature_name = None
		self.rig_name = None
		# self.blender_armature = None
		# self.blender_rig = None
		super(MDL_NODE_SKELETON, self).__init__(parent)

	def get_blender_armature(self):
		import bpy

		if self.armature_name:
			return bpy.data.armatures[self.armature_name]
		else:
			return None

	def get_blender_rig(self):
		import bpy

		if self.rig_name:
			return bpy.data.objects[self.rig_name]
		else:
			return None

	def register_bone_node(self, bone_node):
		print("Registering bone node:", bone_node.bone_name)
		# Add bone node to our bone nodes array
		self.bone_nodes.append(bone_node)

	def get_bone_node(self, bone_name):
		for bone_node in self.bone_nodes:
			if bone_node.bone_name == bone_name:
				return bone_node
		return None

	def build_blender_armature(self, blender_context):
		import bpy

		# Keep a reference of the scene object
		blender_context.scene

		# Create an armature
		blender_armature = bpy.data.armatures.new('Armature')
		self.armature_name = blender_armature.name

		# Show the names of the bones inside the armature
		blender_armature.show_names = True

		# Set the bone draw type
		blender_armature.draw_type = 'ENVELOPE'

		# Create an object (rig) for the armature
		blender_rig = bpy.data.objects.new('Rig', blender_armature)
		self.rig_name = blender_rig.name

		# Enable X Ray vision of the bones
		blender_rig.show_x_ray = True

		# Link the rig to the scene
		blender_context.scene.objects.link(blender_rig)

		super(MDL_NODE_SKELETON, self).build_blender_armature(blender_context)