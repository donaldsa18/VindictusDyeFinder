copy *.py src\main\python\
rmdir /S /Q "target\Vindictus Dye Finder\"
fbs freeze %1
xcopy "resources" "target\Vindictus Dye Finder\resources\" /s /i
