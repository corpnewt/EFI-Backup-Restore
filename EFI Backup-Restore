#!/bin/bash

#This script will let you backup and restore EFI folders/partitions to zip
#files.


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"

# Turn on case-insensitive matching
shopt -s nocasematch
# turn on extended globbing
shopt -s extglob

backupLocation="~/EFI Backup-Restore"

driveName=""
driveMount=""
driveIdent=""
driveDisk=""
drivePart=""

efiFolder=""

efiName=""
efiMount=""
efiIdent=""
efiDisk=""
efiPart=""

driveSourceName=""
driveSourceMount=""
driveSourceIdent=""
driveSourceDisk=""
driveSourcePart=""

efiSourceName=""
efiSourceMount=""
efiSourceIdent=""
efiSourceDisk=""
efiSourcePart=""

function expandPath () {
    
    echo "${1/#\~/$HOME}"

}

function checkRoot () {
	if [[ "$(whoami)" != "root" ]]; then
		clear
		echo This script requires root privileges.
		echo Please enter your admin password to continue.
		echo 
		sudo "$0" "$1"
		exit $?
	fi

}

function resetVars () {
    driveName=""
    driveMount=""
    driveIdent=""
    driveDisk=""
    drivePart=""
    
    efiFolder=""
    
    efiName=""
    efiMount=""
    efiIdent=""
    efiDisk=""
    efiPart=""
    
    driveSourceName=""
    driveSourceMount=""
    driveSourceIdent=""
    driveSourceDisk=""
    driveSourcePart=""
    
    efiSourceName=""
    efiSourceMount=""
    efiSourceIdent=""
    efiSourceDisk=""
    efiSourcePart=""
}

function setDrive () {
	driveName="$( getDiskName "$1" )"
	driveMount="$( getDiskMountPoint "$1" )"
	driveIdent="$( getDiskIdentifier "$1" )"
	driveDisk="$( getDiskNumber "$1" )"
	drivePart="$( getPartitionNumber "$1" )"
    
    if [[ "$driveName" == "" ]]; then
        driveName="Untitled"
    fi
}

function setEFI () {
    efiName="$( getDiskName "$1" )"
	efiMount="$( getDiskMountPoint "$1" )"
	efiIdent="$( getDiskIdentifier "$1" )"
	efiDisk="$( getDiskNumber "$1" )"
	efiPart="$( getPartitionNumber "$1" )"
    
    if [[ "$efiName" == "" ]]; then
        efiName="Untitled"
    fi
}

function setDriveSource () {
	driveSourceName="$( getDiskName "$1" )"
	driveSourceMount="$( getDiskMountPoint "$1" )"
	driveSourceIdent="$( getDiskIdentifier "$1" )"
	driveSourceDisk="$( getDiskNumber "$1" )"
	driveSourcePart="$( getPartitionNumber "$1" )"
    
    if [[ "$driveSourceName" == "" ]]; then
        driveSourceName="Untitled"
    fi
}

function setEfiSource () {
	efiSourceName="$( getDiskName "$1" )"
	efiSourceMount="$( getDiskMountPoint "$1" )"
	efiSourceIdent="$( getDiskIdentifier "$1" )"
	efiSourceDisk="$( getDiskNumber "$1" )"
	efiSourcePart="$( getPartitionNumber "$1" )"
    
    if [[ "$efiSourceName" == "" ]]; then
        efiSourceName="Untitled"
    fi
}


function mainMenu () {
    resetVars
    clear
    echo \#\#\# EFI Backup-Restore \#\#\#
    echo
    echo 1. Backup EFI
    echo 2. Restore EFI
    echo 3. EFI to EFI copy
    echo 4. Open Backup Directory
    echo
    echo Q. Quit
    echo
    echo Please select a task:
	echo 
	read menuChoice

    if [[ "$menuChoice" == "1" ]]; then
		backupEFI
	elif [[ "$menuChoice" == "2" ]]; then
		restoreEFI
    elif [[ "$menuChoice" == "3" ]]; then
        efiToEFI
    elif [[ "$menuChoice" == "4" ]]; then
        openBackupDirectory
	elif [[ "$menuChoice" == "q" ]]; then
		customQuit
	fi
	mainMenu

}

