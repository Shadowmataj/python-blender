bl_info = {
    "name": "Sculpt Menu",
    "author": "Christian / Antar",
    "version": (4, 0),
    "blender": (4, 0, 2),
    "location": "",
    "description": "Make your own customizable tool pie menu in sculpt mode.",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"
}

import os
import bpy
import rna_keymap_ui
import csv
import sys
from bpy.types import Menu, AddonPreferences, Operator 

my_os=sys.platform

if my_os == 'darwin' or my_os == 'linux':
    file = '/addons/sculpt menu/register scultp menu.csv'
else:
    file = '\\addons\\sculpt menu\\register scultp menu.csv'
    

#Se define la ubicación del archivo que contiene el registro del menú y en el cual se establecen los ultimos #
#pinceles utilizados por el usuario                                                                          #

filepath = bpy.utils.script_path_user() + file



# Se guarda la información del archivo de registro en el diccionario#

dictionary = dict()

with open(filepath, newline = '') as csv_file:
    reader = csv.reader(csv_file)
    for line, words in enumerate(reader):
        dictionary[words[0]] = words[1]
csv_file.close()

#Se emplea un diccionario para poder vincular la palabra clave de los pinceles con la palabra clave de su ícono.#

brush_icon_dictionary = {
                "Draw": "draw",                                      "Draw Sharp": "draw_sharp",
                "Clay": "clay",                                      "Clay Strips": "clay_strips",
                "Clay Thumb": "clay_thumb",                          "Layer": "layer",
                "Inflate": "inflate",                                "Blob": "blob",    
                "Crease": "crease",                                  "Smooth":"smooth",
                "Flatten": "flatten",                                "Fill": "fill",
                "Scrape": "scrape",                                  "Multi-plane Scrape": "multiplane_scrape",
                "Pinch": "pinch",                                    "Grab": "grab",
                "Elastic Deform": "elastic_deform",                  "Snake Hook": "snake_hook",
                "Thumb": "thumb",                                    "Pose": "pose",
                "Nudge": "nudge",                                    "Rotate": "rotate",
                "Slide Relax": "topology",                           "Boundary": "boundary",
                "Cloth": "cloth",                                    "Simplify": "simplify",
                "Mask": "mask",                                      "Multires Displacement Eraser": "displacement_eraser",
                "Multires Displacement Smear": "displacement_smear", "Draw Face Sets": "draw_face_sets",
                "box_mask": "border_mask",                           "box_face_set": "border_face_set",
                "box_hide": "border_hide",                           "move": "translate",
                "scale": "resize",                                   "Paint": "paint",
                "Smear": "smear",
                }

#Del archivo de registro extraido previamente se genera un nuevo diccionario que contiene las palabras claves de los íconos#                 
icon_dictionary = dict()
                
for label in dictionary.keys():
    icon = dictionary.get(label)
    if dictionary.get(label) in brush_icon_dictionary.keys():
        icon_dictionary.update({label : brush_icon_dictionary.get(icon)}) 
    else:
        icon_dictionary.update({label : dictionary.get(label)})                

#Contiene las palabras claves que necesitan un tipo específico para ejecutarse, en específico "builtin.". Para todas las demás se utiliza#
#"builtin_brush."#                
builtin_list = [
                "box_mask", "lasso_mask", "line_mask", "box_hide", "box_face_set", "lasso_face_set", "box_trim",
                "lasso_trim", "line_project", "mesh_filter", "cloth_filter", "box_hide", "face_set_edit","move",
                "rotate","scale","transform", "mask_by_color", "color_filter",
            ]                

