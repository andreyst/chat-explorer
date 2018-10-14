import get from '../get';
import post from '../post';

export const deleteAccount = id => {
  return {
    type: 'DELETE_ACCOUNT',
    id
  }
}

export function fetchAccounts() {
  return async (dispatch) => {
    dispatch({
      type: 'FETCH_ACCOUNTS'
    });

    try {
      const result = await get("accounts")

      dispatch({
        type: 'FETCH_ACCOUNTS_SUCCESS',
        accounts: result.accounts
      })
    } catch (err) {
      dispatch({
        type: 'FETCH_ACCOUNTS_ERROR',
        err: err
      })
    }
  }
}

export function addAccount(accountNumber) {
  return async (dispatch) => {
    dispatch({
      type: 'ADD_ACCOUNT'
    });

    try {
      const result = await post("accounts/add", { accountNumber })

      dispatch({
        type: 'ADD_ACCOUNT_SUCCESS',
        accounts: result.accounts,
      })
    } catch (err) {
      dispatch({
        type: 'ADD_ACCOUNT_ERROR',
        err: err,
      })
    }
  }
}