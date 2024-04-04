bl_info = {
    "name": "EZSculpt",
    "author": "Christian / Antar",
    "version": (1, 1),
    "blender": (3, 0, 3),
    "location": "",
    "description": "Make your own customizable tool pie menu in sculpt mode.",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"
}

import os
import bpy
from bpy.props import EnumProperty
import rna_keymap_ui
import csv
import sys
from bpy.types import Menu, AddonPreferences, Operator, PropertyGroup

selectable_objects = []

def UpdatedFunction(self, context):
    print("In update func...")
    return

def UpdatedFunction_objecs(self, context):
    global objects_list
    objects_list = bpy.data.objects.keys()
    objects_list.append('None')    
    
    selectable_objects = []
    
    for obj in objects_list:
        selectable_objects.append((obj, obj, ''))
    
    return selectable_objects

class MyPropertyGroup(PropertyGroup):
    
    bpy.types.Scene.selectable_objects = EnumProperty(update = UpdatedFunction, items = UpdatedFunction_objecs)

#Meú pie principal.#
class VIEW3D_MT_PIE_EZsculpt(Menu):
    '''Tool'''
    bl_label = "EZSculpt menu"
    bl_idname = "VIEW3D_MT_PIE_EZsculpt"
        
    def draw(self, context):
        
        layout = self.layout
        pie = layout.menu_pie()
        
        
        box = pie.column(align = True)
        left_line_1 = box.row(align = True)
        
        left_line_1.scale_x = 2
        left_line_1.scale_y = 2
        left_line_1.operator('brush.operator', text = '', icon_value = icons_data['paint'])
        
        left_line_2 = box.row(align = True)
        left_line_2.scale_x = 2
        left_line_2.scale_y = 2
        left_line_2.operator('texture.operator', text = '', icon = 'TEXTURE')
        
        box = pie.column(align = True)
        right_line_1 = box.row(align = True)
        
        right_line_1.scale_x = 2
        right_line_1.scale_y = 2
        right_line_1.operator('meshmen.operator', text = '', icon = 'MESH_CUBE').selection_mesh = 'MESH_CUBE'
        
        right_line_2 = box.row(align = True)
        
        right_line_2.scale_x = 2
        right_line_2.scale_y = 2
        right_line_2.operator('meshmen.operator', text = '', icon = 'MESH_UVSPHERE').selection_mesh = 'MESH_UVSPHERE'
        
        right_line_3 = box.row(align = True)
        
        right_line_3.scale_x = 2
        right_line_3.scale_y = 2
        right_line_3.operator('meshmen.operator', text = '', icon = 'MESH_CYLINDER').selection_mesh = 'MESH_CYLINDER'
        
        right_line_4 = box.row(align = True)
        
        right_line_4.scale_x = 2
        right_line_4.scale_y = 2
        right_line_4.operator('meshmen.operator', text = '', icon = 'MESH_MONKEY').selection_mesh = 'MESH_MONKEY'
              
        box = pie.column(align = True)
        down_line_1 = box.row(align = True)   
        
        box = pie.column(align = True)
        up_line_1 = box.row(align = True)
        
        up_line_1.scale_x = 1.5
        up_line_1.scale_y = 2
        up_line_1.operator('remesh.operator', text = '', icon = 'MOD_REMESH')
        up_line_1.operator('dyntopo.operator', text = '', icon = 'DECORATE_KEYFRAME')
        up_line_1.operator('multiresolution.operator', text = '', icon = 'MOD_MULTIRES')
        up_line_1.operator('simetry.operator', text = '',icon = 'MOD_MIRROR')
        
    def execute(self, context):
        bpy.ops.object.multires_subdivide(modifier="Multires")
            
########################################################################################## 
class OBJECT_OT_Mesh_operator(Operator):
    '''Mesh menu'''
    bl_idname = "meshmen.operator"
    bl_label = "Mesh menu"    
    
    meshes = [
            ('MESH_CUBE', 'Cube', 'Selection from de pie menu'),
            ('MESH_UVSPHERE', 'Sphere', 'Selection from de pie menu'),
            ('MESH_CYLINDER', 'Cylinder', 'Selection from de pie menu'),
            ('MESH_MONKEY', 'Monkey', 'Selection from de pie menu'),
            ]    
            
    selection_mesh: bpy.props.EnumProperty(items=meshes)  
    
    
    
    def draw(self,context):
        layout = self.layout
        
        layout.separator()
        scene = context.scene
        
            
        menu_mesh = layout.row(align = True, heading = '')
        menu_mesh.operator('mesh.operator', text = '', icon = self.selection_mesh).selection = self.selection_mesh
        menu_mesh_2 = layout.column(align = True, heading = '')
        
        if context.scene.selectable_objects == 'None':
            menu_mesh_2.enabled = False
        else:
            menu_mesh_2.enabled = True
        
        menu_mesh_2.operator('update_object.operator', text = 'Mark the objects', icon = 'RESTRICT_SELECT_OFF').mark_option = 'MARK'  
        menu_mesh_2.operator('update_object.operator', text = 'Unmark the objects', icon = 'RESTRICT_SELECT_ON').mark_option = 'UNMARK'  
        
        
        objects_list = bpy.data.objects.keys()
        objects_list.append('None')
        menu_join = layout.column(align = True, heading = '')
        for obj in objects_list:            
            menu_join.prop_enum(scene, 'selectable_objects', value = obj) 
        
    
    def execute(self, context): 
             
        return {'FINISHED'} 
    
    def invoke(self, context, event):
        for obj in bpy.context.selected_objects:
            obj.select_set(False)    
        return context.window_manager.invoke_props_dialog(self)           
    
##########################################################################################

class OBJECT_OT_Update_object(Operator):
    '''Update object'''
    bl_idname = "update_object.operator"
    bl_label = "Update object"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    option = [
            ('MARK', 'Mark the selected object',''),
            ('UNMARK', 'Unmark the selected object','')
            ]
    
    mark_option : bpy.props.EnumProperty(items = option)

    def execute(self, context):
        
        if self.mark_option == 'MARK':
            
            try:
                bpy.data.objects[context.scene.selectable_objects].select_set(True)     
            
            except KeyError:
                self.report ({'ERROR'}, 'Select an object')
        
        elif self.mark_option == 'UNMARK':
            
            try:
                bpy.data.objects[context.scene.selectable_objects].select_set(False)     
            
            except KeyError:
                self.report ({'ERROR'}, 'Select an object')
                
        return {'FINISHED'}
            
selected_objects_list = []  
          
