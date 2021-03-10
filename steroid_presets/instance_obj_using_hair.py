import bpy


class STEROID_OT_instance_obj_using_hair(bpy.types.Operator):
    """Instance an object using hair partciles"""
    bl_idname = "steroid.instance_obj_using_hair"
    bl_label = "Instance Object Using Hairs"
    bl_options = {'REGISTER', 'UNDO'}
    category = 'particles'
    
    
    count: bpy.props.IntProperty(
        name="Particle Count",
        description="Number of particle hair instances",
        default=200,
        min=1, soft_max=10000,
    )

    seed: bpy.props.IntProperty(
        name="Seed",
        description="Seed of particle hair instances",
        default=0,
        min=0, soft_max=1000,
    )
    
    length: bpy.props.FloatProperty(
        name="Length",
        description="Length of particle hair instances",
        default=1.0,
        min=0.1, soft_max=10.0,
    )
    
    scale: bpy.props.FloatProperty(
        name="Scale",
        description="Size of particle hair instances",
        default=1.0,
        min=0.01, soft_max=1.0,
    )
    
    size_random: bpy.props.FloatProperty(
        name="Scale Randomness",
        default=0.250,
        min=0.0, max=1,
    )
    
    emit_from: bpy.props.EnumProperty(
        name="Emit From",
        description="Particle source to emit from",
        items=(
            ('VERT', "Verts", ""),
            ('FACE', "Faces", ""),
            ('VOLUME', "Volume", ""),
        ),
        default='FACE',
    )
    
    use_modifier_stack: bpy.props.BoolProperty(
        name="Use Modifier Stack",
        description="Use modifier stack",
        default=False,
    )

    instance_object: bpy.props.StringProperty(
        name="Instance Object",
        default="",
    )
    
    @classmethod
    def poll(cls, context):
            # return context.mode == 'OBJECT' and context.object.type == 'MESH'
            return context.mode == 'OBJECT'
    
    def execute(self, context):
        if not context.selected_objects:
            self.report({'INFO'}, "No objects selected")
            return {'CANCELLED'}

        if len(context.selected_objects) > 2:
            self.report({'INFO'}, "Please select two objects – an instance object and an instancer")
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'INFO'}, "Active object is not a mesh")
            return {'CANCELLED'}

        bpy.ops.object.particle_system_add()
        psys = context.object.particle_systems[-1]
        psys.settings.type = 'HAIR'
        psys.settings.use_advanced_hair = True
        psys.settings.render_type = 'OBJECT'

        instance_object = None
        if len(context.selected_objects) == 2:
            if context.selected_objects[0] == context.active_object:
                instance_object = context.selected_objects[1]
            else:
                instance_object = context.selected_objects[0]
        else:
            try:
                instance_object = context.scene.objects[self.instance_object]
            except KeyError:
                pass

        psys.settings.instance_object = instance_object
        psys.settings.count = self.count
        bpy.context.object.particle_systems[psys.name].seed = self.seed
        psys.settings.hair_length = self.length
        psys.settings.particle_size = self.scale
        psys.settings.size_random = self.size_random
        psys.settings.emit_from = self.emit_from
        psys.settings.use_modifier_stack = self.use_modifier_stack
        
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        col = layout.column()
        col.prop(self, "count")
        col.prop(self, "seed")
        col.prop(self, "length")
        col.prop(self, "scale")
        col.prop(self, "size_random")
        row = col.row(align=True)
        row.prop(self, "emit_from", expand=True)
        col.prop(self, "use_modifier_stack")
        if not len(context.selected_objects) == 2:
            col.prop_search(self, "instance_object", context.scene, "objects")


def register():
    bpy.utils.register_class(STEROID_OT_instance_obj_using_hair)

def unregister():
    bpy.utils.unregister_class(STEROID_OT_instance_obj_using_hair)
    
if __name__ == '__main__':
    register()