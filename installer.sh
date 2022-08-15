#!/bin/bash

# This file is part of wrfplot application
# This is an installer script for installing wrfplot binary files to local
# install location and update bashrc/zshrc files to invoke from terminal
# Author: J Sundar aka wxguy
# Email: wrf.guy@gmail.com

install_directory="$HOME/.wrfplot"

if [[ -d $install_directory || -f $install_directory ]]; then
	echo -e "Removing previous install directory..."
	rm -rf $install_directory
fi

echo -e "Installing wrfplot to $install_directory..."
mv wrfplot $HOME/

echo -e "Renaming '$HOME/wrfplot' directory to '$install_directory'.."
mv $HOME/wrfplot $install_directory

# Create link of wrfplot binary to standard user bin location under home dir
if [ -d $HOME/.local/bin ]; then
	echo -e "'$HOME/.local/bin' directory already exists. Not creating it."
	echo -e "Linking wrfplot executable..."
	ln -sf $HOME/.wrfplot/wrfplot $HOME/.local/bin/wrfplot
else
	echo -e "Creating '$HOME/.local/bin' directory..."
	mkdir -p $HOME/.local/bin
	echo -e "Linking wrfplot executable..."
	ln -sf $HOME/.wrfplot/wrfplot $HOME/.local/bin/wrfplot
fi

# Update rc files for proper detection from terminal
echo -e "Updating .bashrc file to include install directory..."
if echo $PATH | grep -q "$HOME/.local/bin"; then
    echo -e ""$HOME/.local/bin" directory already added to PATH. Skipping..."
else
	echo "export PATH=$PATH:$HOME/.local/bin" >> $HOME/.bashrc
	if [ -f $HOME/.zshrc ]; then
		echo "export PATH=$PATH:$HOME/.local/bin" >> $HOME/.zshrc
	fi
	echo -e "$HOME/.bashrc file updated..."
fi

echo -e "Installation completed. Please restart your terminal to continue using wrfplot..."
