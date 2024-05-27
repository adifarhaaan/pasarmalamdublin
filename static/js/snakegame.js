window.web3 = new Web3(window.ethereum);

rcntaddr = '0x2370f1c27da5048038724843C258168f452A7e4a'; //0xBa778D691f363984984Cd36c83BC81e0062B51c6


const coinabi = [{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Approval",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Transfer",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "allowance",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "approve",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			}
		],
		"name": "balanceOf",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "balances",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "decimals",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "name",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "symbol",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "totalSupply",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "transfer",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "transferFrom",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]

accounts=[]


coincontract = new web3.eth.Contract(coinabi,rcntaddr);





window.addEventListener('load', () => {
    getAccount();

  });
  
  async function getAccount() {
  	if (window.ethereum) {

	  	try	{
	    accounts = await ethereum.request({ method: 'eth_requestAccounts' });
	    const account = accounts[0];
	    document.getElementById("metalogin").innerHTML = "🔗" + account.substring(0,5)+'...'+account.substring(37);

	    _walletbalance = await coincontract.methods.balanceOf(accounts[0]).call();
		document.getElementById("walletbalance").innerHTML = Math.round(_walletbalance/(10**18)) + " RCNT";

	    }
	  
	    catch(error) {
	    document.getElementById("metalogin").innerHTML = "User denied access to wallet";
	  }
  }

	else {
	        $('#metalogin').html('No Metamask (or other Web3 Provider) installed')
	      }



  }























const foodItemsArray = [
  '🐁',
  '🍇',
  '🍉',
  '🍈',
  '🍓',
  '🍍',
  '🍌',
  '🥝',
  '🍏',
  '🍎',
  '🍔',
  '🍅',
  '🥚',
];

function wait(ms = 0) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function randomElementFromArray(arr) {
  const element = arr[Math.floor(Math.random() * arr.length)];
  return element;
}


// game display elements
const grid = document.querySelector('.grid');
const scoreDisplay = document.querySelector('.score');
const startBtn = document.querySelector('.start-btn');
const keyBtns = document.querySelectorAll('.keys-container button');

// game variables
const width = 10;
const numCells = width * width;
grid.style.width = `${width * 10 * 2}px`;
grid.style.height = `${width * 10 * 2}px`;

let currentSnake = [2, 1, 0];
let snakeColor = Math.floor(Math.random() * 360);
let snakeColorIncrement = 10;

let direction = 1;
let intervalTime = 200; // determines speed - frequency of game loop calls
let interval = 0;

let foodItemIndex = 0; // first cell
let score = 0;

// create grid cells
for (let i = 0; i < width * width; i++) {
  const cell = document.createElement('div');
  cell.style.width = `${width * 2}px`;
  cell.style.height = `${width * 2}px`;
  grid.appendChild(cell);
}
const cells = document.querySelectorAll('.grid div');



async function createFood() {
  foodItemIndex = Math.floor(Math.random() * numCells);
  if (currentSnake.includes(foodItemIndex)) {
    await wait(100);
    createFood();
  } else {
    cells[foodItemIndex].classList.add('food-item');
    cells[foodItemIndex].innerText = randomElementFromArray(foodItemsArray);
  }
}


function startGame() {

	grid.classList.remove('shake');

	currentSnake.forEach((i) => {
	  cells[i].style.background = 'none';
	  cells[i].classList.remove('snake');
	  cells[i].innerText = '';
	});

	clearInterval(interval);
	direction = 1;


	currentSnake = [2, 1, 0];
	currentSnake.forEach((i) => {
		snakeColor += snakeColorIncrement % 360;
		cells[i].style.background = `hsl(${snakeColor}, 100%, 50%)`;
		cells[i].classList.add('snake');
	});

	cells[foodItemIndex].classList.remove('food-item');
	cells[foodItemIndex].innerText = '';
	createFood();
	score = 0;
	scoreDisplay.innerHTML = score;

	interval = setInterval(gameLoop, intervalTime);
}
startBtn.addEventListener('click', startGame);



function gameLoop() {
	cells[currentSnake[0]].innerText = '';

	if (
	  (currentSnake[0] + width >= width * width && direction === width) || // hits bottom wall
	  (currentSnake[0] % width === width - 1 && direction === 1) || // hits right wall
	  (currentSnake[0] % width === 0 && direction === -1) || // hits left wall
	  (currentSnake[0] - width < 0 && direction === -width) || // hits the top wall
	  cells[currentSnake[0] + direction].classList.contains('snake') // hits itself
	) {
	  grid.classList.add('shake');
	  clearInterval(interval);
	  alert("Game Over. Your score is: "+ score)
	  MakePayment(score,accounts[0]);

	  //update db for high score
	  //update db for daily play 
	  //update db user has claim token

	  return;
	}

	const tail = currentSnake.pop();
	cells[tail].classList.remove('snake');
	cells[tail].style.background = 'none';
	currentSnake.unshift(currentSnake[0] + direction); // gives direction to the head


	if (cells[currentSnake[0]].classList.contains('food-item')) {
	  cells[currentSnake[0]].classList.remove('food-item');
	  cells[tail].classList.add('snake');
	  snakeColor += snakeColorIncrement % 360;
	  cells[tail].style.background = `hsl(${snakeColor}, 100%, 50%)`;
	  currentSnake.push(tail);
	  score++;
	  scoreDisplay.textContent = score;
	  createFood();
	}

	cells[currentSnake[0]].classList.add('snake');
	cells[currentSnake[0]].innerText = '🐱';
	snakeColor += snakeColorIncrement % 360;
	cells[currentSnake[0]].style.background = `hsl(${snakeColor}, 100%, 50%)`;
}


function moveSnake(moveDirection) {
  let directionVal;
  if (moveDirection === 'ArrowRight' && direction !== -1) {
    directionVal = 1;
    if (currentSnake[0] + directionVal === currentSnake[1]) return;
    direction = directionVal;
  }
  if (moveDirection === 'ArrowLeft' && direction !== 1) {
    directionVal = -1;
    if (currentSnake[0] + directionVal === currentSnake[1]) return;
    direction = directionVal;
  }
  if (moveDirection === 'ArrowUp' && direction !== width) {
    directionVal = -width;
    if (currentSnake[0] + directionVal === currentSnake[1]) return;
    direction = directionVal;
  }
  if (moveDirection === 'ArrowDown' && direction !== -width) {
    directionVal = width;
    if (currentSnake[0] + directionVal === currentSnake[1]) return;
    direction = directionVal;
  }
}

function  MakePayment(score_amount,winner){

        const amountEth = score_amount

        web3.eth.sendTransaction({
        	from: accounts[0],
          to: winner,
          value: amountEth*(10**18)
        }, (err, transactionId) => {
          if  (err) {
            console.log('Payment failed', err)
            $('#status').html('Payment failed')
          } else {
            console.log('Payment successful', transactionId)
            $('#status').html('Payment successful')
          }
        })
}



function handleKeyMove(e) {
  if (!['ArrowRight', 'ArrowLeft', 'ArrowUp', 'ArrowDown'].includes(e.key))
    return;
  moveSnake(e.key);
}


function handleButtonKeyMove(e) {
  const { id } = e.currentTarget;
  moveSnake(id);
}
keyBtns.forEach((keyBtn) => {
  keyBtn.addEventListener('mousedown', handleButtonKeyMove);
  keyBtn.addEventListener('touchstart', handleButtonKeyMove);
});


document.addEventListener('keydown', handleKeyMove);
