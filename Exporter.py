import c4d
import os

def main():
    doc = c4d.documents.GetActiveDocument()

    # 1. Retrieve the export directory from 'ExportHelper'
    export_helper = doc.SearchObject("ExportHelper")
    if not export_helper:
        raise RuntimeError("Could not find 'ExportHelper' object in the scene.")

    base_path = export_helper[c4d.ID_USERDATA, 1]
    if not base_path:
        raise ValueError("Export path in 'ExportHelper' User Data is empty.")

    # 2. Get currently selected objects
    selections = doc.GetActiveObjects(0)
    if not selections:
        print("No objects selected for export.")
        return

    # 3. Setup FBX Exporter (Do this ONCE outside the loop)
    fbx_export_id = c4d.FORMAT_FBX_EXPORT
    plug = c4d.plugins.FindPlugin(fbx_export_id, c4d.PLUGINTYPE_SCENESAVER)
    if plug is None:
        raise RuntimeError("Failed to retrieve the FBX exporter.")

    data = dict()
    if not plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, data):
        raise RuntimeError("Failed to retrieve private data.")

    fbx_export = data.get("imexporter", None)
    if fbx_export is None:
        raise RuntimeError("Failed to retrieve BaseContainer private data.")

    # Defines FBX export settings
    fbx_export[c4d.FBXEXPORT_SELECTION_ONLY] = True

    # 4. Process and export each selected object
    for obj in selections:
        # Deselect all currently active objects
        for active_obj in doc.GetActiveObjects(0):
            doc.SetActiveObject(active_obj, c4d.SELECTION_SUB)

        # Select only the current object in the loop
        doc.SetActiveObject(obj, c4d.SELECTION_ADD)

        # Construct a safe file path
        file_name = f"{obj.GetName()}.fbx"
        file_path = os.path.join(base_path, file_name)

        # Export the document
        if not c4d.documents.SaveDocument(doc, file_path, c4d.SAVEDOCUMENTFLAGS_NONE, fbx_export_id):
            print(f"Failed to save: {file_path}")
        else:
            print(f"Document successfully exported to: {file_path}")

    # 5. Restore the original selection for the user
    for active_obj in doc.GetActiveObjects(0):
        doc.SetActiveObject(active_obj, c4d.SELECTION_SUB)
    for obj in selections:
        doc.SetActiveObject(obj, c4d.SELECTION_ADD)

    # Update Cinema 4D UI
    c4d.EventAdd()

if __name__ == '__main__':
    main()
