import bpy
from math import pi as PI
from mathutils import Vector

class STEROID_OT_add_sunlight_kelvin(bpy.types.Operator):
    """Add a sun lamp with kelvin temperature control (cycles only)"""
    bl_idname = "steroid.add_sunlight_kelvin"
    bl_label = "Add Sun (Blackbody)"
    bl_options = {'REGISTER', 'UNDO'}
    category = 'rendering'

    strength: bpy.props.FloatProperty(
        name="Sun Strength",
        default=1.0,
        min=0.0, soft_max = 100,
    )

    temperature: bpy.props.FloatProperty(
        name="Temperature",
        default=6500,
        min=0.0, 
        soft_min=800,
        max=20000,
        soft_max=12000,
    )
    
    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            return context.mode == 'OBJECT' and context.scene.render.engine == 'CYCLES'
    
    def execute(self, context):
        bpy.ops.object.light_add(type='SUN')
        sun = context.active_object
        cursor_loc = context.scene.cursor.location

        sun.location[0] = cursor_loc[0]
        sun.location[1] = cursor_loc[1]
        if cursor_loc[2] > 7:
            sun.location[2] = cursor_loc[2]
        else:
            sun.location[2] = 7

        sun.rotation_euler = (PI/4, 0, PI/4*3)

        sun.data.use_nodes = True
        node_tree = sun.data.node_tree

        emit_node = None
        for node in node_tree.nodes:
            if node.name == "Emission":
                emit_node = node
                break
        
        blackbody_node = node_tree.nodes.new(type="ShaderNodeBlackbody")
        blackbody_node.location = emit_node.location - Vector((300, 0))

        node_tree.links.new(blackbody_node.outputs['Color'], emit_node.inputs['Color'])

        blackbody_node.inputs['Temperature'].default_value = self.temperature
        sun.data.energy = self.strength

        emit_node.inputs[0].show_expanded = True

        return {'FINISHED'}


def register():
    bpy.utils.register_class(STEROID_OT_add_sunlight_kelvin)

def unregister():
    bpy.utils.unregister_class(STEROID_OT_add_sunlight_kelvin)
    
if __name__ == '__main__':
    register()