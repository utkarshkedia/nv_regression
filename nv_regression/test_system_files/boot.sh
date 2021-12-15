#!/bin/bash
# $Id: //hdclone/storage_customizations/Linux_switch_boot_entry.sh#10 $
#set -x
set -e

##############################################################################
# define a dict to store all the OS entry list
##############################################################################
declare -A dict
dict=()

##############################################################################
# check the script is running under Linux
##############################################################################
if [ -d '/etc/init.d' ];then
    clear 
else
    echo "The OS is not Linux!!!"
    exit 1
fi
echo "Start OS Boot Entry Switch ..."

##############################################################################
# check current mode (legacy or UEFI)
##############################################################################
is_efi=1
if [ -d "/sys/firmware/efi" ];then
    echo "The system is under [UEFI] mode"
    is_efi=1
else
    echo "The system is under [Legacy] mode"
    is_efi=0 
fi

##############################################################################
# mount target boot partition(15 or 1)
##############################################################################
#is_nvme=$(sed -n /nvme/= "/proc/partitions" | head -n 1)
BOOT_PART="/tmp/boot_partition"
test -d $BOOT_PART || mkdir -m 700 $BOOT_PART

if [ $is_efi -eq 1 ];then
    efi_part_count=$(blkid | grep -w ESP | wc -l)
    efi_part=$(blkid | grep -w ESP | sed 's,:.*,,')
    # has multi bootable disk, let user choose which one is in first piror
    if [ $efi_part_count -gt 1 ];then
        echo "You have multi bootable disk, blow are all efi partition found: "
        echo "$efi_part"
        read -p "Please type the efi partition path which you set as first boot option (ex. /dev/sda1): " efi_input
        efi_part=$efi_input
    fi
    efi_dir=$(mount | grep -w $efi_part | head -n 1 | sed 's,.* on ,,; s, type.*,,;')
    if [ -z $efi_dir ];then
        mount $efi_part $BOOT_PART
    else
        BOOT_PART=$efi_dir
    fi
else
    storage_part_count=$(blkid | grep -w STORAGE | wc -l)
    storage_part=$(blkid | grep -w STORAGE | sed 's,:.*,,')
    # has multi storage disk, let user choose which one is in first piror used
    if [ $storage_part_count -gt 1 ];then
        echo "You have multi disk, blow are all storage partition found: "
        echo "$storage_part"
        read -p "Please type the storage partition path which you choose to use (ex. /dev/sda15): " storage_input
        storage_part=$storage_input
    fi
    # storage partition is ntfs type which can only mount once, need to search already mounted dir
    storage_dir=$(mount | grep -w $storage_part | head -n 1 | sed 's,.* on ,,; s, type.*,,;')
    if [ -z $storage_dir ];then
        mount $storage_part $BOOT_PART
    else
        BOOT_PART=$storage_dir
    fi
fi

##############################################################################
# scan current entry list(menu.lst or grub.cfg)
##############################################################################
echo "Current disk's boot entry list:"
if [ $is_efi -eq 1 ];then
    #compatible with the older grub version
    test -d $BOOT_PART/boot/grub||cp -r $BOOT_PART/boot/grub2 $BOOT_PART/boot/grub 
    boot_list=$(grep menuentry $BOOT_PART/boot/grub/grub.cfg |cut -d "'" -f 2| xargs -I {} echo "{}+")
else
    boot_list=$(grep title $BOOT_PART/menu.lst | sed 's,.*title ,,;'| xargs -I {} echo "{}+")
fi
IFS='+'
i=0
for entry in $boot_list
    do
       entry=$(echo $entry | tr -d "\n")
       echo "    [$i] $entry"
       if [ $is_efi -eq 1 ];then
          dict+=([$i]="$entry")
       else
           dict+=([$i]="$i")
       fi
       i=$(($i+1)) 
    done
unset IFS

##############################################################################
# customer pick up the destination partition num
##############################################################################
# user already pass index number as command line args
next_boot=${dict[0]}
# confirm the selection
echo "'$next_boot' is chosen as the next boot option"
# update boot entry file(default or grubenv)
if [ $is_efi -eq 1 ];then
    if [ -e $BOOT_PART/boot/grub/grubenv ];then
        sed -i "s/=.*$/=$next_boot/" $BOOT_PART/boot/grub/grubenv
        test -d $BOOT_PART/boot/grub2 && cp $BOOT_PART/boot/grub/grubenv $BOOT_PART/boot/grub2/grubenv
    elif [ -e $BOOT_PART/boot/grub/GRUBENV ]; then
        sed -i "s/=.*$/=$next_boot/" $BOOT_PART/boot/grub/GRUBENV
        test -d $BOOT_PART/boot/grub2 && cp $BOOT_PART/boot/grub/GRUBENV $BOOT_PART/boot/grub2/GRUBENV
    fi
else
    sed -i "s/^[0-9]\{1,2\}/$next_boot/" $BOOT_PART/default
fi
echo "finish update the next boot entry"

##############################################################################
# unmount the boot partion
##############################################################################
TMP_POINT="/tmp/boot_partition"
if [ "$BOOT_PART" = "$TMP_POINT" ];then
    umount $BOOT_PART
fi

##############################################################################
# query for reboot now
##############################################################################
reboot