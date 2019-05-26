#!/bin/sh
printf '\x02\xFF\x7F\x7f' | nc -u 10.42.0.74 1337
