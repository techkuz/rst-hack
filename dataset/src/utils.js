// @flow

function itarate(count: number, cb: () => any) {
  if (count) {
    // eslint-disable-next-line no-restricted-syntax
    for (const _ of new Array(count)) {
      cb();
    }
  }
}

export { itarate };
