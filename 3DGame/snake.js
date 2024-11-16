// Constants for the game
const WIDTH = 20, HEIGHT = 20, DEPTH = 20; // Larger play area
const BLOCK_SIZE = 1;
const SPEED = 0.2;

// Directions for the snake
const DIRECTIONS = {
  "UP": [0, 1, 0],
  "DOWN": [0, -1, 0],
  "LEFT": [-1, 0, 0],
  "RIGHT": [1, 0, 0],
  "FORWARD": [0, 0, 1],
  "BACKWARD": [0, 0, -1]
};

let snake = [[0, 0, 0]]; // Snake starts with one block
let direction = DIRECTIONS["UP"];
let food = placeFood();
let score = 0;

function placeFood() {
  while (true) {
    let food = [
      Math.floor(Math.random() * (WIDTH + 1)) - WIDTH / 2,
      Math.floor(Math.random() * (HEIGHT + 1)) - HEIGHT / 2,
      Math.floor(Math.random() * (DEPTH + 1)) - DEPTH / 2
    ];
    // Ensure food is not placed on the snake
    if (!snake.some(segment => segment[0] === food[0] && segment[1] === food[1] && segment[2] === food[2])) {
      return food;
    }
  }
}

function moveSnake() {
  let head = snake[snake.length - 1];
  let newHead = [
    head[0] + direction[0],
    head[1] + direction[1],
    head[2] + direction[2]
  ];

  // Check if snake hits the walls or itself
  if (
    newHead[0] < -WIDTH / 2 || newHead[0] > WIDTH / 2 ||
    newHead[1] < -HEIGHT / 2 || newHead[1] > HEIGHT / 2 ||
    newHead[2] < -DEPTH / 2 || newHead[2] > DEPTH / 2 ||
    snake.some(segment => segment[0] === newHead[0] && segment[1] === newHead[1] && segment[2] === newHead[2])
  ) {
    return false; // Game over
  }

  snake.push(newHead);
  if (newHead[0] === food[0] && newHead[1] === food[1] && newHead[2] === food[2]) {
    food = placeFood(); // Place new food
    score++;
  } else {
    snake.shift(); // Remove last segment of snake
  }

  return true;
}

function changeDirection(newDirection) {
  // Prevent reversing direction
  let opposite = direction.map(x => -x);
  if (JSON.stringify(newDirection) !== JSON.stringify(opposite)) {
    direction = newDirection;
  }
}

function drawBlock(position, color) {
  const [x, y, z] = position;
  glColor3f(...color);
  glPushMatrix();
  glTranslatef(x, y, z);
  glutSolidCube(BLOCK_SIZE);
  glPopMatrix();
}

function drawWalls() {
  const wallColor = [0.5, 0.5, 0.5]; // Gray color for walls

  // Draw walls along X, Y, and Z axis at boundaries
  const wallThickness = 0.5;

  // X walls (front and back)
  for (let z = -DEPTH / 2 - 1; z <= DEPTH / 2 + 1; z++) {
    drawBlock([-WIDTH / 2 - 1, 0, z], wallColor); // Left wall
    drawBlock([WIDTH / 2 + 1, 0, z], wallColor); // Right wall
  }

  // Y walls (left and right)
  for (let z = -DEPTH / 2 - 1; z <= DEPTH / 2 + 1; z++) {
    drawBlock([0, -HEIGHT / 2 - 1, z], wallColor); // Bottom wall
    drawBlock([0, HEIGHT / 2 + 1, z], wallColor); // Top wall
  }

  // Z walls (near and far)
  for (let y = -HEIGHT / 2 - 1; y <= HEIGHT / 2 + 1; y++) {
    drawBlock([0, y, -DEPTH / 2 - 1], wallColor); // Near wall
    drawBlock([0, y, DEPTH / 2 + 1], wallColor); // Far wall
  }
}

function render() {
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
  glLoadIdentity();

  // Move camera back
  glTranslatef(0.0, 0.0, -30);

  // Draw the walls
  drawWalls();

  // Draw the snake
  for (let segment of snake) {
    drawBlock(segment, [0, 1, 0]); // Snake color
  }

  // Draw the food
  drawBlock(food, [1, 0, 0]); // Food color

  // Display the score
  document.getElementById("score").innerText = Score: ${score};

  // Flip the display
  pygame.display.flip();
}

// Main game loop
function gameLoop() {
  if (!moveSnake()) {
    alert(Game Over! Your score: ${score});
    resetGame();
  }

  render();
  requestAnimationFrame(gameLoop); // Keep the game running
}

function resetGame() {
  snake = [[0, 0, 0]];
  direction = DIRECTIONS["UP"];
  food = placeFood();
  score = 0;
}

document.addEventListener("keydown", (event) => {
  switch (event.key) {
    case "w":
      changeDirection(DIRECTIONS["UP"]);
      break;
    case "s":
      changeDirection(DIRECTIONS["DOWN"]);
      break;
    case "a":
      changeDirection(DIRECTIONS["LEFT"]);
      break;
    case "d":
      changeDirection(DIRECTIONS["RIGHT"]);
      break;
    case "q":
      changeDirection(DIRECTIONS["FORWARD"]);
      break;
    case "e":
      changeDirection(DIRECTIONS["BACKWARD"]);
      break;
  }
});

function startGame() {
  // Initialize Pygame and OpenGL
  pygame.init();
  let display = [1000, 800];
  pygame.display.set_mode(display, DOUBLEBUF | OPENGL);
  gluPerspective(45, display[0] / display[1], 0.1, 50.0);

  glEnable(GL_DEPTH_TEST);

  gameLoop(); // Start the game loop
}

// Wait until the page is fully loaded
window.onload = startGame;
