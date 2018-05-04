const React = require('react');

const QuestionView = require('./QuestionView.react');

const css = require('./customize.css');

class QuestionContainer extends React.Component {
  constructor(props) {
    super(props);
  }

  renderQuestions() {
    let questionsArray = [];
    for (let i = 0; i < this.props.questions.length; i++) {
      let currentQuestion = this.props.questions[i];
      // if (i !== 0 && i % 5 === 0) questionsArray.push(<br />);
      questionsArray.push(
        <div key={i}>
          <QuestionView
            qid={currentQuestion.id}
            qname={currentQuestion.name}
            qclassName={currentQuestion.class}
            question={currentQuestion.question}
            answers={currentQuestion.answers}
            submit={this.props.submit}
          />
        </div>
      );
    }
    return questionsArray;
  }

  render() {
    let prompt = `Answer the prompt of the gear with a(n) ` + 
    `${this.props.featureHintType} of ${this.props.featureHint}`;
    return (
      <div>
        <h1 id='question'>{prompt}</h1>
        {this.renderQuestions()}
      </div>
    );
  }
}

module.exports = QuestionContainer;
