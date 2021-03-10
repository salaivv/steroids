import bpy
from bpy.props import *


class STEROID_OT_subsurf_displace_noise(bpy.types.Operator):
    """Add a subsurf modifier, followed by a displace modifier with a noise texture"""
    bl_idname = "steroid.subsurf_displace_noise"
    bl_label = "Noise Displacemet"
    bl_options = {'REGISTER', 'UNDO'}
    category = 'modifiers'

    use_subsurf: BoolProperty(
        name='Use Subsurf Modifier',
        default=True,
    ) 

    subsurf_lvl: IntProperty(
        name="Subdivision Level",
        default=1, 
        min=0, soft_max=6,
    )

    subsurf_type: EnumProperty(
        name="Subdivision Type",
        items=(
            ('CATMULL_CLARK', "Catmull-Clark", ""),
            ('SIMPLE', "Simple", ""),
        ),
        default='CATMULL_CLARK',
    )
    
    displace_strength: FloatProperty(
        name="Displace Strength",
        default=1.0, 
        soft_min=-5.0, soft_max=5.0,
    )

    mid_level: FloatProperty(
        name="Mid Level",
        default=0.5,
        min=0.0, max=1.0,
    )
    
    noise_basis: EnumProperty(
        name="Noise Basis",
        items=(
            ('BLENDER_ORIGINAL', "Blender Original", ""),
            ('ORIGINAL_PERLIN', "Original Perlin", ""),
            ('IMPROVED_PERLIN', "Improved Perlin", ""),
            ('VORONOI_F1', "Voronoi F1", ""),
            ('VORONOI_F2', "Voronoi F2", ""),
            ('VORONOI_F3', "Voronoi F3", ""),
            ('VORONOI_F4', "Voronoi F4", ""),
            ('VORONOI_F2_F1', "Voronoi F2-F1", ""),
            ('VORONOI_CRACKLE', "Voronoi Crackle", ""),
            ('CELL_NOISE', "Cell Noise", ""),
        ),
        default='BLENDER_ORIGINAL',
    )
    
    noise_scale: FloatProperty(
        name="Noise Scale",
        default=0.25, 
        min=0.0, max=2.0,
    )
    
    noise_depth: IntProperty(
        name="Noise Depth",
        default=2, 
        min=0, max=24,
    )
    
    ramp_low: FloatProperty(
        name="Ramp Low",
        default=0.0,
        min=0.0, max=1.0,
    )
    
    ramp_high: FloatProperty(
        name="Ramp High",
        default=1.0,
        min=0.0, max=1.0,
    )

    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            return context.mode in ['OBJECT', 'EDIT_MESH']
    
    def execute(self, context):
        obj = context.active_object
        if self.use_subsurf:
            bpy.ops.object.modifier_add(type='SUBSURF')
            obj.modifiers[-1].levels = self.subsurf_lvl
            obj.modifiers[-1].subdivision_type = self.subsurf_type
            obj.modifiers[-1].show_expanded = False

        bpy.ops.object.modifier_add(type='DISPLACE')
        disp_modifier = obj.modifiers[-1]
        bpy.ops.texture.new()
        
        new_texture = [tex for tex in bpy.data.textures if tex.name.startswith('Texture')][-1]
        
        existing = len([tex for tex in bpy.data.textures if tex.name.startswith('displace')])

        if not existing:
            new_texture.name = "displace"
        else:
            new_texture.name = "displace" + ".{:03d}".format(existing)
        
        new_texture.type = 'CLOUDS'
        disp_modifier.texture = new_texture
        disp_modifier.strength = self.displace_strength
        disp_modifier.mid_level = self.mid_level
        disp_modifier.texture.noise_basis = self.noise_basis
        disp_modifier.texture.noise_scale = self.noise_scale
        disp_modifier.texture.noise_depth = self.noise_depth
        new_texture.use_color_ramp = True
        new_texture.color_ramp.elements[0].position = self.ramp_low
        new_texture.color_ramp.elements[1].position = self.ramp_high

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.label(text="Subdivision", icon='MOD_SUBSURF')
        layout.prop(self, "use_subsurf")
        col = layout.column()
        col.enabled = self.use_subsurf
        col.prop(self, "subsurf_lvl")
        col.prop(self, "subsurf_type", expand=True)
        layout.separator()
        layout.label(text="Displacement", icon='MOD_DISPLACE')
        layout.prop(self, "displace_strength")
        layout.prop(self, "mid_level", slider=True)
        layout.separator()
        layout.label(text="Texture", icon='TEXTURE')
        layout.prop(self, "noise_basis", expand=True)
        layout.prop(self, "noise_scale")
        layout.prop(self, "noise_depth")
        layout.separator()
        layout.label(text="Color Ramp", icon='COLORSET_13_VEC')
        layout.prop(self, "ramp_low", slider=True)
        layout.prop(self, "ramp_high", slider=True)


def register():
    bpy.utils.register_class(STEROID_OT_subsurf_displace_noise)

def unregister():
    bpy.utils.unregister_class(STEROID_OT_subsurf_displace_noise)
    
if __name__ == '__main__':
    register()