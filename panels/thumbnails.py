import bpy
from bl_ui.space_sequencer import SequencerButtonsPanel
from ..operators import SE_OT_ImportStoryThumbnails


class SE_PT_Thumbnails(SequencerButtonsPanel, bpy.types.Panel):
    bl_label = "Storyboard Thumbnails"
    bl_idname = "SE_PT_thumbnails_panel"
    bl_category = "Storyboard"

    def draw(self, context: bpy.types.Context):
        layout = self.layout

        op = layout.operator(
            "sequencer.set_range_to_strips",
            text="Set Range to Strips",
        )
        op.preview = False

        layout.operator(
            SE_OT_ImportStoryThumbnails.bl_idname,
            text="Import Story Thumbnails")

        scene = context.scene
        scene: bpy.types.Scene
        strip = scene.sequence_editor.active_strip

        if not strip:
            layout.label(text="No active strip selected.")
            return

        if strip.type != 'IMAGE':
            layout.label(text="Active strip is not an image.")
            return

        layout.prop(strip, "name", text="Strip Name")

        for prop in ["index_row", "index_col", "rows", "cols", "gutters"]:
            layout.label(text=f"{prop}: {strip.get(prop, 'N/A')}")

        width, height = strip.get("image_resolution", ("N/A", "N/A"))
        layout.label(text=f"Image: {width} x {height}")

        width, height = strip.get("thumbnail_resolution", ("N/A", "N/A"))
        layout.label(text=f"Thumbnail: {width} x {height}")