#Meú pie principal.#
class VIEW3D_MT_PIE_Sculpt_menu(Menu):
    '''Tool'''
    bl_label = "Sculpt menu"
    bl_idname = "VIEW3D_MT_PIE_Sculpt_menu"
        
    def draw(self, context):
        
        layout = self.layout
        pie = layout.menu_pie()
        box = pie.column(align = True)
        select_1= box.row(align = True)
        
        #Sección 1: Mediante {dictionary} y {icon_dictionary} se dibujan los elementos principales del menú pie.#  
        select_1.scale_x = 1.2
        select_1.scale_y = 1.5
        select_1.operator("Sub.menu_1", icon = 'BRUSHES_ALL', text = '').selected_brush = 'function_label_1'
        select_1.operator('object.menu_pie', text = "   "+dictionary.get("function_label_1").capitalize(), icon_value = brush_icons[icon_dictionary.get("function_label_1")]).brush = 'function_label_1'
       
        box = pie.column(align = True)
        select_2= box.row(align = True)
        select_2.scale_x = 1.2
        select_2.scale_y = 1.5
        select_2.operator('object.menu_pie', text = "   "+dictionary.get("function_label_2").capitalize(), icon_value = brush_icons[icon_dictionary.get("function_label_2")]).brush = 'function_label_2'
        select_2.operator("Sub.menu_1", icon = 'BRUSHES_ALL', text = '').selected_brush = 'function_label_2'
        
        box = pie.column(align = True)
        select_3= box.row(align = True)
        select_3.scale_x = 1.2
        select_3.scale_y = 1.5
        select_3.operator('object.menu_pie', text = "   "+dictionary.get("function_label_3").capitalize(), icon_value = brush_icons[icon_dictionary.get("function_label_3")]).brush = 'function_label_3'
        select_3.operator('Sub.menu_1', icon = 'BRUSHES_ALL', text = '').selected_brush = 'function_label_3'     
        
        box = pie.column(align = True)
        select_4= box.row(align = True)
        select_4.scale_x = 1.2
        select_4.scale_y = 1.5
        select_4.operator('object.menu_pie', text = "   "+dictionary.get("function_label_5").capitalize(), icon_value = brush_icons[icon_dictionary.get("function_label_5")]).brush = 'function_label_5'
        select_4.operator('Sub.menu_1', icon = 'BRUSHES_ALL', text = '').selected_brush = 'function_label_5'
        
        box = pie.column(align = True)
        select_5= box.row(align = True)
        select_5.scale_x = 1.2
        select_5.scale_y = 1.5
        select_5.operator('Sub.menu_1', icon = 'BRUSHES_ALL', text = '').selected_brush = 'function_label_4'
        select_5.operator('object.menu_pie', text = "   "+dictionary.get("function_label_4").capitalize(), icon_value = brush_icons[icon_dictionary.get("function_label_4")]).brush = 'function_label_4'
        
        box = pie.column(align = True)
        select_6= box.row(align = True)
        select_6.scale_x = 1.2
        select_6.scale_y = 1.5
        select_6.operator('object.menu_pie', text = "   "+dictionary.get("function_label_6").capitalize(), icon_value = brush_icons[icon_dictionary.get("function_label_6")]).brush = 'function_label_6'
        select_6.operator('Sub.menu_1', icon = 'BRUSHES_ALL', text = '').selected_brush = 'function_label_6'
        
        box = pie.column(align = True)
        select_7= box.row(align = True)
        select_7.scale_x = 1.2
        select_7.scale_y = 1.5
        select_7.operator('Sub.menu_1', icon = 'BRUSHES_ALL', text = '').selected_brush = 'function_label_7'            
        select_7.operator('object.menu_pie', text = "   "+dictionary.get("function_label_7").capitalize(), icon_value = brush_icons[icon_dictionary.get("function_label_7")]).brush = 'function_label_7'
        
        box = pie.column(align = True)
        select_8= box.row(align = True)
        select_8.scale_x = 1.2
        select_8.scale_y = 1.5
        select_8.operator('object.menu_pie', text = "   "+dictionary.get("function_label_8").capitalize(), icon_value = brush_icons[icon_dictionary.get("function_label_8")]).brush = 'function_label_8'
        select_8.operator('Sub.menu_1', icon = 'BRUSHES_ALL', text = '').selected_brush = 'function_label_8'
        
        
#Operador para implementar el pincel selecionado en la sección 1 del menú principal.#
class OBJECT_OT_Pie_Menu(Operator):
    '''Tool'''
    bl_idname = "object.menu_pie"
    bl_label = "Some Operator"
    
    #Se transmite un dato desde el menú principal para que le prorgama idéntifique la selección que se realizó.#
    enum = [
            ('function_label_1', 'Brush 1', 'Selection from de pie menu'),
            ('function_label_2', 'Brush 2', 'Selection from de pie menu'),
            ('function_label_3', 'Brush 3', 'Selection from de pie menu'),
            ('function_label_4', 'Brush 4', 'Selection from de pie menu'),
            ('function_label_5', 'Brush 5', 'Selection from de pie menu'),
            ('function_label_6', 'Brush 6', 'Selection from de pie menu'),
            ('function_label_7', 'Brush 7', 'Selection from de pie menu'),
            ('function_label_8', 'Brush 8', 'Selection from de pie menu'),
        ]
    
    brush: bpy.props.EnumProperty(items=enum)
    
    #Eperación a implementar con la etiqueta seleccionada.#
    def execute(self, context):
        if dictionary.get(self.brush) in builtin_list:
            bpy.ops.wm.tool_set_by_id(name = "builtin."+dictionary.get(self.brush), space_type='VIEW_3D')
        else:
            bpy.ops.wm.tool_set_by_id(name = "builtin_brush."+dictionary.get(self.brush), space_type='VIEW_3D')
        
        return {'FINISHED'}      
    
