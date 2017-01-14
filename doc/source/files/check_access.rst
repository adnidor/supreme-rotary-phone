check_access
============

The files in this are scripts that get called to check if a device/user is authorized to access the network.

checkopenvpnaccess.py
---------------------

Gets called like: `./checkopenvpnaccess.py <tmpfile>`

Needs the enviromental variables:

 * `common_name`
 * `config`

Calls `/etc/openvpn/proxyarp-connect.sh` if it exists after finishing

Is supposed to be called in the `client-connect` config option in OpenVPN, the necessary arguments and envvars are supplied by OpenVPN.

Writes the `ifconfig-push` and `redirect-gateway` options in `<tmpfile>` form the database for OpenVPN to read and assign the connected device its IP

checkwifiaccess.py
------------------

Not finished yet, is supposed to be used in FreeRADIUS for controlling access to the wifi
