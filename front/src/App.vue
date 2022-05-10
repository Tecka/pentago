<script setup lang="ts">
import { Ref, ref } from 'vue';
import { Board, Box, Rotation, Step, Turn } from './types';
import axios from 'axios';

const board: Ref<Board> = ref([
  [
    [Box.EMPTY, Box.EMPTY, Box.BLACK],
    [Box.BLACK, Box.EMPTY, Box.BLACK],
    [Box.EMPTY, Box.EMPTY, Box.EMPTY],
  ],
  [
    [Box.EMPTY, Box.BLACK, Box.EMPTY],
    [Box.EMPTY, Box.BLACK, Box.EMPTY],
    [Box.EMPTY, Box.EMPTY, Box.EMPTY],
  ],
  [
    [Box.EMPTY, Box.EMPTY, Box.EMPTY],
    [Box.EMPTY, Box.EMPTY, Box.EMPTY],
    [Box.EMPTY, Box.EMPTY, Box.EMPTY],
  ],
  [
    [Box.EMPTY, Box.EMPTY, Box.EMPTY],
    [Box.EMPTY, Box.EMPTY, Box.EMPTY],
    [Box.EMPTY, Box.EMPTY, Box.EMPTY],
  ],
] as Board);
const turn: Ref<Turn> = ref(Turn.WHITE);
const winner: Ref<Turn | null> = ref(null);
const nextStep: Ref<Step> = ref(Step.PLACE);

const postBoard = async () => {
  const res = await axios.post('http://localhost:8000/state', {
    board: board.value,
    turn: turn.value,
  });
  board.value = res.data.board;
  turn.value = res.data.turn;
  if (res.data.winner) {
    winner.value = res.data.winner;
  }
  nextStep.value = Step.PLACE;
};

const switchTurn = () =>
  (turn.value = turn.value === Turn.WHITE ? Turn.BLACK : Turn.WHITE);

const place = async (
  quadranIndex: number,
  rowIndex: number,
  boxIndex: number
) => {
  if (nextStep.value !== Step.PLACE) {
    return;
  }
  if (board.value[quadranIndex][rowIndex][boxIndex] !== Box.EMPTY) {
    return;
  }

  board.value[quadranIndex][rowIndex][boxIndex] = Box[turn.value];

  nextStep.value = Step.ROTATE;
};

const rotate = (quadranIndex: number, rotationDirection: Rotation) => {
  if (nextStep.value !== Step.ROTATE) {
    return;
  }

  const quadran = board.value[quadranIndex];
  if (rotationDirection === Rotation.CLOCKWISE) {
    board.value[quadranIndex] = [
      [quadran[2][0], quadran[1][0], quadran[0][0]],
      [quadran[2][1], quadran[1][1], quadran[0][1]],
      [quadran[2][2], quadran[1][2], quadran[0][2]],
    ];
  }

  if (rotationDirection === Rotation.ANTI_CLOCKWISE) {
    board.value[quadranIndex] = [
      [quadran[0][2], quadran[1][2], quadran[2][2]],
      [quadran[0][1], quadran[1][1], quadran[2][1]],
      [quadran[0][0], quadran[1][0], quadran[2][0]],
    ];
  }

  switchTurn();
  postBoard();
};
</script>

