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

class MDL_NODE_MATRIX34(MDL_NODE):
	def __init__(self, parent):
		self.orientation = None
		self.position = None
		self.orientation3x3 = []
		super(MDL_NODE_MATRIX34, self).__init__(parent)

	def load_data(self):
		# Explode the matrix values into separate strings
		values = self.data.split()
		# Assert that all 12 matrix values are present (including the "Matrix34" tag)
		if len(values) != 13:
			raise Exception("Matrix data incomplete")

		# Build the orientation matrix
		self.orientation = (
			( float(values[1]), float(values[2]), float(values[3]), float(0.0) ),
			( float(values[4]), float(values[5]), float(values[6]), float(0.0) ),
			( float(values[7]), float(values[8]), float(values[9]), float(0.0) ),
			( float(0.0), float(0.0), float(0.0), float(1.0) )
		)

		# # Build the orientation matrix
		# self.orientation_vol = (
		# 	( float(values[1]), float(values[4]), float(values[7]), float(0.0) ),
		# 	( float(values[2]), float(values[5]), float(values[8]), float(0.0) ),
		# 	( float(values[3]), float(values[6]), float(values[9]), float(0.0) ),
		# 	( float(0.0), float(0.0), float(0.0), float(1.0) )
		# )

		self.matrix_4x4 = (
			( float(values[1]), float(values[2]), float(values[3]), float(values[10]) ),
			( float(values[4]), float(values[5]), float(values[6]), float(values[11]) ),
			( float(values[7]), float(values[8]), float(values[9]), float(values[12]) ),
			( float(0.0), float(0.0), float(0.0), float(1.0) )
		)

		# # Build the orientation matrix
		# self.orientation = (
		# 	( float(values[1]), float(values[4]), float(values[7]), float(0.0) ),
		# 	( float(values[2]), float(values[5]), float(values[8]), float(0.0) ),
		# 	( float(values[3]), float(values[6]), float(values[9]), float(0.0) ),
		# 	( float(0.0), float(0.0), float(0.0), float(1.0) )
		# )

		# Build the orientation matrix
		self.orientation3x3 = ( float(values[1]), float(values[2]), float(values[3]), float(values[4]), float(values[5]), float(values[6]), float(values[7]), float(values[8]), float(values[9]) )

		# Build the translation vector
		self.position = ( float(values[10]), float(values[11]), float(values[12]) )

		super(MDL_NODE_MATRIX34, self).load_data()