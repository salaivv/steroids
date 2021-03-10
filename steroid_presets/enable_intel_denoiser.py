import bpy
from mathutils import Vector
from bpy.props import StringProperty


class STEROID_OT_enable_intel_denoiser(bpy.types.Operator):
    """Activate denoising data passes and setup the intel denoiser (cycles only)"""
    bl_idname = "steroid.enable_intel_denoiser"
    bl_label = "Enable Intel Denoiser"
    bl_options = {'REGISTER', 'UNDO'}
    category = 'rendering'
    
    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            return context.scene.render.engine == 'CYCLES'
    
    def execute(self, context):
        context.view_layer.cycles.denoising_store_passes = True
        context.scene.use_nodes = True
        node_tree = context.scene.node_tree
        
        r_layer_node, comp_node = None, None
        for node in node_tree.nodes:
            if not (r_layer_node and comp_node):
                if node.type == 'R_LAYERS':
                    r_layer_node = node
                    continue

                if node.type == 'COMPOSITE':
                    comp_node = node
                    continue

        r_layer_node.location -= Vector((300, 0))
        denoise_node = node_tree.nodes.new(type="CompositorNodeDenoise")
        denoise_node.location = r_layer_node.location + Vector((400, 0))

        node_tree.links.new(r_layer_node.outputs['Image'], denoise_node.inputs['Image'])
        node_tree.links.new(r_layer_node.outputs['Denoising Albedo'], denoise_node.inputs['Albedo'])
        node_tree.links.new(r_layer_node.outputs['Denoising Normal'], denoise_node.inputs['Normal'])
        node_tree.links.new(denoise_node.outputs['Image'], comp_node.inputs['Image'])

        return {'FINISHED'}


def register():
    bpy.utils.register_class(STEROID_OT_enable_intel_denoiser)

def unregister():
    bpy.utils.unregister_class(STEROID_OT_enable_intel_denoiser)
    
if __name__ == '__main__':
    register()