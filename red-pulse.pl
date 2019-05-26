#!/usr/bin/perl
# (c) 2019 Tobias Girstmair <https://gir.st/>; GPLv3

my $ip = "10.42.0.74";

use strict;
use warnings;
use Math::Trig;

sub packet {
    my ($type, $r, $g, $b) = @_;
    open(my $netcat, "| nc -u $ip 1337");
        print $netcat pack "CC",   0x01, $r                        if ($type eq "power");
        print $netcat pack "CCCC", 0x02, $r*0xFF, $g*0x7F, $b*0x7F if ($type eq "color");
    close($netcat);
}

packet "power", 1;
while(1) {
    for (0..359) {
	packet "color", ((abs sin deg2rad $_), 0, 0);
	select(undef, undef, undef, 0.02);  # sub-second sleep() substitute
    }
}
