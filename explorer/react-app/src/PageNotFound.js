import React, { Component } from 'react';
import Container from './Container';

class PageNotFound extends Component {
  render() {
    return (
      <Container header="Page not found">
      Alas, but this page is not found.
      </Container>
    )
  }
}

export default PageNotFound;
