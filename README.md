# Bones To Mesh Addon

Blender addon to help bake physics simulations to bones inside armatures.



## Description

Select both a mesh object and armature and use the side panel 'BonesToMesh'.
Select 'Create constrained bones' will create vertex groups for the mesh and assign IK constraints for the bones. 
Putting the closest vertex to the bone tail with weight of 1 in its vertex group.

Select the armature and press 'Bake bones' to bake all bone constraints.
Note that you need to bake your physics baked. 
This is only a shortcut to Pose->Animation->Bake with all bones selected. Using visual keying.