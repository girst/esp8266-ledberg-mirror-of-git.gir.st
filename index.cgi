#!/usr/bin/perl

use strict;
use warnings;
use 5.014;

my $host = "10.42.0.74";

use IO::Socket;

my $s = IO::Socket::INET->new(
	Proto => 'udp',
	PeerAddr => $host,
	PeerPort => 1337,
	Timeout => 1,
) or die "socket";


if ($ENV{QUERY_STRING} =~ /o(n|ff)/) {
	$s->send(pack("C*", 1, ($1 eq 'n')));
} elsif ($ENV{QUERY_STRING} =~ /[0-9a-f]+/i) {
	my ($r,$g,$b) = unpack("C*", pack("H*",$ENV{QUERY_STRING}));
	$s->send(pack("C*", 2, $r, $g/2, $b/2));
}

if ($ENV{QUERY_STRING}) {
	print "status: 204 no content\r\n\r\n";
	exit 0;
}

my $buf = "";
$s->send("\x00");
$s->recv($buf,5);
my ($ok, $power, $r, $g, $b) = unpack("C*", $buf);
my $color = sprintf("%02x%02x%02x", $r, 2*$g, 2*$b);

print "content-type: text/html\r\n\r\n";
print "<script>const initial_color='#$color', initial_power=$power;</script>";
print <DATA>;



__DATA__
<title>ESP8266 Ledberg</title>
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<script src="iro.min.js"></script> <!-- https://iro.js.org/ -->

<style> /* https://www.w3schools.com/howto/howto_css_switch.asp */
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
 margin:.5em;
}
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
}
.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
}
input:checked + .slider {
  background-color: #2196F3;
}
input:focus + .slider {
  box-shadow: 0 0 1px #2196F3;
}
input:checked + .slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}
.slider.round {
  border-radius: 34px;
}
.slider.round:before {
  border-radius: 50%;
}
.switch { /*custom css*/
  position: absolute;
  left: 0;
  bottom: 34px;
  margin: 0;
}
</style>

<body style="margin:0">
<div style="display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;min-height:100vh;">
	<div style="position:relative">
	<label class="switch"><input id="power" type="checkbox"><span class="slider round"></span></label>
	<div id="picker"></div>
	</div>
</div>

<script>
"use strict";
const hsv2hsl = (h,s,v,l=v-v*s/2, m=Math.min(l,1-l)) => [h,m?(v-l)/m:0,l]; // https://stackoverflow.com/a/54116681
const hsv2rgb = (h,s,v,f=((n,k=(n+h/60)%6) => v - v*s*Math.max( Math.min(k,4-k,1), 0))) => [f(5),f(3),f(1)]; // https://stackoverflow.com/a/54024653

document.querySelector("#power").checked = initial_power;
document.querySelector("#power").onchange = e => {
	fetch('?' + (e.target.checked? 'on' : 'off'));
};

const colorPicker = new iro.ColorPicker('#picker', {
	wheelLightness: 0,
	color: initial_color
});
colorPicker.on(['color:init', 'color:change'], e=>{
	let [h,s,l] = hsv2hsl(e.hsv.h/360, e.hsv.s/100, 1);
	document.body.style.background = `hsl(${360*h}deg,${100*s}%,${100*l}%)`;
	if (window.request) window.request.abort();
	window.request = new AbortController();
	fetch(e.hexString.replace('#','?'), {signal:window.request.signal});
});
</script>