##########################################################################################         
class OBJECT_OT_Draw(Operator):
    '''Draw'''
    bl_idname = "mesh.operator"
    bl_label = "Draw"    
    
    mesh = [('MESH_CUBE', 'Cube', 'Selection from de pie menu'),
            ('MESH_UVSPHERE', 'Sphere', 'Selection from de pie menu'),
            ('MESH_CYLINDER', 'Cylinder', 'Selection from de pie menu'),
            ('MESH_MONKEY', 'Monkey', 'Selection from de pie menu'),
            ]
    
    selection: bpy.props.EnumProperty(items=mesh)  
    
    x: bpy.props.FloatProperty()
    y: bpy.props.FloatProperty()
    z: bpy.props.FloatProperty()
    selected_object: bpy.props.StringProperty()
    figure_size: bpy.props.FloatProperty()
    previous_position: bpy.props.FloatProperty()
    previous_object: bpy.props.StringProperty() 
        
    def execute(self, context): 
        
        for obj in selected_objects_list:
            selected_objects_list.remove(obj)
        
        for obj in bpy.context.selected_objects:
            selected_objects_list.append(obj.name_full)
        print(selected_objects_list)        
        pass            
        
    def modal(self, context, event):
            
        if event.type == 'MOUSEMOVE':  # Confirm
            
            if self.previous_position == event.mouse_x:
                pass
            elif self.previous_position > event.mouse_x:
                self.figure_size = 0.9
            elif self.previous_position < event.mouse_x:
                self.figure_size = 1.1
                                     
            bpy.ops.transform.resize(value=(self.figure_size, self.figure_size, self.figure_size), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False)
            self.previous_position = event.mouse_x
                
        elif event.type == 'LEFTMOUSE':  # Confirm
                    
            if bpy.context.mode == 'SCULPT':
               bpy.ops.sculpt.sculptmode_toggle()
        
            elif bpy.context.mode == 'EDIT_MESH':
                bpy.ops.object.editmode_toggle()
        
            elif bpy.context.mode == 'PAINT_VERTEX':
                bpy.ops.paint.vertex_paint_toggle()
            
            elif bpy.context.mode == 'PAINT_WEIGHT':
                bpy.ops.paint.weight_paint_toggle()
            
            elif bpy.context.mode == 'PAINT_TEXTURE':
                bpy.ops.paint.texture_paint_toggle()
                
            if self.selected_object != 'None' or bpy.context.selected_objects == []:
                
                for obj in selected_objects_list:
                    try:
                        bpy.data.objects[obj].select_set(True)
                        bpy.ops.object.join()
                    
                    except KeyError:
                        pass 
                        
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
                
            else:
                for obj in selected_objects_list:
                   
                    try:
                        bpy.data.objects[obj].select_set(False)
                    except KeyError:
                        pass
                    
            bpy.ops.sculpt.sculptmode_toggle()    
            
            return {'FINISHED'}
                
        
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancel
            bpy.ops.object.delete(use_global=False, confirm=False)
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}
    
    def invoke(self, context, event):
        self.x = bpy.context.scene.cursor.location[0]
        self.y = bpy.context.scene.cursor.location[1]
        self.z = bpy.context.scene.cursor.location[2]
        context.window_manager.modal_handler_add(self)
        self.execute(context)
        self.previous_position = event.mouse_x
        self.selected_object = context.scene.selectable_objects
            
        if self.selection == 'MESH_CUBE':
            self.figure_size = 1          
            bpy.ops.mesh.primitive_cube_add(size=self.figure_size, enter_editmode=False, align='WORLD', location=(self.x, self.y, self.z), scale=(1, 1, 1))
        elif self.selection == 'MESH_UVSPHERE':
            self.figure_size = 1
            bpy.ops.mesh.primitive_uv_sphere_add(radius=self.figure_size, enter_editmode=False, align='WORLD', location=(self.x, self.y, self.z), scale=(1, 1, 1))
        elif self.selection == 'MESH_CYLINDER':
            self.figure_size = 1
            bpy.ops.mesh.primitive_cylinder_add(radius=self.figure_size, depth=2, enter_editmode=False, align='WORLD', location=(self.x, self.y, self.z), scale=(1, 1, 1))
        elif self.selection == 'MESH_MONKEY':
            self.figure_size = 2
            bpy.ops.mesh.primitive_monkey_add(size=self.figure_size, enter_editmode=False, align='WORLD', location=(self.x, self.y, self.z), scale=(1, 1, 1))

        return {'RUNNING_MODAL'}

##########################################################################################3 
class OBJECT_OT_Remesh(Operator):
    '''Remesh'''
    bl_idname = "remesh.operator"
    bl_label = "Remesh"
    bl_options = {'REGISTER', 'UNDO'}
    
    prop: bpy.props.BoolProperty()
    
    selection_box: bpy.props.StringProperty(
        description="Selection box",
        name="Selection box",
        default= 'CHECKBOX_HLT',
    ) 
        

    def draw(self, context):  
        layout = self.layout
        layout.scale_x = 5
        layout.separator()
        data = bpy.context.object.data
        
        menu = layout.column(align = False, heading = '')
        menu_voxel = menu.row(align = True, heading = 'Voxel size')
        menu_voxel.prop(data,"remesh_voxel_size", text = '')
        menu_voxel.operator('sample_detail_size.operator', icon = 'EYEDROPPER', text = '')
        
        
        menu_adaptative = menu.row(align = True, heading = 'Adaptative')
        menu_adaptative.prop(data ,"remesh_voxel_adaptivity", text = '')
        
        menu_fix_poles = menu.row(align = True, heading = ' ')
        menu_fix_poles.prop(data,"use_remesh_fix_poles", text = 'Fix poles')
        
        menu.separator()
      
        menu_Volume = menu.row(align = True, heading = 'Preserve')
        menu_Volume.prop(data,"use_remesh_preserve_volume", text = 'Volume')
        
        menu_paint_mask = menu.row(align = True, heading = ' ')
        menu_paint_mask.prop(data,"use_remesh_preserve_paint_mask", text = 'Paint mask')
        
        menu_face_sets = menu.row(align = True, heading = ' ')
        menu_face_sets.prop(data,"use_remesh_preserve_sculpt_face_sets", text = 'Face Sets')   
        
        menu_face_sets = menu.row(align = True, heading = ' ')
        menu_face_sets.prop(data,"use_remesh_preserve_vertex_colors", text = 'Face Sets')      
        
        menu_remesh = menu.row(align = True, heading = ' ')
        menu_remesh.enabled = not bpy.context.object.use_dynamic_topology_sculpting
        menu_remesh.operator('remesh_operators.operator', text = 'Remesh')
    
    
    def execute (self, context):
        
        return {'FINISHED'}
            
    def invoke(self, context, event):
        
        return context.window_manager.invoke_props_dialog(self)
    

    
class OBJECT_OT_remesh_operators(Operator):
    '''Remesh_operators'''
    bl_idname = "remesh_operators.operator"
    bl_label = "Remesh operators"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        bpy.ops.object.voxel_remesh()       
        
        return {'FINISHED'}
    
    
