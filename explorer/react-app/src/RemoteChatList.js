import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Container from './Container';

class RemoteChatList extends Component {
  constructor() {
    super()
    this.state = {
      remoteChats: [
        { id: 1, name: "Some name" },
        { id: 2, name: "Some other name" },
      ]
    }
  }

  render() {
    let accountId = this.props.match.params.accountId

    return (
      <Container header="Choose remote chat to import" buttonText="Cancel" buttonLink="/chats" buttonIcon="close" noPadding>
        <table className="table table-striped">
          <tbody>
          {this.state.remoteChats.map((remoteChat) =>
            <tr key={remoteChat.id}>
              <td><h4><Link to={"/chats/import/" + accountId + "/remote/" + remoteChat.id}>{remoteChat.name}</Link></h4></td>
            </tr>
          )}
          </tbody>
        </table>
      </Container>
    )
  }
}

export default RemoteChatList;
