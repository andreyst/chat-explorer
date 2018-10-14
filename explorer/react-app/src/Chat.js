import React, { Component } from 'react';
import Container from './Container'

class Chat extends Component {
  render() {
    const chatId = this.props.match.params.chatId;

    return (
      <Container header={"Chat " + chatId}>
        Chat contents
      </Container>
    )
  }
}

export default Chat