class OBJECT_OT_Sample(Operator):
    '''Sample'''
    bl_idname = "sample_detail_size.operator"
    bl_label = "Sample modal operator"  
     
    bl_options = {'DEPENDS_ON_CURSOR'}
    bl_cursor_pending = 'EYEDROPPER'
   
    x: bpy.props.IntProperty() 
    y: bpy.props.IntProperty()
         
    def execute(self, context):    
         
        bpy.ops.sculpt.sample_detail_size(location=(self.x, self.y), mode='VOXEL')
        print(f'({self.x}, {self.y})')  
        return {'FINISHED'}
        
    def modal(self, context, event):
        
        if event.type == 'MOUSEMOVE':  # Apply
            self.x= event.mouse_x
            self.y = event.mouse_y
        elif event.type == 'LEFTMOUSE':  # Confirm
            
            self.execute(context)
            
            return {'FINISHED'}
        
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancel
        
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}
    
    def invoke(self, context, event):
        self.x = event.mouse_x
        self.y = event.mouse_y
        
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
##########################################################################################    
methods = {
            "SUBDIVIDE": "Subdivide edges",
            "COLLAPSE": "Collapse edges",
            "SUBDIVIDE_COLLAPSE": "Subdivide Collapse",
            "RELATIVE": "Relative detail",
            "CONSTANT": "Constant details",
            "BRUSH": "Brush details",
            "MANUAL": "Manual details",            
            }

class OBJECT_OT_Dyntopo(Operator):
    '''Dyntopo'''
    bl_idname = "dyntopo.operator"
    bl_label = "Dyntopo"
    bl_options = {'REGISTER', 'UNDO'}  
    
    prop: bpy.props.BoolProperty()        
    
    dyntopo_state: bpy.props.BoolProperty(
        default = False
    )


    def draw(self, context):  
        layout = self.layout
        layout.separator()
        sculpt = bpy.context.scene.tool_settings.sculpt
        
            
        if bpy.context.object.use_dynamic_topology_sculpting:
            self.dyntopo_state = True
        else:
            self.dyntopo_state = False 
                
        menu = layout.column(align = True, heading = '')
        
        if bpy.context.object.use_dynamic_topology_sculpting:
            self.selection_box = 'CHECKBOX_HLT'
        else:
            self.selection_box = 'CHECKBOX_DEHLT'   
             
        menu_dyntopo = menu.row(align = True, heading = '')
        if self.dyntopo_state:
            menu_dyntopo.prop(self,'prop', text = ' ', emboss = False)
        else:
            menu_dyntopo.prop(self,'prop', text = 'Dyntopo is not activated', icon = 'ERROR', emboss = False)
            
        menu_dyntopo.operator("dyntopo_activation.operator", text = 'Dyntopo', icon = self.selection_box, emboss = False).selection_dyntopo = 'DYNTOPO'
        
        if bpy.context.object.use_dynamic_topology_sculpting:
            self.dyntopo_state = True
        else:
            self.dyntopo_state = False     
        
        if bpy.context.scene.tool_settings.sculpt.detail_type_method in {'RELATIVE'}:
            menu_detail_size = menu.row(align = False, heading = '')
            menu_detail_size.enabled = bpy.context.object.use_dynamic_topology_sculpting            
            menu_detail_size.prop(self, 'prop', text = 'Detail size', emboss = False)
            menu_detail_size.prop(sculpt,"detail_size", text = '')
            
        
        elif bpy.context.scene.tool_settings.sculpt.detail_type_method in {'CONSTANT', 'MANUAL'}:
            menu_Resolution = menu.row(align = True, heading = '')
            menu_Resolution.enabled = bpy.context.object.use_dynamic_topology_sculpting
            menu_Resolution.prop(self, 'prop', text = 'Resolution', emboss = False)
            menu_Resolution.prop(sculpt,"constant_detail_resolution", text = '')
            menu_Resolution.operator('sample_detail_dyntopo.operator', text = '', icon = 'EYEDROPPER')
        
        elif bpy.context.scene.tool_settings.sculpt.detail_type_method in {'BRUSH'}:
            detail_percent = menu.row(align = False, heading = '')
            detail_percent.enabled = bpy.context.object.use_dynamic_topology_sculpting
            detail_percent.prop(self, 'prop', text = 'Detail percentage', emboss = False)
            detail_percent.prop(sculpt,"detail_percent", text = '')    
                
        menu_refine_method = menu.row(align = False, heading = '')
        menu_refine_method.enabled = bpy.context.object.use_dynamic_topology_sculpting
        menu_refine_method.prop(self, 'prop', text = 'Refine method', emboss = False)
        menu_refine_method.prop_menu_enum(sculpt,"detail_refine_method", text = methods.get(bpy.context.scene.tool_settings.sculpt.detail_refine_method))
        
        menu_refine_method = menu.row(align = False, heading = '')
        menu_refine_method.enabled = bpy.context.object.use_dynamic_topology_sculpting
        menu_refine_method.prop(self, 'prop', text = 'Detailing', emboss = False)
        menu_refine_method.prop_menu_enum(sculpt,"detail_type_method", text = methods.get(bpy.context.scene.tool_settings.sculpt.detail_type_method))
        
        if bpy.context.scene.tool_settings.sculpt.detail_type_method in {'CONSTANT', 'MANUAL'}:
            menu_dyntopo = menu.row(align = True, heading = '')
            menu_dyntopo.enabled = self.dyntopo_state
            
            menu_dyntopo.operator("dyntopo_activation.operator", text = 'Datail flood fill').selection_dyntopo = 'DETAILFLOODFILL' 
         
        menu_smooth_shading = menu.row(align = True, heading = ' ')
        menu_smooth_shading.enabled = bpy.context.object.use_dynamic_topology_sculpting
        menu_smooth_shading.prop(sculpt,"use_smooth_shading", text = 'Smooth shading')          
    
    def execute (self, context):

        return {'FINISHED'}
            
    def invoke(self, context, event):
            
        return context.window_manager.invoke_props_dialog(self)
    
    
    
class OBJECT_OT_Dyntopo_activation(Operator):
    '''Dyntopo activation'''
    bl_idname = "dyntopo_activation.operator"
    bl_label = "Dyntopo activation"
    bl_options = {'REGISTER', 'UNDO'}
    
    dyntop= [
            ('DYNTOPO', 'Dyntopo activation',''),
            ('DETAILFLOODFILL', 'Detail flood fill',''),
            ('SMOOTHSHADING', 'Volume',''),
            ]
            
    selection_dyntopo: bpy.props.EnumProperty(items=dyntop)
        
    def execute(self, context):
        
        if self.selection_dyntopo == 'DYNTOPO':
            try:
                bpy.ops.sculpt.dynamic_topology_toggle()
            except RuntimeError:
                self.report({'ERROR'}, 'The context must be \'SCULPT\'')
                
        elif self.selection_dyntopo == 'DETAILFLOODFILL':
            bpy.ops.sculpt.detail_flood_fill()
        
        return {'FINISHED'}
 
