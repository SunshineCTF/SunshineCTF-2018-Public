# [Forensics 500] Phishy Phishy

This challenge requires you to have an understanding of how file formats work, and how to perform binary diffing/patching. You must also search around to learn how Microsoft Paint3D Projects work "under the hood", as it is not documented (this requires experimentation locally).

## Attachment(s)
[phishy_chall.zip](https://ctf.hackucf.org/challenge-files/phishy_chall.zip)

## Solution
The solution involves several steps:
* Step 1: Identify where Microsoft Paint3D saves Project files. The directory is within AppData, but the directory actually does not exist until you create a project for the first time. Once created, you will be able to find it at: `%localappdata%\Packages\Microsoft.MSPaint_8wekyb3d8bbwe\LocalState\Projects`.
* Step 2: Once located, inspecting the created Paint3D projects (all listed as Untitled, and have ID's mapped to them within `Projects.json`) will provide reference as to the modifications made within the distributed "Phishy Phishy" challenge.
* Step 3: Upon inspecting and locating the Paint3D Project files, you should make a "dummy" project, where you copy and paste the contents of the challenge into the Paint3D Untitled project directory (NOTE: All files should be deleted before copying in challenge files, not replaced).
* Step 4: Once the files have been copied, an attempt to open the project should be made. As expected, the project should fail to open with an error within Paint3D.
* Step 5: Performing a binary diff against `Resources_Mesh_18446744069414584343.bin` and a corresponding `Resources_Mesh_*.bin` in a working project should yield that `FF FF FF FF` which follows an unknown Paint3D header, was replaced with `46 49 53 48` (`FISH`). Replacing `46 49 53 48` with the original `FF FF FF FF` will fix this file.
* Step 6: Performing a binary diff against `Nodes_18446744069414584343_MeshInstance.bin` and a corresponding `Nodes_*_MeshInstance.bin` in a working project should yield that `FF FF FF FF` which tails the file was replaced with `53 54 49 4B` (`STIK`). Replacing `53 54 49 4B` with the original `FF FF FF FF` will fix this file.
* Step 7: Upon fixing the two modified files, the project will open in Paint3D. This will open up a project with a 3d fish model.
* Step 8: Select the fish model with the select tool and rotate the fish, which has Paint3D "Stickers" applied to the model. These stickers spell out the flag in the appropriate format.

## How It Works
The mesh files were chosen to be modified so that when Paint3D attempted to load the 3D Model of the fish, it would not be able to parse and render. This results in Paint3D being unable to load the overall project. Fixing this allows Paint3D to open the project without issues, and thus recovery of the flag possible. Although this is a simple fix on the file level, exploring and understanding how Paint3D handles projects within AppData, as well as investigating what normal Paint3D projects look like in order to fix the challenge project makes this extremely difficult due to lack of file format documentation.
