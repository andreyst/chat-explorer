import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import Container from './Container'

class ChatList extends Component {
  constructor() {
    super()
    this.state = {
      chats: [
        { id: 1, name: "My chat" },
        { id: 2, name: "Other chat" },
      ]
    }
  }

  render() {
    return (
      <Container header="Chats" buttonText="Import chat" buttonLink="/chats/import" buttonIcon="plus" noPadding>
        <table className="table table-striped">
          <tbody>
          {this.state.chats.map((chat) =>
            <tr key={chat.id}>
              <td><h4><Link to={"/chats/" + chat.id}>{chat.name}</Link></h4></td>
            </tr>
          )}
          </tbody>
        </table>
      </Container>
    )
  }
}

export default ChatList;
