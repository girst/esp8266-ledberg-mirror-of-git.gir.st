#!/bin/bash
# (c) 2019 Tobias Girstmair <https://gir.st/>; GPLv3

IP=10.42.0.74

C=(00 3F 7F FF)
old="000000"
while : ;do
	R=${C[((RANDOM%3))]}
	G=${C[((RANDOM%3))]}
	B=${C[((RANDOM%3))]}
	if test "$R$G$B" != "000000" && test "$R$G$B" != "$old"; then
		old="$R$G$B"
		printf "\\x02\\x$R\\x$G\\x$B" | nc -u $IP 1337
		sleep 1
	fi
done
