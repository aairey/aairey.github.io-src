Title: ownCloud 9.1 upgrade on FreeNAS
Date: 2016-11-18 14:21
Modified: 2016-11-21 0:13
Category: homelab
Tags: owncloud, freenas, upgrade
Slug: owncloud-91-upgrade-freenas
Authors: Andy Airey
Summary: Did the upgrade to 9.1 give you a broken setup too? Here is a small guide to resolve it.

Hello there.

I updated my ownCloud FreeNAS plugin to the latest version.

After that I did not get my login page back, but I had to continue doing the update manually through the CLI.

Below are the steps I took.

This might help other people using ownCloud on FreeNAS/FreeBSD.


1. First log in to your FreeNAS box and enter the correct jail

        :::shell
        jls
        jexec 4 tcsh 	# in my case jail number 4 was ownCloud

2. Then you should go to the owncloud install directory

        :::shell
        cd /usr/pbi/owncloud-amd64/www/owncloud

3. Now the following command should be run to conclude the upgrade process (see the official [docs](https://doc.owncloud.org/server/9.1/admin_manual/configuration_server/occ_command.html#command-line-upgrade)).
   On FreeBSD it is a little different:

        :::shell
        su -m www -c 'php occ upgrade'

4. That will give you a bunch of errors, the problem is that php and it's dependencies are not installed.
   Here are all the dependencies I had to install:

        :::shell
        pkg install php56 php56-ctype php56-gd php56-xmlreader php56-xml php56-zip php56-xmlwriter php56-curl \
                    php56-zlib php56-hash php56-mbstring php56-posix php56-pdo php56-sqlite3 php56-pdo_sqlite \
                    php56-json php56-simplexml

5. After that I could run the upgrade command without and I got my login prompt back!

Disclaimer: I am not a FreeBSD expert, so there might be a cleaner way to do this.

I found it really weird that I had to install php56 after a plain update of the ownCloud pbi ...

**Update:** There is now an [official NextCloud plugin for FreeNAS](https://forums.freenas.org/index.php?threads/new-plugins-for-freenas-9-november-2016-nextcloud-madsonic-resilio-nzbhydra.47259/), we should all be using that now. Here's [why](http://www.techrepublic.com/article/owncloud-founder-has-forked-their-product-into-nextcloud/).
