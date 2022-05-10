export enum Box {
  EMPTY = 'EMPTY',
  BLACK = 'BLACK',
  WHITE = 'WHITE',
}

export enum Turn {
  WHITE = 'WHITE',
  BLACK = 'BLACK',
}

export enum Rotation {
  CLOCKWISE = 'CLOCKWISE',
  ANTI_CLOCKWISE = 'ANTI_CLOCKWISE',
}

export enum Step {
  PLACE,
  ROTATE,
}

export type Board = [Quadran, Quadran, Quadran, Quadran];
export type Quadran = [Row, Row, Row];
export type Row = [Box, Box, Box];
