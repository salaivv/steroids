import bpy
from bpy.props import *


class STEROID_OT_particle_density_texture(bpy.types.Operator):
    """Add a noise texture to the active particle system to influence density"""
    bl_idname = "steroid.particle_density_texture"
    bl_label = "Particle Density Texture"
    bl_options = {'REGISTER', 'UNDO'}
    category = 'particles'
    
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
    
    density_factor: FloatProperty(
        name='Density Influence',
        default=0.5,
        min=0.0, max=1.0,
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
    
    texture_coords: EnumProperty(
        name="Coordinates",
        items=(
            ('GLOBAL', "Global", ""),
            ('OBJECT', "Object", ""),
            ('UV', "UV", ""),
            ('ORCO', "Generated", ""),
            ('STRAND', "Strand/Particle", ""),
        ),
        default='OBJECT',
    )
    
    z_offset: FloatProperty(
        name='Z Offset',
        default=0.0,
        min=0.0, soft_max=10.0,
    )
    
    
    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            return context.mode in ['OBJECT', 'EDIT_MESH']
    
    def execute(self, context):
        if not context.selected_objects:
            self.report({'INFO'}, "Please select an object")
            return {'CANCELLED'}
        
        obj = context.active_object
        
        # cancels the operator if there are no particle systems on the active object
        if not obj.particle_systems.active:
            self.report({'INFO'}, "Please add a particle system")
            return {'CANCELLED'}
        
        # gets the active particle system
        psys = obj.particle_systems.active.settings
        
        #no of existing non-empty texture slots
        active_tex_slots = len(list(filter(None, psys.texture_slots)))
        # print(active_tex_slots)
        
        #texture slot to add the new texture to
        if active_tex_slots:
            texture_slot_index = active_tex_slots
        else:
            texture_slot_index = 0
        
        psys.active_texture_index = texture_slot_index
        # print(texture_slot_index)
        

        # new_texture = [tex for tex in bpy.data.textures if tex.name.startswith('Texture')][-1]
        
        existing = len([tex for tex in bpy.data.textures if tex.name.startswith('density control')])

        if not existing:
            tex_name = "density control"
        else:
            tex_name = "density control" + ".{:03d}".format(existing)
        
        # new_texture.type = 'CLOUDS'
        
        new_texture = bpy.data.textures.new(tex_name, 'CLOUDS')
        
        psys.texture_slots.add()
        psys.texture_slots[texture_slot_index].texture = new_texture
        psys.texture_slots[texture_slot_index].blend_type = 'MULTIPLY'
        
        new_texture.noise_basis = self.noise_basis
        new_texture.noise_scale = self.noise_scale
        new_texture.noise_depth = self.noise_depth
        new_texture.use_color_ramp = True
        new_texture.color_ramp.elements[0].position = self.ramp_low
        new_texture.color_ramp.elements[1].position = self.ramp_high
        
        # psys.texture_slots[texture_slot_index].texture_coords = self.texture_coords
        psys.texture_slots[texture_slot_index].offset[2] = self.z_offset
        psys.texture_slots[texture_slot_index].density_factor = self.density_factor
        psys.texture_slots[texture_slot_index].use_map_density = True
        # psys.texture_slots[texture_slot_index].use_map_density = self.psize_affect

        return {'FINISHED'}


def register():
    bpy.utils.register_class(STEROID_OT_particle_density_texture)

def unregister():
    bpy.utils.unregister_class(STEROID_OT_particle_density_texture)
    
if __name__ == '__main__':
    register()