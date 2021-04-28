import time
import os
import tempfile
import bpy


bl_info = {
    "name": "CacheIt",
    "author": "Kursad Karatas",
    "description": "",
    "blender": (2, 82, 0),
    "location": "",
    "warning": "",
    "category": "Generic"
}


def curdir():

    folderpath = os.path.dirname(bpy.data.filepath)
    print(folderpath)
    return folderpath


def getFileName():

    filename = bpy.path.basename(bpy.context.blend_data.filepath)
    filename = os.path.splitext(filename)[0]

    return filename


def getFilePath():

    return bpy.data.filepath


def getFolderPath(fname):

    foldername = os.path.dirname(fname)
    return foldername


def getTempFileName(fname):

    tempfolder = tempfile.gettempdir()
    tempfile = os.path.join(tempfolder, fname)

    return tempfile


def makeCacheFolder(folder):

    cachefolder = os.path.join(folder, ".cache")
    if os.path.exists(cachefolder):
        print(".cache folder exists already")
        print(" >>>>>>>>>>>> "+folder)

    else:
        os.chdir(folder)
        os.mkdir(".cache")
        print(".cache folder is created")

    return cachefolder


def getSelObject():
    selobjs = bpy.context.selected_objects
    print(selobjs)
    return selobjs


def exportAlembic(fname):
    """bpy.ops.wm.alembic_export()
        bpy.ops.wm.alembic_export(filepath="", check_existing=True,
        filter_blender=False, filter_backup=False, filter_image=False,
        filter_movie=False, filter_python=False, filter_font=False,
        filter_sound=False, filter_text=False, filter_btx=False,
        filter_collada=False, filter_alembic=True, filter_folder=True,
        filter_blenlib=False, filemode=8, display_type='DEFAULT',
        sort_method='FILE_SORT_ALPHA', start=-2147483648, end=-2147483648,
        xsamples=1, gsamples=1, sh_open=0, sh_close=1, selected=False,
        renderable_only=True, visible_layers_only=False, flatten=False,
        uvs=True, packuv=True, normals=True, vcolors=False, face_sets=False,
        subdiv_schema=False, apply_subdiv=False, compression_type='OGAWA',
        global_scale=1, triangulate=False, quad_method='SHORTEST_DIAGONAL',
        ngon_method='BEAUTY', export_hair=True, export_particles=True,
        as_background_job=True, init_scene_frame_range=False)
        Export current scene in an Alembic archive
    """

    C = bpy.context

    start = C.scene.frame_start
    end = C.scene.frame_end

    bpy.ops.wm.alembic_export(filepath=fname, selected=True, start=start, end=end, xsamples=1,
                              gsamples=1, uvs=True, packuv=False, normals=True, as_background_job=False)
    print(fname + " is exported as alembic")
    return


def importAlembic(fpath):
    """bpy.ops.wm.alembic_import()
        bpy.ops.wm.alembic_import(filepath="", check_existing=True,
        filter_blender=False, filter_backup=False, filter_image=False,
        filter_movie=False, filter_python=False, filter_font=False,
        filter_sound=False, filter_text=False, filter_btx=False,
        filter_collada=False, filter_alembic=True,
        filter_folder=True, filter_blenlib=False, filemode=8,
        display_type='DEFAULT', sort_method='FILE_SORT_ALPHA',
        scale=1, set_frame_range=True, validate_meshes=False,
        is_sequence=False, as_background_job=True)
    """

    bpy.ops.wm.alembic_import(
        filepath=fpath, set_frame_range=False, as_background_job=False,  is_sequence=False)
    return


def exportAlembicFile(folpath, fname):

    finalpath = os.path.join(folpath, fname+".abc")
    exportAlembic(finalpath)
    return finalpath


def importAlembicFile(fpath):
    print("importing the alembic file from importAlembicFile ->>" + fpath)
    importAlembic(fpath)
    return


class OBJECT_OT_CacheItOperator(bpy.types.Operator):
    bl_idname = "object.cacheit"
    bl_label = "CacheIt"

    def execute(self, context):

        fname = getFileName()
        fpath = getFilePath()
        folpath = getFolderPath(fpath)

        cachefolder = makeCacheFolder(folpath)

        os.chdir(folpath)

        if len(getSelObject()) > 0:
            expAlembicfile = exportAlembicFile(
                cachefolder, getSelObject()[0].name)
            expAlembicfile = os.path.realpath(expAlembicfile)
            self.report(
                {'INFO'}, "Alembic file is exported > " + expAlembicfile)
            self.report({'INFO'}, "Importing the Alembic file......")
            bpy.ops.wm.alembic_import(filepath=expAlembicfile)

            name = context.object.name
            context.object.name = name+".CACHE"

        else:
            self.report({'INFO'}, "No object is selected")

        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_OT_CacheItOperator)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_CacheItOperator)
