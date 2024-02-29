#!/usr/bin/perl -w

# This script compares lumi cache files from two directories to see if they're the same, but ignores small
# differences that may be due to rounding/precision issues.

use strict;

my $olddir = shift or die "Usage: $0 olddir newdir\n";
my $newdir = shift or die "Usage: $0 olddir newdir\n";

my @files = glob("$olddir/lumicalc_cache_????-??-??.csv");

for my $file (@files) {
    my $newfile = $file;
    $newfile =~ s/$olddir/$newdir/;
    open OLDFILE, $file or die "Ack: $!\n";
    unless (open NEWFILE, $newfile) {
        print "Failed to open $newfile: $!\n";
        next;
    }
    my $printedThisFile = 0;
    while (my $oldline = <OLDFILE>) {
        my $newline = <NEWFILE>;

        my @oldfields = split(",", $oldline);
        $oldfields[5] = sprintf("%.3f", $oldfields[5]);
        $oldfields[6] = sprintf("%.3f", $oldfields[6]);
        $oldline = join(",", @oldfields);

        my @newfields = split(",", $newline);
        $newfields[5] = sprintf("%.3f", $newfields[5]);
        $newfields[6] = sprintf("%.3f", $newfields[6]);
        $newline = join(",", @newfields);

        if ($oldline ne $newline) {
            my $diffFields = 0;
	    my $diffOtherFields = 0;
            for (my $i=0; $i<@oldfields; ++$i) {
                if ($oldfields[$i] ne $newfields[$i]) {
                    $diffFields++;
		    if ($i !=5 && $i != 6) {
			$diffOtherFields++;
		    }
                }
            }
            if ($diffOtherFields == 0 && $diffFields <= 1 && abs($newfields[5]-$oldfields[5]) <= 0.0015 && abs($newfields[6]-$oldfields[6] <= 0.0015)) {
                # Probably just a rounding error; can ignore.
            } else {
		if ($printedThisFile == 0) {
		    print "In file $file:\n";
		    $printedThisFile = 1;
		}
                print "< ",$oldline;
                print "> ", $newline;
            }
        }
    }
}

print scalar(@files), " files checked.\n"
