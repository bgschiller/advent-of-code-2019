run_permutation() {
  rm /tmp/advent-07b
  touch /tmp/advent-07b
  cat -u <(echo "$1
0") <(tail -f /tmp/advent-07b) |
  python3 -u 05-advent.py |
  cat -u <(echo $2) - | python3 -u 05-advent.py |
  cat -u <(echo $3) - | python3 -u 05-advent.py |
  cat -u <(echo $4) - | python3 -u 05-advent.py |
  cat -u <(echo $5) - | python3 -u 05-advent.py >> /tmp/advent-07b
}

python -c "from itertools import permutations as p; print('\n'.join(' '.join(perm) for perm in p('98765')))" |
while read -r line; do
  echo $(run_permutation $line) $line
done |
sort -nr |
head -n1
