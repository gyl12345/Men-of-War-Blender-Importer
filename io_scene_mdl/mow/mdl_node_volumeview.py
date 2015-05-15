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

import sys

from mdl_node import MDL_NODE
from mdl_node_material import MDL_NODE_MATERIAL
from mdl_node_diffuse import MDL_NODE_DIFFUSE

from ply import PLY

class MDL_NODE_VOLUMEVIEW(MDL_NODE):
	def __init__(self, parent):
		self.ply = None
		self.blender_mesh = None
		super(MDL_NODE_VOLUMEVIEW, self).__init__(parent)

	def load_data(self):
		# Construct filename path
		filename = self.path + self.data.split()[1][1:-1]

		print(type(self).__name__ + " Loading file " + filename)

		# try:
		# Create a mesh object and load the PLY file
		self.ply = PLY(filename)
		# except:
		# 	print(sys.exc_info()[0])

		if self.ply:
			# Get the name of the MTL file referenced inside the PLY file and add it to our data string for parsing
			print("Material filename:", self.ply.material_file)
			mtl_filename = self.path + self.ply.material_file

			print(type(self).__name__ + " Loading file " + mtl_filename)

			# Create a MDL_NODE_MATERIAL child node
			mdl_node_material = self.create_node_from_type('MATERIAL', self)
			#mdl_node_material.parent = self
			mdl_node_material.path = self.path

			# Load the MTL file
			mdl_node_material.open_file(mtl_filename)

			# Add the new material node to our child nodes
			self.nodes.append(mdl_node_material)

		# Call our superclass load_data() method. This will also call the load_data() method of our newly created child MDL_NODE_MATERIAL
		super(MDL_NODE_VOLUMEVIEW, self).load_data()

	def build_blender_data(self, blender_context):
		from mdl_node_bone import MDL_NODE_BONE
		import bpy
		from bpy_extras.io_utils import unpack_list, unpack_face_list
		from bpy_extras.image_utils import load_image

		super(MDL_NODE_VOLUMEVIEW, self).build_blender_data(blender_context)

		if self.ply:
			print(type(self).__name__ + ".build_blender_data()")

			bone_name = None
			naterial_node = None
			diffuse_node = None

			parent_node = self.parent

			# Get parents bone name
			while True:
				# Check if we found a bone node
				if type(parent_node) == MDL_NODE_BONE:
					bone_name = parent_node.bone_name
					break
				# Check if we reached the root node without finding a bone node
				elif parent_node == None:
					raise Exception("No parent bone node found")
				# Otherwise get the next parent
				else:
					parent_node = parent_node.parent

			# Create a new mesh with our parents bone name
			self.blender_mesh = bpy.data.meshes.new(bone_name)

			# Load vertices data into the mesh
			self.blender_mesh.vertices.add(len(self.ply.positions))
			self.blender_mesh.vertices.foreach_set("co", unpack_list(self.ply.positions))

			# Load face data into the mesh
			self.blender_mesh.tessfaces.add(len(self.ply.indeces))
			self.blender_mesh.tessfaces.foreach_set("vertices", unpack_list(self.ply.indeces))

			# Validate mesh
			self.blender_mesh.validate()

			# Update mesh
			self.blender_mesh.update(calc_edges=True)

			# Create a new UV layer
			self.blender_mesh.uv_textures.new()

			# Get the mesh UV layer
			uv_layer = self.blender_mesh.uv_layers.active

			# Process all faces of the mesh
			for face in self.blender_mesh.polygons:
				# Process all loops of the mesh
				for loop_index in face.loop_indices:
					# Use loop_index to get to the actual loop and then get the vertex index from it
					vertex_index = self.blender_mesh.loops[loop_index].vertex_index
					# With the vertex index, append the UV data from that vertex to the UV array
					uv_layer.data[loop_index].uv = self.ply.UVs[vertex_index]

			# Check if we have a material child node
			for node in self.nodes:
				if type(node) == MDL_NODE_MATERIAL:
					material_node = node

			# Check if the material node has a diffuse node
			for node in material_node.nodes:
				if type(node) == MDL_NODE_DIFFUSE:
					diffuse_node = node

			# Set the texture
			if diffuse_node:
				for uv_face in self.blender_mesh.uv_textures.active.data:
					uv_face.image = diffuse_node.blender_images[diffuse_node.texturename]