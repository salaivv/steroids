import bpy

class STEROID_OT_separate_reset_origins(bpy.types.Operator):
    """Separate the mesh by loose parts and reset their Origin to Geometry"""
    bl_idname = "steroid.separate_reset_origins"
    bl_label = "Separate Parts and Reset Origins"
    bl_options = {'REGISTER', 'UNDO'}
    category = 'mesh'
    
    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            return context.mode in ['OBJECT', 'EDIT_MESH']
    
    def execute(self, context):
        if bpy.context.mode == 'OBJECT':
            bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(STEROID_OT_separate_reset_origins)

def unregister():
    bpy.utils.unregister_class(STEROID_OT_separate_reset_origins)
    
if __name__ == '__main__':
    register()