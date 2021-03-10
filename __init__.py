bl_info = {
    "name": "Steroids",
    "description": "Blender on steroids",
    "author": "Salai Vedha Viradhan",
    "version": (1, 0),
    "category": "Interface",
    "blender": (2, 80, 0),
}

import bpy
import sys
import inspect
import pkgutil
from . import steroid_presets


class VIEW3D_MT_steroids(bpy.types.Menu):
    bl_label = "    Steroids    "
    bl_idname = "STEROID_MT_steroids"

    def draw(self, context):
        layout = self.layout
        layout.menu("VIEW3D_MT_steroids_mesh", text=self.get_text("Mesh"), icon='OUTLINER_OB_MESH')
        layout.menu("VIEW3D_MT_steroids_modifiers", text=self.get_text("Modifiers"), icon='MODIFIER')
        layout.menu("VIEW3D_MT_steroids_particles", text=self.get_text("Particles"), icon='PARTICLES')
        layout.menu("VIEW3D_MT_steroids_camera", text=self.get_text("Camera"), icon='VIEW_CAMERA')
        layout.menu("VIEW3D_MT_steroids_rendering", text=self.get_text("Rendering"), icon='SCENE')

    def get_text(self, txt):
        return " "*4 + txt + " "*8

def draw_steroids_menu(self, context):
    layout = self.layout
    layout.menu(VIEW3D_MT_steroids.bl_idname)


class VIEW3D_MT_PIE_steroids(bpy.types.Menu):
    bl_label = "Steroids"
    bl_idname = "STEROID_MT_PIE_steroids"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        pie.menu("VIEW3D_MT_steroids_mesh", text="Mesh", icon='OUTLINER_OB_MESH')
        pie.menu("VIEW3D_MT_steroids_modifiers", text="Modifiers", icon='MODIFIER')
        pie.menu("VIEW3D_MT_steroids_particles", text="Particles", icon='PARTICLES')
        pie.menu("VIEW3D_MT_steroids_camera", text="Camera", icon='VIEW_CAMERA')
        pie.menu("VIEW3D_MT_steroids_rendering", text="Rendering", icon='RESTRICT_RENDER_OFF')


class VIEW3D_MT_steroids_camera(bpy.types.Menu):
    bl_label = "Camera"

    def draw(self, context):
        layout = self.layout
        for cls in camera_classes:
            layout.operator(cls.bl_idname, text=cls.bl_label)


class VIEW3D_MT_steroids_particles(bpy.types.Menu):
    bl_label = "Particles"

    def draw(self, context):
        layout = self.layout
        for cls in particle_classes:
            layout.operator(cls.bl_idname, text=cls.bl_label)
    
        
class VIEW3D_MT_steroids_modifiers(bpy.types.Menu):
    bl_label = "Modifiers"

    def draw(self, context):
        layout = self.layout
        for cls in modifier_classes:
            layout.operator(cls.bl_idname, text=cls.bl_label)


class VIEW3D_MT_steroids_rendering(bpy.types.Menu):
    bl_label = "Rendering"

    def draw(self, context):
        layout = self.layout
        for cls in rendering_classes:
            layout.operator(cls.bl_idname, text=cls.bl_label)


class VIEW3D_MT_steroids_mesh(bpy.types.Menu):
    bl_label = "Mesh"

    def draw(self, context):
        layout = self.layout
        for cls in mesh_classes:
            layout.operator(cls.bl_idname, text=cls.bl_label)


operator_classes = []

mesh_classes = []
modifier_classes = []
particle_classes = []
rendering_classes = []
camera_classes = []

def register():
    package = steroid_presets
    modules = []
    prefix = package.__name__ + '.'
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
        modules.append(__import__(modname, fromlist='dummy'))

    for module in modules:
        for name, obj in inspect.getmembers(sys.modules[module.__name__]):
            if inspect.isclass(obj) and hasattr(obj, "bl_idname"):
                operator_classes.append(obj)
            
                if obj.category == 'camera':
                    camera_classes.append(obj)
                    continue

                if obj.category == 'mesh':
                    mesh_classes.append(obj)
                    continue

                if obj.category == 'modifiers':
                    modifier_classes.append(obj)
                    continue

                if obj.category == 'particles':
                    particle_classes.append(obj)
                    continue
                
                if obj.category == 'rendering':
                    rendering_classes.append(obj)
                    continue
        
    for cls in operator_classes:
        bpy.utils.register_class(cls)
    
    bpy.utils.register_class(VIEW3D_MT_steroids_camera)
    bpy.utils.register_class(VIEW3D_MT_steroids_mesh)
    bpy.utils.register_class(VIEW3D_MT_steroids_modifiers)
    bpy.utils.register_class(VIEW3D_MT_steroids_particles)
    bpy.utils.register_class(VIEW3D_MT_steroids_rendering)
    bpy.utils.register_class(VIEW3D_MT_steroids)
    bpy.utils.register_class(VIEW3D_MT_PIE_steroids)

    bpy.types.VIEW3D_MT_editor_menus.append(draw_steroids_menu)
    
def unregister():
    bpy.types.VIEW3D_MT_editor_menus.remove(draw_steroids_menu)

    bpy.utils.unregister_class(VIEW3D_MT_PIE_steroids)
    bpy.utils.unregister_class(VIEW3D_MT_steroids)
    bpy.utils.unregister_class(VIEW3D_MT_steroids_rendering)
    bpy.utils.unregister_class(VIEW3D_MT_steroids_particles)
    bpy.utils.unregister_class(VIEW3D_MT_steroids_modifiers)
    bpy.utils.unregister_class(VIEW3D_MT_steroids_mesh)
    bpy.utils.unregister_class(VIEW3D_MT_steroids_camera)

    operator_classes.reverse()
    for cls in operator_classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
