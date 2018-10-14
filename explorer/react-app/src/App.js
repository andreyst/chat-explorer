import React, { Component } from 'react';
import './App.css';
import { Switch, Route, Redirect } from 'react-router-dom';
import Header from './Header.js';
import Accounts from './Accounts.js';
import AddAccount from './components/AddAccount.js';
import ChatList from './ChatList.js';
import Chat from './Chat.js';
import ChatImport from './ChatImport.js';
import RemoteChatList from './RemoteChatList';
import RemoteChatImport from './RemoteChatImport';
import PageNotFound from './PageNotFound';

class App extends Component {
  render() {
    return (
      <React.Fragment>
        <Header />
        <div className="content-wrapper">
          <Switch>
            <Redirect exact from="/" to="/chats"/>
            <Route exact path="/chats/import" component={ChatImport}/>
            <Route path="/chats/import/:accountId/remote/:remoteChatId" component={RemoteChatImport}/>
            <Route path="/chats/import/:accountId" component={RemoteChatList}/>
            <Route exact path="/accounts" component={Accounts}/>
            <Route path="/accounts/add/from/import" component={AddAccount}/>
            <Route path="/accounts/add" component={AddAccount}/>
            <Route exact path="/chats" component={ChatList}/>
            <Route path="/chats/:chatId" component={Chat}/>
            <Route component={PageNotFound}/>
          </Switch>
        </div>
        {/* /.content-wrapper */}
        {/*
        <footer className="main-footer">
          <div className="container">
          </div>
        */}
          {/* /.container */}
        {/* </footer> */}
      </React.Fragment>
    );
  }
}

export default App;

