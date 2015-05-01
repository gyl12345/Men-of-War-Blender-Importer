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

from vol import VOL

class MDL_NODE_POLYHEDRON(MDL_NODE):
	def __init__(self, parent):
		self.name = None
		self.vol = None
		self.blender_mesh = None
		super(MDL_NODE_POLYHEDRON, self).__init__(parent)

	def load_data(self):
		# Get the filename of this volume
		filename = self.path + self.data.split()[1][1:-1]

		print(type(self).__name__ + " Loading file " + filename)

		# Create a volume object and load the VOL file
		self.vol = VOL(filename)

		super(MDL_NODE_POLYHEDRON, self).load_data()

	def build_blender_data(self, blender_context):
		from mdl_node_volume import MDL_NODE_VOLUME
		import bpy
		from bpy_extras.io_utils import unpack_list, unpack_face_list

		super(MDL_NODE_POLYHEDRON, self).build_blender_data(blender_context)

		print(type(self).__name__ + ".build_blender_data()")

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

		# Create a new mesh with our parents volume name
		self.blender_mesh = bpy.data.meshes.new(volume_name)

		# Load vertices data into the mesh
		self.blender_mesh.vertices.add(len(self.vol.positions))
		self.blender_mesh.vertices.foreach_set("co", unpack_list(self.vol.positions))

		# Load face data into the mesh
		self.blender_mesh.tessfaces.add(len(self.vol.indeces))
		self.blender_mesh.tessfaces.foreach_set("vertices", unpack_list(self.vol.indeces))

		# Validate mesh
		self.blender_mesh.validate()

		# Update mesh
		self.blender_mesh.update(calc_edges=True)
