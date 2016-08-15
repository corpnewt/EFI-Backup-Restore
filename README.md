# EFI-Backup-Restore
A smallish script that can backup EFI partitions - and eventually restore them (hopefully).

***

Well, after adding some extras to this - it's no longer smallish.

-

Here's the rundown.  I wrote this script as a way to keep some running (zipped) backups of my EFI partitions so I could either restore them in the event of a failure, or clone them to another drive's EFI.

-

##What Does it do?

When you open this script, you're presented with a few options:

1. Backup EFI
2. Restore EFI
3. EFI to EFI copy
4. Open Backup Directory

-

###Backup EFI

After selecting this option - you'll be presented with a list of mounted volumes from which you can pick the parent drive to backup.  You can pick a drive using one of the following:

* Number in the list
* Mount point
* Volume name
* Disk identifier

Once you've selected a drive, the script will scan the root directory for the existence of an EFI folder (implying a Legacy install).  If it finds one, it will ask if you want to back it up.  If you choose to, it will create a zip file located at the backup directory (~/EFI Backup-Restore by default) with the naming scheme: *VolumeName*-*EFIF*-*TimeStamp*.zip

After that completes, it will check the disk for the existence of an EFI partition, and ask if you'd like to back that up.  If you choose to, it will mount the EFI partition, then create a zip like above, but with the following naming scheme:  *VolumeName*-*EFI*-*TimeStamp*.zip

*EFIF* = EFI Folder

*EFI* = EFI Partition

Note - if you really want to confuse the script, you can mount the EFI partition prior to running it, and choose it as your backup drive.  Since it's both the selected volume *and* the EFI partition - you'll end up with two backups.

After the script finishes backing up the EFI partition - it will ask if you'd like it unmounted, and unmount it for you if you choose.

-

###Restore EFI

After selecting this option - you'll be presented with a list of backups in your backup directory (~/EFI Backup-Restore/ by default).  You can select which backup to restore by choosing the number from the list.

Once you've selected which zip you would like to restore - you'll be presented with a list of mounted volumes.  This list responds to the same options as the one listed in the *Backup EFI* section.

After selecting the drive you'd like to restore to - the script will ask if you want to restore to the root of the drive (i.e. for a Legacy EFI restore), and then ask if you want to restore to the EFI partition (for a UEFI restore).  You can do both if you choose.

Similar to the *Backup EFI* section - the script offers to unmount the EFI partition if it mounted it.

-

###EFI to EFI copy

This section allows you to copy one EFI folder/partition to another drive.  It's useful for post-install EFI copying from a USB installer to the main hard drive.  I also use it to clone my main EFI to my backup install's EFI to ensure they are the same.

It allows you to pick *either* an EFI folder or partition (depending on whether or not it finds any), then copy it to the root of the destination volume and/or the EFI partition.

-

###Open Backup Directory

This is pretty self explanatory.  Selecting this option just opens the backup directory (~/EFI Backup-Restore/ by default) in the Finder.

-

###To Do

I plan to consolidate some of the code so it isn't as wordy.  There are plenty of spots that I could trim down by encapsulating some functions (I'm looking at you, disk listing code).  I may also set up some checks to determine whether or not root access is needed - since it really only comes into effect when on the root of a drive, and not the EFI partition.  Aside from that - I'm sure I could do some general cleanup on the code as a whole, but for the time being it's functional, so I'm not super concerned with this.

-

###Comments/Questions/Bugs

Feel free to post issues here, message me on Reddit (https://www.reddit.com/user/corpnewt/), or hop on [my discord channel](https://discord.gg/GMDjp79).  I hope you find this useful!