function openBackupDirectory () {
    
    open "$backupLocation"

}

function efiToEFI () {
    sourceFolder=""
    sourceIdent=""
    
    destFolder=""
    destIdent=""
    
    resetVars
    clear
    echo \#\#\# EFI to EFI Copy \#\#\#
    echo
    echo Select drive containing EFI source:
    echo 
    
    driveList="$( cd /Volumes/; ls -1 | grep "^[^.]" )"
    unset driveArray
    IFS=$'\n' read -rd '' -a driveArray <<<"$driveList"
    
    #driveCount="${#driveArray[@]}"
    driveCount=0
    driveIndex=0
    
    for aDrive in "${driveArray[@]}"
    do
        (( driveCount++ ))
        echo "$driveCount". "$aDrive"
    done
    
    driveIndex=$(( driveCount-1 ))
    
    #ls /volumes/
    echo 
    echo 
    read drive
    
    if [[ "$drive" == "" ]]; then
        #drive="/"
        efiToEFI
    fi
    
    #Notice - must have the single brackets or this
    #won't accurately tell if $drive is a number.
    if [ "$drive" -eq "$drive" ] 2>/dev/null; then
        #We have a number - check if it's in the array
        if [  "$drive" -le "$driveCount" ] && [  "$drive" -gt "0" ]; then
            drive="${driveArray[ (( $drive-1 )) ]}"
        else
            echo Index "$drive" out of range, checking for drive name...
        fi
    fi
    
    if [[ "$( isDisk "$drive" )" != "0" ]]; then
        if [[ "$( volumeName "$drive" )" ]]; then
			# We have a valid disk
			drive="$( volumeName "$drive" )"
			#setDisk "$drive"
		else
			# No disk available there
			echo \""$drive"\" is not a valid disk name, identifier
			echo or mount point.
			echo 
			read -p "Press [enter] to return to the main menu..."
			mainMenu
		fi
    fi
    setDriveSource "$drive"
    
    hasEFIFolder="$( checkEFIFolder "$driveSourceMount" )"
    
    if [[ "$hasEFIFolder" == "1" ]]; then
        #echo "$driveName" has an EFI folder.
        efiFolder="$driveSourceMount/EFI"
        
        clear
        echo \#\#\# EFI to EFI Copy \#\#\#
        echo
        echo \""$driveSourceName"\" has an EFI folder located at:
        echo \""$efiFolder"\".
        echo
        echo Would you like to use that as your source? \(y/n\):
        echo
        echo If you choose not to, this script will attempt to check
        echo for an EFI partition on \""$driveSourceName"\".
        echo
        read mainMenu
        
        if [[ "$mainMenu" == "" ]]; then 
            mainMenu="y"
        fi
        
        if [[ "$mainMenu" == "y" ]]; then
            sourceFolder="$efiFolder"
        fi
        
    fi
    
    if [[ "$sourceFolder" == "" ]]; then
        hasEFIPartition="$( getEFIIdentifier "$driveSourceIdent" )"
    
        if [[ ! "$hasEFIPartition" == "" ]]; then
    
            clear
            echo \#\#\# EFI to EFI Copy \#\#\#
            echo
            echo \""$driveSourceName"\" has an EFI partition located at:
            echo \""$hasEFIPartition"\".
            echo
            echo Would you like to use that as your source? \(y/n\):
            echo
            read mainMenu
        
            if [[ "$mainMenu" == "" ]]; then 
                mainMenu="y"
            fi
        
            if [[ "$mainMenu" == "y" ]]; then
                diskutil mount "$hasEFIPartition" &>/dev/null
                setEfiSource "$hasEFIPartition"
                sourceIdent="$efiSourceIdent"
            
                if [[ -d "$efiSourceMount/EFI" ]]; then
                    sourceFolder="$efiSourceMount/EFI"
                fi
            fi
        fi
    fi
    
    if [[ "$sourceFolder" == "" ]]; then
        
        if [[ ! "$sourceIdent" == "" ]]; then
            # EFI part was mounted - unmount
            diskutil unmount "$sourceIdent"
        fi
        
        clear
        echo \#\#\# EFI to EFI Copy \#\#\#
        echo
        echo No EFI selected.  Returning to the main menu...
        echo
        sleep 3
        mainMenu
    
    fi
    
    
    #By this point - we have a source, let's get a target.
    
    
    clear
    echo \#\#\# EFI to EFI Copy \#\#\#
    echo
    echo Select destination drive:
    echo 
    
    driveList="$( cd /Volumes/; ls -1 | grep "^[^.]" )"
    unset driveArray
    IFS=$'\n' read -rd '' -a driveArray <<<"$driveList"
    
    #driveCount="${#driveArray[@]}"
    driveCount=0
    driveIndex=0
    
    for aDrive in "${driveArray[@]}"
    do
        (( driveCount++ ))
        echo "$driveCount". "$aDrive"
    done
    
    driveIndex=$(( driveCount-1 ))
    
    #ls /volumes/
    echo 
    echo 
    read drive
    
    if [[ "$drive" == "" ]]; then
        #drive="/"
        efiToEFI
    fi
    
    #Notice - must have the single brackets or this
    #won't accurately tell if $drive is a number.
    if [ "$drive" -eq "$drive" ] 2>/dev/null; then
        #We have a number - check if it's in the array
        if [  "$drive" -le "$driveCount" ] && [  "$drive" -gt "0" ]; then
            drive="${driveArray[ (( $drive-1 )) ]}"
        else
            echo Index "$drive" out of range, checking for drive name...
        fi
    fi
    
    if [[ "$( isDisk "$drive" )" != "0" ]]; then
        if [[ "$( volumeName "$drive" )" ]]; then
			# We have a valid disk
			drive="$( volumeName "$drive" )"
			#setDisk "$drive"
		else
			# No disk available there
			echo \""$drive"\" is not a valid disk name, identifier
			echo or mount point.
			echo 
			read -p "Press [enter] to return to the main menu..."
			mainMenu
		fi
    fi
    setDrive "$drive"
    
    ########################
    
    efiFolder="$driveMount"
        
    clear
    echo \#\#\# EFI to EFI Copy \#\#\#
    echo
    echo Restore EFI folder to the root of:
    echo \""$driveName"\"? \(y/n\): 
    echo
    read mainMenu
        
    if [[ "$mainMenu" == "" ]]; then 
        mainMenu="y"
    fi
        
    if [[ "$mainMenu" == "y" ]]; then
        #Copy EFI to EFI command here
        copyEFI "$sourceFolder" "$efiFolder" "$driveName"
    fi
    
    if [[ ! "$sourceFolder" == "" ]]; then
        hasEFIPartition="$( getEFIIdentifier "$driveIdent" )"
    
        if [[ ! "$hasEFIPartition" == "" ]]; then
    
            clear
            echo \#\#\# EFI to EFI Copy \#\#\#
            echo
            echo \""$driveName"\" has an EFI partition located at:
            echo \""$hasEFIPartition"\".
            echo
            echo Would you like to use that as your destination? \(y/n\):
            echo
            read mainMenu
        
            if [[ "$mainMenu" == "" ]]; then 
                mainMenu="y"
            fi
        
            if [[ "$mainMenu" == "y" ]]; then
                diskutil mount "$hasEFIPartition" &>/dev/null
                setEFI "$hasEFIPartition"
                destIdent="$efiIdent"
            
                efiFolder="$efiMount"
                copyEFI "$sourceFolder" "$efiFolder" "$driveName"
            fi
        fi
    fi
    
    ########################
    
    if [[ ! "$efiMount" == "" ]] || [[ ! "$efiSourceMount" == "" ]]; then
        clear
        echo \#\#\# EFI to EFI Copy \#\#\#
        echo
        echo Unmount all used EFI partitions? \(y/n\):
        echo
        read mainMenu
        
        if [[ "$mainMenu" == "" ]]; then 
            mainMenu="y"
        fi
        
        if [[ "$mainMenu" == "y" ]]; then
            if [[ ! "$efiMount" == "" ]]; then
                diskutil unmount "$efiIdent"
            fi
            if [[ ! "$efiSourceMount" == "" ]]; then
                diskutil unmount "$efiSourceMount"
            fi
        fi
    fi
    
    echo
    echo Done.
    echo
    sleep 3
    mainMenu

}

