#!/usr/bin/env python
# 0.0.0
from Scripts import *
import os, tempfile, datetime, shutil, time, plistlib, json, sys, re

class EFI:
    def __init__(self, **kwargs):
        self.r  = run.Run()
        self.d  = disk.Disk()
        self.u  = utils.Utils("EFI Backup-Restore")
        self.boot_manager = bdmesg.get_bootloader_uuid()
        # Get the tools we need
        self.script_folder = "Scripts"
        
        self.settings_file = kwargs.get("settings", None)
        cwd = os.getcwd()
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        if self.settings_file and os.path.exists(self.settings_file):
            self.settings = json.load(open(self.settings_file))
        else:
            self.settings = {
                # Default settings here
                "default_disk" : None,
                "full_layout"  : False,
                "skip_countdown" : False,
            }
        os.chdir(cwd)
        self.full = self.settings.get("full_layout", False)
        # Verify we have a backup folder - and create it if we don't
        self.save_path = os.path.realpath(os.path.expanduser("~/EFI Backup-Restore"))
        if not os.path.isdir(self.save_path):
            os.mkdir(self.save_path)

    def flush_settings(self):
        if self.settings_file:
            cwd = os.getcwd()
            os.chdir(os.path.dirname(os.path.realpath(__file__)))
            json.dump(self.settings, open(self.settings_file, "w"))
            os.chdir(cwd)

    def default_disk(self):
        self.u.resize(80, 24)
        self.u.head("Select Default Disk")
        print(" ")
        print("1. None")
        print("2. Boot Disk")
        if self.boot_manager:
            print("3. Booted Clover/OC")
        print(" ")
        print("M. Main Menu")
        print("Q. Quit")
        print(" ")
        menu = self.u.grab("Please pick a default disk:  ")
        if not len(menu):
            self.default_disk()
        menu = menu.lower()
        if menu in ["1","2"]:
            self.settings["default_disk"] = [None, "boot"][int(menu)-1]
            self.flush_settings()
            return
        elif menu == "3" and clover:
            self.settings["default_disk"] = "clover"
            self.flush_settings()
            return
        elif menu == "m":
            return
        elif menu == "q":
            self.u.custom_quit()
        self.default_disk()

    def get_efi(self,header=None,allow_main=True):
        while True:
            self.d.update()
            pad = 4
            disk_string = "\n"
            if not self.settings.get("full_layout"):
                boot_disk = self.d.get_parent(self.boot_manager)
                mounts = self.d.get_mounted_volume_dicts()
                # Gather some formatting info
                name_pad = size_pad = type_pad = 0
                index_pad = len(str(len(mounts)))
                for x in mounts:
                    if len(str(x["name"])) > name_pad: name_pad = len(str(x["name"]))
                    if len(x["size"]) > size_pad: size_pad = len(x["size"])
                    if len(str(x["readable_type"])) > type_pad: type_pad = len(str(x["readable_type"]))
                for i,d in enumerate(mounts,start=1):
                    disk_string += "{}. {} | {} | {} | {}".format(
                        str(i).rjust(index_pad),
                        str(d["name"]).ljust(name_pad),
                        d["size"].rjust(size_pad),
                        str(d["readable_type"]).ljust(type_pad),
                        d["identifier"]
                    )
                    if boot_disk and self.d.get_parent(d["identifier"]) == boot_disk:
                        disk_string += " *"
                    disk_string += "\n"
            else:
                mounts = self.d.get_disks_and_partitions_dict()
                disks = list(mounts)
                index_pad = len(str(len(disks)))
                # Gather some formatting info
                name_pad = size_pad = type_pad = 0
                for d in disks:
                    for x in mounts[d]["partitions"]:
                        name = "Container for {}".format(x["container_for"]) if "container_for" in x else str(x["name"])
                        if len(name) > name_pad: name_pad = len(name)
                        if len(x["size"]) > size_pad: size_pad = len(x["size"])
                        if len(str(x["readable_type"])) > type_pad: type_pad = len(str(x["readable_type"]))
                for i,d in enumerate(disks,start=1):
                    disk_string+= "{}. {} ({}):\n".format(
                        str(i).rjust(index_pad),
                        d,
                        mounts[d]["size"]
                    )
                    if mounts[d].get("scheme"):
                        disk_string += "      {}\n".format(mounts[d]["scheme"])
                    if mounts[d].get("physical_stores"):
                        disk_string += "      Physical Store{} on {}\n".format(
                            "" if len(mounts[d]["physical_stores"])==1 else "s",
                            ", ".join(mounts[d]["physical_stores"])
                        )
                    parts = mounts[d]["partitions"]
                    part_list = []
                    for p in parts:
                        name = "Container for {}".format(p["container_for"]) if "container_for" in p else p["name"]
                        p_text = "        - {} | {} | {} | {}".format(
                            str(name).ljust(name_pad),
                            p["size"].rjust(size_pad),
                            str(p["readable_type"]).ljust(type_pad),
                            p["identifier"]
                        )
                        if self.boot_manager and p["disk_uuid"] == self.boot_manager:
                            # Got boot manager
                            p_text += " *"
                        part_list.append(p_text)
                    if len(part_list):
                        disk_string += "\n".join(part_list) + "\n"
            disk_string += "\nS. Switch to {} Output\n".format("Slim" if self.settings.get("full_layout") else "Full")
            disk_string += "B. Select the Boot Drive's EFI\n"
            if self.boot_manager:
                disk_string += "C. Select the Booted EFI (Clover/OC)\n"
            dd = self.settings.get("default_disk")
            dd = self.boot_manager if dd=="clover" else "/" if dd=="boot" else dd
            di = self.d.get_identifier(dd)
            disk_string += "D. Pick Default Disk ({})\n".format(
                "{} - {}".format(self.d.get_volume_name(di),di) if di else "None Set"
            )
            disk_string += ("\nM. Main" if allow_main else "") + "\nQ. Quit\n"
            if self.boot_manager:
                disk_string += "\n(* denotes the booted EFI (Clover/OC)"
            height = max(len(disk_string.split("\n"))+pad,24)
            width  = max((len(x) for x in disk_string.split("\n")))
            if self.settings.get("resize_window",True): self.u.resize(max(80,width), height)
            self.u.head(header)
            print(disk_string)
            menu = self.u.grab("Pick the drive containing your EFI:  ")
            if not len(menu):
                continue
            if menu.lower() == "q":
                if self.settings.get("resize_window",True): self.u.resize(80,24)
                self.u.custom_quit()
            elif allow_main and menu.lower() == "m":
                if self.settings.get("resize_window",True): self.u.resize(80,24)
                return
            elif menu.lower() == "s":
                self.settings["full_layout"] = not self.settings.get("full_layout")
                continue
            elif menu.lower() == "b":
                disk = "/"
                iden = self.d.get_efi("/")
            elif menu.lower() == "c" and self.boot_manager:
                disk = self.boot_manager
                iden = self.d.get_efi(self.boot_manager)
            elif menu.lower() == "d":
                self.default_disk()
                continue
            else:
                try: disk = mounts[int(menu)-1]["identifier"] if isinstance(mounts,list) else list(mounts)[int(menu)-1]
                except: disk = menu
            if self.settings.get("resize_window",True): self.u.resize(80,24)
            iden = self.d.get_identifier(disk)
            if not iden:
                self.u.head("Invalid Disk")
                print("")
                print("'{}' is not a valid disk!".format(disk))
                print("")
                self.u.grab("Returning in 5 seconds...", timeout=5)
                continue
            # Valid disk!
            efi = self.d.get_efi(iden)
            if not efi:
                self.u.head("No EFI Partition")
                print("")
                print("There is no EFI partition associated with {}!".format(iden))
                print("")
                self.u.grab("Returning in 5 seconds...", timeout=5)
                continue
            return efi

    def select_folders(self, dirs, title = "Select Folders"):
        # Iterate through the volumes inside the EFI folder and decide what to keep - or just keep all
        dirs.sort(key=lambda x:x.get("name",""))
        while True:
            num = 0
            out = ""
            for x in dirs:
                num += 1
                out+="{} {}. {}\n".format("[#]" if x["on"] else "[ ]", num, x["name"])
            out += "\nA. All\nN. None\n\nC. Confirm\n\nM. Main\nQ. Quit\n"
            height = len(out.split("\n")) + 5
            if height < 24:
                height = 24
            self.u.resize(80, height)
            self.u.head(title)
            print(" ")
            print(out)
            menu = self.u.grab("Please make a selection:  ")
            if not len(menu):
                continue
            menu = menu.lower()
            if menu == "q":
                self.u.custom_quit()
            elif menu == "m":
                return None
            elif menu == "a":
                for x in dirs:
                    x["on"] = True
                continue
            elif menu == "n":
                for x in dirs:
                    x["on"] = False
                continue
            elif menu == "c":
                return dirs
            # Split args using regex
            menu_list = re.findall(r"[\w']+", menu)
            for m in menu_list:
                # Get numeric value
                try:
                    m = int(m)
                except:
                    continue
                if m > 0 and m <= len(dirs):
                    m_obj = dirs[m-1]
                    m_obj["on"] = False if m_obj["on"] else True

    def backup_efi(self):
        # First we get our EFI
        efi = self.get_efi("Select An EFI To Backup")
        if not efi:
            return
        # Got an EFI
        is_mounted = self.d.is_mounted(efi)
        if not is_mounted:
            self.u.head("Mounting {}".format(efi))
            print("")
            out = self.d.mount_partition(efi)
            if out[2] == 0:
                print(out[0])
            else:
                self.u.grab(out[1], timeout=5)
                return
        # Mounted - let's check for contents
        mp = self.d.get_mount_point(efi)
        mp_efi = os.path.join(mp, "EFI")
        if not os.path.exists(mp_efi):
            if not is_mounted:
                # We need to unmount
                self.d.unmount_partition(efi)
            self.u.grab("Missing EFI folder!", timeout=5)
            return
        dirs = [{"name":x, "on":False} for x in os.listdir(mp_efi) if not x.lower().startswith(".") and os.path.isdir(os.path.join(mp_efi, x))]
        back_list = self.select_folders(dirs, "Please Select Folders To Backup")
        if back_list == None:
            return
        if not any(x["on"] for x in back_list):
            if not is_mounted:
                # We need to unmount
                self.d.unmount_partition(efi)
            self.u.grab("Nothing to backup!", timeout=5)
            return
        # Got folders to backup!
        cwd = os.getcwd()
        os.chdir(mp)
        # Zip shiz up
        zip_name = "EFI-Backup-{:%Y-%m-%d %H.%M.%S}.zip".format(datetime.datetime.now())
        self.u.head("Zipping {}".format(zip_name))
        print("")
        zip_list = [os.path.join("./EFI", x["name"]) for x in back_list if x["on"]]
        args = [
            "zip",
            "-r",
            os.path.join(self.save_path, zip_name)
        ]
        args.extend(zip_list)
        out = self.r.run({"args":args, "stream":True})
        os.chdir(cwd)
        if not is_mounted:
            # We need to unmount
            self.d.unmount_partition(efi)
        if out[2] != 0:
            self.u.grab(out[1], timeout=5)
            return
        self.u.grab("\nCreated {}!\n\nPress [enter] to return...".format(zip_name))

    def restore_efi(self):
        # Get the backups list
        backups = [x for x in os.listdir(self.save_path) if x.lower().endswith(".zip") and not x.startswith(".")]
        backups.sort()
        chosen = None
        while True:
            num = 0
            out = ""
            for x in backups:
                num += 1
                out+="{}. {}\n".format(num, x)
            out += "\nM. Main\nQ. Quit\n"
            height = len(out.split("\n")) + 5
            print(height)
            if height < 24:
                height = 24
            self.u.resize(80, height)
            self.u.head("Please Select A Backup To Restore")
            print(" ")
            print(out)
            menu = self.u.grab("Please make a selection:  ")
            if not len(menu):
                continue
            menu = menu.lower()
            if menu == "q":
                self.u.custom_quit()
            elif menu == "m":
                return
            # Get the int value and stuff
            try:
                menu = int(menu)
            except:
                continue
            if menu < 1 or menu > len(backups):
                continue
            chosen = backups[menu-1]
            break
        # Got our backup - let's list the files and get our list of folders to restore
        out = self.r.run({"args":["unzip", "-Z1", os.path.join(self.save_path, chosen)]})
        paths = out[0].split("\n")
        top_dirs = []
        for p in paths:
            path = os.path.normpath(p).split(os.sep)
            if len(path) > 2:
                top_dirs.append(path[1])
        top_dirs = [{"name":x, "on":False} for x in set(top_dirs) if not x.startswith(".")]
        res_list = self.select_folders(top_dirs, "Please Select Folders To Restore")
        if res_list == None:
            return
        if not any(x["on"] for x in res_list):
            self.u.grab("Nothing to restore!", timeout=5)
            return
        # Now we get our EFI
        efi = self.get_efi("Select An EFI To Restore To")
        if not efi:
            return
        # Got an EFI
        is_mounted = self.d.is_mounted(efi)
        if not is_mounted:
            self.u.head("Mounting {}".format(efi))
            print("")
            out = self.d.mount_partition(efi)
            if out[2] == 0:
                print(out[0])
            else:
                self.u.grab(out[1], timeout=5)
                return
        self.u.head("Restoring {}".format(efi))
        print("")
        # Mounted - let's check for contents
        mp = self.d.get_mount_point(efi)
        if not os.path.exists(os.path.join(mp, "EFI")):
            os.mkdir(os.path.join(mp, "EFI"))
        # Extract to a temp folder - then copy over
        print("Extracting from zip...")
        temp = tempfile.mkdtemp()
        args = [
            "unzip",
            os.path.join(self.save_path, chosen)
        ]
        args.extend(["EFI/{}/*".format(x["name"]) for x in res_list if x["on"]])
        args.extend(["-d", temp])
        out = self.r.run({"args":args, "stream":True})
        if out[2] != 0:
            self.u.grab(out[1], timeout=5)
            shutil.rmtree(temp, ignore_errors=True)
            if not is_mounted:
                # We need to unmount
                self.d.unmount_partition(efi)
            return
        print("Pruning folders...")
        # Iterate through the folders and remove any we're about to replace
        for x in res_list:
            if not x["on"]:
                continue
            if os.path.exists(os.path.join(mp, "EFI", x["name"])):
                print("   Removing {}...".format(x["name"]))
                #try:
                shutil.rmtree(os.path.join(mp, "EFI", x["name"]), ignore_errors=True)
                #except:
                #    print("   - Failed to remove!")
                #    pass
        # Copy folders from the temp dir over to the EFI
        print("Copying new folders...")
        for f in os.listdir(os.path.join(temp, "EFI")):
            # Copy each folder
            if f.startswith("."):
                continue
            print("   {}...".format(f))
            shutil.move(os.path.join(temp, "EFI", f), os.path.join(mp, "EFI", f))
        if not is_mounted:
            # We need to unmount
            self.d.unmount_partition(efi)
        print("Cleaning up temp dir...")
        shutil.rmtree(temp, ignore_errors=True)
        self.u.grab("\nRestored {} to {}!\n\nPress [enter] to return...".format(chosen, efi))

    def efi_to_efi(self):
        # Now we get our EFI
        efi_source = self.get_efi("Select An EFI Source")
        if not efi_source:
            return
        efi_dest = self.get_efi("Select An EFI Destination")
        if not efi_dest:
            return
        self.u.head("{} --> {}".format(efi_source, efi_dest))
        print("")
        s_mounted = self.d.is_mounted(efi_source)
        if not s_mounted:
            out = self.d.mount_partition(efi_source)
            if out[2] == 0:
                print(out[0])
            else:
                self.u.grab(out[1], timeout=5)
                return
        d_mounted = self.d.is_mounted(efi_dest)
        if not d_mounted:
            out = self.d.mount_partition(efi_dest)
            if out[2] == 0:
                print(out[0])
            else:
                if not s_mounted:
                    self.d.unmount_partition(efi_source)
                self.u.grab(out[1], timeout=5)
                return
        # At this point - we should have 2 mounted EFIs
        s_m = self.d.get_mount_point(efi_source)
        d_m = self.d.get_mount_point(efi_dest)
        s_dirs = [x for x in os.listdir(os.path.join(s_m, "EFI")) if not x.startswith(".") and os.path.isdir(os.path.join(s_m, "EFI", x))]
        if not len(s_dirs):
            self.u.grab("Source EFI is empty!", timeout=5)
            if not d_mounted:
                self.d.unmount_partition(efi_dest)
            if not s_mounted:
                self.d.unmount_partition(efi_source)
            return
        # Clear the target EFI
        print("Pruning folders...")
        for x in s_dirs:
            if os.path.exists(os.path.join(d_m, "EFI", x)):
                print("   Removing {}...".format(x))
                #try:
                shutil.rmtree(os.path.join(d_m, "EFI", x), ignore_errors=True)
                #except:
                #    print("   - Failed to remove!")
                #    pass
        # Copy them over
        print("Copying new folders...")
        for f in s_dirs:
            # Copy each folder
            if f.startswith("."):
                continue
            print("   {}...".format(f))
            #try:
            shutil.copytree(os.path.join(s_m, "EFI", f), os.path.join(d_m, "EFI", f))
            #except:
            #    print("   - Failed to copy!")
            #    pass
        if not d_mounted:
            self.d.unmount_partition(efi_dest)
        if not s_mounted:
            self.d.unmount_partition(efi_source)
        self.u.grab("\nCopied {} to {}!\n\nPress [enter] to return...".format(efi_source, efi_dest))
        
    def main(self):
        # Pick our task
        self.u.resize(80, 24)
        self.u.head()
        print("")
        print("1. Backup EFI")
        print("2. Restore EFI")
        print("3. EFI to EFI Copy")
        if os.path.exists(self.save_path):
            print("4. Open Save Path")
        print("")
        print("Q. Quit")
        print("")
        menu = self.u.grab("Please select an option:  ")
        if not len(menu):
            self.main()
            return
        menu = menu.lower()
        if menu == "q":
            self.u.custom_quit()
        elif menu == "1":
            self.backup_efi()
        elif menu == "2":
            self.restore_efi()
        elif menu == "3":
            self.efi_to_efi()
        elif menu == "4" and os.path.exists(self.save_path):
            self.r.run({"args":["open",self.save_path]})
        self.main()

    def quiet_mount(self, disk_list):
        ret = 0
        for disk in disk_list:
            ident = self.d.get_identifier(disk)
            if not ident:
                continue
            efi = self.d.get_efi(ident)
            if not efi:
                continue
            out = self.d.mount_partition(efi)
            if not out[2] == 0:
                ret = out[2]
        exit(ret)

if __name__ == '__main__':

    e = EFI(settings="./Scripts/settings.json")
    # Check for args
    if len(sys.argv) > 1:
        # We got command line args!
        e.quiet_mount(sys.argv[1:])
    else:
        e.main()
