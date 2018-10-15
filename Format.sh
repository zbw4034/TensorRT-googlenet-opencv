for f in $(find . -name '*.c' -or -name '*.cpp' -or -name '*.h' -type f)
do
#astyle --suffix=none --indent=tab --style=break --indent-switches --indent-cases --indent-namespaces --indent-preproc-block --indent-preproc-define --pad-oper --unpad-paren -p $f
astyle --suffix=none --style=break --indent-switches --indent-cases --indent-namespaces --indent-preproc-block --indent-preproc-define --pad-oper --unpad-paren -p $f
done
