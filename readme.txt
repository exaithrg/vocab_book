# Download this repo:
git clone --depth 1 ...

# Considerable Commands:
kd --status
cd ~/.cache/kdcache
cat stat/counter-202411.json
j vocab
mv ~/.cache/kdcache/stat/counter-202411.json $(my_github_repo)
ln -s $(my_github_repo)/counter-202411.json ~/.cache/kdcache/stat
jkdcache
sh caches/cachecopy.sh
p caches/jsonmerge.py
p process/process_vocab_book.py

# Notes
Do not replace 
⸺+\n
with
------------------------------------------------------------------------\n
in original vocab_book.txt
as ⸺+\n will always be appended to the original file.

# Thanks:
https://github.com/Karmenzind/kd
