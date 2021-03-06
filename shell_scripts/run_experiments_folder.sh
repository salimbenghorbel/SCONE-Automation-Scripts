# This script can be used to optimize with SCONE all the files named 'scone_main.scone' found recursively under combinations_dir.
# combinations_dir is a folder path entered as first argument.
# Make sure to update scone_install accordingly.
combinations_dir=$1
current_dir=$(pwd)
scone_install=/data/benghorb/SCONE
cd $scone_install
source ./tools/linux_config
cd $current_dir
find $combinations_dir -type f -name "*scone_main.scone" | while read file_name; do "$scone_install"/build/bin/sconecmd -o "$file_name" -q -s;  done
