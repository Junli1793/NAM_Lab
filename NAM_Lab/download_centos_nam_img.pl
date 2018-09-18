#!/usr/bin/perl -w
use strict;

my $indicator_file = "/tmp/centos_nam_img_download";
my $log_file = "/var/log/download_centos_nam_img.log";
my $black_list_file = "/root/shawn/centos_file_list";
my $black_list_file_dev = "/root/shawn/centos_dev_file_list";
my $black_list_file_release = "/root/shawn/centos_release_file_list";
my $mail_to = 'group.yuzhhuan@cisco.com';
#my $mail_to = 'crdc-nam-automation@cisco.com';
#my $mail_to = 'xiaozh2@cisco.com';
my $version_main = "/var/ftp/pub/nam/DAILY-BUILDS/main/centos_version.txt";

# main
if( -s $indicator_file ) {
    print "Another downloading is in process, exit!\n";
    exit;
}

open IND, ">$indicator_file";
print IND "downloading";
close IND;

`rm -f $version_main; touch $version_main`;


open LOG, ">>$log_file";
my $log_date = `date`;
print LOG "**************************************************\n$log_date\n";

my @main_new_files;
my @daily_new_files;
my ($remote, $local, $title, $content, $date, $old_name, $new_name);
my ($version_name, $version_tmp, $format, $version, $version_sub, $version_year, $version_month, $version_day, $version_time);

my (undef, undef, undef, $day, $mon, $year) = localtime;
$mon++;
$year += 1900;
$date = "$year/$mon/$day";

# black list
my @black_lists;
open BL, "<$black_list_file";
while(<BL>) {
    chomp;
    push @black_lists, $_;
}
close BL;

my @black_lists_dev;
open BL, "<$black_list_file_dev";
while(<BL>) {
    chomp;
    push @black_lists_dev, $_;
}
close BL;

my @black_lists_release;
open BL, "<$black_list_file_release";
while(<BL>) {
    chomp;
    push @black_lists_release, $_;
}
close BL;

#############################
# Download fc builds
#############################
$remote = "https://engci-maven-master.cisco.com/artifactory/nam-builds-group/release/6.4.1/";
$local = "/var/ftp/pub/nam/DAILY-BUILDS/release/6.4.1/";
@daily_new_files = ();
download($remote, $local, \@daily_new_files, 'release');

if(@daily_new_files > 0) {
    $title = "Local NAM FTP Server DAILY build centos images update ($date)";
    $content  = "The NAM image files can be found at:\n";
    $content .= "=========================================\n";
    my $ftp_prefix = "ftp://10.79.46.6/pub/nam/DAILY-BUILDS/release/6.4.1";
    my $http_prefix = "http://10.79.46.6/nam_img/DAILY-BUILDS/release/6.4.1";
    chdir($local) or die "$!";
    foreach(@daily_new_files) {
        $content .= "$ftp_prefix/$_\n\n$http_prefix/$_\n\n"; 
    }
    sendemail($mail_to, $title, $content);
}

#############################
# Download release builds
#############################
$remote = "https://engci-maven-master.cisco.com/artifactory/nam-builds-group/release/";
$local = "/var/ftp/pub/nam/DAILY-BUILDS/release/";
@daily_new_files = ();
download($remote, $local, \@daily_new_files, 'release');

