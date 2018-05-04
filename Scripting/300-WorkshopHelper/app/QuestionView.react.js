const React = require('react');

const css = require('./customize.css');

class QuestionView extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      selected: '',
      answer: '',
      buttonInput: '',
      textInput: ''
    };
  }

  renderMultipleChoice() {
    return this.props.answers.map((element, index) => {
      let curID = `${this.props.qid}-${index}`;
      return (
        <div key={index}>
          <input
            type="radio"
            name={'radAnswer'}
            // value={element}
            id={curID}
            checked={curID === this.state.selected}
            text={element}
            onClick={(e) => {
              e.target.checked = true;
              this.setState({
                'selected': curID,
                'buttonInput': element
              });
            }}
          />{element}
        </div>
      );
    });
  }

  renderFillIn() {
    return (
      <div>
        <label>
          <input
            type="text"
            name="input"
            value={this.state.textInput}
            className='input_thing'
            onChange={(e) => {
              this.setState({
                'textInput': e.target.value
              });
            }}
          />
        </label>
      </div>
    )
  }

  submit() {
    if (this.state.buttonInput !== '') this.props.submit(this.state.buttonInput);
    if (this.state.textInput !== '') this.props.submit(this.state.textInput);
    this.setState({
      'selected': '',
      'buttonInput': '',
      'textInput': ''
    })
  }

  render() {
    return (
      <div
        id={this.props.qid}
        name={this.props.qname}
        className={this.props.qclassName} // + ' ' + 'question_view'}
      >
        {/* <div className='question_view'> */}
        <div>
          <h3>{this.props.question}</h3>
          <form className='question_view' onSubmit={(e) => {
            e.preventDefault();
            e.stopPropagation();
            this.submit();
          }}>
            {this.props.answers.length > 0 ?
              this.renderMultipleChoice() :
              this.renderFillIn()
            }
          </form>
          <button onClick={() => {this.submit()}}>Submit</button>
        </div>
      </div>
    );
  }
}

module.exports = QuestionView;