#!/bin/bash


echo "Bump version? [y/N]"
python bump_version.py

release_version=$(cat wrapper/version.py)
release_version=$(echo "$release_version" | cut -c 3-)
echo $release_version

git add wrapper/version.py
git commit -m "Bump version to ${release_version}\n$@"
git push


echo "Building app..."
./scripts/build.sh
echo "App built."

echo "Are you sure you wish to release ${release_version}? [N/y]"

GITHUB_TOKEN="21b9b335294445199026eda76431621251886775"

#curl \
#    -H "Authorization: token $GITHUB_TOKEN" \
#    -H "Content-Type: $(file -b --mime-type $FILE)" \
#    --data-binary @$FILE "https://uploads.github.com/repos/hubot/singularity/releases/123/assets?name=$(basename $FILE)"

# Create release
response=$( http --json \
    --auth byte-le-royale-slave:$GITHUB_TOKEN \
    post \
    "https://api.github.com/repos/topoftheyear/Byte-le-Royale-2019/releases" \
    tag_name=$release_version \
    tag_commitish="master" \
    name="Version $release_version" \
    body="Release Notes:\n$@" \
    draft:=true 2>&1 )

echo $response


# parse out upload url
set -x
upload_url=$(echo $response | tr , \\n | grep "upload_url" | cut -d ":" -f 2 )#| cut -d / -f 1-8) + "/assets?name=br_launcher.pyz"
echo "Upload URL: $upload_url"


echo "Uploading launcher"
http \
    -a byte-le-royale-slave:$GITHUB_TOKEN \
    post \
    $upload_url
    Content-Type:application/octet-stream \
    file@br_launcher.pyz

echo "Launcher uploaded"
