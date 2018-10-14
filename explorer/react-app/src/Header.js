import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class Header extends Component {
  render() {
    return (
      <header className="main-header">
        <nav className="navbar navbar-static-top">
          <div className="container">
            <div className="navbar-header">
            <Link className="navbar-brand" to="/">Chat Explorer</Link>
            </div>

            {/* Collect the nav links, forms, and other content for toggling */}
            <div className="collapse navbar-collapse pull-left" id="navbar-collapse">
              <ul className="nav navbar-nav">
                <li><Link to="/chats">Chats</Link></li>
                <li><Link to="/accounts">Accounts</Link></li>
              </ul>
            {/*
              <form className="navbar-form navbar-left" role="search">
                <div className="form-group">
                  <input type="text" className="form-control" id="navbar-search-input" placeholder="Search">
                </div>
              </form>
            */}
            </div>
            {/* /.navbar-collapse */}
            {/* Navbar Right Menu */}
            <div className="navbar-custom-menu">
              <ul className="nav navbar-nav">
                {/* User Account Menu */}
                <li className="dropdown">
                  {/* Menu Toggle Button */}
                  <a href="" className="dropdown-toggle" data-toggle="dropdown">
                    <span>username</span>
                  </a>
                  <ul className="dropdown-menu" role="menu">
                    {/* Menu Footer */}
                    {/* if user.is_superuser */}
                    <li><Link to="/admin">Admin</Link></li>
                    <li className="divider"></li>
                    {/* endif */}
                    <li><Link to="/logout">Logout</Link></li>
                  </ul>
                </li>
              </ul>
            </div>
            {/* /.navbar-custom-menu */}
          </div>
          {/* /.container-fluid */}
        </nav>
      </header>
    )
  }
}

export default Header;