class OBJECT_OT_Sample_Dyntopo(Operator):
    '''Sample'''
    bl_idname = "sample_detail_dyntopo.operator"
    bl_label = "Sample modal operator"  
     
    bl_options = {'DEPENDS_ON_CURSOR'}
    bl_cursor_pending = 'EYEDROPPER'
   
    x: bpy.props.IntProperty() 
    y: bpy.props.IntProperty()
         
    def execute(self, context):    
         
        bpy.ops.sculpt.sample_detail_size(location=(self.x, self.y), mode='DYNTOPO')
        print(f'({self.x}, {self.y})')  
        return {'FINISHED'}
        
    def modal(self, context, event):
        
        if event.type == 'MOUSEMOVE':  # Apply
            self.x= event.mouse_x
            self.y = event.mouse_y
        elif event.type == 'LEFTMOUSE':  # Confirm
            
            self.execute(context)
            
            return {'FINISHED'}
        
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancel
        
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}
    
    def invoke(self, context, event):
        self.x = event.mouse_x
        self.y = event.mouse_y
        
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
     
    
##########################################################################################        
        
class OBJECT_OT_Multiresolution(Operator):
    '''Multiresolution'''
    bl_idname = "multiresolution.operator"
    bl_label = "Multiresolution"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    selected_modifier: bpy.props.StringProperty(
        description = "Shows the name of the selected object. No modification",
        name = "Selected object",
        default=''
    )      
    
    warning: bpy.props.BoolProperty(
        description="Optimal display",
        name="Optimal display",
        default=False
    )
    
    subdivision_subdivision: bpy.props.BoolProperty(
        description="Subdivision",
        name="Subdivision",
        default=False
    )
            
    shape: bpy.props.BoolProperty(
        description="Shape",
        name="Shape",
        default=False
    )
    
    generate: bpy.props.BoolProperty(
        description="Generate",
        name="Generate",
        default=False
    )
    
    advanced_quality: bpy.props.FloatProperty(
        description = "Quality",
        name = "Quality",
        default=0,
        min=0,
        step=0.01
    )
    
    depress: bpy.props.BoolProperty(
        description="Depress",
        name="Depress",
        default=False
    )
    
    icon: bpy.props.StringProperty(
        description="Depress",
        name="Depress",
        default=''
    )
#inutiles apartir de aqu[i    
    advanced_use_creases: bpy.props.BoolProperty(
        description="Use creases",
        name="Use creases",
        default=False
    )
    
    advanced_use_custom_normals: bpy.props.BoolProperty(
        description="Use custom normals",
        name="Use custom normals",
        default=False
    )
    
    uv_smooth = [
            ('SMOOTH_ALL', 'All',''),
            ('PRESERVE_BOUNDARIES', 'Keep all boundaries', ''),
            ('PRESERVE_CORNERS_JUNCTIONS_AND_CONCAVE', 'Keep corners, Junctions, Concave', ''),
            ('PRESERVE_CORNERS_AND_JUNCTIONS', 'Keep corners, Junctions', ''),
            ('NONE', 'Monkey', 'None'),
            ]
    
    selection_uv_smooth: bpy.props.EnumProperty(items=uv_smooth) 
    
    boundary_smooth = [
            ('ALL', 'All',''),
            ('PRESERVE_CORNERS', 'Keep corners', ''),
            ]
    
    selection_boundary_smooth: bpy.props.EnumProperty(items=boundary_smooth) 
    
    
    def draw(self, context):  
        layout = self.layout
        layout.scale_x = 5
        layout.separator()
        
        try:
            modifier_keys = bpy.context.object.modifiers.keys()
            
            modifier= bpy.context.object.modifiers[modifier_keys[0]]
            
            self.selected_modifier = modifier_keys[0]
            
            
            object = layout.row(align = True, heading = 'Selected modifier')
            object.enabled = True
            object.prop(self,"selected_modifier", text = '', )
                    
            object.prop(modifier,"show_viewport", text = '')
                             
            object.prop(modifier,"show_render", text = '')
            
            object.operator("multires_operators.operator", text = '', icon = 'X', emboss = False).operators_selection = 'REMOVE'
                    
            menu = layout.column(align = True, heading = '')
            
            menu_level_viewport = menu.row(align = False, heading = 'Level viewport')
            menu_level_viewport.prop(modifier,"levels", text = '')
            
            menu_sculpt = menu.row(align = False, heading = 'Sculpt')
            menu_sculpt.prop(modifier,"sculpt_levels", text = '')
            
            menu_render = menu.row(align = False, heading = 'Render')
            menu_render.prop(modifier,"render_levels", text = '')
            
            menu_sculpt_base_mesh = menu.row(align = False, heading = ' ')
            menu_sculpt_base_mesh.prop(modifier, 'use_sculpt_base_mesh')        
            
            menu_optimal_display = menu.row(align = False, heading = ' ')
            menu_optimal_display.prop(modifier, 'show_only_control_edges')
            
            if bpy.context.object.use_dynamic_topology_sculpting:
                menu_subdivision = menu.column(align = False, heading = '')
                menu_subdivision.prop(self, 'warning', text = 'Not superted in Dyntopo', icon = 'ERROR', emboss = False)
        
            if self.subdivision_subdivision:   
                menu_subdivision = menu.column(align = False, heading = '')
                menu_subdivision.prop(self,"subdivision_subdivision", icon = 'DOWNARROW_HLT', emboss = False)
            else:
                menu_subdivision = menu.column(align = False, heading = '')
                menu_subdivision.prop(self,"subdivision_subdivision", icon = 'RIGHTARROW', emboss = False)
            if self.subdivision_subdivision:
            
                menu.separator()
                 
                menu_subdivide = menu.row(align = True, heading = '')
                
                menu.separator()
                
                menu_subdivide.operator('multires_subdivision.operator', text = 'Subdivide').selection_divisions = 'CATMULL_CLARK'
                menu_simple_linear = menu.row(align = False)
                
                menu_simple_linear.operator('multires_subdivision.operator', text = 'Simple').selection_divisions = 'SIMPLE'
                menu_simple_linear.operator('multires_subdivision.operator', text = 'Linear').selection_divisions = 'LINEAR'
                
                menu.separator()
                menu.separator()
                
                menu_simple_unsubdivide = menu.row(align = False)
                menu_simple_unsubdivide.operator('multires_subdivision.operator', text = 'Unsubdivide').selection_divisions = 'UNSUBDIVIDE'
                
                menu.separator()
                
                menu_simple_unsubdivide = menu.row(align = False)
                menu_simple_unsubdivide.operator('multires_subdivision.operator', text = 'Delete Higher').selection_divisions = 'DELETE_HIGHER'
                
                menu.separator()
                
            if self.shape:
                menu_shape = menu.column(align = False, heading = '')
                menu_shape.prop(self,"shape", icon = 'DOWNARROW_HLT', emboss = False)
            else:
                menu_shape = menu.column(align = False, heading = '')
                menu_shape.prop(self,"shape", icon = 'RIGHTARROW', emboss = False)

            if self.shape:
            
                menu.separator()
                 
                menu_shape_1 = menu.row(align = False, heading = '')
            
                menu.separator()
                
                menu_shape_1.operator('multires_subdivision.operator', text = 'Reshape').selection_divisions = 'CATMULL_CLARK'
                menu_shape_1.operator('multires_subdivision.operator', text = 'Apply Base').selection_divisions = 'SIMPLE'
            
                menu.separator()
            
            if self.generate:
                menu_generate = menu.row(align = False, heading = '')
                menu_generate.prop(self,"generate", icon = 'DOWNARROW_HLT', emboss = False)
            else:
                menu_generate = menu.row(align = False, heading = '')
                menu_generate.prop(self,"generate", icon = 'RIGHTARROW', emboss = False)
            if self.generate:
            
                menu.separator()
            
                menu_generate_1 = menu.row(align = False, heading = '')
                menu_generate_1.operator('multires_subdivision.operator', text = 'No sé qué va...').selection_divisions = 'CATMULL_CLARK'
            
                menu.separator()
            
                menu_generate_2 = menu.row(align = False, heading = '')
                menu_generate_2.operator('multires_subdivision.operator', text = 'Save external...').selection_divisions = 'SIMPLE'
            
                menu.separator()
        except KeyError:
            object = layout.row(align = True, heading = 'Object')
            object.operator("multires_operators.operator", text = 'Add multires modifier').operators_selection = 'ADDMODIFIER'           
        
        except IndexError:    
            object = layout.row(align = True, heading = 'Object')
            object.operator("multires_operators.operator", text = 'Add multires modifier').operators_selection = 'ADDMODIFIER' 
            pass
        
    def execute (self, context):
        return {'FINISHED'}
            
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
class OBJECT_OT_Subdividivision(Operator):
    '''Multires subdivision'''
    bl_idname = "multires_subdivision.operator"
    bl_label = "Multires subdivision"
    bl_options = {'REGISTER', 'UNDO'}
    
    divisions = [
            ('CATMULL_CLARK', 'Subdivide',''),
            ('SIMPLE', 'Simple', ''),
            ('LINEAR', 'Linear', ''),
            ('UNSUBDIVIDE', 'Unsubdivide', ''),
            ('DELETE_HIGHER', 'Delete higher', ''),
            ]
        
    selection_divisions: bpy.props.EnumProperty(items=divisions)     
    
    def execute(self, context):     
        if self.selection_divisions == 'DELETE_HIGHER':
            bpy.ops.object.multires_higher_levels_delete(modifier="Multires")
  
        elif self.selection_divisions == 'UNSUBDIVIDE':
            pass    
        elif self.selection_divisions in {'CATMULL_CLARK', 'SIMPLE', 'LINEAR'}:
            bpy.ops.object.multires_subdivide(modifier="Multires", mode=self.selection_divisions)
            
    
        return {'FINISHED'}
    
