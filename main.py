import threading
import tkinter
import tkinter.filedialog
import customtkinter
import os
import json
import subprocess
import sys
import base64
from github import Github
import webbrowser
import re
from functools import partial

# GitHub setup
username = "FantomWolf182"
repository_name = "MindCraftGUI"
file_path = "pyproject.toml"  # or "setup.py", depending on your project

# Local version
local_version = "1.0.0"  # Replace with your local version

# Get the repository content from GitHub
g = Github()
user = g.get_user(username)
repo = user.get_repo(repository_name)
file_content = repo.get_contents(file_path)

# Decodes the content to get the version string
content = base64.b64decode(file_content.content).decode("utf-8")

# Extract the version string
github_version = None
for line in content.splitlines():
    if "version=" in line or "version =" in line:
        github_version = line.split("=")[1].strip().strip("\"'")




# Function to check for updates and show a popup
def check_for_updates(parent):
    if local_version != github_version:
       show_update_popup(parent, github_version, local_version)
def show_update_popup(parent, new_version, current_version):
    popup = customtkinter.CTkToplevel(parent)
    popup.title("Update Available")
    frame = customtkinter.CTkFrame(popup)
    frame.pack(padx=10, pady=10, fill="both", expand=True)
    update_label = customtkinter.CTkLabel(frame,
                                          text=f"Update Available:\nVersion: {new_version}\nCurrent Version: {current_version}",
                                          font=customtkinter.CTkFont(size=20, weight="bold"))
    update_label.pack(padx=10, pady=10)

    update_button = customtkinter.CTkButton(frame, text="Update", command=update_and_restart)
    update_button.pack(side="left", padx=10, pady=10)

    dismiss_button = customtkinter.CTkButton(frame, text="Dismiss", command=popup.destroy)
    dismiss_button.pack(side="right", padx=10, pady=10)

#
def update_and_restart():
    # URL to the latest release
    update_url = "https://github.com/FantomWolf182/MindCraftGUI/releases/latest"
    webbrowser.open(update_url)


customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

CONFIG_FILE = "config.json"


# Load the config.json file
with open(CONFIG_FILE, 'r') as file:
    config = json.load(file)

# Retrieve the last selected folder path
folder_path = config.get('last_selected_folder', '')
#print(folder_path)

