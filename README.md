# macautoclicker
a free mac auto clicker for all the people who want one. <br>
Its built better with python

# verify permissions

cd /path/to/your/folder 
// would look like cd ~/Downloads/macautoclicker-main<br>
xattr -d com.apple.quarantine ./start.command<br>
chmod +x ./start.command<br>
ls -l ./start.command<br>
./start.command<br>

# installing dependencies 
# pip3
pip3 install time threading tktinker json pynput PIL os

# pip
pip install time threading tktinker json pynput PIL os