function copyEFI () {
    
    local __source="$1"
    local __dest="$2" 
    local __name="$3"
    
    clear
    echo \#\#\# Copying EFI \#\#\#
    echo
    echo Copying EFI from \""$__name"\" to:
    echo \""$__dest"\"...
    
    if [[ -d "$__dest/EFI" ]]; then
        rm -Rf "$__dest/EFI"
    fi
    
    cp -R "$__source" "$__dest"
    
    if [ "$?" -ne 0 ]; then
        echo Failed to copy EFI - Error Code: "$?"
    fi

}

function restoreEFI () {
    resetVars
    zipList="$( cd "$backupLocation"; ls -1 *.zip )"
    
    unset driveArray
    IFS=$'\n' read -rd '' -a zipArray <<<"$zipList"
    
    echo "$zipList"
    
    zipTestcount="${#zipArray[@]}"
    zipCount=0
    zipIndex=$(( zipTestcount-1 ))
    
    #zipIndex=$(( zipCount-1 ))

    clear
    echo \#\#\# Restore EFI \#\#\#
    echo
    
    if [ "$zipTestcount" -lt "1" ]; then
        echo No backups!
        echo
        read -p "Press [enter] to return to the main menu..."
        mainMenu
    fi
    
    echo Select a backup to restore:
    echo
    
    for aZip in "${zipArray[@]}"
    do
        (( zipCount++ ))
        echo "$zipCount". "$aZip"
    done
    
    echo
    echo
    read zip
    
    if [[ "$zip" == "" ]]; then
        restoreEFI
    fi
    
    #Notice - must have the single brackets or this
    #won't accurately tell if $drive is a number.
    if [ "$zip" -eq "$zip" ] 2>/dev/null; then
        #We have a number - check if it's in the array
        if [  "$zip" -le "$zipCount" ] && [  "$zip" -gt "0" ]; then
            zip="${zipArray[ (( $zip-1 )) ]}"
        else
            echo Index "$zip" out of range...
            echo
            sleep 3
            mainMenu
        fi
    fi
    
    #We've got our backup zip
    clear
    echo \#\#\# Restore EFI \#\#\#
    echo
    echo Select drive to restore to:
    echo 
    
    driveList="$( cd /Volumes/; ls -1 | grep "^[^.]" )"
    unset driveArray
    IFS=$'\n' read -rd '' -a driveArray <<<"$driveList"
    
    #driveCount="${#driveArray[@]}"
    driveCount=0
    driveIndex=0
    
    for aDrive in "${driveArray[@]}"
    do
        (( driveCount++ ))
        echo "$driveCount". "$aDrive"
    done
    
    driveIndex=$(( driveCount-1 ))
    
    #ls /volumes/
    echo 
    echo 
    read drive
    
    if [[ "$drive" == "" ]]; then
        #drive="/"
        restoreEFI
    fi
    
    #Notice - must have the single brackets or this
    #won't accurately tell if $drive is a number.
    if [ "$drive" -eq "$drive" ] 2>/dev/null; then
        #We have a number - check if it's in the array
        if [  "$drive" -le "$driveCount" ] && [  "$drive" -gt "0" ]; then
            drive="${driveArray[ (( $drive-1 )) ]}"
        else
            echo Index "$drive" out of range, checking for drive name...
        fi
    fi
    
    if [[ "$( isDisk "$drive" )" != "0" ]]; then
        if [[ "$( volumeName "$drive" )" ]]; then
			# We have a valid disk
			drive="$( volumeName "$drive" )"
			#setDisk "$drive"
		else
			# No disk available there
			echo \""$drive"\" is not a valid disk name, identifier
			echo or mount point.
			echo 
			read -p "Press [enter] to return to the main menu..."
			mainMenu
		fi
    fi
    
    setDrive "$drive"
        
    clear
    echo \#\#\# Restore EFI \#\#\#
    echo
    echo Restore EFI folder to the root of:
    echo \""$driveName"\"? \(y/n\): 
    echo
    read mainMenu
      
    if [[ "$mainMenu" == "" ]]; then 
        mainMenu="y"
    fi  
      
    if [[ "$mainMenu" == "y" ]]; then
        restore "$backupLocation" "$zip" "$driveMount/EFI"
    fi

    hasEFIPartition="$( getEFIIdentifier "$driveIdent" )"
    
    if [[ ! "$hasEFIPartition" == "" ]]; then
    
        clear
        echo \#\#\# Backup EFI Partition \#\#\#
        echo
        echo \""$driveName"\" has an EFI partition located at:
        echo \""$hasEFIPartition"\".
        echo
        echo Would you like to restore there? \(y/n\):  
        echo
        read mainMenu
        
        if [[ "$mainMenu" == "" ]]; then 
            mainMenu="y"
        fi
        
        if [[ "$mainMenu" == "y" ]]; then
            diskutil mount "$hasEFIPartition" &>/dev/null
            setEFI "$hasEFIPartition"
            
            #if [[ -d "$efiMount/EFI" ]]; then
            restore "$backupLocation" "$zip" "$efiMount/EFI"
            #fi
            
            echo Unmount EFI partition? \(y/n\):
            read mainMenu
        
            if [[ ! "$mainMenu" == "n" ]]; then
                diskutil unmount "$efiIdent"
            fi
            
        fi
        
    fi
    
    echo
    echo Done.
    echo
    sleep 3
    mainMenu
    
}