settings_js_path = os.path.join(folder_path, 'settings.js')



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()


        def loadmemory_toggle_change(self):
            # Check the actual state of the switch
            is_on = self.advanced_switch.get() == "on"
            #print(f"Switch is now {'on' if is_on else 'off'}")

            if is_on:
                #print("Load memory is ON.")
                # Path to the settings.js file
                settings_js_path = os.path.join(self.selected_folder_path, 'settings.js')

                # Check if the file exists
                if os.path.exists(settings_js_path):
                    with open(settings_js_path, 'r') as js_file:
                        contents = js_file.read()

                    # Define the regular expression pattern to find the load_memory key
                    pattern = r'("load_memory":\s*)[^,}\s]*'
                    replacement = r'\1true'

                    # Replace the value of the load_memory key
                    updated_contents = re.sub(pattern, replacement, contents)

                    # Write the updated contents back to the file
                    with open(settings_js_path, 'w') as js_file:
                        js_file.write(updated_contents)

                    print(f"Updated 'load_memory' field in '{settings_js_path}' to 'true'.")
                else:
                    print(f"Error: '{settings_js_path}' does not exist or you forgot to select a MindCraft folder")
            else:
                #print("Load memory is OFF.")
                # Path to the settings.js file
                settings_js_path = os.path.join(self.selected_folder_path, 'settings.js')

                # Check if the file exists
                if os.path.exists(settings_js_path):
                    with open(settings_js_path, 'r') as js_file:
                        contents = js_file.read()

                    # Define the regular expression pattern to find the load_memory key
                    pattern = r'("load_memory":\s*)[^,}\s]*'
                    replacement = r'\1false'

                    # Replace the value of the load_memory key
                    updated_contents = re.sub(pattern, replacement, contents)

                    # Write the updated contents back to the file
                    with open(settings_js_path, 'w') as js_file:
                        js_file.write(updated_contents)

                    print(f"Updated 'load_memory' field in '{settings_js_path}' to 'false'.")
                else:
                    print(f"Error: '{settings_js_path}' does not exist or you forgot to select a MindCraft folder")

        def insecurecoding_toggle_change(self):
            switch_value = self.insecure_switch.get()
            #print(f"Switch value retrieved: {switch_value}")  # Debugging statement
            if switch_value == 1:
                # print("Load memory is ON.")
                # Path to the settings.js file
                settings_js_path = os.path.join(self.selected_folder_path, 'settings.js')

                # Check if the file exists
                if os.path.exists(settings_js_path):
                    with open(settings_js_path, 'r') as js_file:
                        contents = js_file.read()

                    # Define the regular expression pattern to find the load_memory key
                    pattern = r'("allow_insecure_coding":\s*)[^,}\s]*'
                    replacement = r'\1true'

                    # Replace the value of the load_memory key
                    updated_contents = re.sub(pattern, replacement, contents)

                    # Write the updated contents back to the file
                    with open(settings_js_path, 'w') as js_file:
                        js_file.write(updated_contents)

                    print(f"Updated 'insecure coding' field in '{settings_js_path}' to 'true'.")
                else:
                    print(f"Error: '{settings_js_path}' does not exist or you forgot to select a MindCraft folder")
            if switch_value == 0:
                # print("Load memory is ON.")
                # Path to the settings.js file
                settings_js_path = os.path.join(self.selected_folder_path, 'settings.js')

                # Check if the file exists
                if os.path.exists(settings_js_path):
                    with open(settings_js_path, 'r') as js_file:
                        contents = js_file.read()

                    # Define the regular expression pattern to find the load_memory key
                    pattern = r'("allow_insecure_coding":\s*)[^,}\s]*'
                    replacement = r'\1false'

                    # Replace the value of the load_memory key
                    updated_contents = re.sub(pattern, replacement, contents)

                    # Write the updated contents back to the file
                    with open(settings_js_path, 'w') as js_file:
                        js_file.write(updated_contents)

                    print(f"Updated 'insecure coding' field in '{settings_js_path}' to 'false'.")
                else:
                    print(f"Error: '{settings_js_path}' does not exist or you forgot to select a MindCraft folder")

        def verbose_toggle_change(self):
            switch_value = self.verbose_switch.get()
            #print(f"Switch value retrieved: {switch_value}")  # Debugging statement
            if switch_value == 1:
                settings_js_path = os.path.join(self.selected_folder_path, 'settings.js')
                if os.path.exists(settings_js_path):
                    with open(settings_js_path, 'r') as js_file:
                        contents = js_file.read()

                    pattern = r'("verbose_commands":\s*)[^,}\s]*'
                    replacement = r'\1true'

                    updated_contents = re.sub(pattern, replacement, contents)

                    with open(settings_js_path, 'w') as js_file:
                        js_file.write(updated_contents)

                    print(f"Updated 'verbose commands' field in '{settings_js_path}' to 'true'.")
                else:
                    print(f"Error: '{settings_js_path}' does not exist or you forgot to select a MindCraft folder")
            elif switch_value == 0:
                settings_js_path = os.path.join(self.selected_folder_path, 'settings.js')
                if os.path.exists(settings_js_path):
                    with open(settings_js_path, 'r') as js_file:
                        contents = js_file.read()

                    pattern = r'("verbose_commands":\s*)[^,}\s]*'
                    replacement = r'\1false'

                    updated_contents = re.sub(pattern, replacement, contents)

                    with open(settings_js_path, 'w') as js_file:
                        js_file.write(updated_contents)

                    print(f"Updated 'verbose commands' field in '{settings_js_path}' to 'false'.")
                else:
                    print(f"Error: '{settings_js_path}' does not exist or you forgot to select a MindCraft folder")

        def narrate_behavior_toggle_change(self):
            switch_value = self.narrate_behavior_switch.get()
            #print(f"Switch value retrieved: {switch_value}")  # Debugging statement
            settings_js_path = os.path.join(self.selected_folder_path, 'settings.js')

            if os.path.exists(settings_js_path):
                with open(settings_js_path, 'r') as js_file:
                    contents = js_file.read()

                # Regular expression pattern to find the narrate_behavior key
                pattern = r'("narrate_behavior":\s*)[^,}\s]*'
                replacement = r'\1true' if switch_value == 1 else r'\1false'

                # Replace the value of the narrate_behavior key
                updated_contents = re.sub(pattern, replacement, contents)

                # Write the updated contents back to the file
                with open(settings_js_path, 'w') as js_file:
                    js_file.write(updated_contents)

                status = "true" if switch_value == 1 else "false"
                print(f"Updated 'narrate behavior' field in '{settings_js_path}' to '{status}'.")
            else:
                print(f"Error: '{settings_js_path}' does not exist or you forgot to select a MindCraft folder")

        # Configure window
        self.title("MindCraft GUI")
        self.geometry(f"{1100}x{580}")
        self.iconbitmap("icon.ico")

        # Configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Usage:",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # useage buttons
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Locally",
                                                        command=self.locally_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Online servers",
                                                        command=self.online_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.config_label = customtkinter.CTkLabel(self.sidebar_frame, text="Config:",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.config_label.grid(row=3, column=0, padx=20, pady=(20, 10))


        # Configuration buttons
        self.folder_selector_button = customtkinter.CTkButton(self.sidebar_frame, text="Select MindCraft folder",
                                                        command=self.open_folder_dialog_event)
        self.folder_selector_button.grid(row=4, column=0, padx=20, pady=(10, 0))
        self.string_input_button = customtkinter.CTkButton(self.sidebar_frame, text="API Keys",
                                                        command=self.open_input_dialog_event
)
        self.string_input_button.grid(row=5, column=0, padx=20, pady=(10, 0))

        for i in range(1, 10):  # Assuming you have 10 rows in total
            self.sidebar_frame.grid_rowconfigure(i, weight=1)

        # Appearance mode and scaling options
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))

        # main entry and button
        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2,text_color=("white", "#FFFFFF"), text = "Run Bots", border_color=("green", "#4F7942"), command=self.run_bots_button_event)
        self.main_button_1.grid(row=3, column=1, padx=(20,20), pady=(20, 20), sticky="nsew")


        # CTkTextbox as 'terminal'
        self.text_label = customtkinter.CTkTextbox(self, font=("Arial", 12), wrap=tkinter.WORD, height=400, width=200)
        self.text_label.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")

        class TextRedirector:
            def __init__(self, widget):
                self.widget = widget

            def write(self, text):
                self.widget.configure(state="normal")  # Enable the textbox to add text
                self.widget.insert(tkinter.END, text)
                self.widget.configure(state="disabled")  # Disable the textbox to prevent editing
                self.widget.see(tkinter.END)  # Scroll to the end

            def flush(self):
                pass

        #this basically redirects terminal
        sys.stdout = TextRedirector(self.text_label)
        print("Please select a folder by clicking the 'Select MindCraft Folder'")


        self.text_label.configure(state="disabled")  # Start with the text box disabled


        # Create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Settings")
        self.scrollable_frame.grid(row=0, column=2, padx=(0, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.configure(height=700)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        # Create and place textboxes in the scrollable frame
        self.scrollable_frame_entries = []
        self.version_entry = customtkinter.CTkEntry(master=self.scrollable_frame, placeholder_text="Minecraft Version")
        self.version_entry.grid(row=1, column=0, padx=10, pady=(0, 20), sticky="ew")
        self.scrollable_frame_entries.append(self.version_entry)

        self.address_entry = customtkinter.CTkEntry(master=self.scrollable_frame,
                                       placeholder_text="Host Address (can use 'localhost')")
        self.address_entry.grid(row=2, column=0, padx=10, pady=(0, 20), sticky="ew")
        self.scrollable_frame_entries.append(self.address_entry)

        self.port_entry = customtkinter.CTkEntry(master=self.scrollable_frame, placeholder_text="Port")
        self.port_entry.grid(row=3, column=0, padx=10, pady=(0, 20), sticky="ew")
        self.scrollable_frame_entries.append(self.port_entry)

        # Advanced label
        self.label_advanced = customtkinter.CTkLabel(master=self.scrollable_frame, text="Advanced:",
                                                     font=('Helvetica bold', 15))
        self.label_advanced.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        # divider
        divider = customtkinter.CTkProgressBar(master=self.scrollable_frame, orientation="horizontal",
                                               mode="determinate")
        divider.set(100)  # Set the progress bar value to 100
        divider.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Alabel for the switch
        self.advanced_label = customtkinter.CTkLabel(master=self.scrollable_frame, text="Load memory")
        self.advanced_label.grid(row=6, column=0, padx=10, pady=(10, 5), sticky="ew")
        self.advanced_label = customtkinter.CTkLabel(master=self.scrollable_frame,
                                                     text="(loads memory from previous session)",
                                                     font=('Helvetica bold', 10))
        self.advanced_label.grid(row=7, column=0, padx=10, pady=(1, 5), sticky="ew")

        # True/false switch
        load_memory_toggle_state = customtkinter.StringVar(value="on")
        self.advanced_switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text="",
                                                       command=lambda: loadmemory_toggle_change(self), onvalue="on",
                                                       offvalue="off")
        self.advanced_switch.grid(row=8, column=0, padx=10, pady=(5, 10), sticky="ew")

        # Label for the switch
        self.advanced_label = customtkinter.CTkLabel(master=self.scrollable_frame, text="Allow Insecure Coding")
        self.advanced_label.grid(row=9, column=0, padx=10, pady=(10, 5), sticky="ew")
        self.advanced_label = customtkinter.CTkLabel(master=self.scrollable_frame, text="(Enable At Own Risk)",
                                                     font=('Helvetica bold', 10))
        self.advanced_label.grid(row=10, column=0, padx=10, pady=(1, 5), sticky="ew")

        # True/false switch
        self.insecure_switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text="",
                                                       command=lambda: insecurecoding_toggle_change(self))
        self.insecure_switch.grid(row=11, column=0, padx=10, pady=(5, 10), sticky="ew")

        #label for the switch
        self.advanced_label = customtkinter.CTkLabel(master=self.scrollable_frame, text="Verbose Commands?")
        self.advanced_label.grid(row=12, column=0, padx=10, pady=(10, 5), sticky="ew")
        self.advanced_label = customtkinter.CTkLabel(master=self.scrollable_frame, text="(shows full command syntax)",
                                                     font=('Helvetica bold', 10))
        self.advanced_label.grid(row=13, column=0, padx=10, pady=(1, 5), sticky="ew")

        #true/false switch
        self.verbose_switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text="",
                                                      command=lambda: verbose_toggle_change(self))
        self.verbose_switch.grid(row=14, column=0, padx=10, pady=(5, 10), sticky="ew")

        #label for the switch
        self.advanced_label = customtkinter.CTkLabel(master=self.scrollable_frame, text="Narrate Behavior?")
        self.advanced_label.grid(row=15, column=0, padx=10, pady=(10, 5), sticky="ew")
        self.advanced_label = customtkinter.CTkLabel(master=self.scrollable_frame,
                                                     text="(Chats simple automatic actions ('Picking up item!'))",
                                                     font=('Helvetica bold', 10))
        self.advanced_label.grid(row=16, column=0, padx=10, pady=(1, 5), sticky="ew")

        #true/false switch
        self.narrate_behavior_switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text="",
                                                               command=lambda: narrate_behavior_toggle_change(self))
        self.narrate_behavior_switch.grid(row=17, column=0, padx=10, pady=(5, 20), sticky="ew")

        # advanced entries
        self.timeout_entry = customtkinter.CTkEntry(master=self.scrollable_frame,
                                       placeholder_text="Code Timeout Mins (-1 for no timeout)")
        self.timeout_entry.grid(row=18, column=0, padx=10, pady=(0, 20), sticky="ew")
        self.scrollable_frame_entries.append(self.timeout_entry)

        self.max_commands_entry = customtkinter.CTkEntry(master=self.scrollable_frame, placeholder_text="Max Commands (-1 for no limit)")
        self.max_commands_entry.grid(row=19, column=0, padx=10, pady=(0, 20), sticky="ew")
        self.scrollable_frame_entries.append(self.max_commands_entry)

        # Checkbox and switch frame (checkboxes added automatically)
        self.checkbox_slider_frame = customtkinter.CTkScrollableFrame(self)
        self.checkbox_slider_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        # Default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.folder_selector_button.configure(text="Select MindCraft Folder")
        self.verbose_switch.select()
        self.narrate_behavior_switch.select()

        # Instance variable to store folder path
        self.selected_folder_path = ""

        check_for_updates(self)

    def run_npm_install(self, folder_path):
        os.chdir(folder_path)
        process = subprocess.Popen(["npm", "install"], cwd=folder_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Display the output in real-time
        for line in process.stdout:
            print(line.decode("utf-8"), end="")

        for line in process.stderr:
            print(line.decode("utf-8"), end="")

    def run_bots_button_event(self):
        thread = threading.Thread(target=self.run_bots)
        thread.start()


    def run_bots(self):
        minecraft_version = self.version_entry.get()
        address = self.address_entry.get()
        port = self.port_entry.get()
        timeout = self.timeout_entry.get()
        max_commands = self.max_commands_entry.get()

        # Path to the settings.js file
        settings_js_path = os.path.join(self.selected_folder_path, 'settings.js')

        # Check if the file exists
        if os.path.exists(settings_js_path):
            with open(settings_js_path, 'r', encoding='utf-8') as js_file:
                contents = js_file.read()

            # Update settings based on user input
            contents = re.sub(r'("minecraft_version":\s*)".*?"', lambda m: f'{m.group(1)}"{minecraft_version}"',
                              contents)
            contents = re.sub(r'("host":\s*)".*?"', lambda m: f'{m.group(1)}"{address}"', contents)
            contents = re.sub(r'("port":\s*)\d+', lambda m: f'{m.group(1)}{port}', contents)
            contents = re.sub(r'("code_timeout_mins":\s*)\d+', lambda m: f'{m.group(1)}{timeout}', contents)
            contents = re.sub(r'("max_commands":\s*)-?\d+', lambda m: f'{m.group(1)}{max_commands}', contents)


            contents = re.sub(r',\s*}', '}', contents)  # Removes trailing comma before the closing brace

            # Handle empty values for `code_timeout_mins` and `max_commands` properly
            contents = re.sub(r'("code_timeout_mins":\s*,)', '"code_timeout_mins": -1,', contents)
            contents = re.sub(r'("max_commands":\s*,)', '"max_commands": -1,', contents)

            # Write the updated contents back to the file
            with open(settings_js_path, 'w', encoding='utf-8') as js_file:
                js_file.write(contents)

            print(f"Settings updated in '{settings_js_path}':")
            print(f"Minecraft Version: {minecraft_version}")
            print(f"Address: {address}")
            print(f"Port: {port}")
            print(f"Code Timeout: {timeout}")
            print(f"Max Commands: {max_commands}")

            # Run the main.js script
            os.chdir(self.selected_folder_path)
            process = subprocess.Popen(
                ["node", "main.js"],
                cwd=self.selected_folder_path,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Display the output in real-time
            for line in process.stdout:
                print(line, end="")

            for line in process.stderr:
                print(line, end="")

            process.wait()

        else:
            print(f"Error: '{settings_js_path}' does not exist or you forgot to select a Minecraft folder")

    def load_checkboxes(self):
        # Clear any existing checkboxes
        for widget in self.checkbox_slider_frame.winfo_children():
            widget.destroy()

        # Ensure a folder has been selected
        if not self.selected_folder_path:
            return

        # Iterate through all JSON files in the selected folder
        profile_path = os.path.join(self.selected_folder_path, 'profiles')
        json_files = [f for f in os.listdir(profile_path) if f.endswith('.json')]

        # Clear previous checkboxes
        self.checkboxes = []

        for idx, json_file in enumerate(json_files):
            # Create a checkbox and ensure it captures the current `json_file`
            checkbox = customtkinter.CTkCheckBox(
                master=self.checkbox_slider_frame,
                text=json_file
            )
            # Use partial to bind the checkbox to the event handler
            checkbox.configure(command=partial(self.checkbox_toggle_event, checkbox))
            checkbox.grid(row=idx, column=0, pady=(20, 0) if idx == 0 else (10, 0), padx=20, sticky="n")
            # Add checkbox to the list
            self.checkboxes.append(checkbox)

    def checkbox_toggle_event(self, checkbox):
        profile_name = f"./profiles/{checkbox.cget('text')}"
        js_file_path = 'settings.js'

        try:
            #Read the content of settings.js
            if os.path.exists(js_file_path):
                with open(js_file_path, 'r') as js_file:
                    content = js_file.read()

                # Find the profiles array in the content
                profiles_match = re.search(r'"profiles":\s*\[([^\]]*)\]', content)
                if not profiles_match:
                    raise ValueError("Profiles section not found in settings.js")

                # Extract current profiles list
                profiles_content = profiles_match.group(1).strip()
                current_profiles = re.findall(r'"(.*?)"', profiles_content)

                # Modify the profiles list based on the checkbox state
                if checkbox.get():  # Checkbox is checked
                    if profile_name not in current_profiles:
                        current_profiles.append(profile_name)
                        print(f"Added {profile_name} to profiles")
                else:  # Checkbox is unchecked
                    if profile_name in current_profiles:
                        current_profiles.remove(profile_name)
                        print(f"Removed {profile_name} from profiles")

                # Creates the new profiles content in a single line
                new_profiles_content = ', '.join(f'"{profile}"' for profile in current_profiles)
                updated_content = content[:profiles_match.start(1)] + new_profiles_content + content[
                                                                                             profiles_match.end(1):]

                # Writes the updated content back to settings.js
                with open(js_file_path, 'w') as js_file:
                    js_file.write(updated_content)

                print(f"Settings.js updated successfully")

            else:
                raise FileNotFoundError(f"{js_file_path} does not exist")

        except Exception as e:
            print(f"An error occurred: {e}")

    def open_folder_dialog_event(self):
        folder_path = tkinter.filedialog.askdirectory(title="Select a Folder")
        if folder_path:
            if any(os.path.isfile(os.path.join(folder_path, f)) for f in os.listdir(folder_path)):
                self.selected_folder_path = folder_path
            else:
                subfolders = [f.path for f in os.scandir(folder_path) if f.is_dir()]
                if subfolders:
                    self.selected_folder_path = subfolders[0]
                else:
                    print("Selected folder is empty and contains no subfolders.")
                    self.selected_folder_path = folder_path

            print("Selected folder:", self.selected_folder_path)

            # Saves the selected folder path to config.json
            config['last_selected_folder'] = self.selected_folder_path
            with open(CONFIG_FILE, 'w') as file:
                json.dump(config, file, indent=4)
            print("Updated config.json with the selected folder path.")

            self.load_checkboxes()

            example_file_path = os.path.join(self.selected_folder_path, 'keys.example.json')
            new_file_path = os.path.join(self.selected_folder_path, 'keys.json')

            os.chdir(folder_path)

            threading.Thread(target=self.run_npm_install, args=(folder_path,)).start()



            if os.path.isfile(example_file_path):
                os.rename(example_file_path, new_file_path)
                print(f"Renamed '{example_file_path}' to '{new_file_path}'")
            else:
                pass
                #print(f"No 'keys.example.json' file found in the selected folder.")

            settings_js_path = os.path.join(folder_path, 'settings.js')

            if os.path.exists(settings_js_path):
                # Read the file contents
                with open(settings_js_path, 'r') as js_file:
                    contents = js_file.read()

                # Define the regular expression patterns and replacements
                patterns_replacements = [
                    (r'("allow_insecure_coding":\s*)[^,}\s]*', r'\1false'),
                    (r'("load_memory":\s*)[^,}\s]*', r'\1false'),
                    (r'("verbose_commands":\s*)[^,}\s]*', r'\1true'),
                    (r'("narrate_behavior":\s*)[^,}\s]*', r'\1true')
                ]

                # Apply all patterns and replacements
                updated_contents = contents
                for pattern, replacement in patterns_replacements:
                    updated_contents = re.sub(pattern, replacement, updated_contents)

                # Write the updated contents back to the file
                with open(settings_js_path, 'w') as js_file:
                    js_file.write(updated_contents)

            else:
                print("Alert: An issue occurred this may have happened due to an outdated mindcraft version.")

            try:
                # Reads the content of settings.js
                if os.path.exists(settings_js_path):
                    with open(settings_js_path, 'r') as js_file:
                        content = js_file.read()

                    # Finds the profiles array in the content
                    profiles_match = re.search(r'"profiles":\s*\[([^\]]*)\]', content)
                    if not profiles_match:
                        raise ValueError("Profiles section not found in settings.js")

                    #Replaces the profiles array with an empty array
                    updated_content = re.sub(r'"profiles":\s*\[[^\]]*\]', '"profiles": []', content)

                    #Writes the updated content back to settings.js
                    with open(settings_js_path, 'w') as js_file:
                        js_file.write(updated_content)

                    print(f"Profiles array cleared successfully in settings.js")

                else:
                    raise FileNotFoundError(f"{settings_js_path} does not exist")

            except Exception as e:
                print(f"An error occurred: {e}")


    def open_input_dialog_event(self):
        # Checks if the folder has been selected
        if not self.selected_folder_path:
            print("No folder selected.")
            return

        print(f"Selected folder path in open_input_dialog_event: {self.selected_folder_path}")

        json_file_path = os.path.join(self.selected_folder_path, 'keys.json')
        if os.path.isfile(json_file_path):
            with open(json_file_path, 'r') as f:
                try:
                    json_data = json.load(f)
                    self.show_json_in_popup(json_data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON file: {e}")
        else:
            print(f"No 'keys.json' file found in the selected folder.")


        json_file_path = os.path.join(self.selected_folder_path, 'keys.json')
        if os.path.isfile(json_file_path):
            with open(json_file_path, 'r') as f:
                try:
                    json_data = json.load(f)
                    self.show_json_in_popup(json_data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON file: {e}")
        else:
            print(f"No 'keys.json' file found in the selected folder.")

    def show_json_in_popup(self, json_data):
        # Creates a new top-level window
        popup = customtkinter.CTkToplevel(self)
        popup.title("API Keys")

        # Creates a frame for the table
        table_frame = customtkinter.CTkFrame(popup)
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        #  headers
        headers = ["NAME:", "API KEY:"]
        for idx, header in enumerate(headers):
            label = customtkinter.CTkLabel(table_frame, text=header, font=("Arial", 12, "bold"))
            label.grid(row=0, column=idx, padx=10, pady=5, sticky="n")

        # rows and store entries
        entry_widgets = {}
        for row_idx, (key, value) in enumerate(json_data.items()):
            name_label = customtkinter.CTkLabel(table_frame, text=key)
            name_label.grid(row=row_idx + 1, column=0, padx=10, pady=5, sticky="n")

            text_entry = customtkinter.CTkEntry(table_frame, width=200)
            text_entry.insert(0, str(value))
            text_entry.grid(row=row_idx + 1, column=1, padx=10, pady=5, sticky="ew")

            entry_widgets[key] = text_entry

        # save function
        def save_changes():
            for key, entry in entry_widgets.items():
                json_data[key] = entry.get()

            json_file_path = os.path.join(self.selected_folder_path, 'keys.json')
            with open(json_file_path, 'w') as f:
                json.dump(json_data, f, indent=4)
            print("API keys saved successfully!")
            save_button.configure(state="disabled")

        # monitors changes in entry widgets
        def on_entry_change(var, index, mode):
            for key, entry in entry_widgets.items():
                if entry.get() != json_data[key]:
                    save_button.configure(state="normal")
                    break
            else:
                save_button.configure(state="disabled")

        # Attach trace to each entry widget's text variable
        for key, entry in entry_widgets.items():
            entry_var = entry.cget("textvariable")
            if not entry_var:
                entry_var = tkinter.StringVar(value=str(json_data[key]))
                entry.configure(textvariable=entry_var)
            entry_var.trace_add("write", on_entry_change)

        # Create Save and Exit buttons
        save_button = customtkinter.CTkButton(popup, text="Save", command=save_changes, state="disabled")
        save_button.pack(padx=20, pady=10, side="left", expand=True)

        exit_button = customtkinter.CTkButton(popup, text="Exit", command=popup.destroy)
        exit_button.pack(padx=20, pady=10, side="right", expand=True)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def online_button_event(self):
        settings_js_path = os.path.join(self.selected_folder_path, 'settings.js')

        # Reads existing settings
        if os.path.exists(settings_js_path):
            with open(settings_js_path, 'r') as js_file:
                contents = js_file.read()

            # Defines the regular expression pattern to find the auth key
            pattern = r'("auth":\s*")([^"]*)(")'
            replacement = r'\1microsoft\3'

            # Replaces the value of the auth key
            updated_contents = re.sub(pattern, replacement, contents)

            # Writes the updated contents back to the file
            with open(settings_js_path, 'w') as js_file:
                js_file.write(updated_contents)

            print(f"Updated 'auth' field in '{settings_js_path}' to 'microsoft'.")
        else:
            print(f"Error: '{settings_js_path}' does not exist. Did you select a MindCraft folder?")

    def locally_button_event(self):
        settings_js_path = os.path.join(self.selected_folder_path, 'settings.js')

        # Reads existing settings
        if os.path.exists(settings_js_path):
            with open(settings_js_path, 'r') as js_file:
                contents = js_file.read()

            # Defines the regular expression pattern to find the auth key
            pattern = r'("auth":\s*")([^"]*)(")'
            replacement = r'\1offline\3'

            # Replaces the value of the auth key
            updated_contents = re.sub(pattern, replacement, contents)

            # Writes the updated contents back to the file
            with open(settings_js_path, 'w') as js_file:
                js_file.write(updated_contents)

            print(f"Updated 'auth' field in '{settings_js_path}' to 'offline'.")
        else:
            print(f"Error: '{settings_js_path}' does not exist. Did you select a MindCraft folder?")







if __name__ == "__main__":
    app = App()
    app.mainloop()