if(@daily_new_files > 0) {
    $title = "Local NAM FTP Server DAILY build centos images update ($date)";
    $content  = "The NAM image files can be found at:\n";
    $content .= "=========================================\n";
    my $ftp_prefix = "ftp://10.79.46.6/pub/nam/DAILY-BUILDS/release";
    my $http_prefix = "http://10.79.46.6/nam_img/DAILY-BUILDS/release";
    chdir($local) or die "$!";
    foreach(@daily_new_files) {
        $old_name = $_;
        $content .= "$ftp_prefix/$_\n\n$http_prefix/$_\n\n"; 
        # For daily build, need to update the MAIN-LATEST soft links
        #if(/(.*?)\.(.*?)\-(.*?)\..*/){
        if(/(.*?)\.(.*?)(\-[0-9][0-9]\..*)/){
            $new_name = "$1.MAIN-LATEST$3"; 
            #print "old name: $old_name, new name: $new_name\n";

            $version_tmp = "$2$3";
            $format = "$3";
            $version_name = "$version_tmp";
        }
        if(/(.*?)\.(.*?)\.(.*)/){
            $new_name = "$1.MAIN-LATEST.$3"; 
            #print "old name: $old_name, new name: $new_name\n";
            `rm -f $new_name; ln -s $old_name $new_name`
        }
    }
    if($version_name){
        $_ = "$version_name";
        if(/(.*)\-(.*)\-(.*)\-(.*)\-([0-9][0-9][0-9][0-9])([0-9][0-9])([0-9][0-9])\-([0-9][0-9])/){
            $version = "$1\.$2";
            $version_sub = "$3";
            $version_year = "$5";
            $version_month = "$6";
            $version_day = "$7";
            $version_time = "$8";
    }
	open VERSION_MAIN, ">$version_main";
	print VERSION_MAIN "$version\($version_sub\.$version_year$version_month$version_day-$version_time\) INTERIM NIGHTLY BUILD [$version_year\-$version_month-$version_day]\n";
	close VERSION_MAIN;
	`cp $version_main /var/ftp/pub/usr/minmlin/centos_build_version.txt`;
    }
    sendemail($mail_to, $title, $content);
}

#############################
# Download daily builds
#############################
$remote = "https://engci-maven-master.cisco.com/artifactory/nam-builds-group/dev/";
$local = "/var/ftp/pub/nam/DAILY-BUILDS/dev/";
@daily_new_files = ();
download($remote, $local, \@daily_new_files, 'dev');

if(@daily_new_files > 0) {
    $title = "Local NAM FTP Server DAILY build centos images update ($date)";
    $content  = "The NAM image files can be found at:\n";
    $content .= "=========================================\n";
    my $ftp_prefix = "ftp://10.79.46.6/pub/nam/DAILY-BUILDS/dev";
    my $http_prefix = "http://10.79.46.6/nam_img/DAILY-BUILDS/dev";
    chdir($local) or die "$!";
    foreach(@daily_new_files) {
        $old_name = $_;
        $content .= "$ftp_prefix/$_\n\n$http_prefix/$_\n\n"; 
        # For daily build, need to update the MAIN-LATEST soft links
        if(/(.*?)\.(.*?)(\-[0-9][0-9]\..*)/){
            $new_name = "$1.MAIN-LATEST$3"; 

            $version_tmp = "$2$3";
            $format = "$3";
            $version_name = "$version_tmp";
        }
        if(/(.*?)\.(.*?)\.(.*)/){
            `rm -f $new_name; ln -s $old_name $new_name`
        }
    }
    if($version_name){
        $_ = "$version_name";
        if(/(.*)\-(.*)\-(.*)\-(.*)\-([0-9][0-9][0-9][0-9])([0-9][0-9])([0-9][0-9])\-([0-9][0-9])/){
            $version = "$1\.$2";
            $version_sub = "$3";
            $version_year = "$5";
            $version_month = "$6";
            $version_day = "$7";
            $version_time = "$8";
    }
	open VERSION_MAIN, ">$version_main";
	print VERSION_MAIN "$version\($version_sub\.$version_year$version_month$version_day-$version_time\) INTERIM NIGHTLY BUILD [$version_year\-$version_month-$version_day]\n";
	close VERSION_MAIN;
	`cp $version_main /var/ftp/pub/usr/minmlin/centos_build_version.txt`;
    }
    sendemail($mail_to, $title, $content);
}

close LOG;
# Finished downloading, remove indicator file
unlink $indicator_file;

####################
# Sub routines
####################

