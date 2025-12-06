#!/bin/bash
set -e

# ==============================================================================
# 統 CONFIGURATION (edit this section)
# ==============================================================================
# ⭐️ IMPORTANT: Update these three variables for each project ⭐️
APP_NAME="OrnamentBuddy"                 
# AddIns or Scripts
APP_TYPE="AddIns"
IDENTIFIER="com.makingwithanedj.ornamentbuddy"         
VERSION="1.0"
# ==============================================================================

# GET PARENT FOLDER NAME
# We assume the script is in /[Repo Name]/Installers/
# So ".." is /[Repo Name]/
REPO_ROOT=".."
FOLDER_NAME=$(basename "$(cd "$REPO_ROOT" && pwd)")
INSTALL_LOCATION="Library/Application Support/Autodesk/Autodesk Fusion 360/API/$APP_TYPE/$FOLDER_NAME"

# Define the final output name using the desired convention
FINAL_PACKAGE_NAME="${APP_NAME}Installer_Mac.pkg"

echo "=========================================="
echo "      MAC USER-ONLY INSTALLER BUILDER"
echo "=========================================="

# 1. CLEANUP OLD BUILDS
rm -f "$FINAL_PACKAGE_NAME" # Updated to remove the dynamically named file
rm -f "component.pkg"
rm -f "distribution.xml"
rm -rf "staging_area"

# 2. CREATE STAGING AREA (To exclude 'Installers' folder from the build)
echo "逃 Staging files..."
mkdir -p "staging_area"
# Copy everything from Parent to Staging, excluding specific items
rsync -av --exclude='Installers' --exclude='.git' --exclude='.gitignore' --exclude='.DS_Store' --exclude='__pycache__' "$REPO_ROOT/" "staging_area/"

# 3. PERMISSIONS FIX
echo "肌 Fixing permissions..."
find "staging_area" -type f -exec chmod 644 {} \;
find "staging_area" -type d -exec chmod 755 {} \;

# 4. BUILD COMPONENT
echo "逃 Building Component..."
pkgbuild --root "staging_area" \
         --identifier "$IDENTIFIER" \
         --version "$VERSION" \
         --install-location "$INSTALL_LOCATION" \
         component.pkg

# 5. GENERATE DISTRIBUTION XML
echo "統 Generating XML..."
cat <<EOF > distribution.xml
<?xml version="1.0" encoding="utf-8"?>
<installer-gui-script minSpecVersion="1">
    <title>$APP_NAME</title>
    <options customize="never" require-scripts="false"/>
    
    <license file="../resources/License.rtf"/>
    
    <domains enable_anywhere="false" enable_currentUserHome="true" enable_localSystem="false" />
    <choices-outline>
        <line choice="default"/>
    </choices-outline>
    <choice id="default" title="$APP_NAME">
        <pkg-ref id="$IDENTIFIER"/>
    </choice>
    <pkg-ref id="$IDENTIFIER" version="$VERSION" onConclusion="none">component.pkg</pkg-ref>
</installer-gui-script>
EOF

# 6. BUILD FINAL INSTALLER
echo "珍 Creating Final Installer..."
productbuild --distribution distribution.xml \
             --package-path . \
             "$FINAL_PACKAGE_NAME" # <--- Uses the dynamic name variable

# 7. CLEANUP
rm component.pkg
rm distribution.xml
rm -rf "staging_area"

echo "=========================================="
echo "笨 SUCCESS! Installer created: $FINAL_PACKAGE_NAME"
echo "=========================================="
