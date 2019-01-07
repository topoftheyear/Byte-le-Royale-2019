
rm -rf _build

make html

rm -rf ../docs/documentation!
mkdir ../docs/documentation!
cp -r _build/html/* ../docs/documentation!