class OBJECT_OT_Multires_operators(Operator):
    '''Multires operators'''
    bl_idname = "multires_operators.operator"
    bl_label = "Multires operators"
    bl_options = {'REGISTER', 'UNDO'}
    
    operators = [
            ('ADDMODIFIER', 'Add modifier',''),
            ('REALTIME', 'Realtime',''),
            ('RENDER', 'Render',''),
            ('REMOVE', 'Remove',''),
            ('SCULPTBASEMESH', 'Sculpt Base Mesh',''),
            ('OPTIMADISPLAY', 'Optimal Display', ''),
            
            ]
        
    operators_selection: bpy.props.EnumProperty(items=operators)     
    
    def execute(self, context):     
        if self.operators_selection == 'ADDMODIFIER':
            bpy.ops.object.modifier_add(type='MULTIRES')
            
        elif self.operators_selection == 'REALTIME':
            bpy.context.object.modifiers["Multires"].show_viewport = not bpy.context.object.modifiers["Multires"].show_viewport 
                    
        elif self.operators_selection == 'RENDER':
            bpy.context.object.modifiers["Multires"].show_render = not bpy.context.object.modifiers["Multires"].show_render
        
        elif self.operators_selection == 'REMOVE':
            bpy.ops.object.modifier_remove(modifier="Multires")
             
        elif self.operators_selection == 'SCULPTBASEMESH':
            bpy.context.object.modifiers["Multires"].use_sculpt_base_mesh = not bpy.context.object.modifiers["Multires"].use_sculpt_base_mesh

        elif self.operators_selection == 'OPTIMADISPLAY':
            bpy.context.object.modifiers["Multires"].show_only_control_edges = not bpy.context.object.modifiers["Multires"].show_only_control_edges 
    
        return {'FINISHED'}
##########################################################################################    

simetry_dictionary = {
            "NEGATIVE_X": "-X to +X",
            "POSITIVE_X": "+X to -X",
            "NEGATIVE_Y": "-Y to +Y",
            "POSITIVE_Y": "+Y to -Y",
            "NEGATIVE_Z": "-Z to +Z",
            "POSITIVE_Z": "+Z to -Z",
            }    
            
class OBJECT_OT_simetry(Operator):
    '''Simetry'''
    bl_idname = "simetry.operator"
    bl_label = "Simetry"
    bl_options = {'REGISTER', 'UNDO'}
    
    prop: bpy.props.BoolProperty(
        description = "Prop",
        name = "Prop",
        default = False
    )
    
    enabled_value:bpy.props.BoolProperty(
        description = "Enabled value",
        name = "Enabled value",
        default = False
    )
        
    
    def draw(self, context):  
        layout = self.layout
        layout.scale_x = 50
        layout.separator()
        sculpt = bpy.context.scene.tool_settings.sculpt
        
        modifier_keys = bpy.context.object.modifiers.keys()
        
        
        menu = layout.row(align = True, heading = 'Mirror')
        menu.prop(self,'prop', text = '', emboss = False)        
        menu.operator("symetry_operators.operator", text = 'Z', depress = bpy.context.object.data.use_mirror_x).operators_selection = 'MIRRORX'
        menu.operator("symetry_operators.operator", text = 'Y', depress = bpy.context.object.data.use_mirror_y).operators_selection = 'MIRRORY'
        menu.operator("symetry_operators.operator", text = 'Z', depress = bpy.context.object.data.use_mirror_z).operators_selection = 'MIRRORZ'
        
