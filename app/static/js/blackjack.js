const debug = true;
const suits = ["C", "D", "H", "S"];
const values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"];
const ACE_VALUE = 11;

const hand = new Map();
const aceCount = new Map();

let hiddenCard;
let deck = [];
let canHit = true;
let canStay = true;
let firstTime = true;
let sounds = true;
let animationDelay = 500;

let hitBtn;
let stayBtn;
let soundsBtn;
let playAgainBtn;

window.onload = function () {
    preloadImages();
    hitBtn = document.getElementById("hit-btn");
    stayBtn = document.getElementById("stay-btn");
    soundsBtn = document.getElementById("sounds-btn");
    playAgainBtn = document.getElementById("play-again-btn");

    hitBtn.addEventListener("click", hit);
    stayBtn.addEventListener("click", stay);
    soundsBtn.addEventListener("click", toggleSound);
    playAgainBtn.addEventListener("click", playAgain);
    playAgainBtn.style.visibility = "hidden";

    startGame();
};

async function startGame() {
    const ms = firstTime ? 0 : animationDelay;

    buildDeck();
    shuffleDeck();

    hand.set("dealer", 0);
    hand.set("player", 0);
    aceCount.set("dealer", 0);
    aceCount.set("player", 0);

    addHiddenCard();
    await wait(ms);
    await addCardTo("dealer");
    await wait(ms);
    await addCardTo("player");
    await wait(ms);
    await addCardTo("player");

    canHit = true;
    canStay = true;
    firstTime = false;
}

function buildDeck() {
    deck = []; // reset the deck
    for (let i = 0; i < suits.length; i++) {
        for (let j = 0; j < values.length; j++) {
            deck.push(values[j] + "-" + suits[i]);
        }
    }
}

function shuffleDeck() {
    let currentIndex = deck.length;

    while (currentIndex !== 0) {
        let randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;
        [deck[currentIndex], deck[randomIndex]] = [deck[randomIndex], deck[currentIndex]];
    }
}

async function addCardTo(subject) {
    let card = deck.pop();
    let value = getCardValue(card);

    addValueToHand(value, subject);
    spawnCard(createCard(card), subject);
}

function addHiddenCard() {
    hiddenCard = document.createElement("img");
    hiddenCard.src = "../static/cards/hidden.png";
    spawnCard(hiddenCard, "dealer");
}

function spawnCard(card, subject) {
    document.getElementById(subject + "-hand").appendChild(card);
}

function createCard(card) {
    let img = document.createElement("img");
    img.src = "../static/cards/" + card + ".png";
    return img;
}

function addValueToHand(value, subject) {
    let currentValue = hand.get(subject);
    hand.set(subject, currentValue + value);

    log("adding " + value + " to " + subject);
    if (value === ACE_VALUE) {
        adjustAceCount(1, subject);
    }
}

async function hit() {
    if (!canHit) return;

    await addCardTo("player");

    if (getHand("player") > 21) {
        await wait(animationDelay);
        await stay();
    }
}

async function stay() {
    if (!canStay) return;

    canStay = false;
    canHit = false;

    await wait(animationDelay * 0.25);
    revealCard();
    await wait(animationDelay);

    while (getHand("dealer") < 17) {
        await addCardTo("dealer");
        await wait(animationDelay * 1.5);
    }

    await wait(animationDelay);
    checkWinner();
}

function getHand(subject) {
    let total = hand.get(subject);
    let aces = aceCount.get(subject);

    while (total > 21 && aces > 0) {
        total -= 10;
        aces--;
    }

    return total;
}

function revealCard() {
    let card = deck.pop();
    hiddenCard.src = createCard(card).src;

    let value = getCardValue(card);
    hand.set("dealer", hand.get("dealer") + value);
    if (value === ACE_VALUE) {
        adjustAceCount(1, "dealer");
    }
}

function checkWinner() {
    const status = document.getElementById("game-status");
    const dealer = getHand("dealer");
    const player = getHand("player");

    if (player > 21) {
        status.innerText = "Dealer won!\nPlayer busted";
    } else if (dealer > 21) {
        status.innerText = "Player won!\nDealer busted";
    } else if (player === dealer) {
        status.innerText = "Draw!";
    } else {
        status.innerText = player > dealer ? "Player won!" : "Dealer won!";
    }
    endGame();
}

function endGame() {
    playAgainBtn.style.visibility = "visible";
    playAgainBtn.focus();
    hitBtn.style.visibility = "hidden";
    stayBtn.style.visibility = "hidden";
}

function clearHands() {
    document.getElementById("dealer-hand").innerHTML = '';
    document.getElementById("player-hand").innerHTML = '';
}

function playAgain() {
    playAgainBtn.style.visibility = "hidden";
    hitBtn.style.visibility = "visible";
    stayBtn.style.visibility = "visible";
    document.getElementById("game-status").innerText = "";
    clearHands();
    startGame();
}

function adjustAceCount(increment, subject) {
    aceCount.set(subject, aceCount.get(subject) + increment);
}

function getCardValue(card) {
    const face = card.split("-")[0];
    if (face === "A") return ACE_VALUE;
    if (["T", "J", "Q", "K"].includes(face)) return 10;
    return parseInt(face);
}

function preloadImages() {
    suits.forEach(suit => {
        values.forEach(value => {
            const img = new Image();
            img.src = "../static/cards/" + value + "-" + suit + ".png";
        });
    });
}

function toggleSound() {
    sounds = !sounds;
    soundsBtn.style.opacity = sounds ? 1 : 0.5;
}

function playSound(audio) {
    if (audio && typeof audio.play === 'function' && sounds) {
        audio.play();
    }
}

function log(message) {
    if (debug) console.log(message);
}

function wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
