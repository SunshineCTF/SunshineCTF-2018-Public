const bodyParser = require('body-parser');
const crypto = require('crypto');
const express = require('express');
const fs = require('fs');
// const randomNumber = require('random-number-csprng');
const uuidv4 = require('uuid/v4');
const webpack = require('webpack');
const webpackDevMiddleware = require('webpack-dev-middleware');

const webpackConfig = require('./webpack.config');

const app = express();
const compiler = webpack(webpackConfig);

const PORT = 50001;

let FLAG = '';

fs.readFile('flag.txt', 'utf8', (err, data) => {
  if (err) throw err;
  FLAG = data;
});

const NUM_USERS = 500;
const LOW = 1;
const HIGH = 1000000;
const ANSWER_RANGE = 100;
const NUM_QUESTIONS = 30;
const OPERATIONS = ["+", "-", "*", "/", "%"];
const FEATURES = ["id", "name", "class"];
// Give the player a couple extra seconds as buffer
const TIME_LIMIT_SECONDS = 12;

// Create users array set to length of 500, cause we ain't going to use a db
// Then fill it with objects with a few values:
let users = Array(NUM_USERS);
users.fill(0);
let emptyUser = {
  "token": "",
  "level": "",
  "time-made": "",
  "answer": ""
};
users = users.map((i) => {
  return Object.assign({}, emptyUser);
});

function randomNumber(low, high) {
  return parseInt((Math.random() * (high - low) + low));
}

function randomChoice(arr) {
  return arr[randomNumber(0, arr.length)];
}

function makeQuestions() {
  let questions = [];
  let answers = [];
  for (let i = 0; i < NUM_QUESTIONS; i++) {
    let currentQuestion = {};
    let a = randomNumber(LOW, HIGH);
    let b = randomNumber(LOW, HIGH);
    let operation = randomChoice(OPERATIONS);
    let question = `${a} ${operation} ${b}`;
    let question_type = randomNumber(0, 2);
    let answer = parseInt(eval(question));
    for (let feature in FEATURES) {
      currentQuestion[FEATURES[feature]] = "" + randomNumber(LOW, HIGH);
    }
    answers.push(answer);
    let other_answers = [];
    if (question_type === 0) {
      // If question_type is 0 we will have a multiple choice question
      other_answers = [
        randomNumber(answer - ANSWER_RANGE, answer + ANSWER_RANGE),
        randomNumber(answer - ANSWER_RANGE, answer + ANSWER_RANGE),
        randomNumber(answer - ANSWER_RANGE, answer + ANSWER_RANGE)
      ];
      let answer_loc = randomNumber(0, 4);
      other_answers.splice(answer_loc, 0, answer);
    } else {
      // don't need to do anything here
    }
    currentQuestion["question"] = question;
    currentQuestion["answers"] = other_answers;
    questions.push(currentQuestion);
  }
  return {
    "questions": questions,
    "answers": answers
  };
}

function closeRange(t1, t2, range, loop=0) {
  loop = loop || 0;
  return (t2 - t1 <= range && t2 >= t1) || (t2 + loop - t1 <= range);
}

function checkExpired(user) {
  let time = user["time-made"];
  let curTime = new Date();
  if (closeRange(time.getHours(), curTime.getHours(), 1, 24)) {
    if (closeRange(time.getMinutes(), curTime.getMinutes(), 1, 60)) {
      if (closeRange(time.getSeconds(), curTime.getSeconds(), 12, 60)) {
        return false;
      }
    }
  }
  return true;
  // let curTime = (new Date()).toLocaleTimeString();
  // user_seconds = parseInt(time.split(" ")[0].split(":")[2]);
  // cur_seconds = parseInt(time.split(" ")[0].split(":")[2]);
  // return (
  //   (cur_seconds - user_seconds) > 33 ||
  //   (cur_seconds + 60 - user_seconds > 33)
  // );
  // (new Date()).to
}

function makeNewUser() {
  let found = false;
  let loc = -1;
  let newUser = {};
  for (let i = 0; i < NUM_USERS; i++) {
    if (users[i]["token"] === "") {
      if (!found) {
        found = true;
        users[i] = {
          "token": uuidv4(),
          "level": 0,
          "time-made": new Date(),
          "answer" : ""
        };
        loc = i;
        break;
      }
    } else {
      if (checkExpired(users[i])) {
        users[i] = Object.assign({}, emptyUser);
        if (!found) {
          found = true;
          users[i] = {
            "token": uuidv4(),
            "level": 0,
            "time-made": new Date(),
            "answer": ""
          };
          loc = i;
          break;
        }
      }
    }
  }
  if (loc !== -1) {
    return users[loc];
  } else {
    return -1;
  }
}

function questionsAndAnswer() {
  let questionsAndAnswers = makeQuestions();
  let questions = questionsAndAnswers["questions"];
  let answers = questionsAndAnswers["answers"];
  let questionSelection = randomNumber(0, NUM_QUESTIONS);
  let featureSelection = randomChoice(FEATURES);
  return {
    'questions': questions,
    'answer': answers[questionSelection].toString(),
    'featureHintType': featureSelection,
    'featureHint': questions[questionSelection][featureSelection]
  };
}

function findUser(token) {
  for (let i = 0; i < NUM_USERS; i++) {
    if (users[i]['token'] === token) {
      return users[i];
    }
  }
  return undefined;
}

function setUserNextProblem(user) {
  let qsAndA = questionsAndAnswer();
  let reply = {
    'token': user['token'],
    'level': user['level'],
    'questions': qsAndA['questions'],
    'featureHintType': qsAndA['featureHintType'],
    'featureHint': qsAndA['featureHint']
  };
  user['answer'] = qsAndA['answer'].toString();
  user['time-made'] = new Date();
  user['level'] = user['level'] + 1;
  return reply;
}

// App
app.use(webpackDevMiddleware(compiler, {
  hot: true,
  filename: 'bundle.js',
  publicPath: '/',
  stats: {
    colors: true
  },
  historyApiFallback: true
}));

// Tell the application the default location of the html and bundle files
app.use(express.static(__dirname + '/www'));

// Set up bodyParser
app.use(bodyParser.json());

app.get('/', (req, res) => {
  res.status(200).send({});
});

app.get('/submit', (req, res) => {
  let token = req.headers.authorization;
  let answer = req.query.answer;
  if (token === undefined) {
    res.status(400).send('Authentication token required');
  } else if (answer === undefined) {
    res.status(400).send('Answer required');
  } else {
    let user = findUser(token);
    if (user === undefined) {
      res.status(201).send({
        'message': 'Did you take too long to answer?'
      });
      return;
    }
    let reply = {};
    // console.log(answer, user['answer'], typeof answer, typeof user['answer']);
    if (checkExpired(user)) {
      res.status(201).send({
        'message': 'Did you take too long to answer?'
      });
      return;
    }
    let statusCode = 200;
    if (answer === user['answer']) {
      reply = setUserNextProblem(user);
      reply['result'] = 'Correct';
      if (user['level'] > NUM_QUESTIONS) {
        reply['flag'] = FLAG;
        statusCode = 202;
      }
    } else {
      reply = {'message': 'Incorrect answer'};
      // res.status(201).send(reply);
      statusCode = 201;
    }
    res.status(statusCode).send(reply);
  }
});

app.get('/start', (req, res) => {
  let user = makeNewUser();
  if (user === -1) {
    // Do something for the case that there is no available spots
  } else {
    let reply = setUserNextProblem(user);
    res.status(200).send(reply);
  }
});

const server = app.listen(PORT, () => {
  console.log(`listening on port ${PORT}!`);
})