function restore () {

    local __source="$1"
    local __name="$2"
    local __dest="$3"
    
    local __tempFolder=`mktemp -d -t 'efi-backup-restore'`
    
    
    clear
    echo \#\#\# Restoring \#\#\#
    echo
    echo Restoring \""$__name"\" to:
    echo \""$__dest"\"...
    
    
    cd "$__source"
    unzip "$__name" -d "$__tempFolder"
    cd "$DIR"
    
    if [ "$?" -ne 0 ]; then
        echo Failed to unzip backup - Error Code: "$?"
    else
    
        if [[ -d "$__tempFolder/EFI" ]]; then
            #Valid EFI folder
            #Remove the destination folder
            if [[ -d "$__dest" ]]; then
                rm -Rf "$__dest"
            fi
            cp -R "$__tempFolder/EFI" "$__dest"
        else
            echo Backup not valid - needs to unzip to EFI folder...
        fi
    fi
    rm -R "$__tempFolder"
}

function backupEFI () {
    resetVars
    clear
    echo \#\#\# Backup EFI \#\#\#
    echo
    echo Select drive containing EFI to backup:
    echo 
    
    driveList="$( cd /Volumes/; ls -1 | grep "^[^.]" )"
    unset driveArray
    IFS=$'\n' read -rd '' -a driveArray <<<"$driveList"
    
    #driveCount="${#driveArray[@]}"
    driveCount=0
    driveIndex=0
    
    for aDrive in "${driveArray[@]}"
    do
        (( driveCount++ ))
        echo "$driveCount". "$aDrive"
    done
    
    driveIndex=$(( driveCount-1 ))
    
    #ls /volumes/
    echo 
    echo 
    read drive
    
    if [[ "$drive" == "" ]]; then
        #drive="/"
        backupEFI
    fi
    
    #Notice - must have the single brackets or this
    #won't accurately tell if $drive is a number.
    if [ "$drive" -eq "$drive" ] 2>/dev/null; then
        #We have a number - check if it's in the array
        if [  "$drive" -le "$driveCount" ] && [  "$drive" -gt "0" ]; then
            drive="${driveArray[ (( $drive-1 )) ]}"
        else
            echo Index "$drive" out of range, checking for drive name...
        fi
    fi
    
    if [[ "$( isDisk "$drive" )" != "0" ]]; then
        if [[ "$( volumeName "$drive" )" ]]; then
			# We have a valid disk
			drive="$( volumeName "$drive" )"
			#setDisk "$drive"
		else
			# No disk available there
			echo \""$drive"\" is not a valid disk name, identifier
			echo or mount point.
			echo 
			read -p "Press [enter] to return to the main menu..."
			mainMenu
		fi
    fi
    
    setDrive "$drive"
    
    hasEFIFolder="$( checkEFIFolder "$driveMount" )"
    
    if [[ "$hasEFIFolder" == "1" ]]; then
        #echo "$driveName" has an EFI folder.
        efiFolder="$driveMount/EFI"
        
        clear
        echo \#\#\# Backup EFI \#\#\#
        echo
        echo \""$driveName"\" has an EFI folder located at:
        echo \""$efiFolder"\".
        echo
        echo Would you like to back that up? \(y/n\):  
        echo
        read mainMenu
        
        if [[ "$mainMenu" == "" ]]; then 
            mainMenu="y"
        fi
        
        if [[ "$mainMenu" == "y" ]]; then
            backup "$efiFolder" "$driveName-EFIF-"
        fi
        
    fi
    
    hasEFIPartition="$( getEFIIdentifier "$driveIdent" )"
    
    if [[ ! "$hasEFIPartition" == "" ]]; then
    
        clear
        echo \#\#\# Backup EFI Partition \#\#\#
        echo
        echo \""$driveName"\" has an EFI partition located at:
        echo \""$hasEFIPartition"\".
        echo
        echo Would you like to back that up? \(y/n\):  
        echo
        read mainMenu
        
        if [[ "$mainMenu" == "" ]]; then 
            mainMenu="y"
        fi
        
        if [[ "$mainMenu" == "y" ]]; then
            diskutil mount "$hasEFIPartition" &>/dev/null
            setEFI "$hasEFIPartition"
            
            if [[ -d "$efiMount/EFI" ]]; then
                backup "$efiMount/EFI" "$driveName-EFI-"
            fi
            
            echo Unmount EFI partition? \(y/n\):
            read mainMenu
        
            if [[ ! "$mainMenu" == "n" ]]; then
                diskutil unmount "$efiIdent"
            fi
            
        fi
        
    fi
    
    echo
    echo Done.
    echo
    sleep 3
    mainMenu

}

