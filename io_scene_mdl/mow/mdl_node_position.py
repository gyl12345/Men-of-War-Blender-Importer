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

class MDL_NODE_POSITION(MDL_NODE):
	def __init__(self, parent):
		super(MDL_NODE_POSITION, self).__init__(parent)

	def load_data(self):
		# Explode the position values into separate strings
		values = self.data.split()
		# Assert that all 3 position values are present (including the Position tag)
		if len(values) != 4:
			raise Exception("Position data incomplete")

		self.position = ( float(values[1]), float(values[2]), float(values[3]) )

		super(MDL_NODE_POSITION, self).load_data()