class OBJECT_OT_Operator_Menu(Operator): 
    '''Make your own customizable tool pie menu in sculpt mode.'''
    bl_idname = "sub.menu_1"
    bl_label = "Select your tool"
    
    #Lista enum: sirve para especificar el pincel que se modificará.#
    enum = [
            ('function_label_1', 'Brush 1', 'Selection from de pie menu'),
            ('function_label_2', 'Brush 2', 'Selection from de pie menu'),
            ('function_label_3', 'Brush 3', 'Selection from de pie menu'),
            ('function_label_4', 'Brush 4', 'Selection from de pie menu'),
            ('function_label_5', 'Brush 5', 'Selection from de pie menu'),
            ('function_label_6', 'Brush 6', 'Selection from de pie menu'),
            ('function_label_7', 'Brush 7', 'Selection from de pie menu'),
            ('function_label_8', 'Brush 8', 'Selection from de pie menu'),
        ]
    
    #Lista change_1: sirve para especificar el elemento que reemplazará al que se encuentra actualmente en la etiqueta seleccionada.# 
    change_1 = [
            ('Draw', 'Draw', 'Selection'),                             ('Draw Sharp', 'Draw Sharp', 'Selection'),
            ('Clay', 'Clay', 'Selection'),                             ('Clay Strips', 'Clay Strips', 'Selection'),
            ('Clay Thumb', 'Clay Thumb', 'Selection'),                 ('Layer', 'Layer', 'Selection'),
            ('Inflate', 'Inflate', 'Selection'),                       ('Blob', 'Blob', 'Selection'),
            ('Crease', 'Crease', 'Selection'),                         ('Smooth', 'Smooth', 'Selection'),
            ('Flatten', 'Flatten', 'Selection'),                       ('Fill', 'Fill', 'Selection'),
            ('Scrape', 'Scrape', 'Selection'),                         ('Multi-plane Scrape', 'Multi-plane Scrape', 'Selection'),
            ('Pinch', 'Pinch', 'Selection'),                           ('Grab', 'Grab', 'Selection'),
            ('Elastic Deform', 'Elastic Deform', 'Selection'),         ('Snake Hook', 'Snake Hook', 'Selection'),
            ('Thumb', 'Thumb', 'Selection'),                           ('Pose', 'Pose', 'Selection'),
            ('Nudge', 'Nudge', 'Selection'),                           ('Rotate', 'Rotate', 'Selection'),
            ('Slide Relax', 'Slide Relax', 'Selection'),               ('Boundary', 'Boundary', 'Selection'),
            ('Cloth', 'Cloth', 'Selection'),                           ('Simplify', 'Simplify', 'Selection'),                       
            ('Mask', 'Mask', 'Selection'),                             ('Multires Displacement Eraser', 'Multires Displacement Eraser', 'Selection'),
            ('Multires Displacement Smear', 'Multires Displacement Smear', 'Selection'),    ('Draw Face Sets', 'Draw Face Sets', 'Selection'),
            
            ('box_mask', 'Box Mask', 'Selection'),                     ('lasso_mask', 'Lasso Mask', 'Selection'),
            ('line_mask', 'Line Mask', 'Selection'),                   ('box_hide', 'Box Hide', 'Selection'),
            ('box_face_set', 'Box Face Set', 'Selection'),             ('lasso_face_set', 'Lasso Face Set', 'Selection'),
            ('box_trim', 'Box Trim', 'Selection'),                     ('lasso_trim', 'Lasso Trim', 'Selection'),
            ('line_project', 'Line Project', 'Selection'),             ('mesh_filter', 'Mesh Filter', 'Selection'),
            ('cloth_filter', 'Cloth Filter', 'Selection'),             ('face_set_edit', 'Face Set Edit', 'Selection'),
            ('move', 'Move', 'Selection'),                             ('rotate', 'Rotate', 'Selection'),
            ('scale', 'Scale', 'Selection'),                           ('transform', 'Transform', 'Selection'),
            ('Paint', 'Paint', 'Selection'),                           ('mask_by_color', 'Mask by color', 'Selection'),
            ('color_filter', 'Color Filter', 'Selection'),             ('Smear', 'Smear', 'Selection'),
        ]     

    selected_brush: bpy.props.EnumProperty(items=enum)
    change: bpy.props.EnumProperty(name = "Tools", description = "Allows you to modify the brush palette", items=change_1)
    
    def invoke(self,context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context):  
        layout = self.layout
        layout.separator()
        
        #Despliega el menú de selección.#
        layout.prop(self,"change", text = 'Tool')
    
    #Funciones a implementar una vez que se selecciona el nuevo elemento del menú.#    
    def execute(self, context):   
                                          
        #Se evalúa que no se esté seleccionando un elemento que ya se encuentra en el menú.# 
        if self.change not in dictionary.values():                                                                                                           
            #Modifica el pincel seleccionado.#
            dictionary[self.selected_brush] = self.change 
            #Si el cambio a realizar se encuentra dentro de las llaves del {brush_icon_dictionary} cambia el icono utilizando la traducción.#    
            if self.change in brush_icon_dictionary.keys():
                icon_dictionary[self.selected_brush] = brush_icon_dictionary.get(self.change)
            #De lo contrario, hace el cambio directo.
            else:
                icon_dictionary[self.selected_brush] = self.change
            
            #El condicional se encarga de implementar el nuevo pincel.        
            if dictionary.get(self.selected_brush) in builtin_list:
                bpy.ops.wm.tool_set_by_id(name = "builtin."+dictionary.get(self.selected_brush), space_type='VIEW_3D')
            else:
                bpy.ops.wm.tool_set_by_id(name = "builtin_brush."+dictionary.get(self.selected_brush), space_type='VIEW_3D')
                
            #Se actualiza en el archivo de registro el cambio.#    
            with open(filepath, 'w', newline = '') as csv_file:
                writer = csv.writer(csv_file)
                for item in dictionary.keys():
                    list = [item, dictionary.get(item)]
                    writer.writerow(list)
            csv_file.close()
        
        return {'FINISHED'}

