import adsk.core, adsk.fusion, traceback
import json
import os

# CONSTANTS
SKETCH_NAME = "nameText"
GROUP_PREFIX = "BG_"
ATTR_GROUP = "EdJ_Orn"
ATTR_FOLDER = "Last_Folder"

def get_design():
    app = adsk.core.Application.get()
    return app.activeProduct

def scan_model():
    """Scans for nameText sketch and BG groups."""
    design = get_design()
    if not design: return json.dumps({"error": "No design"})
    
    # 1. Find Text Info
    text_val = ""
    height_val = 10.0 
    
    root = design.rootComponent
    sk = root.sketches.itemByName(SKETCH_NAME)
    
    if sk and sk.sketchTexts.count > 0:
        txt_ent = sk.sketchTexts.item(0)
        text_val = txt_ent.text
        # Convert cm to mm for UI
        height_val = txt_ent.height * 10 

    # 2. Find Background Groups
    bg_groups = []
    timeline = design.timeline
    
    for group in timeline.timelineGroups:
        if group.name.startswith(GROUP_PREFIX):
            bg_groups.append({
                "name": group.name,
                "isActive": not group.isSuppressed
            })

    # 3. Get Last Folder
    last_folder = ""
    attr = root.attributes.itemByName(ATTR_GROUP, ATTR_FOLDER)
    if attr: 
        last_folder = attr.value.replace('\\', '/')

    return json.dumps({
        "current_text": text_val,
        "current_height": height_val,
        "bg_groups": bg_groups,
        "saved_folder": last_folder
    })

def update_text_entity(new_text, new_height_mm):
    design = get_design()
    root = design.rootComponent
    sk = root.sketches.itemByName(SKETCH_NAME)
    
    if sk and sk.sketchTexts.count > 0:
        txt_ent = sk.sketchTexts.item(0)
        txt_ent.text = new_text
        try:
            h_cm = float(new_height_mm) / 10.0
            txt_ent.height = h_cm
        except:
            pass 

def set_active_bg(target_name):
    design = get_design()
    timeline = design.timeline
    
    for group in timeline.timelineGroups:
        if group.name.startswith(GROUP_PREFIX):
            should_suppress = (group.name != target_name)
            if group.isSuppressed != should_suppress:
                group.isSuppressed = should_suppress
                
    return scan_model()

def pick_folder_dialog():
    ui = adsk.core.Application.get().userInterface
    folderDlg = ui.createFolderDialog()
    folderDlg.title = 'Select Export Folder'
    
    dialogResult = folderDlg.showDialog()
    if dialogResult == adsk.core.DialogResults.DialogOK:
        safe_path = folderDlg.folder.replace('\\', '/')
        design = get_design()
        design.rootComponent.attributes.add(ATTR_GROUP, ATTR_FOLDER, safe_path)
        return safe_path
    return ""

def load_saved_settings():
    pass

def export_files(folder_path, formats, base_filename, palette):
    """Exports files and shows a summary message box."""
    app = adsk.core.Application.get()
    ui = app.userInterface
    design = app.activeProduct
    exportMgr = design.exportManager
    root = design.rootComponent
    
    # 1. Validation: Check if any format is selected
    if not formats or len(formats) == 0:
        ui.messageBox("Please select one or more output file formats.", "Export Warning")
        return

    # 2. Validation: Check Folder
    if not os.path.exists(folder_path):
        ui.messageBox("Error: Output folder not found.", "Export Error")
        return

    safe_name = "".join([c for c in base_filename if c.isalpha() or c.isdigit() or c in " ._-"]).strip()
    if not safe_name: safe_name = "Ornament"

    exported_files = []
    
    try:
        # STL
        if 'stl' in formats:
            fname = safe_name + ".stl"
            path = os.path.join(folder_path, fname)
            stlOptions = exportMgr.createSTLExportOptions(root, path)
            stlOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
            stlOptions.isBinaryFormat = True
            exportMgr.execute(stlOptions)
            exported_files.append(fname)

        # 3MF
        if '3mf' in formats:
            fname = safe_name + ".3mf"
            path = os.path.join(folder_path, fname)
            thremfOptions = exportMgr.createC3MFExportOptions(root, path)
            exportMgr.execute(thremfOptions)
            exported_files.append(fname)

        # STEP
        if 'step' in formats:
            fname = safe_name + ".step"
            path = os.path.join(folder_path, fname)
            stepOptions = exportMgr.createSTEPExportOptions(path, root)
            exportMgr.execute(stepOptions)
            exported_files.append(fname)
            
        # Reset Palette Status (Optional visual cleanup)
        if palette:
            palette.sendInfoToHTML('export_complete', "Ready")
            adsk.doEvents()

        # Build Success Message
        msg = "Export Successful!\n\nFiles created:\n"
        for f in exported_files:
            msg += f"- {f}\n"
        
        msg += f"\nExported to:\n{folder_path}"
        
        ui.messageBox(msg, "Ornament Export")

    except:
        ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))