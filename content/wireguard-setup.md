Title: Wireguard Setup on Fedora
Date: 2018-09-10 21:49
Modified: 2018-09-10 23:06
Category: homelab
Tags: fedora, security, vpn
Slug: wireguard-setup
Authors: Andy Airey
Summary: How To setup and use Wireguard on Fedora Workstation as client and Fedora Server as PtP and VPN server. Also covers the setup on Android

Ever since Linus Torvalds [praised](http://lkml.iu.edu/hypermail/linux/kernel/1808.0/02472.html) Wireguard, I've been wanting to try it out.  
Last week I finally got around to play with it, and boy was it easy and elegant to set up.

It was really easy to set up, it took me longer to write this blog post than to set up wireguard on 3 peers.


I used a Fedora Server as a first endpoint and my Fedora Workstation as a second endpoint.  
Later on I also easily added my Android phone as a third endpoint, and set up the Fedora Server as a VPN server (routing traffic to the internal and external networks).

Let me walk you through the setup steps.

# Installation

We need to install wireguard first as it is not yet part of the mainline kernel.

On the Fedora Server and Workstation:
```bash
sudo dnf copr enable jdoss/wireguard
sudo dnf install wireguard-dkms wireguard-tools
```

# Setting up the endpoints

As you will see below the setup is very similar for both endpoints.  
Note the difference in IP addresses.

We will choose a static tunnel IP per host in the 10.0.0.0/24 range, but it could be any range of your choosing.

Create a keypair on each host:
```bash
wg genkey > private
wg pubkey < private
```
Take note of the public key to configure your other client later on.

## First peer
Our first endpoint has a private IP address of 192.168.2.1/24 on enp2s0, adapt it to match your machine's private IP address.

Interface Settings:
```bash
ip link add dev wg0 type wireguard
ip address add dev wg0 10.0.0.1/24
wg set wg0 listen-port 51820 private-key ./private
```
Peer Settings:
```bash
wg set wg0 peer <peer2-public-key> allowed-ips 10.0.0.2/32 endpoint <peer2-pulic-ip>:51820
ip link set wg0 up
```
The `allowed-ips` setting denotes what network lies at the other end of the tunnel.  
Routes will automatically be set up towards these networks when the interface becomes active.  
As a starting point we can use the other peer's tunnel IP address.

## Second peer
Interface Settings:
```bash
ip link add dev wg0 type wireguard
ip address add dev wg0 10.0.0.2/24
wg set wg0 listen-port 51820 private-key ./private
```
Peer Settings:
```bash
wg set wg0 peer <peer2-public-key> allowed-ips 10.0.0.1/24 endpoint <peer1-pulic-ip>:51820
ip link set wg0 up
```

## Check connectivity

At this point you should be able to ping the other endpoint his 10.0.0.x address after the interface is up.

The `wg` command should show you some useful output as well.

Remember when doing tcpdump and forwarding ports, the connection is over UDP, not TCP!  
Hint if you run with firewalld enabled: `firewall-cmd --add-port 51820/udp`, see Additional Settings below to do this automatically.

## NAT and Dynamic endpoint IP address

If you are, like me, trying to set up your laptop to connect to a remote server, your public IP will most definitely change a lot.

The solution to this is to use Dynamic DNS and use this DNS name in your endpoint configuration.  
Even on Android [there is an app for that](https://play.google.com/store/apps/details?id=com.icecoldapps.dynamicdnsupdate).

Also, there is a setting called `persistent-keepalive` that will assist firewalls to keep the tunnel alive.


## Persistent configuration

The CLI tools are nice and all, but I want the VPN link to come up with my Fedora Server and easily bring up the connection with one commmand on my Workstation.

No problem, `wg-quick` has got you covered.

First export the current config to a file, link it to the device and enable the systemd service (if you want to bring the device up at boot time).
```bash
wg showconf > /etc/wiregaurd/wg0.conf
chmod 700 /etc/wireguard/wg0.conf
wg setconf wg0 /etc/wireguard/wg0.conf
```
You can now easily issue `wg-quick up wg0` and `wg-quick down wg0`.  
To have it start at boot-time issue `systemctl enable wg-quick@wg0`. (make sure you stop it first manually before starting the service)

# Android peer

Once you have Dynamic DNS set up on your Android using [this app](https://play.google.com/store/apps/details?id=com.icecoldapps.dynamicdnsupdate),

## Android app setup

Install the [Wireguard Android app](https://play.google.com/store/apps/details?id=com.wireguard.android).

The configuration is pretty straight-forward, but maybe just choose a different port than the one for your laptop, in case you are on the same network.

On the `allowed-ips` section, specify '0.0.0.0/0. ::0/0' if you want to forward all internet traffic over this VPN (recommended for public WiFi).

## Add peer configuration on the server

I added this Peer configuration to the existing `wg0.conf` file on the Server:
```
[Peer]
#mobile
PublicKey           = <android-public-key>
AllowedIPs          = 10.0.0.3/32
Endpoint            = server.dyndns.com:51821
PersistentKeepalive = 25
```

When forwarding traffic to the outside, make sure IP forwarding is on.
```bash
sysctl net.ipv4.ip_forward=1
```


# Additional settings

To have the port and masquerading be set up automatically whenever I bring up the wireguard interface, I added soem `PostUp` and `PostDown` commands.

My Interface Settings on the server are as follows;
```
[Interface]
Address    = 10.0.0.1/24
PostUp     = firewall-cmd --add-port 51820/udp && firewall-cmd --add-rich-rule='rule family=ipv4 source address=10.0.0.0/24 masquerade'
PostDown   = firewall-cmd --remove-port 51820/udp && firewall-cmd --remove-rich-rule='rule family=ipv4 source address=10.0.0.0/24 masquerade'
ListenPort = 51820
PrivateKey = <private-key>

```

Now you can enjoy a very fast and easy to maintain VPN configuration on the road, whether it's on your mobile or on your laptop.

# More Resources

* Wireguard docs for [installation](https://www.wireguard.com/install/)
* Wireguard docs for [QuickStart setup](https://www.wireguard.com/install/)
* [Arch Wiki](https://wiki.archlinux.org/index.php/WireGuard) was really helpful, as always.
* [Blog post](https://www.rootusers.com/how-to-use-firewalld-rich-rules-and-zones-for-filtering-and-nat/) on firewalld, scroll down to masquerading 