#       
        
        menu_1 = layout.row(align = True, heading = 'Lock')
        menu_1.prop(self,'prop', text = '', emboss = False)
        menu_1.operator("symetry_operators.operator", text = 'X', depress = bpy.context.scene.tool_settings.sculpt.lock_x).operators_selection = 'LOCKX'
        menu_1.operator("symetry_operators.operator", text = 'Y', depress = bpy.context.scene.tool_settings.sculpt.lock_y).operators_selection = 'LOCKY'
        menu_1.operator("symetry_operators.operator", text = 'Z', depress = bpy.context.scene.tool_settings.sculpt.lock_z).operators_selection = 'LOCKZ'
        
        
        menu_2 = layout.row(align = True, heading = 'Tiling')
        menu_2.prop(self,'prop', text = '', emboss = False)
        menu_2.operator("symetry_operators.operator", text = 'X', depress = bpy.context.scene.tool_settings.sculpt.tile_x).operators_selection = 'TILINGX'
        menu_2.operator("symetry_operators.operator", text = 'Y', depress = bpy.context.scene.tool_settings.sculpt.tile_y).operators_selection = 'TILINGY'
        menu_2.operator("symetry_operators.operator", text = 'Z', depress = bpy.context.scene.tool_settings.sculpt.tile_z).operators_selection = 'TILINGZ'
        
        menu_feather = layout.row(align = False, heading = ' ')
        menu_feather.prop(sculpt, 'use_symmetry_feather', text = 'Feather')
        
        menu_4_1 = layout.column(align = True, heading = 'Radial')
        menu_4_1.prop(sculpt, 'radial_symmetry', text = '')
        
        menu_5_1 = layout.column(align = True, heading = 'Tiling')
        menu_5_1.prop(sculpt, 'tile_offset', text = '')
        
        menu_6 = layout.row(align = False, heading = 'Direction')
        menu_6.prop_menu_enum(sculpt, 'symmetrize_direction', text = simetry_dictionary.get(bpy.context.scene.tool_settings.sculpt.symmetrize_direction))
        
        
        if modifier_keys == []:
            self.enabled_value = True
        else:
            self.enabled_value = False
                          
        menu_7 = layout.row(align = False, heading = 'Direction')
        menu_7.enabled = self.enabled_value
        menu_7.operator("symetry_operators.operator", text = 'Symmetrize').operators_selection = 'SYMMETRIZE'
        
        
        
        
        
        
    def execute (self, context):
        
        return {'FINISHED'}
            
    def invoke(self, context, event):
        
        return context.window_manager.invoke_props_dialog(self)
    
    
class OBJECT_OT_Symetry_operators(Operator):
    '''Symetry operators'''
    bl_idname = "symetry_operators.operator"
    bl_label = "Symetry operators"
    bl_options = {'REGISTER', 'UNDO'}
    
    operators = [
            ('MIRRORX', 'Mirror x',''),
            ('MIRRORY', 'Mirror y',''),
            ('MIRRORZ', 'Mirror z',''),
            ('LOCKX', 'Lock x',''),
            ('LOCKY', 'Lock y',''),
            ('LOCKZ', 'Lock z', ''),
            ('TILINGX', 'Tiling x',''),
            ('TILINGY', 'Tiling y',''),
            ('TILINGZ', 'Tiling z', ''),
            ('SYMMETRIZE', 'Symmetrize', ''),
            ]
        
    operators_selection: bpy.props.EnumProperty(items=operators)     
    
    def execute(self, context):     
        if self.operators_selection == 'MIRRORX':
            bpy.context.object.data.use_mirror_x = not bpy.context.object.data.use_mirror_x 
        
        elif self.operators_selection == 'MIRRORY':
            bpy.context.object.data.use_mirror_y = not bpy.context.object.data.use_mirror_y
            
        elif self.operators_selection == 'MIRRORZ':
            bpy.context.object.data.use_mirror_z = not bpy.context.object.data.use_mirror_z
            
        elif self.operators_selection == 'LOCKX':
            bpy.context.scene.tool_settings.sculpt.lock_x = not bpy.context.scene.tool_settings.sculpt.lock_x
            
        elif self.operators_selection == 'LOCKY':
            bpy.context.scene.tool_settings.sculpt.lock_y = not bpy.context.scene.tool_settings.sculpt.lock_y
            
        elif self.operators_selection == 'LOCKZ':
            bpy.context.scene.tool_settings.sculpt.lock_z = not bpy.context.scene.tool_settings.sculpt.lock_z
            
        elif self.operators_selection == 'TILINGX':
            bpy.context.scene.tool_settings.sculpt.tile_x = not bpy.context.scene.tool_settings.sculpt.tile_x
            
        elif self.operators_selection == 'TILINGY':
            bpy.context.scene.tool_settings.sculpt.tile_y = not bpy.context.scene.tool_settings.sculpt.tile_y
            
        elif self.operators_selection == 'TILINGZ':
            bpy.context.scene.tool_settings.sculpt.tile_z = not bpy.context.scene.tool_settings.sculpt.tile_z
            
        elif self.operators_selection == 'SYMMETRIZE':
            try:     
                bpy.ops.sculpt.symmetrize()
            except RuntimeError:
                self.report({'ERROR','WARNING'}, 'You can\'t use simmetrize while Multiresolution is activated')
                                                            
        return {'FINISHED'}
    
##########################################################################################

brush_dictionary = {
            "CUSTOM": "Custom",
            "SMOOTH": "Smooth",
            "SMOOTHER": "Smoother",
            "SPHERE": "Sphere",
            "ROOT": "Root",
            "SHARP": "Sharp",
            "LIN": "Linear",
            "POW4": "Sharper",
            "INVSQUARE": "Inverse square",
            "CONSTANT": "Constant",
            }  
            
brush_icon_dictionary = {
            "CUSTOM": "RNDCURVE",
            "SMOOTH": "SMOOTHCURVE",
            "SMOOTHER": "SMOOTHCURVE",
            "SPHERE": "SPHERECURVE",
            "ROOT": "ROOTCURVE",
            "SHARP": "SHARPCURVE",
            "LIN": "LINCURVE",
            "POW4": "SHARPCURVE",
            "INVSQUARE": "INVERSESQUARECURVE",
            "CONSTANT": "NOCURVE",
            }    

strokes_dictionary = {
            "DOTS": "Dots",
            "DRAG_DOT": "Drag dot",
            "SPACE": "Space",
            "AIRBRUSH": "Airbrush",
            "ANCHORED": "Anchored",
            "LINE": "Line",
            "CURVE": "Curve",
            }              