function backup () {
    
    local __source="$1"
    local __name="$2"
    
    #local __sourceName="$( basename $__source )"
    local __timeStamp="$( getTimestamp )"
    
    #cd "$__source"
    #local __sourceParent="$( cd "../"; pwd )"
    #cd "$__sourceParent"
    
    local __sourceParent="${__source%/*}"
    local __sourceName="${__source##*/}"
    
    clear
    echo \#\#\# Backing Up \#\#\#
    echo
    echo Backing up \""$__source"\" to:
    echo \""$backupLocation"/"$__name"-"$__timeStamp".zip\"...

    echo
    echo Source Parent: "$__sourceParent"
    echo Source Name:   "$__sourceName"
    
    cd "$__sourceParent"
    
    zip -r "$backupLocation/$__name$__timeStamp.zip" "$__sourceName"
    
    if [ "$?" -ne 0 ]; then
        echo Failed to create backup - Error Code: "$?"
    fi
    
    cd "$DIR"
}

function checkEFIFolder () {
    local __vol=$1
	if [[ -d "$__vol/EFI" ]]; then
        echo 1
    else
        echo 0
    fi
}

function getTimestamp () {
    date +%Y%m%d_%H%M%S%Z
}

function makeBackupLocation () {
    #Expand tilde in backupLocation if relative
    #backupLocation="${backupLocation/#\~/$HOME}"
        
    if [[ ! -e "$backupLocation" ]]; then
        mkdir "$backupLocation"
    fi

}

