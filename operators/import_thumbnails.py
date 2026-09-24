import bpy
import PIL.Image as Image
from pathlib import Path
from ..constants import IMAGE_EXTENSIONS
from ..utils import fit


class SE_OT_ImportStoryThumbnails(bpy.types.Operator):
    bl_idname = "se.import_story_thumbnails"
    bl_label = "Import Story Thumbnails"
    bl_description = "Import and cut storyboard thumbnails"
    bl_options = {"REGISTER", "UNDO"}

    directory: bpy.props.StringProperty(  # type: ignore
        subtype='DIR_PATH',
        options={'HIDDEN'})

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

    def execute(self, context: bpy.types.Context):
        # Storyboard images constants
        ROWS, COLS = self.rows, self.cols
        GUTTERS = self.gutters
        N = ROWS * COLS

        # Context constants
        scene: bpy.types.Scene = context.scene
        scene_width, scene_height = (
            scene.render.resolution_x, scene.render.resolution_y)
        sequencer = scene.sequence_editor

        images = self.images
        if not images:
            self.report({'ERROR'}, "No valid images found.")
            return {"CANCELLED"}

        for path, image in images.items():
            # Calculing effective thumbnail dimensions
            width, height = (
                (image.width - (GUTTERS * (ROWS - 1))) / ROWS,
                (image.height - (GUTTERS * (COLS - 1))) / COLS
            )
            # Resizing the thumbnail to fit the scene's width
            # while maintaining aspect ratio
            match self.fit_method:
                case 'WIDTH':
                    ratio_x = scene_width / width
                    ratio_y = ratio_x
                case 'HEIGHT':
                    ratio_y = scene_height / height
                    ratio_x = ratio_y
                case 'STRETCH':
                    ratio_x = scene_width / width
                    ratio_y = scene_height / height
                case _:
                    self.report(
                        {'ERROR'},
                        f"Unknown fit method: {self.fit_method}")
                    return {"CANCELLED"}

            # Calculating offsets and max values for transformations
            delta_x = (width + GUTTERS) * ratio_x
            delta_y = (height + GUTTERS) * ratio_y
            max_x = delta_x * (COLS - 1)
            max_y = delta_y * (ROWS - 1)

            # Create a new strip for each thumbnail
            for i in range(N):
                # Calculate row and column indices
                index_row = i % ROWS
                index_col = i // ROWS

                # Calculate offsets
                x_offset = delta_x * index_row
                y_offset = delta_y * index_col

                # Add the image strip to the sequencer
                strip = sequencer.strips.new_image(
                    name=f"{path.stem}_{i + 1:02d}",
                    filepath=str(path),
                    channel=1,
                    frame_start=scene.frame_current + i * self.duration
                )
                strip: bpy.types.ImageStrip
                strip.right_handle = strip.frame_final_start + self.duration

                # Set custom properties and transform offsets
                strip.transform.offset_x = fit(
                    x_offset,
                    0, max_x,
                    max_x / 2, -max_x / 2
                )
                strip.transform.offset_y = fit(
                    y_offset,
                    0, max_y,
                    -max_y / 2, max_y / 2
                )

        self.report(
            {'INFO'},
            f"Imported {len(images)} images with {N} thumbnails each.")
        return {"FINISHED"}

    def invoke(self, context: bpy.types.Context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}
