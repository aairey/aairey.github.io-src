Title: certbot renew on FreeBSD
Date: 2016-08-17 22:27
Modified: 2016-08-17 23:30
Category: homelab
Tags: owncloud, security, letsencrypt, freenas, cerbot, jails
Slug: certbot-renew-freebsd
Authors: Andy Airey
Summary: A small post on how to renew a LetsEncrypt certificate in a FreeBSD jail

Hi there,


In [my last post](../owncloud-letsencrypt) I talked about getting a free certificate fron [LetsEncrypt](https://letsencrypt.org/) using py27-letsencrypt.

Turns out I was not using the right package for the job.
The package [certbot](https://certbot.eff.org/docs/using.html) is available now and this (also Python) is used in favor of `py27-letsencrypt`.

I found out when I wanted to renew my certificate:

    # letsencrypt renew -d your.domain.org
    Currently, the renew verb is only capable of renewing all installed certificates that are due to be renewed; individual domains cannot be specified with this action. If you would like to renew specific certificates, use the certonly command. The renew verb may provide other options for selecting certificates to renew in the future.
    root@owncloud_1:~ # letsencrypt renew

    -------------------------------------------------------------------------------
    Processing /usr/local/etc/letsencrypt/renewal/your.domain.org.conf
    -------------------------------------------------------------------------------

    -------------------------------------------------------------------------------
    The program httpd (process ID 12020) is already listening on TCP port 80. This
    will prevent us from binding to that port. Please stop the httpd program
    temporarily and then try again. For automated renewal, you may want to use a
    script that stops and starts your webserver. You can find an example at
    https://letsencrypt.org/howitworks/#writing-your-own-renewal-script.
    Alternatively you can use the webroot plugin to renew without needing to stop
    and start your webserver.
    -------------------------------------------------------------------------------
    2016-08-17 20:54:09,442:WARNING:letsencrypt.renewal:Attempting to renew cert from /usr/local/etc/letsencrypt/renewal/your.domain.org.conf produced an unexpected error: At least one of the (possibly) required ports is already taken.. Skipping.

    All renewal attempts failed. The following certs could not be renewed:
      /usr/local/etc/letsencrypt/live/your.domain.org/fullchain.pem (failure)
    1 renew failure(s), 0 parse failure(s)


Due to the first error, I wondered if my version was out of date.

    pkg update
    pkg upgrade

Yes there was an update, but after the upgrade it was even worse:

    # letsencrypt renew --certonly
    Traceback (most recent call last):
      File "/usr/local/bin/letsencrypt", line 5, in <module>
        from pkg_resources import load_entry_point
      File "/usr/local/lib/python2.7/site-packages/pkg_resources/__init__.py", line 2927, in <module>
        @_call_aside
      File "/usr/local/lib/python2.7/site-packages/pkg_resources/__init__.py", line 2913, in _call_aside
        f(*args, **kwargs)
      File "/usr/local/lib/python2.7/site-packages/pkg_resources/__init__.py", line 2940, in _initialize_master_working_set
        working_set = WorkingSet._build_master()
      File "/usr/local/lib/python2.7/site-packages/pkg_resources/__init__.py", line 637, in _build_master
        return cls._build_from_requirements(__requires__)
      File "/usr/local/lib/python2.7/site-packages/pkg_resources/__init__.py", line 650, in _build_from_requirements
        dists = ws.resolve(reqs, Environment())
      File "/usr/local/lib/python2.7/site-packages/pkg_resources/__init__.py", line 829, in resolve
        raise DistributionNotFound(req, requirers)
    pkg_resources.DistributionNotFound: The 'acme==0.5.0' distribution was not found and is required by letsencrypt
    root@owncloud_1:~ # letsencrypt
    Traceback (most recent call last):
      File "/usr/local/bin/letsencrypt", line 5, in <module>
        from pkg_resources import load_entry_point
      File "/usr/local/lib/python2.7/site-packages/pkg_resources/__init__.py", line 2927, in <module>
        @_call_aside
      File "/usr/local/lib/python2.7/site-packages/pkg_resources/__init__.py", line 2913, in _call_aside
        f(*args, **kwargs)
      File "/usr/local/lib/python2.7/site-packages/pkg_resources/__init__.py", line 2940, in _initialize_master_working_set
        working_set = WorkingSet._build_master()
      File "/usr/local/lib/python2.7/site-packages/pkg_resources/__init__.py", line 637, in _build_master
        return cls._build_from_requirements(__requires__)
      File "/usr/local/lib/python2.7/site-packages/pkg_resources/__init__.py", line 650, in _build_from_requirements
        dists = ws.resolve(reqs, Environment())
      File "/usr/local/lib/python2.7/site-packages/pkg_resources/__init__.py", line 829, in resolve
        raise DistributionNotFound(req, requirers)
    pkg_resources.DistributionNotFound: The 'acme==0.5.0' distribution was not found and is required by letsencrypt


After some googling, it seemed I needed letsencrypt-auto or certbot-auto, both not available through the package manager in FreeBSD. So not really my preference.

I found [this page](https://certbot.eff.org/all-instructions/#freebsd-apache) so I installed plain certbot

    pkg search certbot
    pkg install certbot

Turns out this was requiring the same `acme` dependency and version:

    # certbot
    An unexpected error occurred:
    VersionConflict: (acme 0.8.1 (/usr/local/lib/python2.7/site-packages), Requirement.parse('acme==0.5.0'))
    Please see the logfile 'certbot.log' for more details.


I then found [this solution](https://github.com/certbot/certbot/issues/3221) and uninstalled it with `pip`:

    pip uninstall letsencrypt

I could then do a renew [as follows](https://certbot.eff.org/docs/using.html):

    # certbot renew --dry-run

    -------------------------------------------------------------------------------
    Processing /usr/local/etc/letsencrypt/renewal/your.domain.org.conf
    -------------------------------------------------------------------------------

    -------------------------------------------------------------------------------
    The program httpd (process ID 12020) is already listening on TCP port 80. This
    will prevent us from binding to that port. Please stop the httpd program
    temporarily and then try again. For automated renewal, you may want to use a
    script that stops and starts your webserver. You can find an example at
    https://letsencrypt.org/howitworks/#writing-your-own-renewal-script.
    Alternatively you can use the webroot plugin to renew without needing to stop
    and start your webserver.
    -------------------------------------------------------------------------------
    2016-08-17 21:52:47,093:WARNING:certbot.renewal:Attempting to renew cert from /usr/local/etc/letsencrypt/renewal/your.domain.org.conf produced an unexpected error: At least one of the (possibly) required ports is already taken.. Skipping.
    ** DRY RUN: simulating 'certbot renew' close to cert expiry
    **          (The test certificates below have not been saved.)

    All renewal attempts failed. The following certs could not be renewed:
      /usr/local/etc/letsencrypt/live/your.domain.org/fullchain.pem (failure)
    ** DRY RUN: simulating 'certbot renew' close to cert expiry
    **          (The test certificates above have not been saved.)
    1 renew failure(s), 0 parse failure(s)

So it tries to run it's own webserver and auto-approve the renewal this way by connecting to it.
This is of course not possible when Apache is running and using the same port on the system.
It is possible to specify a [different port](https://community.letsencrypt.org/t/le-client-needs-to-bind-to-port-80-which-im-already-using/2739/10), but then you need to set up a NAT/Proxy rule to this port so that it is accessible through standard HTTP on port 80.

This is not a production server so I wrapped it with these hooks (as recommended):

    certbot renew --standalone --pre-hook "/usr/pbi/owncloud-amd64/etc/rc.d/apache24 stop" --post-hook "/usr/pbi/owncloud-amd64/etc/rc.d/apache24 start" --dry-run

The dry-run was succesful! (in retrospect - could've done this with the original `py27-letsencrypt` too ...)
Finally, I set up crontab to take care of this for me in the future:

    0 3 1 */3 * root certbot renew --standalone --pre-hook "/usr/pbi/owncloud-amd64/etc/rc.d/apache24 stop" --post-hook "/usr/pbi/owncloud-amd64/etc/rc.d/apache24 start"

This will check and renew the cert every 3 (1st of Jan, Apr, Jul, Oct).

Future-you will thank you!