function customQuit () {
	clear
	echo \#\#\# EFI Backup-Restore \#\#\#
	echo by CorpNewt
	echo 
	echo Thanks for testing it out, for bugs/comments/complaints
	echo send me a message on Reddit, or check out my GitHub:
	echo 
	echo www.reddit.com/u/corpnewt
	echo www.github.com/corpnewt
	echo 
	echo Have a nice day/night!
	echo 
	echo 
	shopt -u extglob
	shopt -u nocasematch
	exit $?
}

function displayWarning () {
	clear
	echo \#\#\# WARNING \#\#\#
	echo 
	echo This script is provided with NO WARRANTY whatsoever.
	echo I am not responsible for ANY problems or issues you
	echo may encounter, or any damages as a result of running
	echo this script.
	echo 
	echo To ACCEPT this warning and FULL RESPONSIBILITY for
	echo using this script, press [enter].
	echo 
	read -p "To REFUSE, close this script."
    makeBackupLocation
    checkRoot "MainMenu"
	mainMenu
}

###################################################
###               Disk Functions                ###
###################################################


function isDisk () {
	# This function checks our passed variable
	# to see if it is a disk
	# Accepts mount point, diskXsX and an empty variable
	# If empty, defaults to "/"
	local __disk=$1
	if [[ "$__disk" == "" ]]; then
		__disk="/"
	fi
	# Here we run diskutil info on our __disk and see what the
	# exit code is.  If it's "0", we're good.
	diskutil info "$__disk" &>/dev/null
	# Return the diskutil exit code
	echo $?
}

