#!/bin/sh

dir_path=$(dirname $0)
cd ${dir_path}/../

if ! [ -x "$(command -v pdoc3)" ]; then
  echo 'Failed: pdoc3 is not installed. See: https://github.com/pdoc3/pdoc.'
  exit 1
fi

pdoc3 --html --template-dir doc/template -f -o doc/html pylash
echo 'Success: doc generated.'
