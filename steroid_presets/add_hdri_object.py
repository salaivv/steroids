import bpy
from mathutils import Vector
from bpy.props import StringProperty

class STEROID_OT_add_hdri_object(bpy.types.Operator):
    """Add an environment texture with an empty controller for rotation"""
    bl_idname = "steroid.add_hdri_mapping"
    bl_label = "Add HDR Environment"
    bl_options = {'REGISTER', 'UNDO'}
    category = 'rendering'

    filepath = StringProperty(subtype='FILE_PATH')
    
    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            return context.mode == 'OBJECT'
    
    def execute(self, context):
        context.scene.world.use_nodes = True
        hdr_image = bpy.data.images.load(filepath=self.filepath)
        node_tree = context.scene.world.node_tree
        env_node = node_tree.nodes.new(type="ShaderNodeTexEnvironment")
        env_node.image = hdr_image
        
        bg_node = None
        for node in node_tree.nodes:
            if node.type == 'BACKGROUND':
                bg_node = node
                break

        node_tree.links.new(env_node.outputs['Color'], bg_node.inputs['Color'])
        env_node.location = bg_node.location - Vector((300, 0))

        for obj in context.scene.objects:
            if obj.name.startswith('HDR_controller'):
                empty = obj
                break
        else:
            bpy.ops.object.empty_add(type='SPHERE', location=(0, 0, 0))
            empty = context.active_object
            empty.name = 'HDR_controller'
            empty.empty_display_size = 1.5

        tex_coord = node_tree.nodes.new(type="ShaderNodeTexCoord")
        tex_coord.object = empty
        tex_coord.location = env_node.location - Vector((300, 0))

        node_tree.links.new(tex_coord.outputs['Object'], env_node.inputs['Vector'])

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


def register():
    bpy.utils.register_class(STEROID_OT_add_hdri_object)

def unregister():
    bpy.utils.unregister_class(STEROID_OT_add_hdri_object)
    
if __name__ == '__main__':
    register()