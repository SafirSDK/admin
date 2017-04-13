#!/bin/bash

read -p "Are you sure? Double check the script! Otherwise press ctr-c."

VERSION=6.3.7

cd ~/tmp

#raspbian
rm -rf tmp tmp.zip
wget "https://connect.consoden.se/safir/view/All/job/Build%20tag/Config=Release,label=debian-jessie-rpi-build/lastSuccessfulBuild/artifact/tmp/*zip*/tmp.zip"
unzip tmp.zip
cd tmp
tar cvfj  safir-sdk-core_$VERSION-1_armhf-raspbian-jessie.debs.tar.bz2 *.deb
mv *.tar.bz2 ..
cd ..

#14.04 32
rm -rf tmp tmp.zip
wget "https://connect.consoden.se/safir/view/All/job/Build%20tag/Config=Release,label=ubuntu-trusty-lts-32-build/lastSuccessfulBuild/artifact/tmp/*zip*/tmp.zip"
unzip tmp.zip
cd tmp
tar cvfj  safir-sdk-core_$VERSION-1_i386-Ubuntu-14.04.debs.tar.bz2 *.deb
mv *.tar.bz2 ..
cd ..

#14.04 64
rm -rf tmp tmp.zip
wget "https://connect.consoden.se/safir/view/All/job/Build%20tag/Config=Release,label=ubuntu-trusty-lts-64-build/lastSuccessfulBuild/artifact/tmp/*zip*/tmp.zip"
unzip tmp.zip
cd tmp
tar cvfj  safir-sdk-core_$VERSION-1_amd64-Ubuntu-14.04.debs.tar.bz2 *.deb
mv *.tar.bz2 ..
cd ..

#16.04 32
rm -rf tmp tmp.zip
wget "https://connect.consoden.se/safir/view/All/job/Build%20tag/Config=Release,label=ubuntu-xenial-lts-32-build/lastSuccessfulBuild/artifact/tmp/*zip*/tmp.zip"
unzip tmp.zip
cd tmp
tar cvfj  safir-sdk-core_$VERSION-1_i386-Ubuntu-16.04.debs.tar.bz2 *.deb
mv *.tar.bz2 ..
cd ..

#16.04 64
rm -rf tmp tmp.zip
wget "https://connect.consoden.se/safir/view/All/job/Build%20tag/Config=Release,label=ubuntu-xenial-lts-64-build/lastSuccessfulBuild/artifact/tmp/*zip*/tmp.zip"
unzip tmp.zip
cd tmp
tar cvfj  safir-sdk-core_$VERSION-1_amd64-Ubuntu-16.04.debs.tar.bz2 *.deb
mv *.tar.bz2 ..
cd ..
