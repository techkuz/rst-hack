// @flow

// Standard Normal variate using Box-Muller transform.
// from: https://stackoverflow.com/a/49434653
function randomBM(min: number, max: number, skew: number = 1): number {
  let u = 0;
  let v = 0;
  while (u === 0) u = Math.random();
  while (v === 0) v = Math.random();
  let num = Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);

  num = num / 10.0 + 0.5;
  if (num > 1 || num < 0) num = randomBM(min, max, skew);
  num **= skew;
  num *= max - min;
  num += min;

  return Math.floor(num);
}

function random(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function randomize(weights: Array<number>, results: any) {
  const num = Math.random();
  let s = 0;
  const lastIndex = weights.length - 1;

  for (let i = 0; i < lastIndex; ++i) {
    s += weights[i];
    if (num < s) {
      return results[i];
    }
  }

  return results[lastIndex];
}

export { randomBM, random, randomize };
