import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import Container from '../Container';

class AddAccountTelegramConfirm extends Component {
  constructor() {
    super()
    this.state = {
      code: "",
      confirmed: false
    }

    this.onCodeChange = this.onCodeChange.bind(this)
    this.onConfirm = this.onConfirm.bind(this)
  }

  onCodeChange(e) {
    this.setState({ code: e.target.value })
  }

  onConfirm(e) {
    // store.dispatch(addAccount())
    setTimeout(() => { this.setState({ confirmed: true }) }, 1000)
  }

  render() {
    return (
      <Container header="Enter Telegram confirmation code">
        {this.state.confirmed &&
          <Redirect to={this.props.match.url + "/complete"} />
        }
        <form className="form-horizontal add-account-form">
          <div className="form-group">
            <label htmlFor="code" className="col-sm-5 control-label">Confirmation code</label>
            <div className="col-sm-7">
              <input id="code" type="text" className="form-control" onChange={this.onCodeChange} value={this.state.code} placeholder="00000"/>
            </div>
          </div>
          <a className="btn btn-primary btn-block" onClick={this.onConfirm}>Next</a>
        </form>
      </Container>
    )
  }
}

export default AddAccountTelegramConfirm;