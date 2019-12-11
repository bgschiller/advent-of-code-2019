type CardinalDir = 'U' | 'R' | 'L' | 'D';

type Pos = [number, number];

interface Step {
  dir: CardinalDir;
  units: number;
}

function assertUnreachable(x: never): never {
  throw new Error(`expected to never reach here: ${x}`);
}

function unitVec(dir: CardinalDir): Pos {
  if (dir === 'U') return [0, 1];
  if (dir === 'D') return [0, -1];
  if (dir === 'L') return [-1, 0];
  if (dir === 'R') return [1, 0];
  assertUnreachable(dir);
}

function nextPos(curr: Pos, step: Step): Pos {
  const unit = unitVec(step.dir);
  return [
    curr[0] + unit[0] * step.units,
    curr[1] + unit[1] * step.units,
  ];
}

function positions(steps: Step[]): Pos[] {
  let curr: Pos = [0, 0];
  const posns = [curr];
  steps.forEach(s => {
    curr = nextPos(curr, s);
    posns.push(curr);
  });
  return posns;
}

type Segment = [Pos, Pos];
function segments(posns: Pos[]): Segment[] {
  return new Array(posns.length - 1)
    .fill(null)
    .map((_, ix) => [posns[ix], posns[ix + 1]]);
}

type Interval = [number, number] & { readonly __tag: unique symbol };

function toInterval([a, b]: [number, number]): Interval {
  return [
    Math.min(a, b),
    Math.max(a, b),
  ] as Interval;
}

function intervalsIntersect([a, b]: Interval, [c, d]: Interval): number | null {
    // a      c   b      d
    // ■ ─ ─ ─■───■ ─ ─ ─■
    return a <= d && c <= b ? c : null;
}

function isVertical([a, b]: Segment): boolean {
  return a[0] === b[0]
}

function truthTable(x: boolean, y: boolean): 'tt' | 'tf' | 'ft' | 'ff' {
  if (x && y) return 'tt';
  if (x && !y) return 'tf';
  if (!x && y) return 'ft';
  return 'ff';
}

function segmentsIntersect(ab: Segment, cd: Segment): Pos | null {
  const abVerticalCdVertical = truthTable(
    isVertical(ab),
    isVertical(cd));

  const [a, b] = ab;
  const [c, d] = cd;
  if (abVerticalCdVertical === 'tt') {
    if (a[0] !== c[0]) {
      // but not the same x value
      return null;
    }
    const yInter = intervalsIntersect(
      toInterval([a[1], b[1]]),
      toInterval([c[1], d[1]]));
    return yInter ? [a[0], yInter] : null;
  } else if (abVerticalCdVertical === 'ff') {
    if (a[1] !== c[1]) {
      // but not the same y value
      return null;
    }
    const xInter = intervalsIntersect(
      toInterval([a[0], b[0]]),
      toInterval([c[0], d[0]]));
    return xInter ? [xInter, a[1]] : null;
  } else if (abVerticalCdVertical === 'tf') {
    return segmentsIntersect(cd, ab);
  } else if (abVerticalCdVertical === 'ft') {
    /*
          ■ d
          │
    a     │    b
    ■─────┼────■
          │
          ■ c
    */
    const [ax, bx] = toInterval([a[0], b[0]]);
    const [cy, dy] = toInterval([c[1], d[1]]);
    const cx = c[0];
    const ay = a[1];
    return (
      cy <= ay && ay <= dy &&
      ax <= cx && cx <= bx
    ) ? [cx, ay] : null;
  }
  assertUnreachable(abVerticalCdVertical);
}

function intersections(steps1: Step[], steps2: Step[]): Pos[] {
  const inters: Pos[] = [];
  const segs1 = segments(positions(steps1));
  const segs2 = segments(positions(steps2));
  for (const s1 of segs1) {
    for (const s2 of segs2) {
      const inter = segmentsIntersect(s1, s2);
      if (inter) {
        inters.push(inter);
      }
    }
  }
  return inters;
}

function toStep(s: string): Step {
  return {
    dir: s.charAt(0) as CardinalDir,
    units: Number(s.slice(1)),
  };
}

function distance(input: string): number {
  const [r1, r2] = input.split('\n');
  const steps1 = r1.split(',').map(toStep);
  const steps2 = r2.split(',').map(toStep);
  const inters = intersections(steps1, steps2);
  const distances = inters
    .filter(([x,y]) => x !== 0 || y !== 0)
    .map(([x, y]) => Math.abs(x) + Math.abs(y));
  return Math.min(...distances);
}
