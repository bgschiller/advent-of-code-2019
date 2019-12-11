seq 197487 673251 | # numbers in the range
grep -E '(.)\1' | # with at least one repeated digit
# Strictly speaking, ☝️ is no longer necessary, as
# the if-stmt below takes care of this condition too.
# however, running a new process for each line (like we
# do in the if-stmt) is very slow, so we speed things
# up significantly by doing the first pass with grep.
python -c 'import sys; [sys.stdout.write(line) for line in sys.stdin if line.strip() == "".join(sorted(line.strip()))]' | # digits are in sorted order
while read -r line ; do # within each line,
  if [[ -n "$(echo $line |
      fold -w1 | # put each character on own line
      uniq -c | # collapse repeats, including a count
      awk '{ if ($1 == 2) print; }' # print, but only if the number of repeats is exactly 2
  )" ]]; then
    # if that pipeline produced output, include the line
    echo $line
  fi
done |
wc -l # count lines