mkdir -p ~/.local/lib/krunner-plugins/krunner-mac-plugin/
mkdir -p ~/.local/share/kservices5/

# Copy files
cp ./krunner-mac-plugin.py ~/.local/lib/krunner-plugins/krunner-mac-plugin/
cp ./db.json ~/.local/lib/krunner-plugins/krunner-mac-plugin/

# Register in krunner
cp ./krunner-mac-plugin.desktop ~/.local/share/kservices5/

# Make autostart
cp ./krunner-mac-plugin-start.desktop ~/.config/autostart/

# Run it
python3.8 ~/.local/lib/krunner-plugins/krunner-mac-plugin/krunner-mac-plugin.py &