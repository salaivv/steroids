import bpy
from bpy.props import IntProperty, FloatProperty, BoolProperty

class STEROID_OT_camera_shift(bpy.types.Operator):
    """Adjust camera shift X/Y"""
    bl_idname = "steroid.camera_shift"
    bl_label = "Adjust Camera Shift"
    bl_options = {'REGISTER', 'UNDO'}
    category = 'camera'
    
    first_mouse_x: IntProperty()
    first_mouse_y: IntProperty()
    first_shift_x: FloatProperty()
    first_shift_y: FloatProperty()
    restrict_x: BoolProperty(default=True)
    restrict_y: BoolProperty(default=True)
    use_shift: FloatProperty(default=1.0)

    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            return context.mode == 'OBJECT' and context.scene.camera

    def modal(self, context, event):
        camera = context.scene.camera.data

        if event.type == 'MOUSEMOVE':
            delta_x = self.first_mouse_x - event.mouse_x
            delta_y = self.first_mouse_y - event.mouse_y
            camera.shift_x = self.first_shift_x - delta_x * 0.001 \
                                * self.use_shift * int(self.restrict_y)
            camera.shift_y = self.first_shift_y - delta_y * 0.001 \
                                * self.use_shift * int(self.restrict_x)

        if event.type == 'X' and event.value == 'PRESS':
            self.restrict_x = not self.restrict_x
            if not self.restrict_y:
                self.restrict_y = not self.restrict_y

        if event.type == 'Y' and event.value == 'PRESS':
            self.restrict_y = not self.restrict_y
            if not self.restrict_x:
                self.restrict_x = not self.restrict_x

        if event.type in ('LEFT_SHIFT', 'RIGHT_SHIFT') and event.value == 'PRESS':
            self.use_shift = 0.1

        if event.type in ('LEFT_SHIFT', 'RIGHT_SHIFT') and event.value == 'RELEASE':
            self.use_shift = 1

        elif event.type == 'LEFTMOUSE':
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            camera.shift_x = self.first_shift_x
            camera.shift_y = self.first_shift_y
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.first_mouse_x = event.mouse_x
        self.first_mouse_y = event.mouse_y
        self.first_shift_x = context.scene.camera.data.shift_x
        self.first_shift_y = context.scene.camera.data.shift_y

        self.restrict_x = True
        self.restrict_y = True
        self.use_shift = 1.0

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

class STEROID_OT_reset_camera_shift(bpy.types.Operator):
    """Adjust camera shift X/Y"""
    bl_idname = "steroid.reset_camera_shift"
    bl_label = "Reset Camera Shift"
    bl_options = {'REGISTER', 'UNDO'}
    category = 'camera'

    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            return context.mode == 'OBJECT'

    def execute(self, context):
        if not context.scene.camera:
            self.report({'INFO'}, "No active camera found")
            return {'CANCELLED'}

        camera = context.scene.camera.data

        camera.shift_x = 0
        camera.shift_y = 0

        return {'FINISHED'}

def register():
    bpy.utils.register_class(STEROID_OT_camera_shift)
    bpy.utils.register_class(STEROID_OT_reset_camera_shift)

def unregister():
    bpy.utils.unregister_class(STEROID_OT_camera_shift)
    bpy.utils.unregister_class(STEROID_OT_reset_camera_shift)
    
if __name__ == '__main__':
    register()