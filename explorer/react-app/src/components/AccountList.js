import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import AccountHelper from '../AccountHelper';
import { fetchAccounts } from '../actions';

class AccountList extends Component {
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
    controls: PropTypes.bool,
    onDeleteAccountClick: PropTypes.func,
  }

  render() {
    const { accounts } = this.props;

    if (accounts.isFetching) {
      return (
        <div>Loading...</div>
      )
    }

    if (accounts.isError) {
      return (
        <div>Error while loading accounts. <a onClick={() => this.props.dispatch(fetchAccounts())}>Try again</a></div>
      )
    }

    if (!accounts.items.length) {
      return (
        <div>You do not currently have any chat accounts.</div>
      )
    }

    const toPrefix = this.props.to || null;

    return (
        <table className="table table-striped">
          <tbody>
          {this.props.accounts.items.map((account) =>
            <tr key={account.id}>
              <td>
                <h4 className="pull-left">
                  <i className={"account-icon fa " + AccountHelper.getIcon(account.messenger_type)}></i>
                  {!toPrefix ?
                    account.name
                    :
                    <Link to={toPrefix + "/" + account.id}>{account.name}</Link>
                  }
                </h4>
                {this.props.controls &&
                  <button type="button" className="btn btn-default pull-right" onClick={() => this.props.onDeleteAccountClick(account.id)}>
                    <i className="fa fa-trash-o"></i>
                  </button>
                }
              </td>
            </tr>
          )}
          </tbody>
        </table>
      )
  }
}

export default AccountList;
