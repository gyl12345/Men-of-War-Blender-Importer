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
from mdl_node_skeleton import MDL_NODE_SKELETON
from mdl_node_position import MDL_NODE_POSITION
from mdl_node_orientation import MDL_NODE_ORIENTATION
from mdl_node_matrix34 import MDL_NODE_MATRIX34 
from mdl_node_volume import MDL_NODE_VOLUME
from mdl_node_lodview import MDL_NODE_LODVIEW
from mdl_node_volumeview import MDL_NODE_VOLUMEVIEW

class MDL_NODE_BONE(MDL_NODE):
	def __init__(self, parent):
		self.bone_name = None
		self.blender_object_name = None
		self.blender_bone_name = None
		# blender_object = None
		# blender_bone = None
		self.parent_skeleton_node = None
		self.orientation_matrix = None
		super(MDL_NODE_BONE, self).__init__(parent)

		# Find our parent skeleton node
		self.find_skeleton_parent()
		# Let our parent skeleton node know that we exist
		self.register_on_skeleton()

	def find_skeleton_parent(self):
		# Check if still don't have a reference to our parent skeleton node
		if self.parent_skeleton_node == None:
			node = self
			# Find the skeleton node
			while type(node) != MDL_NODE_SKELETON and node != None:
				node = node.parent
			# Check if we found a skeleton node
			if type(node) == MDL_NODE_SKELETON:
				# Set this node as our skeleton parent
				self.parent_skeleton_node = node

	def register_on_skeleton(self):
		# Check if we have a skeleton parent
		if self.parent_skeleton_node:
			print("Trying to register on skeleton")
			self.parent_skeleton_node.register_bone_node(self)

	def get_blender_orientation_matrix(self, matrix=None):
		import bpy
		import mathutils

		if not matrix:
			matrix = mathutils.Matrix().to_3x3()

		parent_node = self.find_parent(MDL_NODE_BONE)
		if parent_node:
			return parent_node.get_blender_orientation_matrix() * self.orientation_matrix.inverted()
		else:
			return self.orientation_matrix.inverted()

	def get_blender_bone(self):
		blender_armature = None
		bone = None

		# Get the armature rig from our parent skeleton node
		if self.parent_skeleton_node:
			blender_armature = self.parent_skeleton_node.get_blender_armature()

		# Get the pose bone
		bone = blender_armature.bones[self.blender_bone_name]

		# Return the pose bone
		return bone

	def get_blender_pose_bone(self):
		blender_rig = None
		pose_bone = None

		# Get the armature rig from our parent skeleton node
		if self.parent_skeleton_node:
			blender_rig = self.parent_skeleton_node.get_blender_rig()

		# Get the pose bone
		if blender_rig:
			return blender_rig.pose.bones[self.blender_bone_name]
		else:
			return None

	def get_blender_edit_bone(self):
		blender_armature = None
		edit_bone = None

		# Get the armature rig from our parent skeleton node
		if self.parent_skeleton_node:
			blender_armature = self.parent_skeleton_node.get_blender_armature()

		# Get the pose bone
		if blender_armature:
			return blender_armature.edit_bones[self.blender_bone_name]
		else:
			return None

	def get_blender_object(self):
		import bpy

		if self.blender_object_name:
			return bpy.data.objects[self.blender_object_name]
		else:
			return None

	def load_data(self):
		# Split the parameters of this bone into two possible components
		tokens = self.data.split()[1:3]

		# Check if we find the name of this bone
		for token in tokens:
			if token[0] == '"':
				self.bone_name = token[1:-1]

		# Check if we haven't found the bone name
		if self.bone_name == None:
			# Set a dummy name
			self.bone_name = '<unknown>'

		super(MDL_NODE_BONE, self).load_data()

	def build_blender_armature(self, blender_context):
		import bpy
		import mathutils

		skeleton_node = None
		blender_armature = None
		blender_rig = None
		parent_blender_edit_bone = None

		position_node = None
		orientation_node = None
		matrix34_node = None

		# Check if we are just a property of a Volume node
		if type(self.parent) == MDL_NODE_VOLUME:
			# We are just a volume property, so don't do anything
			pass
		else:
			print(type(self).__name__ + " Building bone " + self.bone_name)

			# Find our parent skeleton node
			skeleton_node = self.find_parent(MDL_NODE_SKELETON)

			# Check if we found the skeleton node
			if skeleton_node == None:
				raise Exception("Unable to find skeleton node")

			# Get a reference of the rig
			blender_rig = skeleton_node.get_blender_rig()

			# Search for important child nodes
			for node in self.nodes:
				if type(node) == MDL_NODE_POSITION:
					position_node = node
				elif type(node) == MDL_NODE_ORIENTATION:
					orientation_node = node
					self.orientation_node = orientation_node
				elif type(node) == MDL_NODE_MATRIX34:
					matrix34_node = node

			# Select the rig
			blender_context.scene.objects.active = blender_rig

			# Enter edit mode
			bpy.ops.object.editmode_toggle()

			# Get a reference of the armature
			blender_armature = skeleton_node.get_blender_armature()

			# Create the bone
			blender_edit_bone = blender_armature.edit_bones.new(self.bone_name)
			self.blender_bone_name = blender_edit_bone.name

			# Find a parent bone node
			parent_node = self.find_parent(MDL_NODE_BONE)

			# Check if we found a node
			if parent_node:
				# Get the reference of its blender edit bone
				parent_blender_edit_bone = parent_node.get_blender_edit_bone()
			else:
				print("Found no parent bone node!!!")

			if parent_blender_edit_bone == None:
				print("No bone exists!!!")

			# Set our bones head to the tail of our parent bone
			if parent_blender_edit_bone:
				print("Linking bone to", parent_blender_edit_bone.name)
				blender_edit_bone.parent = parent_blender_edit_bone
				blender_edit_bone.head = parent_blender_edit_bone.tail
			else:
				print("Positioning root bone at world center")
				blender_edit_bone.head = (0,0,0)

			# Attach bones head to parents tail
			blender_edit_bone.use_connect = True

			# # Do not inherit parents rotation
			#blender_edit_bone.use_inherit_rotation = False

			# # Do not inherit parents scale
			blender_edit_bone.use_inherit_scale = True
			
			# Transofrmations are relative to parent
			#if parent_blender_edit_bone:
			# blender_edit_bone.use_relative_parent = True
			# if blender_edit_bone.use_relative_parent == False:
			# 	print('Relative parent still false!!!')

			#blender_edit_bone.use_local_location = False

			blender_edit_bone.envelope_distance = 4.0

