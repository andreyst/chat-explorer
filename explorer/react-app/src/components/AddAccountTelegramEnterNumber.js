import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Redirect } from 'react-router-dom';
import Container from '../Container';

class AddAccountTelegramEnterNumber extends Component {
  static propTypes = {
    accounts: PropTypes.shape({
      isFetching: PropTypes.bool,
      isError: PropTypes.bool,
      items: PropTypes.arrayOf(
        PropTypes.shape({
          id: PropTypes.number.isRequired,
          name: PropTypes.string.isRequired,
          messenger_type: PropTypes.number.isRequired,
        })
      )
    }).isRequired,
    onAddAccountClick: PropTypes.func,
  }

  constructor() {
    super()
    this.state = {
      number: "",
      accountId: null,
      accountCreated: false,
    }

    this.onNumberChange = this.onNumberChange.bind(this)
  }

  onNumberChange(e) {
    this.setState({ number: e.target.value })
  }

  render() {
    const { accounts } = this.props;

    let content = ""
    if (accounts.isAddingAccount) {
      content = (
        <div>Loading...</div>
      )
    } else {
      content = (
        <form className="form-horizontal add-account-form">
          <div className="form-group">
            <label htmlFor="number" className="col-sm-5 control-label">Phone number</label>
            <div className="col-sm-7">
              <input id="number" type="phone" className="form-control" onChange={this.onNumberChange} value={this.state.number} placeholder="+123456789"/>
            </div>
          </div>
          <a className="btn btn-primary btn-block" onClick={() => this.props.onAddAccountClick(this.state.number)}>Next</a>
        </form>
      )
    }

    return (
      <Container header="Enter Telegram phone number">
        {accounts.isAddAccountError &&
          <div className="alert alert-danger alert-dismissible">Error occurred while adding account, please try again</div>
        }
        {accounts.isAccountAdded &&
          <Redirect to={this.props.match.url + "/confirm/" + accounts.addedAccountId} />
        }
        {content}
      </Container>
    )
  }
}

export default AddAccountTelegramEnterNumber;