sub download
{
    my ($ftp_root, $dnld_dir, $new_files, $version) = @_;
    my $total_ct = 0;
    my $skip_ct = 0;
    my $success_ct = 0;
    my $failed_ct = 0;
    my $del_ct = 0;

    if ($version eq 'dev') {
        open BL, ">>$black_list_file_dev";
    } else {
        open BL, ">>$black_list_file_release";
    }
    #open BL, ">>$black_list_file";
    chdir($dnld_dir) or die "$!";
    print LOG "\nGetting file list from $ftp_root...";
    ########################################
    # Get remote file list 
    #
    my @tmp_flist = `curl $ftp_root --silent`;
    my @remote_flist;
    my $file_name;
    foreach(@tmp_flist) {
        chomp;
        if(/(nam\-app\-x86.*)(").*/) {
            $file_name = $1;
            push @remote_flist, $file_name;
            #if($file_name =~ /SSA/) {
                #    push @remote_flist, $file_name;
                #}else{
                #}
        }
        if(/(secpa\-app\-x86.*)(").*/) {
            $file_name = $1;
            push @remote_flist, $file_name;
        }

        if(/(vsecpa\-app\-x86.*)(").*/) {
            $file_name = $1;
            push @remote_flist, $file_name;
        }

        if(/^\-.*(nam\-vapp\-x86.*)$/) {
            push @remote_flist, $1;
        }
    }
    print LOG "Done\n\n";
    $total_ct = $#remote_flist + 1;
    
    ########################################
    # Get local file list 
    #
    # we are now in $dnld_dir
    my @local_flist = glob("nam\-v*app\-x86*");
    #print "remote: @remote_flist\nlocal: @local_flist";
    
    #####################################################################
    # Download files 
    #   Note: only download those files that we has not downloaded yet
    #
    my %local_files;
    foreach(@local_flist) {
        $local_files{"$_"} = 0;
    }
    #print %local_files;
    my $retval;
    foreach(@remote_flist) {
        if((($version eq 'dev') && ($_ ~~ @black_lists_dev))
        || (($version eq 'release') && ($_ ~~ @black_lists_release))) {
            print LOG "File $_ in black list!";
        } else {
            if(exists $local_files{"$_"}) {
                print LOG "File $_ exists!\n\n";
                # set a flag here to say we want to keep this file
                $local_files{"$_"}++;
                $skip_ct++;
            } else {
                print LOG "File $_ does not exists, start downloading...\n";
                print LOG "${ftp_root}$_\n";
                for (my $i=0; $i <= 9; $i++) {
                    $retval = system("wget ${ftp_root}$_ --no-check-certificate"); 
                    if($retval == 0) {
                        print LOG "File $_ download successfully!\n";
                        $success_ct++;
                        push @$new_files, $_;
                        print BL "$_\n";
                        $i = 10;
                    } else {
                        if ($i < 9) {
                            print LOG "File $_ download failed!\nRemoving file $_...";
                        }else{
                            print LOG "File $_ download failed!\nRemoving file $_...";
                            #unlink $_ or die "$!";
			                `rm -rf $_`;
                            print LOG "Done\n";
                            $failed_ct++;
                            close BL;
                        }
                    }
                }
            }
        }
        print LOG "\n";
    }

    # NOTICE: here we get a problem, sometimes the SJC server gives out an empty file list, which would make this script delete all the files
    ## Clear up files that the server has deleted
    #my ($key, $value);
    #while(($key, $value) = each %local_files) {
    #    #print "$key: $value\n";
    #    if(($value == 0) && !(-l $key)) {
    #        print LOG "Not found $key on server, deleting it...";
    #        unlink $key or die "$!";
    #        print LOG "Done\n";
    #        $del_ct++;
    #    }
    #}

    print LOG "\n===================================================\n";
    print LOG "Total file count: $total_ct\n";
    print LOG "Skipped: $skip_ct, Succeeded: $success_ct, Failed: $failed_ct, Deleted: $del_ct";
    print LOG "\n===================================================\n";
    close BL;
}

sub sendemail
{
    my ($to, $title, $cont) = @_;
    my $cmd = "echo \'$cont\' | mail -s \'$title\' $to";
    system($cmd);
}