#			blender_edit_bone.tail = blender_edit_bone.head + mathutils.Vector((0,0,0.001))
#			blender_edit_bone.tail = mathutils.Vector((0,0,0.001))

			# Set a default identity orientation matrix as our orientation matrix
			self.orientation_matrix = mathutils.Matrix().to_3x3()

			# Retrieve our parents orientation matrix
			parent_orientation_matrix = mathutils.Matrix().to_3x3()
			if parent_node:
				parent_orientation_matrix = parent_node.get_blender_orientation_matrix()

			# If we have position data, set objects location
			if position_node != None:
				print("Applying position data")

				# Check if position is zero (blender can't handle zero-length bones)
				if position_node.position == (0,0,0):
					position_node.position = (0,0,0.001)

				# Set position
				blender_edit_bone.tail = blender_edit_bone.head + ( parent_orientation_matrix * mathutils.Vector(position_node.position) )

			# If we have orientation data, set objects orientation
			if orientation_node != None:
				print("Applying orientation data")

				# Set position
				blender_edit_bone.tail = blender_edit_bone.head + ( parent_orientation_matrix * mathutils.Vector((0,0,0.001)) )

				# Replace our default orientation matrix with the one provided in the orientation data
				#self.orientation_matrix = mathutils.Matrix(orientation_node.orientation).to_3x3()

			# If we have a matrix34 node, set objects orientation and location from it
			if matrix34_node != None:
				print("Applying matrix data")

				# Check if position is zero (blender can't handle zero-length bones)
				if matrix34_node.position == (0,0,0):
					matrix34_node.position = (0,0,0.001)				

				# Set position
				blender_edit_bone.tail = blender_edit_bone.head + ( parent_orientation_matrix * mathutils.Vector(matrix34_node.position) )

				# Replace our default orientation matrix with the one provided in the matrix data
				self.orientation_matrix = mathutils.Matrix(matrix34_node.orientation).to_3x3()

			# Exit edit mode
			bpy.ops.object.editmode_toggle()

			# bpy.ops.object.mode_set(mode='OBJECT')
			# bpy.ops.object.select_all(action='DESELECT')

			# blender_context.scene.update()

			# # Set transforms relative to parent
			# blender_edit_bone.use_relative_parent = True
			#blender_armature.bones[self.bone_name].use_relative_parent = True
			# bpy.data.armatures['Armature'].bones[self.bone_name].use_relative_parent = True

		# Enter object mode
		bpy.ops.object.mode_set(mode='OBJECT')

		super(MDL_NODE_BONE, self).build_blender_armature(blender_context)

	def build_blender_data(self, blender_context):
		import bpy
		import mathutils

		super(MDL_NODE_BONE, self).build_blender_data(blender_context)

		# Check if we are a bone of a Skeleton or a "bone" property of a Volume object
		if type(self.parent) == MDL_NODE_VOLUME:
			# We are just a volume property, so dont do anything
			pass
		else:
			lod_node = None
			mesh_node = None
			position_node = None
			orientation_node = None
			matrix34_node = None
			blender_mesh = None

			# Search for important child nodes
			for node in self.nodes:
				if type(node) == MDL_NODE_VOLUMEVIEW:
					mesh_node = node
				elif type(node) == MDL_NODE_LODVIEW:
					lod_node = node
				elif type(node) == MDL_NODE_POSITION:
					position_node = node
				elif type(node) == MDL_NODE_ORIENTATION:
					orientation_node = node
				elif type(node) == MDL_NODE_MATRIX34:
					matrix34_node = node

			# If we found a LOD node, get the first VolumeView from it
			if lod_node:
				mesh_node = lod_node.nodes[0]

			# If we found a mesh node, get the blender mesh from it
			if mesh_node:
				blender_mesh = mesh_node.blender_mesh

			# Create a new object with the name of this bone and (if available) a mesh
			blender_object = bpy.data.objects.new(self.bone_name, blender_mesh)
			self.blender_object_name = blender_object.name

			if blender_object:
				# If we have position data, set objects location
				if position_node:
					blender_object.location = position_node.position

				# If we have orientation data, set objects orientation
				if orientation_node:
					pass
					#blender_object.scale = (orientation_node.orientation[0][0], orientation_node.orientation[1][1], orientation_node.orientation[2][2])
					#blender_object.rotation_quaternion = mathutils.Matrix(orientation_node.orientation).to_3x3().to_quaternion()

				# If we have a matrix34 node, set objects orientation and location from it
				if matrix34_node:
					blender_object.matrix_local = matrix34_node.orientation
					blender_object.location = matrix34_node.position
					
					#blender_object.rotation_quaternion = mathutils.Matrix(matrix34_node.orientation).to_3x3().to_quaternion()
					#blender_object.matrix_world = matrix34_node.matrix_4x4

	def build_blender_scene(self, blender_context):
		import bpy

		blender_object = self.get_blender_object()

		# Don't do anything if we don't have a blender object
		if blender_object == None:
			return

		# Link our blender object to the scene
		blender_context.scene.objects.link(blender_object)

		parent_node = self.parent

		print("Object %s is starting search for a parent bone..." % blender_object.name)

		# Search for a parent bone node
		while True:
			print("... testing node of type %s " % type(parent_node))
			if type(parent_node) == MDL_NODE_BONE:
				# Set the parents bone node blender objects as our parent object
				blender_object.parent = parent_node.get_blender_object()

				if blender_object.parent == None:
					print("... found bone %s with no blender object" % parent_node.bone_name)
					parent_blender_bone = parent_node.get_blender_bone()
					if parent_blender_bone:
						blender_object.parent = parent_blender_bone
				break
			elif parent_node == None:
				break
			else:
				parent_node = parent_node.parent

		# if blender_object.parent == None:
		# 	print("Object %s has found no parent!!!" % blender_object.name)
		# else:
		# 	# Now unparent our object, keeping its current transformation
		# 	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
		# 	bpy.ops.object.select_all(action='DESELECT')
		# 	blender_object.select = True
		# 	bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

		# # Parent our object to the bone
		# skeleton_node = self.parent_skeleton_node
		# if skeleton_node:
		# 	# Enter pose mode
		# 	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
		# 	# Deselect any selected object
		# 	bpy.ops.object.select_all(action='DESELECT')
		# 	# Select the mesh object
		# 	blender_object.select = True
		# 	# Get the blender rig from the skeleton node
		# 	blender_rig = skeleton_node.get_blender_rig()
		# 	# Select armature
		# 	blender_rig.select = True
		# 	# Enter pose mode
		# 	bpy.ops.object.mode_set(mode='POSE', toggle=False)
		# 	# Get the pose bone
		# 	pose_bone = self.get_blender_pose_bone()
		# 	# Select the pose bone
		# 	blender_rig.data.bones.active = pose_bone.bone
		# 	# Parent mesh object to pose bone
		# 	bpy.ops.object.parent_set(type='BONE')

		# 	# if pose_bone:
		# 	# 	# Set relative parent
		# 	# 	pose_bone.bone.use_relative_parent = True

		# bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
		# bpy.ops.object.select_all(action='DESELECT')

		super(MDL_NODE_BONE, self).build_blender_scene(blender_context)

	# def find_bone_node_down(self, entity):
	# 	# Check if we are the bone being searched for
	# 	if self.bone_name == entity:
	# 		return self

	# 	# Search the child nodes
	# 	for node in self.nodes:
	# 		# Check if this child node is a bone node
	# 		if type(node) == MDL_NODE_BONE:
	# 			# Check if its name matches the entity we are searching for
	# 			if node.bone_name == entity:
	# 				return node
	# 			# Search the children of the bone node
	# 			bone_node = node.find_bone_node_down(entity)
	# 			# Check if we found a bone node
	# 			if bone_node != None:
	# 				# Return the bone node
	# 				return bone_node

	# 	# If we reached this its because we found nothing
	# 	return None