function volumeName () {
	# This is a last-resort function to check if maybe
	# Just the name of a volume was passed.
	local __disk=$1
	if [[ ! -d "$__disk" ]]; then
		if [ -d "/volumes/$__disk" ]; then
			#It was just volume name
			echo "/Volumes/$__disk"
		fi
	else
		echo "$__disk"
	fi
}

function getDiskMounted () {
	local __disk=$1
	# If variable is empty, set it to "/"
	if [[ "$__disk" == "" ]]; then
		__disk="/"
	fi
	# Output the "Volume Name" of __disk
	echo "$( diskutil info "$__disk" | grep 'Mounted' | cut -d : -f 2 | sed 's/^ *//g' | sed 's/ *$//g' )"
}

function getDiskName () {
	local __disk=$1
	# If variable is empty, set it to "/"
	if [[ "$__disk" == "" ]]; then
		__disk="/"
	fi
	# Output the "Volume Name" of __disk
	echo "$( diskutil info "$__disk" | grep 'Volume Name' | cut -d : -f 2 | sed 's/^ *//g' | sed 's/ *$//g' )"
}

function getDiskMountPoint () {
	local __disk=$1
	# If variable is empty, set it to "/"
	if [[ "$__disk" == "" ]]; then
		__disk="/"
	fi
	# Output the "Mount Point" of __disk
	echo "$( diskutil info "$__disk" | grep 'Mount Point' | cut -d : -f 2 | sed 's/^ *//g' | sed 's/ *$//g' )"
}

function getDiskIdentifier () {
	local __disk=$1
	# If variable is empty, set it to "/"
	if [[ "$__disk" == "" ]]; then
		__disk="/"
	fi
	# Output the "Mount Point" of __disk
	echo "$( diskutil info "$__disk" | grep 'Device Identifier' | cut -d : -f 2 | sed 's/^ *//g' | sed 's/ *$//g' )"
}

function getDiskNumbers () {
	local __disk=$1
	# If variable is empty, set it to "/"
	if [[ "$__disk" == "" ]]; then
		__disk="/"
	fi
	# Output the "Device Identifier" of __disk
	# If our disk is "disk0s1", it would output "0s1"
	echo "$( getDiskIdentifier "$__disk" | cut -d k -f 2 )"
}

function getDiskNumber () {
	local __disk=$1
	# If variable is empty, set it to "/"
	if [[ "$__disk" == "" ]]; then
		__disk="/"
	fi
	# Get __disk identifier numbers
	local __diskNumbers="$( getDiskNumbers "$__disk" )"
	# return the first number
	echo "$( echo "$__diskNumbers" | cut -d s -f 1 )"
}

function getPartitionNumber () {
	local __disk=$1
	# If variable is empty, set it to "/"
	if [[ "$__disk" == "" ]]; then
		__disk="/"
	fi
	# Get __disk identifier numbers
	local __diskNumbers="$( getDiskNumbers "$__disk" )"
	# return the second number
	echo "$( echo "$__diskNumbers" | cut -d s -f 2 )"	
}

