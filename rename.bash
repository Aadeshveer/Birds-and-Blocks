# used to rename assets
files=$(find . -name ".*[0-9].png")
for file in $files; do
    new_file=$(echo $file | sed 's/.*\([0-9]\).png/dust0\1.png/')
    mv $file $new_file
done