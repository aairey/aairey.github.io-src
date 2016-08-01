Title: letsencrypt and OwnCloud
Date: 2016-07-07 22:20
Modified: 2016-08-01 23:52
Category: homelab
Tags: owncloud, security, letsencrypt, freenas
Slug: owncloud-letsencrypt
Authors: Andy Airey
Summary: A small post on how to set up ownCloud to use a letsencrypt certificate within a FreeNAS jail

Hello there.

Recently I was in the need of an SSL certificate for my personal [ownCloud](https://owncloud.org/) server.
On my setup, ownCloud runs as a [plugin for FreeNAS 9.10](https://doc.freenas.org/9.10/freenas_plugins.html#installing-plugins).

At the time of writing [letsencrypt was out of beta](https://letsencrypt.org/2016/04/12/leaving-beta-new-sponsors.html) for some months and I decided to give it a go.
I've had good experience with [StartSSL](https://www.startssl.com/) and their free certificate for one hostname, but I've been following the letsencrypt developments and I really stand behind what they are doing.

I have to say I was somewhat surprised by the results. It was really easy to set up and the certificate was trusted, no problem. Even [SSL Labs](https://www.ssllabs.com/) didn't complain :).

Here's how I did it.

1. On your FreeNAS host, find out which jail is runing owncloud and enter it:
   
        :::shell 
        jls
        jexec 3 tcsh


2. Install the needed packages within this jail:

        :::shell 
        pkg install py27-letsencrypt


3. Stop apache and start the setup wizard:

        :::shell 
        /usr/pbi/owncloud-amd64/etc/rc.d/apache24 stop
        letsencrypt certonly

4. Softlink the new certs from the apache directory (replace your.domain.org with the domain name from step 3)

        :::shell 
        /usr/pbi/owncloud-amd64/etc/rc.d/apache24 start
        cd /usr/pbi/owncloud-amd64/etc/apache24/
        ln -s /usr/local/etc/letsencrypt/live/your.domain.org/cert.pem letsencrypt.crt
        ln -s /usr/local/etc/letsencrypt/live/your.domain.org/privkey.pem letsencrypt.key
        ln -s /usr/local/etc/letsencrypt/live/your.domain.org/chain.pem letsencrypt_chain.crt

5. edit extra/httpd-ssl.conf and change it so that

        #!apache
        SSLProtocol all -SSLv2 -SSLv3`
        SSLHonorCipherOrder on
        SSLCipherSuite "EECDH+ECDSA+AESGCM EECDH+aRSA+AESGCM EECDH+ECDSA+SHA384 EECDH+ECDSA+SHA256 EECDH+aRSA+SHA384 EECDH+aRSA+SHA256 EECDH+aRSA+RC4 EECDH EDH+aRSA RC4 !aNULL !eNULL !LOW !3DES !MD5 !EXP !PSK !SRP !DSS"
        
        SSLCertificateFile "/usr/pbi/owncloud-amd64/etc/apache24/letsencrypt.crt"
        SSLCertificateKeyFile "/usr/pbi/owncloud-amd64/etc/apache24/letsencrypt.key"
        SSLCACertificateFile "/usr/pbi/owncloud-amd64/etc/apache24/letsencrypt_chain.crt"

6. Restart Apache HTTPD:

        :::shell 
        ../rc.d/apache24 restart

7. Check the logs for errors:

        :::shell 
        tail /var/log/httpd-error.log
