const async = require('async');
const axios = require('axios');
const React = require('react');

const QuestionContainer = require('./QuestionContainer.react');

// const css = require('./customize.css');

const START = "START";
const QUESTIONS = "QUESTIONS";
const WRONG = "WRONG";
const FLAG = "FLAG";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      view: START,
      url: 'start',
      questions: [],
      flag: '',
      authorization: '',
      featureHintType: '',
      featureHint: ''
    };
  }

  async getQuestions() {
    axios({
      method: 'get',
      url: this.state.url,
      authorization: this.state.authorization
    })
      .then((response) => {
        let ret = [
          response.data.questions,
          response.data.token
        ];
        return ret;
      })
      .catch((error) => {
        return [];
      });
  }

  renderView() {
    switch (this.state.view) {
      case START: return this.renderStartView();
      case QUESTIONS: return this.renderQuestionsView();
      case WRONG: return this.renderWrongView();
      case FLAG: return this.renderFlagView();
      default: return <span />;
    }
  }

  goToQuestionView(answer) {
    axios({
      method: 'get',
      url: this.state.url,
      headers: {
        Authorization: this.state.authorization
      },
      params: {
        answer: ((answer === 0 ? '0': answer) || 'no_answer')
      }
    })
      .then((response) => {
        if (response.status === 201) {
          this.setState({
            'view': WRONG,
            'url': 'start',
            'flag': response.data.message
          });
        } else if (response.status === 202) {
          this.setState({
            'view': FLAG,
            'url': 'start',
            'flag': response.data.flag
          });
        } else {
          this.setState({
            'view': QUESTIONS,
            'url': 'submit',
            'questions': response.data.questions,
            'authorization': response.data.token,
            'featureHintType': response.data.featureHintType,
            'featureHint': response.data.featureHint
          });
        }
      })
      .catch((error) => {
      });
  }

  changeView() {
    let newView = this.state.view;
    switch (this.state.view) {
      case START:
        this.goToQuestionView();
        newView = QUESTIONS;
        break;
      case WRONG:
        newView = START;
        break;
    }
    return newView;
  }

  renderStartView() {
    return (
      <div>
        <h1>
          Hello there! Welcome to my workshop! I need to get some things done, can you help?
        </h1>
        <p>
          We are given a clue about which problem we need to solve and then we have to figure out which one the clues matches to. Once we do that, we then solve that problem and submit that solution. We have to be quick though, because we only have 10 seconds for each problem! Hit the start button once you are ready to begin!
        </p>
        <button onClick={() => {this.goToQuestionView()}}>Start</button>
      </div>
    );
  }

  renderQuestionsView() {
    return <QuestionContainer
      questions={this.state.questions}
      featureHintType={this.state.featureHintType}
      featureHint={this.state.featureHint}
      submit={this.goToQuestionView.bind(this)}
    />;
  }

  renderWrongView() {
    return (
      <div>
        <h1>
          Oh no! It seems you got a wrong answer! Hit the button below to begin again!
        </h1>
        <p>{this.state.flag}</p>
        <button onClick={() => {this.goToQuestionView()}}>Start again</button>
      </div>
    );
  }

  renderFlagView() {
    return (
      <div>
        <h1>
          Yay! We got all the answers correct! Here is the flag:
        </h1>
        <p>
          {this.state.flag}
        </p>
      </div>
    );
  }

  render() {
    return (
      <div>
        {this.renderView()}
      </div>
    );
  }

}

module.exports = App;