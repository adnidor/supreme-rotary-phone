Database Structure
==================

SRP uses one database with the following tables. For most tables here there is a corresponding class in :doc:`helpers`.

devices
-------

Corresponding class: :class:`Device`

In this table all the information for devices is stored

============    =============
Column          Content
============    =============
identifier      The unique identifier for the device, normally a MAC address in the format xx:xx:xx:xx:xx
ip              The IP address for the device
context         The id of the context the device belongs to
hostname        The hostname of the device
altname         Alternative hostname, optional
description     Human-readable name
type            Addressing method, one of "dhcp", "static" and "vpn"
devicetype      Id of the devices' devicetype
connection      How the device is connected to the network, one of "wifi", "ethernet" and "openvpn"
ports           Huge mess, for wifi the comma-seperated id of the wifis the device is allowed to join, for openvpn the name of the config file the device is allowed to connect to
internet        If the device should access the internet, one of 1 and 0
alwayson        If the device is always on (e.g. for monitoring), one of 1 and 0
formfactor      The formfactor of the device. See :doc:`formfactors` for details
osversion       The version of the OS (not used much) (intended values like: "debian", "arch")
============    =============

contexts
--------

Corresponding class: :class:`Context`

In this table all the information about contexts is stored.

============    =============
Column          Content
============    =============
i               ID
name            Name of the context, for use in FQDNs and similar
iprange         Subnet for the context, in CIDR notation
description     Human-readable name
dhcp            If dynamic DHCP should be enabled for this context/subnet, one of 1 and 0
parent          ID of the parrent context, NULL if root
email           Email of the Admin
============    =============

cnames
------

No corresponding class

Each entry in this table generates a CNAME entry in the DNS

============    =============
Column          Content
============    =============
id              ID
name            Name
target          Target
context         Name of the containing context
============    =============

aps
---

Corresponding class: :class:`AccessPoint`

This table contains information about Wireless Access Points

============    =============
Column          Content
============    =============
id              ID
device          ID of the corresponding device entry
channel         Channel to operate in
radiussecret    RADIUS passphrase
radiusserver    RADIUS server address
name            Name of the ap
vlans           VLANs the AP should belong in, comma-separated
mvlan           Management VLAN
switch          Config for integrated switch, see :doc:`switch_config`
model           Model of the AP, currently only "wr841n" supported
interfaces      Interfaces to enable, comma-separated
wifi_enabled    If WIFI should be enabled, one of 1 and 0
============    =============

wifis
-----

Corresponding class: :class:`WifiNetwork`

This table contains information about Wireless Networks

============    =============
Column          Content
============    =============
id              ID
ssid            SSID of the network
vlan            VLAN that should be bridged to the network
authmethod      Authentication method, one of "none" (open), "radius" (WPA-EAP), "passphrase" (WPA-PSK) and "wep" (WEP)
aps             List of AP-ids the network should be broadcasted on, comma-separated
hidden          If the network should hide its SSID, one of 1 and 0
passphrase      The network passphrase if authmethod is "passphrase" or "wep"
mode            Mode of the network, one of "ap" and "adhoc"
whitelist       If a whitelist should be active (see column ports in table devices), one of 1 and 0
enabled         If the network should be enabled, one of 1 and 0
============    =============

vlans
-----

Corresponding class: :class:`Vlan`

This table contains information about VLANs

============    =============
Column          Content
============    =============
id              VLAN tag
name            Human-readable name
============    =============

devicetypes
-----------

Corresponding class: :class:`DeviceType`

This table contains all possible device types

============    =============
Column          Content
============    =============
number          ID
name            Human-readable name (e.g. "linux-desktop", "network-device")
os              Operating System (e.g. "linux", "windows")
platform        Platform (e.g. "desktop", "mobile")
============    =============

