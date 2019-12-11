pbpaste |
fold -w150 |
python3 -c "import sys; [print(line.count('0'), line.strip()) for line in sys.stdin if line.strip()]" |
sort -n |
head -n1 |
cut -f2 -d' ' |
python3 -c "import sys; [print(line.count('1') * line.count('2')) for line in sys.stdin]"
