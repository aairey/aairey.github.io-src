Title: VirtualBox on a SecureBoot enabled system
Date: 2016-10-06 13:27
Modified: 2016-10-17 13:30
Category: security
Tags: security, fedora, virtualisation, kernel
Slug: secureboot-virtualbox
Authors: Andy Airey
Summary: Installing VirtualBox on a SecureBoot enabled system can be tedious. Here I explain how to sign the kernel modules so that you can load them into the kernel.

Hello again,


Apparently the kernel modules that Oracle provide for VirtualBox [are not signed](https://gorka.eguileor.com/vbox-vmware-in-secureboot-linux/).

When starting `virtualbox` you will get an error that the modules are not loaded.

    WARNING: The vboxdrv kernel module is not loaded. Either there is no module
             available for the current kernel (4.7.5-200.fc24.x86_64) or it failed to
             load. Please recompile the kernel module and install it by

               sudo /sbin/vboxconfig

             You will not be able to start VMs until this problem is fixed.

When you run `sudo /sbin/vboxconfig`, it will take very long and eventually fail.

	vboxdrv.sh: Building VirtualBox kernel modules.
	vboxdrv.sh: Starting VirtualBox services.
	vboxdrv.sh: Building VirtualBox kernel modules.
	vboxdrv.sh: failed: modprobe vboxdrv failed. Please use 'dmesg' to find out why.

	There were problems setting up VirtualBox.  To re-start the set-up process, run
	  /sbin/vboxconfig
	as root.


So we can sign them ourselves and load them into the kernel.

The only downside is you have to do this after every kernel update.

So I wrote a little script to simplify that for me.
This was done on Fedora 23 and 24 Workstation.

    #!bash
    KERNEL_VERSION=$(uname -r)
    openssl req -new -x509 -newkey rsa:2048 -keyout MOK_$KERNEL_VERSION.priv -outform DER -out MOK_$KERNEL_VERSION.der -nodes -days 36500 -subj "/CN=$KERNEL_VERSION/"
    sudo /usr/src/kernels/$KERNEL_VERSION/scripts/sign-file sha256 ./MOK_$KERNEL_VERSION.priv ./MOK_$KERNEL_VERSION.der $(sudo modinfo -n vboxdrv)
    sudo /usr/src/kernels/$KERNEL_VERSION/scripts/sign-file sha256 ./MOK_$KERNEL_VERSION.priv ./MOK_$KERNEL_VERSION.der $(sudo modinfo -n vboxnetflt)
    sudo /usr/src/kernels/$KERNEL_VERSION/scripts/sign-file sha256 ./MOK_$KERNEL_VERSION.priv ./MOK_$KERNEL_VERSION.der $(sudo modinfo -n vboxnetadp)
    sudo /usr/src/kernels/$KERNEL_VERSION/scripts/sign-file sha256 ./MOK_$KERNEL_VERSION.priv ./MOK_$KERNEL_VERSION.der $(sudo modinfo -n vboxpci)
    sudo mokutil --import MOK_$KERNEL_VERSION.der


So basicly you will have to do:

    sudo dnf update -y && sudo systemctl reboot     # update kernel
    ~/bin/mokutil.sh                                # run script against new kernel
    sudo reboot                                     # reboot and follow the signing process at boot time


After the reboot you can then check the logs if the module was loaded with the following commands:

    sudo keyctl list %:.system_keyring
    dmesg | grep 'EFI: Loaded cert'

