import bpy

class STEROID_OT_mirror_using_empty(bpy.types.Operator):
    """Mirror an object using an Empty as the mirror object"""
    bl_idname = "steroid.mirror_using_empty"
    bl_label = "Mirror Using Empty (WIP)"
    bl_options = {'REGISTER', 'UNDO'}
    category = 'modifiers'
    
    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            return context.mode in ['OBJECT', 'EDIT_MESH'] \
                and context.active_object.type in ['MESH', 'CURVE']
    
    def execute(self, context):
        if not context.selected_objects:
            self.report({'INFO'}, "Please select an object to mirror.")
            return {'CANCELLED'}

        if len(context.selected_objects) > 1:
            self.report({'INFO'}, "Please select 'one' object to mirror.")
            return {'CANCELLED'}
        
        if context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle()

        obj = context.active_object
        bpy.ops.object.modifier_add(type='MIRROR')
        mod = obj.modifiers[-1]
        bpy.ops.object.empty_add(location=obj.location)
        empty = context.object
        empty.name = obj.name + "_mirror"
        mod.mirror_object = empty
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(STEROID_OT_mirror_using_empty)

def unregister():
    bpy.utils.unregister_class(STEROID_OT_mirror_using_empty)
    
if __name__ == '__main__':
    register()