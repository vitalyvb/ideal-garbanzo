# Firejail profile

# generic server profile
# it allows /sbin and /usr/sbin directories - this is where servers are installed
# depending on your usage, you can enable some of the commands below:

blacklist /tmp/.X11-unix

noblacklist /sbin
noblacklist /usr/sbin
# noblacklist /var/opt

noblacklist /etc/profile.d

include disable-common.inc
include disable-devel.inc
# include disable-interpreters.inc
include disable-passwdmgr.inc
include disable-programs.inc
#include disable-xdg.inc

caps
caps.keep net_raw
ipc-namespace
# netfilter /etc/firejail/webserver.net
no3d
nodbus
nodvd
# nogroups
# nonewprivs
# noroot
nosound
notv
nou2f
novideo

# these force nonewprivs = no suid binaries, no new caps
#seccomp
#protocol unix,inet,inet6,netlink,packet

dns 127.0.0.1

#shell none

# disable-mnt
# private
# private-bin program
# private-cache
private-dev
# private-etc none
# private-lib
private-tmp

# memory-deny-write-execute
# noexec ${HOME}
noexec /tmp

