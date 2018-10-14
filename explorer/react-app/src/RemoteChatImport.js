import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Container from './Container';

class RemoteChatImport extends Component {
  constructor() {
    super()

    this.state = {
      loading: true
    }
  }

  componentDidMount() {
    setTimeout(() => this.setState({ loading: false }), 1000)
  }

  render() {
    let remoteChatId = this.props.match.params.remoteChatId

    return (
      <Container header="Importing remote chat">
        {this.state.loading ?
          <div>Remote chat is being imported, please wait...</div>
          :
          <React.Fragment>
            <div>Remote chat has been successfully imported!</div>
            <Link to={"/chats/" + remoteChatId} className="btn btn-primary" role="button">Open chat</Link>
          </React.Fragment>
        }
      </Container>
    )
  }
}

export default RemoteChatImport;
