import { connect } from 'react-redux'
import { deleteAccount } from '../actions'
import AccountList from '../components/AccountList'
 
const mapStateToProps = state => {
  return {
    accounts: state.accounts
  }
}
 
const mapDispatchToProps = dispatch => {
  return {
    onDeleteAccountClick: id => dispatch(deleteAccount(id)),
    dispatch
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(AccountList)
