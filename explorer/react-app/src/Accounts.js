import React, { Component } from 'react';
import Container from './Container';
import AccountList from './containers/AccountList';

class Accounts extends Component {
  render() {
    return (
      <Container header="Chat accounts" buttonText="Add chat account" buttonLink="/accounts/add" buttonIcon="plus" noPadding>
        <AccountList controls />
      </Container>
    )
  }
}

export default Accounts;