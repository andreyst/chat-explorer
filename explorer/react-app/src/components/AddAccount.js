import React, { Component } from 'react';
import { Redirect, Switch, Route } from 'react-router-dom';
import AddAccountSelectType from './AddAccountSelectType';
import AddAccountTelegramEnterNumber from '../containers/AddAccountTelegramEnterNumber';
import AddAccountTelegramConfirm from './AddAccountTelegramConfirm';

class AddAccount extends Component {
  render() {
    const url = this.props.match.url;
    const completeRedirectTo = this.props.match.url.indexOf("/from/import") !== -1 ? "/chats/import" : "/accounts";

    return (
      <Switch>
        <Route exact path={url + "/"} component={AddAccountSelectType} />
        <Redirect from={url + "/telegram/confirm/:accountId/complete"} to={completeRedirectTo} />
        <Route path={url + "/telegram/confirm/:accountId"} component={AddAccountTelegramConfirm} />
        <Route exact path={url + "/telegram"} component={AddAccountTelegramEnterNumber} />
      </Switch>
    )
  }
}

export default AddAccount;