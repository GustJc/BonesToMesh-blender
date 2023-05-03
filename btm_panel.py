
from bpy.types import Panel

class GDEV_PT_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Bones to mesh"
    bl_category = "BonesToMesh"

    @classmethod
    def poll(cls, context):
        obj = context.object

        if obj.mode == "OBJECT":
            return True

        return False

    def draw(self, context):
        layout = self.layout

        # 2 Column buttons
        row = layout.row()
        row.operator("object.create_bones_vertex_groups", text="Create constrained bones")

        row = layout.row()
        row.operator("object.bake_all_pose", text="Bake bones")

        #col = row.column()
        row = layout.row()
        row.operator("object.remove_all_bone_constrains", text="Remove IK constraints")

        row = layout.row()
        row.operator("object.remove_all_vertexgroups", text="Remove vertex groups")