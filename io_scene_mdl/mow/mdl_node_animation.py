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

from mdl_node_root import MDL_NODE_ROOT
from mdl_node_bone import MDL_NODE_BONE
from mdl_node_skeleton import MDL_NODE_SKELETON
from mdl_node_sequence import MDL_NODE_SEQUENCE
from anm_frame_position import ANM_FRAME_POSITION
from anm_frame_quaternion import ANM_FRAME_QUATERNION

class MDL_NODE_ANIMATION(MDL_NODE):
	def __init__(self, parent):
		super(MDL_NODE_ANIMATION, self).__init__(parent)

	def build_blender_animation(self, blender_context):
		super(MDL_NODE_ANIMATION, self).build_blender_animation(blender_context)

		self.build_blender_animation_mesh(blender_context)
		#self.build_blender_animation_bone(blender_context)

	def build_blender_animation_bone(self, blender_context):
		import bpy

		# Go trough all animations (sequences) of this animation node
		for seq in self.nodes:
			if type(seq) == MDL_NODE_SEQUENCE:
				# Check if this sequence has animation data loaded
				if seq.anm == None:
					continue

				entities = {}
				time_of_last_frame = 0

				print("Sequence:", seq.name)

				# Build a lookup table of the entities
				for index, entity in enumerate(seq.anm.entities):
					entities[index] = self.find_bone_node(entity)

				# Process every frame of this sequence
				for frame in seq.anm.keyframes:
					print("Frame time:", frame.time)
					# Keep the time of the last frame to calculate action strip offsets inside the NLA track
					time_of_last_frame = frame.time

					# Go trough every frame event
					for event in frame.events:
						print("Event index:", event.index)
						print("Entity:", seq.anm.entities[event.index])

						# Get the blender object from our lookup table
						bone_node = entities[event.index]
						skeleton_node = bone_node.parent_skeleton_node

						if skeleton_node:
							# Get the blender rig from the skeleton node
							blender_rig = skeleton_node.get_blender_rig()

						# Check if the rig already has animation data
						if not blender_rig.animation_data:
							# Create new animation data for the rig
							blender_rig.animation_data_create()

						# Get the animation data
						animation_data = blender_rig.animation_data

						# Enter pose mode
#						bpy.ops.object.mode_set(mode='POSE')

						# Get the pose bone
#						blender_pose_bone = entities[event.index].get_blender_pose_bone()

						# Compile action name
						bone_name   = entities[event.index].blender_bone_name
						action_name = bone_name + '_' + seq.name

						# Check if the rig already has an NLA track for this bone
						if bone_name not in animation_data.nla_tracks:
							# Create new NLA Track for this bone
							nla_track = animation_data.nla_tracks.new()
							# Name the NLA Track the after its bone name
							nla_track.name = bone_name

						# Get the (already existing or newly created) NLA track
						nla_track = animation_data.nla_tracks[bone_name]

						# Check if current action already exists
						if action_name not in bpy.data.actions:
							# Create a new Blender animation action for this sequence
							bpy.data.actions.new(name=action_name)

						# Get the animation action
						action = bpy.data.actions[action_name]

						# # Build the name of the data path
						# data_path = 'pose.bones["' + bone_name + '"].location'

						# # Check if action already has location fcurves, and if not, create new ones
						# fcurve_lx = next((fcurve for fcurve in action.fcurves if fcurve.data_path == data_path and fcurve.array_index == 0), None)
						# if fcurve_lx == None:
						# 	fcurve_lx = action.fcurves.new(data_path=data_path, index=0)

						# fcurve_ly = next((fcurve for fcurve in action.fcurves if fcurve.data_path == data_path and fcurve.array_index == 1), None)
						# if fcurve_ly == None:
						# 	fcurve_ly = action.fcurves.new(data_path=data_path, index=1)

						# fcurve_lz = next((fcurve for fcurve in action.fcurves if fcurve.data_path == data_path and fcurve.array_index == 2), None)
						# if fcurve_lz == None:
						# 	fcurve_lz = action.fcurves.new(data_path=data_path, index=2)

						# Create new rotation W, X, Y and Z transformation curve if necessary
