// @flow

import path from 'path';
import { startWriteFiles } from './dataGenerator';

function main() {
  startWriteFiles({
    fileLimit: 3,
    limitByFile: 2,
    debug: true,
    output: path.join(__dirname, '../data')
  });
}

main();
