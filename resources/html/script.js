document.addEventListener('DOMContentLoaded', function() {
    // --- THEME LOGIC ---
    const toggleSwitch = document.getElementById('theme-checkbox');
    const savedTheme = localStorage.getItem('edj_orn_theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    toggleSwitch.checked = (savedTheme === 'dark');
    
    toggleSwitch.addEventListener('change', function(e) {
        const newTheme = e.target.checked ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('edj_orn_theme', newTheme);
    });

    // --- EVENT LISTENERS ---
    document.getElementById('refreshBtn').addEventListener('click', refreshData);
    document.getElementById('browseBtn').addEventListener('click', selectFolder);
    document.getElementById('exportBtn').addEventListener('click', doExport);
    document.getElementById('nameInput').addEventListener('input', triggerUpdate);
    document.getElementById('heightInput').addEventListener('change', triggerUpdate);

    waitForFusion();
});

let currentData = {};
let currentFolder = "";

// --- CONNECTION MANAGER ---

function waitForFusion() {
    if (window.adsk) {
        window.fusionJavaScriptHandler = {
            handle: function(action, data) {
                try {
                    var parsed = typeof data === 'string' ? JSON.parse(data) : data;
                    if (action === 'update_ui') renderUI(parsed);
                    if (action === 'folder_selected') updateFolder(parsed);
                    // No more status handling needed here
                } catch (e) {
                    console.error(e);
                }
                return "OK";
            }
        };
        refreshData();
    } else {
        setTimeout(waitForFusion, 500);
    }
}

function sendToFusion(action, data = {}) {
    data.action = action;
    const jsonStr = JSON.stringify(data);
    if (window.adsk && window.adsk.fusion) {
        window.adsk.fusion.sendCommand(jsonStr);
    } else if (window.adsk && window.adsk.fusionSendData) {
        window.adsk.fusionSendData('send', jsonStr);
    }
}

// --- LOGIC ---

function refreshData() { sendToFusion('refresh_data'); }

let timeout = null;
function triggerUpdate() {
    updateFilenamePreview();
    const text = document.getElementById('nameInput').value;
    const height = document.getElementById('heightInput').value;
    clearTimeout(timeout);
    timeout = setTimeout(() => {
        sendToFusion('update_text', { text: text, height: height });
    }, 400);
}

function selectFolder() { sendToFusion('select_folder'); }

function updateFolder(path) {
    currentFolder = path;
    const disp = document.getElementById('folderPath');
    disp.innerText = path || "No folder selected";
    disp.title = path;
}

function renderUI(data) {
    currentData = data;
    
    const nameIn = document.getElementById('nameInput');
    if (!nameIn.value && data.current_text) nameIn.value = data.current_text;
    
    const heightIn = document.getElementById('heightInput');
    if (document.activeElement !== heightIn) heightIn.value = data.current_height;

    const list = document.getElementById('bgList');
    list.innerHTML = '';
    let activeStyle = "";

    if (data.bg_groups) {
        data.bg_groups.forEach(bg => {
            const row = document.createElement('div');
            row.className = 'radio-row';
            if (bg.isActive) {
                row.classList.add('selected');
                activeStyle = bg.name.replace("BG_", "");
            }
            row.innerHTML = `<div class="radio-circle">${bg.isActive ? '●' : ''}</div><span>${bg.name}</span>`;
            row.onclick = () => { sendToFusion('set_active_bg', { bg_name: bg.name }); };
            list.appendChild(row);
        });
    }

    if (data.saved_folder && !currentFolder) updateFolder(data.saved_folder);
    window.currentActiveStyle = activeStyle;
    updateFilenamePreview();
}

function updateFilenamePreview() {
    const name = document.getElementById('nameInput').value || "Name";
    const style = window.currentActiveStyle || "Style";
    const fname = document.getElementById('filenameInput');
    if (document.activeElement !== fname) fname.value = `${name}_${style}`;
}

function doExport() {
    const folder = currentFolder;
    const filename = document.getElementById('filenameInput').value;
    const formats = [];
    document.querySelectorAll('.format-row input:checked').forEach(cb => formats.push(cb.value));

    if (!folder) {
        alert("Please select an output folder.");
        return;
    }
    
    // Just send the command, no local UI changes needed
    sendToFusion('do_export', { folder: folder, formats: formats, filename: filename });
}