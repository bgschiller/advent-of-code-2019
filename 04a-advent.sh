seq 197487 673251 | # numbers in the range
grep -E '(.)\1{,1}' | # with at least one repeated digit
python -c 'import sys; [sys.stdout.write(line) for line in sys.stdin if line.strip() == "".join(sorted(line.strip()))]' | # digits are in sorted order
# ☝️ Anyone know a better way to do this?
wc -l # count the lines