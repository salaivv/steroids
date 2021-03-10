
import bpy
from bpy.props import *

'''
def myNodeTree():
    if 'TestCurveData' not in bpy.data.node_groups:
        ng = bpy.data.node_groups.new('TestCurveData', 'ShaderNodeTree')
        ng.fake_user = True
    return bpy.data.node_groups['TestCurveData'].nodes

curve_node_mapping = {}
def myCurveData(curve_name):
    if curve_name not in curve_node_mapping:
        cn = myNodeTree().new('ShaderNodeRGBCurve')
        curve_node_mapping[curve_name] = cn.name
    return myNodeTree()[curve_node_mapping[curve_name]]
'''

class STEROID_OT_steroid_array(bpy.types.Operator):
    """Array with non-linear spacing, rotation and scale"""
    bl_idname = "steroid.steroid_array"
    bl_label = "Steroid Array (WIP)"
    bl_options = {'REGISTER', 'UNDO'}
    category = 'mesh'

    count: IntProperty(
        name="Count",
        description="Number of objects",
        default=1,
        min=0, soft_max=100,
    )

    offset: FloatVectorProperty(
        name="Offset",
        default=[0, 0, 0],
        size=3,
    )
    
    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            return context.mode in ['OBJECT', 'EDIT_MESH']
    
    def execute(self, context):
        if not context.active_object:
            self.report({'INFO'}, "Please select an object")
            return {'CANCELLED'}
        
        obj = context.active_object
        obj_list = []

        for i in range(self.count):
            new_obj = obj.copy()
            context.collection.objects.link(new_obj)
            obj_list.append(new_obj)
        
        for i, cpy in enumerate(obj_list):
            cpy.location = (obj.location[0] + i*self.offset[0],
                obj.location[1] + i*self.offset[1],
                obj.location[2] + i*self.offset[2])

        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        layout.prop(self, "count")
        layout.prop(self, "offset")
        # layout.template_curve_mapping(myCurveData('TestOne'), "mapping")


def register():
    bpy.utils.register_class(STEROID_OT_steroid_array)

def unregister():
    bpy.utils.unregister_class(STEROID_OT_steroid_array)
    
if __name__ == '__main__':
    register()