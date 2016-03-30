# supreme-rotary-phone

Requirements: bind9 dnsmasq dokuwiki python3.4

tested on Ubuntu 14.04

recommended way of installing: put it in /opt/srp and create cronjob for the update.sh script

## server_config

Located in /etc/networkmanagement/server_config.py

has to contain:
* `host` the hostname of the mysql server (usually localhost)
* `user` the mysql username
* `passwd` the mysql password
* `db` the mysql database name
* `domain` the domain everything is below
* `email` e-mail address to be included in the SOA records
* `nameserver` nameserver to be include in the SOA records

##TODO
- [ ] Better documentation
- [ ] Better structure
- [ ] Packaging
