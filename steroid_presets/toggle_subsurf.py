import bpy

class STEROID_OT_toggle_subsurf(bpy.types.Operator):
    """Toggle subsurf modifier visibility in the viewport"""
    bl_idname = "steroid.toggle_subsurf"
    bl_label = "Toggle Subsurf Modifier"
    bl_options = {'REGISTER', 'UNDO'}
    category = 'modifiers'
    
    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            return context.mode in ['OBJECT', 'EDIT_MESH']
    
    def execute(self, context):
        if not context.selected_objects:
            self.report({'INFO'}, "Please select an object(s)")
            return {'CANCELLED'}
        
        show_viewport = None
        for mod in context.object.modifiers:
            if mod.type == 'SUBSURF':
                show_viewport = not mod.show_viewport
                break
        else:
            self.report({'INFO'}, "Object has no subsurf modifier")
            return {'CANCELLED'}
    
        for obj in context.selected_objects:
            for mod in obj.modifiers:
                if mod.type == 'SUBSURF':
                    mod.show_viewport = show_viewport
                    
        return {'FINISHED'}
    

def register():
    bpy.utils.register_class(STEROID_OT_toggle_subsurf)

def unregister():
    bpy.utils.unregister_class(STEROID_OT_toggle_subsurf)
    
if __name__ == '__main__':
    register()