#Sección para generar los icon_value de cada pincel.#    
brush_icons = {}

def create_icons():
    global brush_icons
    icons_directory = bpy.utils.system_resource('DATAFILES', path = "icons")
    brushes = ["crease", "blob", "smooth", "draw", "clay", "clay_strips", "inflate", "grab",
        "nudge", "thumb", "snake_hook", "rotate", "flatten", "scrape", "fill", "pinch",
        "layer", "mask", "draw_sharp", "boundary", "clay_thumb", "cloth", "displacement_eraser", 
        "displacement_smear", "draw_face_sets", "elastic_deform", "fill", "multiplane_scrape", 
        "pose", "simplify", "thumb", "topology", "paint", "smear"] 
        
    brushes_1 = ["border_mask","lasso_mask","line_mask","border_hide","border_face_set","lasso_face_set",
            "box_trim","lasso_trim","line_project","mesh_filter","cloth_filter","face_set_edit", "mask_by_color", 
            "color_filter"]
            
    transformations = ["translate","rotate","resize","transform"]

    for brush in brushes:
        filename = os.path.join(icons_directory, f"brush.sculpt.{brush}.dat")
        icon_value = bpy.app.icons.new_triangles_from_file(filename)
        brush_icons[brush] = icon_value
    
    for brush in brushes_1:
        filename = os.path.join(icons_directory, f"ops.sculpt.{brush}.dat")
        icon_value = bpy.app.icons.new_triangles_from_file(filename)
        brush_icons[brush] = icon_value
        
    for transform in transformations:
        filename = os.path.join(icons_directory, f"ops.transform.{transform}.dat")
        icon_value = bpy.app.icons.new_triangles_from_file(filename)
        brush_icons[transform] = icon_value
    
    

def release_icons():
    global brush_icons
    for value in brush_icons.values():
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
        kmi = get_hotkey_entry_item(km, 'wm.call_menu_pie', 'VIEW3D_MT_PIE_Sculpt_menu')
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
        kmi = km.keymap_items.new('wm.call_menu_pie', 'Q', 'PRESS', ctrl=False, shift=True, alt=False)
        kmi.properties.name = 'VIEW3D_MT_PIE_Sculpt_menu'
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
            VIEW3D_MT_PIE_Sculpt_menu,
            OBJECT_OT_Pie_Menu,
            OBJECT_OT_Operator_Menu,
            UI_PT_Addon_Pref,
            USERPREF_OT_Change_Hotkey,
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
    
    bpy.ops.wm.call_menu_pie(name = "VIEW3D_MT_PIE_Sculpt_menu")