function getPartitionType () {
	local __disk=$1
	# If variable is empty, set it to "/"
	if [[ "$__disk" == "" ]]; then
		__disk="/"
	fi
	# Output the "Volume Name" of __disk
	echo "$( diskutil info "$__disk" | grep 'Partition Type' | cut -d : -f 2 | sed 's/^ *//g' | sed 's/ *$//g' )"
}

function getEFIIdentifier () {
	local __disk=$1
	local __diskName="$( getDiskName "$__disk" )"
	local __diskNum="$( getDiskNumber "$__disk" )"
	# If variable is empty, set it to "/"
	if [[ "$__disk" == "" ]]; then
		__disk="/"
	fi
	# Output the "Device Identifier" for the EFI partition of __disk
	endOfDisk="0"
	i=1
	while [[ "$endOfDisk" == "0" ]]; do
		# Iterate through all partitions of the disk, and return those that
		# are EFI
		local __currentDisk=disk"$__diskNum"s"$i"
		# Check if it's a valid disk, and if not, exit the loop
		if [[ "$( isDisk "$__currentDisk" )" != "0" ]]; then
			endOfDisk="true"
			continue
		fi

		local __currentDiskType="$( getPartitionType "$__currentDisk" )"

		if [ "$__currentDiskType" == "EFI" ]; then
			echo "$( getDiskIdentifier "$__currentDisk" )"
		fi
		i="$( expr $i + 1 )"
	done
}

function mountEFI () {
	# This function iterates through the partitions of a disk
	# and mounts the ones with the "EFI" partition type
	local __disk=$1
	local __diskName="$( getDiskName "$__disk" )"
	local __diskNum="$( getDiskNumber "$__disk" )"
	clear
	echo \#\#\# Mounting Partitions on "$__diskName" \#\#\#
	echo 

	endOfDisk="0"
	i=1

	echo Searching for EFI partitions on "$__diskName":
	echo 

	while [[ "$endOfDisk" == "0" ]]; do
		# Iterate through all partitins of the disk, and mount those that
		# are EFI
		local __currentDisk=disk"$__diskNum"s"$i"
		# Check if it's a valid disk, and if not, exit the loop
		if [[ "$( isDisk "$__currentDisk" )" != "0" ]]; then
			echo End of partitions.
			echo 
			endOfDisk="true"
			continue
		fi
		echo Checking "$__currentDisk"...
		local __currentDiskType="$( getPartitionType "$__currentDisk" )"

		echo Current Disk Type: "$__currentDiskType"

		if [[ "$__currentDiskType" == "EFI" ]]; then
			echo Partition Type is EFI.
			echo Mounting...
			diskutil mount "$__currentDisk"
		fi
		i="$( expr $i + 1 )"
		echo 
	done
	echo Done.
	echo 
	read -p "Press [enter] to return to the main menu..."
	mainMenu
}

function getUUID () {
	local __disk=$1
	# If variable is empty, set it to "/"
	if [[ "$__disk" == "" ]]; then
		__disk="/"
	fi
	# Output the "Disk / Partition UUID" of __disk
	echo "$( diskutil info "$__disk" | grep 'Disk / Partition UUID' | cut -d : -f 2 | sed 's/^ *//g' | sed 's/ *$//g' )"
}

function diskInfo () {
	# Echoes some info on the passed disk
	if [[ "$( isDisk "$1" )" == "0" ]]; then
		echo Is Disk: YES
		echo Disk Name: "$( getDiskName "$1" )"
		echo Mount Point: "$( getDiskMountPoint "$1" )"
		echo Disk Identifier: "$( getDiskIdentifier "$1" )"
		echo Disk Numbers: "$( getDiskNumbers "$1" )"
		echo Disk Number: "$( getDiskNumber "$1" )"
		echo Partition Number: "$( getPartitionNumber "$1" )"
	else
		echo Is Disk: NO
	fi

}

###################################################
###             End Disk Functions              ###
###################################################

backupLocation="$( expandPath "$backupLocation" )"

if [[ "$1" == "MainMenu" ]]; then
    mainMenu
fi

displayWarning
