#!/usr/bin/perl -0777wn
use strict;

my ($info, $rev, $date, $time, $author) =
m{<div class="patternRevInfo">\s*(Topic revision: (r\d+) - (\d\d \w+ 20\d\d) - (\d\d:\d\d:\d\d) -).*?>(\w+)</a>\s*</div>}s;

my ($rawtext) =
m{<textarea [^>]*>(.*?)</textarea>}s;

my ($pagename) =
m{<base href="https://twiki.opensciencegrid.org/bin/view/([^"]+)"></base>};

print "$pagename\n\n";
print "$info $author\n";
print "\n";
print "$rawtext\n";