<template>
  <div class="flex bg-zinc-500">
    <div class="h-24 p-4 flex items-center space-x-4">
      <h1 v-if="!winner" class="text-center text-2xl">Turn</h1>
      <h1 v-if="winner" class="text-3xl bg-yellow-300">Winner:</h1>
      <div
        class="h-16 w-16 rounded-full"
        :class="{
          'bg-gray-900': turn === Turn.BLACK,
          'bg-gray-300': turn === Turn.WHITE,
        }"
      ></div>
    </div>
    <div class="flex justify-center">
      <div class="h-screen flex flex-col justify-between">
        <div class="h-1/2 py-8 flex flex-col justify-between">
          <div
            @click="rotate(0, Rotation.CLOCKWISE)"
            class="h-8 w-8 flex justify-center items-center cursor-pointer rounded-full border"
            :class="{
              'border-black text-black': nextStep === Step.ROTATE,
              'border-gray-700 text-gray-700': nextStep !== Step.ROTATE,
            }"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
          <div
            @click="rotate(0, Rotation.ANTI_CLOCKWISE)"
            class="h-8 w-8 flex justify-center items-center cursor-pointer rounded-full border"
            :class="{
              'border-black text-black': nextStep === Step.ROTATE,
              'border-gray-700 text-gray-700': nextStep !== Step.ROTATE,
            }"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
        </div>
        <div class="h-1/2 py-8 flex flex-col justify-between">
          <div
            @click="rotate(2, Rotation.CLOCKWISE)"
            class="h-8 w-8 flex justify-center items-center cursor-pointer rounded-full border"
            :class="{
              'border-black text-black': nextStep === Step.ROTATE,
              'border-gray-700 text-gray-700': nextStep !== Step.ROTATE,
            }"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
          <div
            @click="rotate(2, Rotation.ANTI_CLOCKWISE)"
            class="h-8 w-8 flex justify-center items-center cursor-pointer rounded-full border"
            :class="{
              'border-black text-black': nextStep === Step.ROTATE,
              'border-gray-700 text-gray-700': nextStep !== Step.ROTATE,
            }"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
        </div>
      </div>
      <div class="w-128 mr-7 h-screen p-2 flex flex-wrap bg-zinc-500">
        <div class="flex">
          <!-- TOP LEFT QUADRAN -->
          <div class="h-96 w-96 grow mr-2 mb-1 bg-gray-500">
            <div
              v-for="(row, i) in board[0]"
              :key="i"
              class="h-1/3 flex flex-row"
            >
              <div
                @click="place(0, i, j)"
                v-for="(box, j) in row"
                :key="j"
                class="w-1/3 flex justify-center items-center bg-amber-900 border border-black"
              >
                <div
                  class="h-16 w-16 rounded-full"
                  :class="{
                    'bg-gray-900': box === Box.BLACK,
                    'bg-gray-300': box === Box.WHITE,
                    'bg-gray-500': box === Box.EMPTY,
                  }"
                ></div>
              </div>
            </div>
          </div>
          <!-- TOP RIGHT QUADRAN -->
          <div class="h-96 w-96 grow ml-1 mb-1 bg-gray-500">
            <div
              v-for="(row, i) in board[1]"
              :key="i"
              class="h-1/3 flex flex-row"
            >
              <div
                @click="place(1, i, j)"
                v-for="(box, j) in row"
                :key="j"
                class="w-1/3 flex justify-center items-center bg-amber-900 border border-black"
              >
                <div
                  class="h-16 w-16 rounded-full"
                  :class="{
                    'bg-gray-900': box === Box.BLACK,
                    'bg-gray-300': box === Box.WHITE,
                    'bg-gray-500': box === Box.EMPTY,
                  }"
                ></div>
              </div>
            </div>
          </div>
        </div>
        <div class="flex">
          <!-- BOT LEFT QUADRAN -->
          <div class="h-96 w-96 grow mr-2 mt-1 bg-gray-500">
            <div
              v-for="(row, i) in board[2]"
              :key="i"
              class="h-1/3 flex flex-row"
            >
              <div
                @click="place(2, i, j)"
                v-for="(box, j) in row"
                :key="j"
                class="w-1/3 flex justify-center items-center bg-amber-900 border border-black"
              >
                <div
                  class="h-16 w-16 rounded-full"
                  :class="{
                    'bg-gray-900': box === Box.BLACK,
                    'bg-gray-300': box === Box.WHITE,
                    'bg-gray-500': box === Box.EMPTY,
                  }"
                ></div>
              </div>
            </div>
          </div>
          <!-- BOT RIGHT QUADRAN -->
          <div class="h-96 w-96 grow ml-1 mt-1 bg-gray-500">
            <div
              v-for="(row, i) in board[3]"
              :key="i"
              class="h-1/3 flex flex-row"
            >
              <div
                @click="place(3, i, j)"
                v-for="(box, j) in row"
                :key="j"
                class="w-1/3 flex justify-center items-center bg-amber-900 border border-black"
              >
                <div
                  class="h-16 w-16 rounded-full"
                  :class="{
                    'bg-gray-900': box === Box.BLACK,
                    'bg-gray-300': box === Box.WHITE,
                    'bg-gray-500': box === Box.EMPTY,
                  }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="h-screen flex flex-col justify-between">
        <div class="h-1/2 py-8 flex flex-col justify-between">
          <div
            @click="rotate(1, Rotation.ANTI_CLOCKWISE)"
            class="h-8 w-8 flex justify-center items-center cursor-pointer rounded-full border"
            :class="{
              'border-black text-black': nextStep === Step.ROTATE,
              'border-gray-700 text-gray-700': nextStep !== Step.ROTATE,
            }"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M10 19l-7-7m0 0l7-7m-7 7h18"
              />
            </svg>
          </div>
          <div
            @click="rotate(1, Rotation.CLOCKWISE)"
            class="h-8 w-8 flex justify-center items-center cursor-pointer rounded-full border"
            :class="{
              'border-black text-black': nextStep === Step.ROTATE,
              'border-gray-700 text-gray-700': nextStep !== Step.ROTATE,
            }"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M10 19l-7-7m0 0l7-7m-7 7h18"
              />
            </svg>
          </div>
        </div>
        <div class="h-1/2 py-8 flex flex-col justify-between">
          <div
            @click="rotate(3, Rotation.ANTI_CLOCKWISE)"
            class="h-8 w-8 flex justify-center items-center cursor-pointer rounded-full border"
            :class="{
              'border-black text-black': nextStep === Step.ROTATE,
              'border-gray-700 text-gray-700': nextStep !== Step.ROTATE,
            }"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M10 19l-7-7m0 0l7-7m-7 7h18"
              />
            </svg>
          </div>
          <div
            @click="rotate(3, Rotation.CLOCKWISE)"
            class="h-8 w-8 flex justify-center items-center cursor-pointer rounded-full border"
            :class="{
              'border-black text-black': nextStep === Step.ROTATE,
              'border-gray-700 text-gray-700': nextStep !== Step.ROTATE,
            }"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M10 19l-7-7m0 0l7-7m-7 7h18"
              />
            </svg>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
