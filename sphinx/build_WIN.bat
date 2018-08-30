
del /s/q _build

call make.bat html

rmdir /s/q "docs/~documentation"
md "docs/~documentation"
xcopy /s/e/i "_build/html" "docs/~documentation"

pause