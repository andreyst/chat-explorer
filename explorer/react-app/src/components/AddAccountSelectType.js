import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Container from '../Container';
import AccountHelper from '../AccountHelper';

class AddAccountSelectType extends Component {
  render() {
    const accountTypes = [
      { name: "Facebook", "slug": "facebook" },
      { name: "Slack",    "slug": "slack"    },
      { name: "VK",       "slug": "vk"       },
      { name: "Telegram", "slug": "telegram" },
    ];

    return (
      <Container header="Select account type">
        <div className="account-type-picker">
          {accountTypes.map(accountType =>
            <Link key={accountType.slug} to={this.props.match.url + "/" + accountType.slug} className="btn btn-app account-type-picker-button">
              <i className={"fa " + AccountHelper.getIcon(accountType.slug)}></i> {accountType.name}
            </Link>
          )}
        </div>
      </Container>
    )
  }
}

export default AddAccountSelectType;