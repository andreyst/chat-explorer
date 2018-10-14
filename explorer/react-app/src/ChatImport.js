import React, { Component } from 'react';
import Container from './Container';
import AccountList from './containers/AccountList';

class ChatImport extends Component {
  render() {
    return (
      <Container header="Choose account to import chat from" buttonText="Add chat account" buttonLink="/accounts/add/from/import" buttonIcon="plus" noPadding>
        <AccountList to="/chats/import" controls={false} />
      </Container>
    )
  }
}

export default ChatImport;
