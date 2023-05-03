import bpy
import numpy as np
from bpy.types import Operator

class GDEV_OT_CreateVertexGroupsOperator(bpy.types.Operator):
    """Create a vertex group for each bone in the selected armature"""
    bl_idname = "object.create_bones_vertex_groups"
    bl_label = "Create Vertex Groups"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.object

        if obj.mode == "OBJECT" and len(context.selected_objects) == 2:
            if context.selected_objects[0].type == 'MESH' and \
                    context.selected_objects[1].type == 'ARMATURE':
                return True
            if context.selected_objects[1].type == 'MESH' and \
                    context.selected_objects[0].type == 'ARMATURE':
                return True

        return False

    def execute(self, context):
        # Assuming the mesh is active object
        if context.selected_objects[0].type == 'MESH':
            mesh_obj = context.selected_objects[0]
            armature_obj = context.selected_objects[1]
        else:
            mesh_obj = context.selected_objects[1]
            armature_obj = context.selected_objects[0]

        bone_names = [bone.name for bone in armature_obj.data.bones]
        vertices = np.array(mesh_obj.data.vertices)

        for bone_name in bone_names:
            bone_tail = armature_obj.pose.bones[bone_name].tail
            vertex_group = mesh_obj.vertex_groups.new(name=bone_name)

            closest_vertex_idx = np.argmin([np.linalg.norm(v.co - bone_tail) for v in vertices])
            vertex_group.add([int(closest_vertex_idx)], 1.0, 'REPLACE')

            # Add IK constraint
            bone_constraint = armature_obj.pose.bones[bone_name].constraints.new(type='IK')
            bone_constraint.target = mesh_obj
            bone_constraint.subtarget = bone_name
            bone_constraint.chain_count = 1

        return {'FINISHED'}

class GDEV_OT_BakeConstraintsOperator(Operator):
    bl_idname = "object.bake_all_pose"
    bl_label = "Bake pose constrains"
    bl_description = "Bake all pose constrains"
    bl_options = {'REGISTER', 'UNDO'}

    frame_start: bpy.props.IntProperty(
        name="Start Frame",
        description="Start frame for baking",
        min=0, max=300000,
        default=1,
    )
    frame_end: bpy.props.IntProperty(
        name="End Frame",
        description="End frame for baking",
        min=1, max=300000,
        default=250,
    )
    step: bpy.props.IntProperty(
        name="Frame Step",
        description="Frame Step",
        min=1, max=120,
        default=1,
    )
    use_current_action: bpy.props.BoolProperty(
        name="Overwrite Current Action",
        description="Bake animation into current action, instead of creating a new one "
        "(useful for baking only part of bones in an armature)",
        default=False,
    )
    clean_curves: bpy.props.BoolProperty(
        name="Clean Curves",
        description="After baking curves, remove redundant keys",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        obj = context.object

        if obj.mode == "OBJECT" and obj.type == "ARMATURE":
            return True

        return False

    def execute(self, context):
        # Active object is ARMATURE

        bpy.ops.nla.bake(only_selected=False, visual_keying=True, clear_constraints=True,bake_types={'POSE'},
                         clean_curves=self.clean_curves,
                         frame_start=self.frame_start, 
                         frame_end=self.frame_end, 
                         step=self.step,
                         use_current_action=self.use_current_action)

        return {'FINISHED'}

    def invoke(self, context, _event):
        scene = context.scene
        if scene.use_preview_range:
            self.frame_start = scene.frame_preview_start
            self.frame_end = scene.frame_preview_end
        else:
            self.frame_start = scene.frame_start
            self.frame_end = scene.frame_end

        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class GDEV_OT_RemoveConstraintsOperator(Operator):
    bl_idname = "object.remove_all_bone_constrains"
    bl_label = "Remove pose constrains"
    bl_description = "Remove all pose constrains"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.object

        if obj.mode == "OBJECT" and obj.type == "ARMATURE":
            return True

        return False

    def execute(self, context):
        # Active object is ARMATURE
        armature_obj = context.active_object

        bone_names = [bone.name for bone in armature_obj.data.bones]

        for bone_name in bone_names:

            # Add IK constraint
            constraint = armature_obj.pose.bones[bone_name].constraints.get("IK")
            if constraint:
                armature_obj.pose.bones[bone_name].constraints.remove(constraint)

        return {'FINISHED'}


class GDEV_OT_RemoveVertexOperator(Operator):
    bl_idname = "object.remove_all_vertexgroups"
    bl_label = "Remove vertexgroups"
    bl_description = "Remove all vertexgroups"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.object

        if obj.mode == "OBJECT" and obj.type == "MESH":
            return True

        return False

    def execute(self, context):
        # Active object is ARMATURE
        mesh_obj = context.active_object

        mesh_obj.vertex_groups.clear()

        return {'FINISHED'}