class OBJECT_OT_Brush(Operator):
    '''Brush'''
    bl_idname = "brush.operator"
    bl_label = "Brush"
    bl_options = {'REGISTER', 'UNDO'}
    
    prop: bpy.props.BoolProperty(
        description = "Prop",
        name = "Prop",
        default = False
    )
    
    enabled_value:bpy.props.BoolProperty(
        description = "Enabled value",
        name = "Enabled value",
        default = False
    )
        
    
    def draw(self, context):  
        layout = self.layout
        layout.scale_x = 50
        layout.separator()
        radious_setting = bpy.context.scene.tool_settings.unified_paint_settings
        brush_settings = bpy.data.brushes[bpy.context.tool_settings.sculpt.brush.name_full]
        samples = bpy.context.scene.tool_settings.sculpt
        
        menu_radius = layout.row(align = True, heading = '')
        if radious_setting.use_unified_size:
            menu_radius.prop(radious_setting, 'size', text = 'Radius', slider = True)
        else: 
            menu_radius.prop(brush_settings, 'size', text = 'Radius', slider = True)
        
        menu_radius.prop(brush_settings, 'use_pressure_size', text = '')
        menu_radius.prop(radious_setting, 'use_unified_size', text = '', icon = 'BRUSHES_ALL')

        menu_strength = layout.row(align = True, heading = '')
        
        if radious_setting.use_unified_strength:
            menu_strength.prop(radious_setting, 'strength', text = 'Strength')
        else:
            menu_strength.prop(brush_settings, 'strength', text = 'Strength')
            
        menu_strength.prop(brush_settings, 'use_pressure_strength', text = '')
        menu_strength.prop(radious_setting, 'use_unified_strength', text = '', icon = 'BRUSHES_ALL')
        
        menu_auto_masking = layout.row(align = True, heading = 'Auto-Masking')
        menu_auto_masking.prop(brush_settings, 'use_automasking_topology', text = 'Topology')
        menu_auto_masking = layout.row(align = True, heading = ' ')
        menu_auto_masking.prop(brush_settings, 'use_frontface', text = 'Front faces only')
        
        layout.separator(factor = 2) 
        
        menu_stroke_method = layout.row(align = True, heading = 'Stroke method')
        menu_stroke_method.prop_menu_enum(brush_settings, 'stroke_method', text = strokes_dictionary.get(brush_settings.stroke_method))
        
        layout.separator(factor = 2) 
        
        if brush_settings.stroke_method in {'ANCHORED'}:
            menu_use_edge_to_edge = layout.row(align = True, heading = ' ')
            menu_use_edge_to_edge.prop(brush_settings, 'use_edge_to_edge', text = 'Edge to edge')
        
        
        if brush_settings.stroke_method in {'AIRBRUSH'}:
            menu_rate = layout.row(align = True, heading = 'Rate')
            menu_rate.prop(brush_settings, 'rate', text = '', slider = True)
        
        
        if brush_settings.stroke_method in {'SPACE', 'LINE', 'CURVE'}:
            menu_spacing = layout.row(align = True, heading = 'Spacing')
            menu_spacing.prop(brush_settings, 'spacing', text = '')
            
        if brush_settings.stroke_method in {'SPACE'}:   
            menu_spacing.prop(brush_settings, 'use_pressure_spacing', text = '')
         
        if brush_settings.stroke_method in {'DOTS', 'DRAG_DOT', 'SPACE', 'AIRBRUSH', 'ANCHORED', 'LINE', 'CURVE'}:    
            menu_stroke_method = layout.row(align = True, heading = 'Spacing distance')
            menu_stroke_method.prop_enum(brush_settings, 'use_scene_spacing', value = 'VIEW')
            menu_stroke_method.prop_enum(brush_settings, 'use_scene_spacing', value = 'SCENE' )
         
        if brush_settings.stroke_method in {'SPACE', 'LINE', 'CURVE'}:    
            menu_use_space_attenuation = layout.row(align = True, heading = ' ')
            menu_use_space_attenuation.prop(brush_settings, 'use_space_attenuation', text = 'Adjust strength for spacing')
            
            layout.separator() 
                    
            menu_dash_ratio = layout.row(align = True, heading = 'Dash ratio')
            menu_dash_ratio.prop(brush_settings, 'dash_ratio', text = '')
        
            menu_dash_samples = layout.row(align = True, heading = 'Dash length')
            menu_dash_samples.prop(brush_settings, 'dash_samples', text = '')
            
        if brush_settings.stroke_method in {'DOTS', 'SPACE', 'AIRBRUSH', 'LINE', 'CURVE'}:
            
            layout.separator() 
            
            menu_jitter = layout.row(align = True, heading = 'Jitter')
        
            if brush_settings.jitter_unit == 'BRUSH':
                menu_jitter.prop(brush_settings, 'jitter', text = '', slider = True)
            
            if brush_settings.jitter_unit == 'VIEW':
                menu_jitter.prop(brush_settings, 'jitter_absolute', text = '', slider = True)
            
            menu_jitter.prop(brush_settings, 'use_pressure_jitter', icon_only = True)
        
            menu_jitter_unit = layout.row(align = True, heading = 'Jitter unit')
            menu_jitter_unit.prop_enum(brush_settings, 'jitter_unit', value = 'VIEW')
            menu_jitter_unit.prop_enum(brush_settings, 'jitter_unit', value = 'BRUSH' )
        
        
        if brush_settings.stroke_method in {'DOTS', 'DRAG_DOT', 'SPACE', 'AIRBRUSH', 'ANCHORED', 'LINE', 'CURVE'}:
            menu_input_samples = layout.row(align = True, heading = 'Input samples')
            menu_input_samples.prop(samples, 'input_samples', text = '')
        
        if brush_settings.stroke_method in {'DOTS', 'SPACE', 'AIRBRUSH'}:
            
            layout.separator() 
        
            menu_stabilize = layout.row(align = True, heading = 'Stabilize stroke')
            menu_stabilize.prop(brush_settings, 'use_smooth_stroke', text = 'Stabilize stroke')
                
            menu_stabilize_stroke = layout.row(align = True, heading = 'Radius')
            menu_stabilize_stroke.enabled = brush_settings.use_smooth_stroke
            menu_stabilize_stroke.prop(brush_settings, 'smooth_stroke_radius', text = '')
            menu_stabilize_stroke = layout.row(align = True, heading = 'Factor')
            menu_stabilize_stroke.enabled = brush_settings.use_smooth_stroke
            menu_stabilize_stroke.prop(brush_settings, 'smooth_stroke_factor', text = '')
            
        layout.separator(factor = 2)            

        menu_falloff = layout.row(align = True, heading = 'Auto-Masking')
        menu_falloff.prop_menu_enum(brush_settings, 'curve_preset', text = brush_dictionary.get(brush_settings.curve_preset), icon = brush_icon_dictionary.get(brush_settings.curve_preset))
        menu_falloff_shape = layout.row(align = True, heading = 'Falloff shape')
        menu_falloff_shape.prop_enum(brush_settings, 'falloff_shape', value = 'SPHERE')
        menu_falloff_shape.prop_enum(brush_settings, 'falloff_shape', value = 'PROJECTED')
        
    def execute (self, context):
        
        return {'FINISHED'}
            
    def invoke(self, context, event):
        
        return context.window_manager.invoke_props_dialog(self)
        
