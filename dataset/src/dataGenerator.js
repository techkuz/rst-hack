// @flow

import { writeFileSync } from 'fs';
import rimraf from 'rimraf';
import path from 'path';
import nanoId from 'nanoid';

import { randomBM, random, randomize } from './random';

export type Order = {|
  order_id: string,
  pickup_location_x: number,
  pickup_location_y: number,
  pickup_from: number,
  pickup_to: number,
  dropoff_location_x: number,
  dropoff_location_y: number,
  dropoff_from: number,
  dropoff_to: number,
  payment: number
|};
type Courier = {|
  courier_id: string,
  location_x: number,
  location_y: number
|};

export type RandomArgsInput = [number, number];
export type RandomArgsResult = [number, number];
export type PickupLocationPositionRange = RandomArgsInput;
export type PickupFrom = RandomArgsInput;
export type PickupTo = RandomArgsInput;
export type DropoffLocationPositionRange = RandomArgsInput;
export type DropoffFrom = RandomArgsInput;
export type DropoffTo = RandomArgsInput;
export type CourierPosition = RandomArgsInput;

export type RandomArgsСompatible =
  | PickupLocationPositionRange
  | DropoffLocationPositionRange
  | DropoffFrom
  | DropoffTo
  | CourierPosition;

const MIN = 0;
const MAX = 1;

const min = (arr: RandomArgsСompatible): number => arr[MIN];
const max = (arr: RandomArgsСompatible): number => arr[MAX];
const getRandomArgs = (arr: RandomArgsСompatible): RandomArgsResult => [
  min(arr),
  max(arr)
];

type CreateOrderOptions = {|
  plp: PickupLocationPositionRange,
  pFrom: PickupFrom,
  dlp: DropoffLocationPositionRange,
  dFrom: DropoffFrom,
  payment: number
|};

function createOrder({
  plp,
  pFrom,
  dlp,
  dFrom,
  payment
}: CreateOrderOptions): Order {
  const pickupLocation = randomBM(...getRandomArgs(plp));
  const dropoffLocation = randomBM(...getRandomArgs(dlp));
  const dropoffFrom = randomBM(...getRandomArgs(dFrom));
  const dropoffTo = random(dropoffFrom, dropoffFrom + 200);
  const pickupFrom = randomBM(...getRandomArgs(pFrom));
  const pickupTo = random(pickupFrom, pickupFrom + 200);

  return {
    order_id: nanoId(),
    pickup_location_x: pickupLocation,
    pickup_location_y: pickupLocation + random(0, 45),
    pickup_from: pickupFrom,
    pickup_to: pickupTo,
    dropoff_location_x: dropoffLocation,
    dropoff_location_y: dropoffLocation + random(0, 34),
    dropoff_from: dropoffFrom,
    dropoff_to: dropoffTo,
    payment
  };
}

function createCourier(position: CourierPosition): Courier {
  const locationX = randomBM(...getRandomArgs(position));
  const locationY = locationX + random(locationX, 55);

  return {
    courier_id: nanoId(),
    location_x: locationX,
    location_y: locationY
  };
}

type DataGeneratorOptions = {|
  couriersLimit: number,
  ordersLimit: number
|};

type DataGeneratorOutput = {|
  couriers: Array<Courier>,
  orders: Array<Order>
|};

function dataGenerator(options: DataGeneratorOptions): DataGeneratorOutput {
  const couriers = [];
  const orders = [];

  for (let i = 0; i < options.couriersLimit; i++) {
    couriers.push(createCourier([100, 200]));
  }

  for (let i = 0; i < options.ordersLimit; i++) {
    orders.push(
      createOrder({
        plp: [50, 400],
        pFrom: randomize([0.4, 0.4, 0.2], [[0, 360], [360, 720], [720, 1440]]),
        dlp: [200, 500],
        dFrom: randomize(
          [0.2, 0.4, 0.2],
          [[540, 720], [720, 960], [960, 1440]]
        ),
        payment: randomize([0.3, 0.3, 0.4], [400, 450, 500])
      })
    );
  }

  return {
    couriers,
    orders
  };
}

type WriteFileOptions = {|
  fileLimit?: number,
  limitByFile?: number,
  debug?: boolean,
  output?: string
|};

function startWriteFiles(
  options: WriteFileOptions = {
    fileLimit: 50,
    limitByFile: 3,
    debug: false,
    output: path.join(__dirname, '../data')
  }
): void {
  rimraf(path.join(options.output, '*'), () => {
    for (let i = 0; i <= options.fileLimit; i++) {
      try {
        const jsonData = JSON.stringify(
          dataGenerator({
            couriersLimit: 2,
            ordersLimit: 10
          }),
          null,
          2
        );
        if (!options.debug) {
          writeFileSync(path.join(options.output, `${i}.json`), jsonData, {
            encoding: 'utf8'
          });
        }
      } catch (e) {
        console.error(e);
      }
    }
  });
}

export { startWriteFiles };
