#!/usr/bin/perl
# (c) 2019 Tobias Girstmair <https://gir.st/>; GPLv3

my $ip = "10.42.0.74";

use strict;
use warnings;

sub hue2rgb {
    my $h = $_[0] / 60;
    my $t = $h - int $h;
    my $q = 1.0 - $t;

    return ( 1, $t, 00) if $h < 1;
    return ($q,  1, 00) if $h < 2;
    return (00,  1, $t) if $h < 3;
    return (00, $q,  1) if $h < 4;
    return ($t, 00,  1) if $h < 5;
    return ( 1, 00, $q) if $h < 6;
}
sub packet {
    my ($type, $r, $g, $b) = @_;
    open(my $netcat, "| nc -u $ip 1337");
        print $netcat pack "CC",   0x01, $r                        if ($type eq "power");
        print $netcat pack "CCCC", 0x02, $r*0xFF, $g*0x7F, $b*0x7F if ($type eq "color");
    close($netcat);
}

packet "power", 1;
while(1) {
    for (1..359) {
	packet "color", hue2rgb($_, 1, 1);
	select(undef, undef, undef, 0.2);  # sub-second sleep() substitute
    }
}
