import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';

class Container extends Component {
  render() {
    return (
      <div className="container">
        {/* Content Header (Page header) */}
        <section className="content-header">
          <h1>{this.props.header}
           {this.props.buttonText &&
            <Link className="btn btn-primary pull-right" to={this.props.buttonLink} role="button"><i className={"fa fa-" + this.props.buttonIcon}>&nbsp;</i> {this.props.buttonText}</Link>
            }
          </h1>
          {/*
          <ol className="breadcrumb">
            <li><a href="#"><i className="fa fa-dashboard"></i> Home</a></li>
            <li><a href="#">Layout</a></li>
            <li className="active">Top Navigation</li>
          </ol>
           */}
        </section>
        {/* Main content */}
        <section className="content">
          <div className="box box-default box-content">
            <div className={"box-body box-body-content " + (this.props.noPadding ? "no-padding" : "")}>
              {this.props.children}
            </div>
            {/* /.box-body */}
          </div>
          {/* /.box */}
        </section>
        {/* /.content */}
      {/* /.container */}
      </div>
    )
  }
}

Container.propTypes = {
  header: PropTypes.string.isRequired,
  children: PropTypes.node.isRequired,
  buttonText: PropTypes.string,
  buttonLink: PropTypes.string,
  buttonIcon: PropTypes.string,
  noPadding: PropTypes.bool
}

export default Container;