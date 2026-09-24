import bpy


class SE_OT_ImportStoryThumbnails(bpy.types.Operator):
    bl_idname = "se.import_story_thumbnails"
    bl_label = "Import Story Thumbnails"
    bl_description = "Import and cut storyboard thumbnails"
    bl_options = {"REGISTER", "UNDO"}

    directory: bpy.props.StringProperty(  # type: ignore
        subtype='DIR_PATH',
        options={'SKIP_SAVE', 'HIDDEN'})

    files: bpy.props.CollectionProperty(  # type: ignore
        type=bpy.types.OperatorFileListElement,
        options={'SKIP_SAVE', 'HIDDEN'})

    rows: bpy.props.IntProperty(  # type: ignore
        name="Rows",
        description="Number of rows in the image",
        default=4,
        min=1,
    )

    cols: bpy.props.IntProperty(  # type: ignore
        name="Columns",
        description="Number of columns in the image",
        default=4,
        min=1,
    )

    def execute(self, context):
        # TODO
        return {"FINISHED"}

    def invoke(self, context: bpy.types.Context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}
