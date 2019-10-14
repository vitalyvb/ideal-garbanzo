# bash

if [ "`id -u`" -eq 0 ]; then
  true
else
  PATH="/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin"
  export PATH
fi
