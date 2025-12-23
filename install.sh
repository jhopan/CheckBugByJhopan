#!/bin/bash

ARCH=$(uname -m)

echo "Detected architecture: $ARCH"

if [[ $ARCH == *"aarch64"* ]] || [[ $ARCH == *"arm64"* ]]; then
    echo "Downloading ARM64 version..."
    wget https://github.com/XTLS/Xray-core/releases/download/v25.12.8/Xray-android-arm64-v8a.zip
    unzip Xray-android-arm64-v8a.zip
    CONFIG="xray.linux.arm64.64bit"
    
elif [[ $ARCH == *"x86_64"* ]] || [[ $ARCH == *"amd64"* ]]; then
    echo "Downloading AMD64 version..."
    wget https://github.com/XTLS/Xray-core/releases/download/v25.12.8/Xray-android-amd64.zip
    unzip Xray-android-amd64.zip
    CONFIG="xray.linux.amd64.64bit"
    
else
    echo "Unsupported architecture: $ARCH"
    echo "Only ARM64 and AMD64 are supported"
    exit 1
fi

wget "https://github.com/wannazid/XWan/raw/main/onering/$CONFIG"

cp xray $PREFIX/bin/
cp $CONFIG $PREFIX/bin/

chmod +x $PREFIX/bin/xray
chmod +x $PREFIX/bin/$CONFIG

rm -f Xray-*.zip geoip.dat geosite.dat LICENSE README.md

echo "Installation complete!"
echo "Xray installed to: $PREFIX/bin/xray"
echo "Config file: $PREFIX/bin/$CONFIG"
