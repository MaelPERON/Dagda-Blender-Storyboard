import bpy
import PIL.Image as Image
from pathlib import Path
from ..constants import IMAGE_EXTENSIONS


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

    gutters: bpy.props.IntProperty(  # type: ignore
        name="Gutters",
        description="Space between thumbnails in pixels",
        default=20,
        min=0,
    )

    duration: bpy.props.IntProperty(  # type: ignore
        name="Duration",
        description="Duration of each thumbnail in frames",
        default=24,
        min=1,
    )

    fit_method: bpy.props.EnumProperty(  # type: ignore
        name="Fit Method",
        description="Method to fit the image in the strip",
        items=[
            ('WIDTH', "Width", "Fit the image to the strip width"),
            ('HEIGHT', "Height", "Fit the image to the strip height"),
            ('STRETCH', "Stretch", "Stretch the image to fill the strip size"),
        ],
        default='WIDTH'
    )

    @property
    def images(self) -> dict[Path, Image.Image]:
        images = {}
        if not self.directory:
            return images

        for file in self.files:
            file_path = Path(self.directory) / file.name
            if file_path.suffix.lower() in IMAGE_EXTENSIONS:
                try:
                    images[file_path] = Image.open(file_path)
                except Exception as e:
                    self.report(
                        {'ERROR'},
                        f"Failed to open image {file_path}: {e}")

        return images

    def execute(self, context):
        # TODO
        return {"FINISHED"}

    def invoke(self, context: bpy.types.Context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}
