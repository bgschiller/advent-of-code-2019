run_permutation() {
  echo "$1
0" | python3 05-advent.py |
  cat <(echo $2) - | python3 05-advent.py |
  cat <(echo $3) - | python3 05-advent.py |
  cat <(echo $4) - | python3 05-advent.py |
  cat <(echo $5) - | python3 05-advent.py
}

python -c "from itertools import permutations as p; print('\n'.join(' '.join(perm) for perm in p('01234')))" |
while read -r line; do
  echo $(run_permutation $line) $line
done |
sort -nr |
head -n1
