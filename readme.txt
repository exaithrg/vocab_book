# Download this repo:
git clone --depth 1 ...

# Build Repo:
kd --status
cd ~/.cache/kdcache
cat stat/counter-202411.json
j vocab
mv ~/.cache/kdcache/stat/counter-202411.json $(my_github_repo)
ln -s $(my_github_repo)/counter-202411.json ~/.cache/kdcache/stat

