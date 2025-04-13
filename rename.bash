# used to rename assets
files=$(find . -name "file_name[0-9].png")
for file in $files; do
    new_file=$(echo $file | sed 's/file_name\([0-9]\).png/file_name0\1.png/')
    mv $file $new_file
done