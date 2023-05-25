#! /usr/bin/env python3

import json
import subprocess
import os
import uuid
import time

# Check if the obsidian.json file exists
if os.path.isfile(os.path.expanduser("~/.config/obsidian/obsidian.json")) == False:
    print('obsidian.json file not found')
    exit()
else:
    obsidian_json_path = os.path.expanduser("~/.config/obsidian/obsidian.json")

def add_new_vault():
    print("Adding a new vault...")
    # Check if ~/Documents/ObsidianVaults exists. If not, creates it. This will hold the vaults.
    if os.path.isdir(os.path.expanduser('~/Documents/ObsidianVaults')) == False:
        print('Creating ~/Documents/ObsidianVaults directory')
        os.makedirs(os.path.expanduser('~/Documents/ObsidianVaults'))
        print('Directory created. Your new vaults will be saved here.')
    
    new_vault = input('Enter the name of your new vault: ')
    new_vault_path = os.path.expanduser('~/Documents/ObsidianVaults/' + new_vault)
    os.makedirs(new_vault_path)
    # Obsidian can use any value of string as a vault ID. This will generate a uniquie ID value in a different
    # format than Obsidian's 16-character value.
    new_vault_id = str(uuid.uuid4())

    # Add the new vault to the obsidian.json. Obsidian queries this file, and the vaults found here are what it lists as available vaults.
    with open(obsidian_json_path, "r") as file:
        obsidian_data = json.load(file)
        obsidian_data["vaults"][new_vault_id] = {
            "path": new_vault_path,
            "ts": int(time.time() * 1000)
    }

    # Save the updated obsidian.json
    with open(obsidian_json_path, "w") as file:
        json.dump(obsidian_data, file, indent=4)
    print("Your new vault has been added. Vault path: " + new_vault_path)
    print("You can now open it in Obsidian.")


def open_existing_vault():
    with open(obsidian_json_path, 'r') as f:
        config_data = json.load(f)

    vaults = config_data.get("vaults", {})
    if not vaults:
        print("No existing vaults found.")
        return

    print("Existing Vaults:")
    for i, vault_info in enumerate(vaults.values(), 1):
        vault_path = vault_info.get("path")
        vault_name = os.path.basename(vault_path)
        print(f"{i}. {vault_name}")
        print(f"   {vault_path}")

    selected = input("Enter the number of the vault to open (or 'q' to quit): ")

    if selected.lower() == 'q':
        return

    try:
        selected_index = int(selected) - 1
        selected_vault = list(vaults.values())[selected_index]
        vault_name = os.path.basename(selected_vault["path"])
        vault_path = os.path.expanduser(selected_vault["path"])

        if os.path.isdir(vault_path):
            # xdg-open is used to call the Obsidian URI to open the vault.
            subprocess.run(['xdg-open', f'obsidian://open?path={vault_path}'])
        else:
            print("Vault path is invalid.")

    except (ValueError, IndexError):
        print("Invalid selection.")


def main():
    print("Simple Obsidian Vault Manager")
    
    while True:
        print("\nMenu:")
        print("1. Add a new vault")
        print("2. Open an existing vault")
        print("3. Quit")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            add_new_vault()
        elif choice == '2':
            open_existing_vault()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
             
