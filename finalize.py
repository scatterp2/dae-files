import bpy
import os

with open('/content/temp.txt') as f:
    darray = ["/content/" + item + ".dae" for item in f.read().splitlines()]
with open('/content/temp.txt') as f:
    parray = ["/content/" + item + ".png" for item in f.read().splitlines()]

# create an empty list to store the imported objects
imported_objects = []
log = []
for dae,png in zip(darray, parray):
    log.append("Importing: " + dae)
    bpy.ops.wm.collada_import(filepath=dae)
    filepath = bpy.data.filepath
    directory = os.path.dirname(filepath)
    x = filepath.replace("dae","png")
    for mat in bpy.data.materials:
        log.append("Applying image texture: " + png + " to material: " + mat.name)
        try:
            img = bpy.data.images.load(png, check_existing=True)
            mat = bpy.data.materials[mat.name]
            bsdf_node = mat.node_tree.nodes.get("Principled BSDF")
            img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
            img_node.image = img
            mat.node_tree.links.new(img_node.outputs[0], bsdf_node.inputs['Base Color'])
        except Exception:
            log.append("Failed to apply image texture: " + png + " to material: " + mat.name)
            pass

log.append("Exporting all objects to: /content/dae-files/all.dae")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.wm.collada_export(filepath="/content/dae-files/all.dae", selected=True)

print(log)
