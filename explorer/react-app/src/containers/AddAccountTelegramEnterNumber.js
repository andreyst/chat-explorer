import { connect } from 'react-redux'
import { addAccount } from '../actions'
import AddAccountTelegramEnterNumber from '../components/AddAccountTelegramEnterNumber'
 
const mapStateToProps = state => {
  return {
    accounts: state.accounts
  }
}
 
const mapDispatchToProps = dispatch => {
  return {
    onAddAccountClick: number => dispatch(addAccount(number)),
    dispatch
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(AddAccountTelegramEnterNumber)
