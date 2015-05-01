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

from __future__ import print_function

class MDL_NODE(object):
	def __init__(self, parent):
		self.parent = parent
		self.data 	= None
		self.path   = None
		self.nodes  = []

	def print_type(self, depth=0):
		node_name = ''

		for i in range(0, depth):
			node_name += '  '

		node_name += type(self).__name__

		print(node_name)

		depth += 1

		for node in self.nodes:
			node.print_type(depth)

	@staticmethod
	def create_node_from_type(type, parent):
		module_name = 'mdl_node_' + type.lower()
		class_name = module_name.upper()
		m = __import__(module_name)
		return getattr(m, class_name)(parent)

	def parse_mdl_node(self, data):
		self.data = data

		child_node_type = ''
		child_node_data = ''
		bracket_counter = 0
		bracket_start   = 0
		bracket_end     = 0

		searching_for_closing_bracket = False

		# Get number of data lines
		length = len(self.data)

		i = 0

		while i < length:
			# Found open bracket
			if self.data[i] == '{':
				# Increment our bracket counter
				bracket_counter += 1
				# Check if this is the first open bracket we found (new node)
				if bracket_counter == 1:
					# Enter a state to find the corresponding closing bracket of this new node
					searching_for_closing_bracket = True
					# Save the index of the starting bracket
					bracket_start = i

			# Found closing bracket (at beginning or end of string)
			elif self.data[i] == '}':
				# Decrement our bracket counter
				bracket_counter -= 1
				# Check if our bracket counter reached 0
				if bracket_counter == 0:
					# Check if we were searching for a closing bracket
					if searching_for_closing_bracket == True:						
						# We are not searching for it anymore
						searching_for_closing_bracket = False
						# Store child node data (without enclosing brackets)
						child_node_data = self.data[bracket_start+1:i]
						# Get node type
						child_node_type = child_node_data[0:].partition(' ')[0]
						# Create a new child node with this node as its parent
						child_node = self.create_node_from_type(child_node_type, self)
#						child_node.parent = self
						child_node.path = self.path
						# Parse the child data
						child_node.parse_mdl_node(child_node_data)
						# Add node to our list of children nodes
						self.nodes.append(child_node)
						# Clear things up for further processing
						child_node_name = ''
						child_node_data = []

			# Increment character index
			i += 1

		if searching_for_closing_bracket == True or bracket_counter > 0:
			raise Exception("Reached end of data while expecting a closing bracket")

	def find_parent(self, node_type):
		parent_node = self.parent

		while(True):
			# Return if we found the specified node or we reached the end of the hierarchy
			if type(parent_node) == node_type or parent_node == None:
				return parent_node
			# Step up one level
			parent_node = parent_node.parent

	def load_data(self):
		for node in self.nodes:
			node.load_data()

	def build_blender_armature(self, blender_context):
		for node in self.nodes:
			node.build_blender_armature(blender_context)

	def build_blender_data(self, blender_context):
		for node in self.nodes:
			node.build_blender_data(blender_context)

	def build_blender_scene(self, blender_context):
		for node in self.nodes:
			node.build_blender_scene(blender_context)

	def build_blender_animation(self, blender_context):
		for node in self.nodes:
			node.build_blender_animation(blender_context)