##########################################################################################
mapping_dictionary = {
            "VIEW_PLANE": "View plane",
            "AREA_PLANE": "Area plane",
            "TILED": "Tiled",
            "3D": "3D",
            "RANDOM": "Random",
            "STENCIL": "Stencil",
            }

class OBJECT_OT_Texture(Operator):
    '''Texture'''
    bl_idname = "texture.operator"
    bl_label = "Texture"
    bl_options = {'REGISTER', 'UNDO'}
        
    def draw(self, context):  
        layout = self.layout
        layout.scale_x = 50
        layout.separator()
        brush_mapping = bpy.data.brushes[bpy.context.tool_settings.sculpt.brush.name_full].texture_slot
        brush_bias = bpy.data.brushes[bpy.context.tool_settings.sculpt.brush.name_full]

        menu_mapping = layout.row(align = True, heading = 'Mapping')
        menu_mapping.prop_menu_enum(brush_mapping, 'map_mode', text = mapping_dictionary.get(brush_mapping.map_mode))
        
        if brush_mapping.map_mode == 'STENCIL':
            menu_reset_transform = layout.row(align = False, heading = '')
            menu_reset_transform.operator("texture_operator.operator", text = 'Reset transform')
            
        if brush_mapping.map_mode not in {'3D'}:   
            
            menu_angle = layout.row(align = False, heading = 'Angle')
            menu_angle.prop(brush_mapping, 'angle', text = '')
        
            if brush_mapping.map_mode not in {'TILED', 'STENCIL'}:
        
                menu_rake = layout.row(align = False, heading = ' ')
                menu_rake.prop(brush_mapping, 'use_rake', text = 'Rake')
        
                menu_random = layout.row(align = False, heading = ' ')
                menu_random.prop(brush_mapping, 'use_random', text = 'Random' )
                
        menu_offset = layout.column(align = False, heading = 'Offset ')
        menu_offset.prop(brush_mapping, 'offset', text = '' )
        
        menu_scale = layout.column(align = False, heading = 'Size ')
        menu_scale.prop(brush_mapping, 'scale', text = '' )

        menu_bias = layout.row(align = False, heading = 'Sample bias')
        menu_bias.prop(brush_bias, 'texture_sample_bias', text = '', slider = True)
       
    def execute (self, context):
        
        return {'FINISHED'}
            
    def invoke(self, context, event):
        
        return context.window_manager.invoke_props_dialog(self)    
    
class OBJECT_OT_Texture_operator(Operator):
    '''Texture operator'''
    bl_idname = "texture_operator.operator"
    bl_label = "Texture operator"
    bl_options = {'REGISTER', 'UNDO'}
               
    def execute (self, context):
        
        bpy.ops.brush.stencil_reset_transform()
        
        return {'FINISHED'}
        
        
    
    ##########################################################################################

icons_data = {}

def create_icons():
    global icons_data
    icons_directory = bpy.utils.system_resource('DATAFILES', path = "icons")
    
    icons = ["paint"] 


    for icon in icons:
        filename = os.path.join(icons_directory, f"brush.sculpt.{icon}.dat")
        icon_value = bpy.app.icons.new_triangles_from_file(filename)
        icons_data[icon] = icon_value
    
    
def release_icons():
    global icons_data
    for value in icons_data.values():
        bpy.app.icons.release(value)

#Sección para establecer la hotkey que permitará implementar el addon directamente.         
class UI_PT_Addon_Pref(AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.separator()
        wm = context.window_manager
        kc = wm.keyconfigs.user
        km = kc.keymaps['3D View Generic']
        kmi = get_hotkey_entry_item(km, 'wm.call_menu_pie', 'VIEW3D_MT_PIE_EZsculpt')
        if kmi:
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
        else:
            col.label(text="No hotkey found!", icon="ERROR")
            col.operator("add_hotkey.smenu", text="Add hotkey")
            
def get_hotkey_entry_item(km, kmi_name, kmi_value):
    for i, km_item in enumerate(km.keymap_items):
        if km.keymap_items.keys()[i] == kmi_name:
            if km.keymap_items[i].properties.name == kmi_value:
                return km_item
    return None
    
def add_hotkey():
    
    #####################################################################################################
    #¡CUIDADO! PARA QUE EL CÓDIGO CORRA DEBES MOVER LA SIGUIENTE LÍNEA (322) A LA LÍNEA 347. SI CORRES  #
    #EL SCRIPT MIENTRAS EL ADDON ESTÁ INSTALADO PUEDE GENERAR ERRORES EN EL REGISTRO DE LA HOTKEY       #
    #Y CAUSAR UN BUG QUE NO TE PERMITIRÁ UTILIZAR EL ADDON DE FORMA DIRECTA AL INICIAR BLENDER.         #
    #####################################################################################################
        
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View Generic', space_type='VIEW_3D', region_type= 'WINDOW')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'P', 'PRESS', ctrl=False, shift=False, alt=False)
        kmi.properties.name = 'VIEW3D_MT_PIE_EZsculpt'
        kmi.active = True
        addon_keymaps.append((km, kmi))

def remove_hotkey():

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()
    
class USERPREF_OT_Change_Hotkey(Operator):
    '''Add hotkey'''
    bl_idname = "add_hotkey.smenu"
    bl_label = "Add Hotkey"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        
        addon_prefs = bpy.context.preferences.addons[__name__].preferences
            
       
        add_hotkey()
        
        return {'FINISHED'}

addon_keymaps = []
    
classes = ( 
            VIEW3D_MT_PIE_EZsculpt,
            OBJECT_OT_simetry,
            OBJECT_OT_Draw,
            UI_PT_Addon_Pref,
            USERPREF_OT_Change_Hotkey,
            OBJECT_OT_Remesh,
            OBJECT_OT_Dyntopo,
            OBJECT_OT_Multiresolution,
            OBJECT_OT_Subdividivision,
            OBJECT_OT_remesh_operators,
            OBJECT_OT_Sample,
            OBJECT_OT_Dyntopo_activation,
            OBJECT_OT_Multires_operators,
            OBJECT_OT_Symetry_operators,
            OBJECT_OT_Brush,
            OBJECT_OT_Texture,
            OBJECT_OT_Texture_operator,
            OBJECT_OT_Sample_Dyntopo,
            OBJECT_OT_Mesh_operator,
            MyPropertyGroup,
            OBJECT_OT_Update_object
            )
            
def register():
    for item in classes:    
        bpy.utils.register_class(item)
    create_icons()
    add_hotkey()

        
def unregister():
    for item in classes:    
        bpy.utils.unregister_class(item)  
    release_icons()
    remove_hotkey()
        
if __name__ == "__main__":
    register()
    bpy.ops.wm.call_menu_pie(name = "VIEW3D_MT_PIE_EZsculpt")