# Ornament Buddy
**Rapidly configure and export personalized ornaments.**

![Ornament Buddy Icon](resources/OrnamentBuddyAppIcon.png)

## Introduction: The "Why" and "What"
Let's be honest: manually editing a sketch to change a name, then hunting through the timeline to suppress and unsuppress different background patterns for every single ornament order is a tedious nightmare. I built this tool because I wanted to spend less time clicking through menus and more time printing.

**Ornament Buddy** is a dedicated Palette for Fusion 360 that acts as a "remote control" for your design. It links directly to specific sketches and timeline groups, allowing you to configure unique ornaments in seconds.

* **Instant Text Updates:** Update the name and font height without ever entering the Sketch environment.
* **One-Click Styling:** Switch between different background patterns (Timeline Groups) instantly.
* **Batch Exporting:** Auto-generates filenames and exports to STL, 3MF, and STEP simultaneously.

## Installation

### Windows Users
1.  **Download:** Download the latest installer (`OrnamentBuddy_Win.exe` or `.msi`) from the **Releases** section on the right.
2.  **Install:** Double-click the installer to run it.
    * *Note: If Windows protects your PC saying "Unknown Publisher," click **More Info** → **Run Anyway**.*
3.  **Restart:** If Fusion is open, restart it to load the new add-in.

### Mac Users
1.  **Download:** Download the latest package (`OrnamentBuddy_Mac.pkg`) from the **Releases** section on the right.
2.  **Install:** Double-click the package to run the installer.
    * *Note: If macOS prevents the install, Right-Click the file and choose **Open**, then click **Open** again in the dialog box.*
3.  **Restart:** If Fusion is open, restart it to load the new add-in.

### Verify Installation
Once installed, **Ornament Buddy** should be available in Fusion.

1.  Open Fusion.
2.  Look for the **Ornament Buddy** icon in the **Solid > Modify** panel.
3.  If you don't see it:
    * Press `Shift+S` to open **Scripts and Add-Ins**.
    * Make sure the **Add-Ins** tab is selected.
    * Find "Ornament Buddy" in the list and ensure **Run on Startup** is checked.
    * Click **Run**.

## Using Ornament Buddy

### Preparing Your File
For the add-in to work, your Fusion design needs two specific things:
1.  A sketch named **`nameText`** containing the text you want to change.
2.  Timeline Groups named starting with **`BG_`** (e.g., `BG_Snowflake`, `BG_Stars`) containing the bodies/features for that specific style.

### The Palette Interface
Click the **Ornament Buddy** button in the Modify panel to open the palette.

* **Name (Text):** Type a name here to instantly update the `nameText` sketch.
* **Font Height:** Adjusts the size of the text (in mm).
* **Style List:** Shows all timeline groups that start with `BG_`. Clicking one will unsuppress that group and suppress all others.
* **Export:** Select your output folder and file formats (STL, 3MF, STEP). The filename is auto-generated based on the Name and Style you selected.

## Tech Stack

For the fellow coders and makers out there, here is how Ornament Buddy was built:

* **Language:** Python (Fusion 360 API)
* **Interface:** HTML/CSS/JavaScript (Palette based)
* **Data Handling:** JSON for communicating between the Python backend and the JavaScript frontend.

## Acknowledgements & Credits

* **Developer:** Ed Johnson ([Making With An EdJ](https://www.youtube.com/@makingwithanedj))
* **AI Assistance:** Developed with coding assistance from Google's Gemini.
* **Lucy (The Cavachon Puppy):**
    ***Chief Wellness Officer & Director of Mandatory Breaks***
    * Thank you for ensuring I maintained healthy circulation by interrupting my deep coding sessions with urgent requests for play.
* **License:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.

***

*Happy Making!*
*— EdJ*