#						blender_pose_bone.rotation_mode = "QUATERNION"

						data_path = 'pose.bones["' + bone_name + '"].rotation_quaternion'

						fcurve_rw = next((fcurve for fcurve in action.fcurves if fcurve.data_path == data_path and fcurve.array_index == 0), None)
						if fcurve_rw == None:
							fcurve_rw = action.fcurves.new(data_path=data_path, index=0)

						fcurve_rx = next((fcurve for fcurve in action.fcurves if fcurve.data_path == data_path and fcurve.array_index == 1), None)
						if fcurve_rx == None:
							fcurve_rx = action.fcurves.new(data_path=data_path, index=1)

						fcurve_ry = next((fcurve for fcurve in action.fcurves if fcurve.data_path == data_path and fcurve.array_index == 2), None)
						if fcurve_ry == None:
							fcurve_ry = action.fcurves.new(data_path=data_path, index=2)

						fcurve_rz = next((fcurve for fcurve in action.fcurves if fcurve.data_path == data_path and fcurve.array_index == 3), None)
						if fcurve_rz == None:
							fcurve_rz = action.fcurves.new(data_path=data_path, index=3)

						# Go trough every event property
						for prop in event.properties:
							# Check if this is a position property
							if type(prop) == ANM_FRAME_POSITION:
								pass
								# # Apply position transformation
								# fcurve_lx.keyframe_points.insert(float(frame.time), prop.x)
								# fcurve_ly.keyframe_points.insert(float(frame.time), prop.y)
								# fcurve_lz.keyframe_points.insert(float(frame.time), prop.z)
							# Check if this is a quaternion rotation property
							elif type(prop) == ANM_FRAME_QUATERNION:
								pass
								# Apply rotation transformation
								fcurve_rw.keyframe_points.insert(float(frame.time), prop.w)
								fcurve_rx.keyframe_points.insert(float(frame.time), prop.x)
								fcurve_ry.keyframe_points.insert(float(frame.time), prop.y)
								fcurve_rz.keyframe_points.insert(float(frame.time), prop.z)

				# Add newly created actions to the NLA track of its respective entity object
				for index, entity in enumerate(seq.anm.entities):
					# Compile action name of this entity
					bone_node = entities[index]
					action_name = bone_node.bone_name + '_' + seq.name

					# Get the NLA track
					nla_track = animation_data.nla_tracks[bone_node.bone_name]

					# Get entities action
					action = bpy.data.actions[action_name]

					# Add action strip to NLA track
					print("Adding action %s to NLA Track" % action_name)
					nla_track.strips.new(action_name, blender_context.scene.frame_current, action)

				# Increment the global frame cursor position to an amount equal to the time of this animation sequence
				blender_context.scene.frame_current += time_of_last_frame

		# Exit pose mode (enter object mode)
		bpy.ops.object.mode_set(mode='OBJECT')

	def build_blender_animation_mesh(self, blender_context):
		import bpy

		# Go trough all animations (sequences) of this animation node
		for seq in self.nodes:
			if type(seq) == MDL_NODE_SEQUENCE:
				# Check if this sequence has animation data loaded
				if seq.anm == None:
					continue

				entities = {}
				time_of_last_frame = 0

				print("Sequence:", seq.name)

				# Build a lookup table of the entities
				for index, entity in enumerate(seq.anm.entities):
					entities[index] = self.find_bone_node(entity)

				# Process every frame of this sequence
				for frame in seq.anm.keyframes:
					print("Frame time:", frame.time)
					# Keep the time of the last frame to calculate action strip offsets inside the NLA track
					time_of_last_frame = frame.time

					# Go trough every frame event
					for event in frame.events:
						print("Event index:", event.index)
						print("Entity:", seq.anm.entities[event.index])

						# Get the blender object from our lookup table
						blender_object_name = entities[event.index].blender_object_name
						blender_object = bpy.data.objects[blender_object_name]

						# Compile action name
						bone_name   = entities[event.index].bone_name
						action_name = bone_name + '_' + seq.name

						# Check if the object already has animation data
						if blender_object.animation_data == None:
							# Create new Blender animation data
							blender_object.animation_data_create()

						# Get the animation data
						animation_data = blender_object.animation_data

						# Check if the object already has an NLA track
						if not animation_data.nla_tracks:
							# Create new NLA Track for this object
							nla_track = animation_data.nla_tracks.new()
							# Name the NLA Track the after its bone name
							nla_track.name = bone_name

						# Get the NLA track
						nla_track = animation_data.nla_tracks[0]

						# Check if action already exists
						if action_name not in bpy.data.actions:
							# Create a new Blender animation action for this sequence
							bpy.data.actions.new(name=action_name)

						# Get the animation action
						action = bpy.data.actions[action_name]

						# Check if action already has location fcurves, and if not, create new ones
						fcurve_lx = next((fcurve for fcurve in action.fcurves if fcurve.data_path == 'location' and fcurve.array_index == 0), None)
						if fcurve_lx == None:
							fcurve_lx = action.fcurves.new(data_path="location", index=0)

						fcurve_ly = next((fcurve for fcurve in action.fcurves if fcurve.data_path == 'location' and fcurve.array_index == 1), None)
						if fcurve_ly == None:
							fcurve_ly = action.fcurves.new(data_path="location", index=1)

						fcurve_lz = next((fcurve for fcurve in action.fcurves if fcurve.data_path == 'location' and fcurve.array_index == 2), None)
						if fcurve_lz == None:
							fcurve_lz = action.fcurves.new(data_path="location", index=2)

						# Create new rotation W, X, Y and Z transformation curve if necessary
						blender_object.rotation_mode = "QUATERNION"
						fcurve_rw = next((fcurve for fcurve in action.fcurves if fcurve.data_path == 'rotation_quaternion' and fcurve.array_index == 0), None)
						if fcurve_rw == None:
							fcurve_rw = action.fcurves.new(data_path="rotation_quaternion", index=0)

						fcurve_rx = next((fcurve for fcurve in action.fcurves if fcurve.data_path == 'rotation_quaternion' and fcurve.array_index == 1), None)
						if fcurve_rx == None:
							fcurve_rx = action.fcurves.new(data_path="rotation_quaternion", index=1)

						fcurve_ry = next((fcurve for fcurve in action.fcurves if fcurve.data_path == 'rotation_quaternion' and fcurve.array_index == 2), None)
						if fcurve_ry == None:
							fcurve_ry = action.fcurves.new(data_path="rotation_quaternion", index=2)

						fcurve_rz = next((fcurve for fcurve in action.fcurves if fcurve.data_path == 'rotation_quaternion' and fcurve.array_index == 3), None)
						if fcurve_rz == None:
							fcurve_rz = action.fcurves.new(data_path="rotation_quaternion", index=3)

						# Go trough every event property
						for prop in event.properties:
							# Check if this is a position property
							if type(prop) == ANM_FRAME_POSITION:
								# Apply position transformation
								fcurve_lx.keyframe_points.insert(float(frame.time), prop.x)
								fcurve_ly.keyframe_points.insert(float(frame.time), prop.y)
								fcurve_lz.keyframe_points.insert(float(frame.time), prop.z)
							# Check if this is a quaternion rotation property
							elif type(prop) == ANM_FRAME_QUATERNION:
								# Apply rotation transformation
								fcurve_rw.keyframe_points.insert(float(frame.time), prop.w)
								fcurve_rx.keyframe_points.insert(float(frame.time), prop.x)
								fcurve_ry.keyframe_points.insert(float(frame.time), prop.y)
								fcurve_rz.keyframe_points.insert(float(frame.time), prop.z)

				# Add newly created actions to the NLA track of its respective entity object
				for index, entity in enumerate(seq.anm.entities):
					# Compile action name of this entity
					bone_node = entities[index]
					action_name = bone_node.bone_name + '_' + seq.name

					# Get blender object
					blender_object_name = bone_node.blender_object_name
					blender_object = bpy.data.objects[blender_object_name]

					# Get the NLA track
					nla_track = blender_object.animation_data.nla_tracks[0]

					# Get entities action
					action = bpy.data.actions[action_name]

					# Add action strip to NLA track
					print("Adding action %s to NLA Track" % action_name)
					nla_track.strips.new(action_name, blender_context.scene.frame_current, action)

				# Increment the global frame cursor position to an amount equal to the time of this animation sequence
				blender_context.scene.frame_current += time_of_last_frame

	def find_bone_node(self, entity):
		skeleton_node = self

		# Find the skeleton node
		while type(skeleton_node) != MDL_NODE_SKELETON and skeleton_node != None:
			skeleton_node = skeleton_node.parent

		if skeleton_node:
			print("Found skeleton node!")
			bone_node = skeleton_node.get_bone_node(entity)
			if bone_node:
				return bone_node

		# 	# If this is a bone node, keep it's reference as the upmost bone node we found so far
		# 	if type(node) == MDL_NODE_BONE:
		# 		upmost_bone_node = node

		# # Check if we found a bone node
		# if upmost_bone_node:
		# 	print("Found upmost bone node: ", upmost_bone_node.bone_name)
		# 	# Start the search downwards
		# 	bone_node = node.find_bone_node_down(entity)

		# 	# Check if we found a node
		# 	if bone_node != None:
		# 		# Return the found node
		# 		return bone_node

		raise Exception("Unable to find bone:", entity)