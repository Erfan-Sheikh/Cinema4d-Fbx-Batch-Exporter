import c4d
def main():
    # Retrieves a path to save the exported file
    # filePath = c4d.storage.LoadDialog(title="Save File for Mamad Export", flags=c4d.FILESELECT_SAVE, force_suffix="fbx")
    filePath = ""
    filePathConst = ""
    docc = c4d.documents.GetActiveDocument()
    allObjects = docc.GetObjects()
    for val in allObjects:
        if val.GetName() == "ExportHelper":
            filePathConst = val[c4d.ID_USERDATA, 1]
    docc = c4d.documents.GetActiveDocument()
    selections = docc.GetActiveObjects(0)
    for x in range(0, len(selections)):
        docc.SetActiveObject(selections[x], c4d.SELECTION_SUB)
        docc.GetActiveObject()
    for x in range(0, len(selections)):
        docc.SetActiveObject(selections[x], c4d.SELECTION_ADD)
        docc.GetActiveObject()
        selectionName = selections[x].GetName()
        filePath = filePathConst + "/" +  selectionName + ".fbx"
        # filePath = c4d.storage.LoadDialog(title="Save File for Mamad Export", flags=c4d.FILESELECT_SAVE, force_suffix="fbx")
        if not filePath:
            return
        # Retrieves Obj export plugin, defined in R17 as FORMAT_OBJ2EXPORT and below R17 as FORMAT_OBJEXPORT
        fbxExportId = c4d.FORMAT_FBX_EXPORT
        plug = c4d.plugins.FindPlugin(fbxExportId, c4d.PLUGINTYPE_SCENESAVER)
        if plug is None:
            raise RuntimeError("Failed to retrieve the OBJ exporter.")
        data = dict()
        # Sends MSG_RETRIEVEPRIVATEDATA to OBJ export plugin
        if not plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, data):
            raise RuntimeError("Failed to retrieve private data.")
        # BaseList2D object stored in "imexporter" key hold the settings
        objExport = data.get("imexporter", None)
        if objExport is None:
            raise RuntimeError("Failed to retrieve BaseContainer private data.")
        # Defines OBJ export settings
        objExport[c4d.FBXEXPORT_SELECTION_ONLY] = True
        # objExport[c4d.OBJEXPORTOPTIONS_EXPORT_UVS] = c4d.OBJEXPORTOPTIONS_UV_ORIGINAL
        # Finally export the document
        if not c4d.documents.SaveDocument(doc, filePath, c4d.SAVEDOCUMENTFLAGS_NONE, fbxExportId):
            raise RuntimeError("Failed to save the document.")
        print("Document successfully exported to:", filePath)
        filePath = ""
        docc.SetActiveObject(selections[x], c4d.SELECTION_SUB)
        docc.GetActiveObject()
if __name__ == '__main__':
    main()