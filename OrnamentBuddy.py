# OrnamentBuddy.py
import adsk.core, adsk.fusion, traceback
import os, json
import importlib 

# Import logic
from . import ornament_logic

# FORCE RELOAD for dev
importlib.reload(ornament_logic)

app = None
ui = None
handlers = []
palette_id = 'EdJ_Orn_Palette'
command_id = 'EdJOrnCmd'

class MyCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            command = args.command
            onExecute = MyCommandExecuteHandler()
            command.execute.add(onExecute)
            handlers.append(onExecute)
        except:
            if ui: ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class MyCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            palette = ui.palettes.itemById(palette_id)
            
            # 1. Create Palette if it doesn't exist
            if not palette:
                script_folder = os.path.dirname(os.path.realpath(__file__))
                html_path = os.path.join(script_folder, 'resources', 'html', 'index.html')
                
                # Path Fixes for Windows
                url = html_path.replace('\\', '/')
                if not url.startswith('file:///'):
                    url = 'file:///' + url
                
                palette = ui.palettes.add(palette_id, 'Ornament Buddy', url, True, True, True, 350, 600)
                palette.dockingState = adsk.core.PaletteDockingStates.PaletteDockStateRight

                # --- MOVED HANDLER REGISTRATION HERE ---
                # Only add the "ear" (handler) when we create the palette.
                # This prevents adding a second ear if you click the button twice.
                onHtmlEvent = MyHTMLEventHandler()
                palette.incomingFromHTML.add(onHtmlEvent)
                handlers.append(onHtmlEvent)

            # 2. Show Palette
            palette.isVisible = True
            
            # 3. Initial Scan (Refresh Data)
            # We do this every time the button is clicked to ensure data is fresh
            payload = ornament_logic.scan_model()
            palette.sendInfoToHTML('update_ui', payload)

        except:
            if ui: ui.messageBox('Execution Failed:\n{}'.format(traceback.format_exc()))

class MyHTMLEventHandler(adsk.core.HTMLEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            html_args = adsk.core.HTMLEventArgs.cast(args)
            data = json.loads(html_args.data)
            action = data.get('action')
            palette = ui.palettes.itemById(palette_id)
            
            if action == 'refresh_data':
                payload = ornament_logic.scan_model()
                if palette: palette.sendInfoToHTML('update_ui', payload)

            elif action == 'update_text':
                ornament_logic.update_text_entity(data.get('text'), data.get('height'))
            
            elif action == 'set_active_bg':
                payload = ornament_logic.set_active_bg(data.get('bg_name'))
                if palette: palette.sendInfoToHTML('update_ui', payload)

            elif action == 'select_folder':
                folder_path = ornament_logic.pick_folder_dialog()
                # --- FIX IS HERE ---
                # We use json.dumps() to wrap the path in quotes (e.g. "C:/Path")
                # so the JavaScript JSON.parse() doesn't crash.
                if palette: 
                    palette.sendInfoToHTML('folder_selected', json.dumps(folder_path))

            elif action == 'do_export':
                # Pass 'palette' so logic can reset the status message when done
                ornament_logic.export_files(
                    data.get('folder'),
                    data.get('formats'), 
                    data.get('filename'),
                    palette
                )

        except:
            if ui: ui.messageBox('HTML Event Failed:\n{}'.format(traceback.format_exc()))

def run(context):
    global ui, app
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # 1. CLEAN UP ZOMBIES (Crucial Step)
        # We look for the button in the panel AND the command definition
        # and delete them to ensure a clean slate.
        
        modify_panel = ui.allToolbarPanels.itemById('SolidModifyPanel')
        if modify_panel:
            existing_control = modify_panel.controls.itemById(command_id)
            if existing_control:
                existing_control.deleteMe()

        cmdDefs = ui.commandDefinitions
        oldCmd = cmdDefs.itemById(command_id)
        if oldCmd: oldCmd.deleteMe()

        # 2. CREATE NEW COMMAND
        script_folder = os.path.dirname(os.path.realpath(__file__))
        resource_dir = os.path.join(script_folder, 'resources')
        
        cmdDef = cmdDefs.addButtonDefinition(
            command_id,
            'Ornament Buddy', 
            'Batch Tools',
            resource_dir 
        )
        
        # Optional: Set toolclip if it exists
        # cmdDef.toolClipFilename = os.path.join(resource_dir, 'toolClip.png')
        
        onCommandCreated = MyCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        handlers.append(onCommandCreated)
        
        # 3. ADD TO PANEL
        if modify_panel:
            control = modify_panel.controls.addCommand(cmdDef)
            control.isPromoted = False 
        
    except:
        if ui: ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    try:
        # 1. Delete Palette
        palette = ui.palettes.itemById(palette_id)
        if palette: palette.deleteMe()

        # 2. Delete Control (Button) from Panel
        modify_panel = ui.allToolbarPanels.itemById('SolidModifyPanel')
        if modify_panel:
            cntrl = modify_panel.controls.itemById(command_id)
            if cntrl: cntrl.deleteMe()
            
        # 3. Delete Command Definition
        cmdDef = ui.commandDefinitions.itemById(command_id)
        if cmdDef: cmdDef.deleteMe()
    except:
        pass