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

bl_info = {
    "name": "Men of War MDL Format",
    "author": "Björn Martins Paz",
    "version": (1, 0, 0),
    "blender": (2, 7, 2),
    "location": "File > Import-Export",
    "description": "Import Men of War MDL",
    "warning": "",
    "support": 'TESTING',
    "category": "Import-Export"}

if "bpy" in locals():
    import imp
    if "import_mdl" in locals():
        imp.reload(import_mdl)
    if "export_mdl" in locals():
        imp.reload(export_mdl)


import bpy
from bpy.props import (BoolProperty,
                       FloatProperty,
                       StringProperty,
                       EnumProperty,
                       )
from bpy_extras.io_utils import (ImportHelper,
                                 ExportHelper,
                                 path_reference_mode,
                                 axis_conversion,
                                 )


class ImportMDL(bpy.types.Operator, ImportHelper):
    """Load a Men of War MDL File"""
    bl_idname = "import_scene.mdl"
    bl_label = "Import MDL"
    bl_options = {'PRESET', 'UNDO'}

    filename_ext = ".def"
    filter_glob = StringProperty(
            default="*.def",
            options={'HIDDEN'},
            )

    use_animations = BoolProperty(
            name="Animations",
            description="Import animations",
            default=True,
            )

    def execute(self, context):
        # print("Selected: " + context.active_object.name)
        from . import import_mdl

        keywords = self.as_keywords()
#        keywords['filepath'] = self.filepath

        return import_mdl.load(self, context, **keywords)

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.prop(self, "use_animations")

class ExportMDL(bpy.types.Operator, ExportHelper):
    """Save a Men of War MDL File"""

    bl_idname = "export_scene.mdl"
    bl_label = 'Export MDL'
    bl_options = {'PRESET'}

    filename_ext = ".mdl; .def"
    filter_glob = StringProperty(
            default="*.mdl;*.def",
            options={'HIDDEN'},
            )

    def execute(self, context):
        from . import export_mdl

        from mathutils import Matrix

        return export_mdl.save(self, context, self.filepath)


def menu_func_import(self, context):
    self.layout.operator(ImportMDL.bl_idname, text="Men of War (.def)")


def menu_func_export(self, context):
    self.layout.operator(ExportMDL.bl_idname, text="Men of War (.def)")


def register():
    bpy.utils.register_module(__name__)

    bpy.types.INFO_MT_file_import.append(menu_func_import)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_module(__name__)

    bpy.types.INFO_MT_file_import.remove(menu_func_import)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()
