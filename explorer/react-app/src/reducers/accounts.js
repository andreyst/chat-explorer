// const defaultAccounts = [
//   { id: 1, name: "+79312010222", type: 'telegram' },
//   { id: 2, name: "+11111111111", type: 'slack' },
//   { id: 3, name: "+22222222222", type: 'facebook' },
//   { id: 4, name: "+33333333333", type: 'vk' },
// ]
const defaultAccounts = {
  isFetching: false,
  isError: false,
  isAddingAccount: false,
  isAccountAdded: false,
  isAddAccountError: false,
  addAccountError: null,
  didInvalidate: true,
  items: []
}

const accounts = (state = defaultAccounts, action) => {
  switch (action.type) {
    case 'FETCH_ACCOUNTS':
      return Object.assign({}, state, {
        isFetching: true,
        isError: false,
        didInvalidate: false,
      });
    case 'FETCH_ACCOUNTS_SUCCESS':
      return Object.assign({}, state, {
        isFetching: false,
        items: action.accounts
      });
    case 'FETCH_ACCOUNTS_ERROR':
      return Object.assign({}, state, {
        isFetching: false,
        isError: true,
      });
    case 'START_ADD_ACCOUNT':
      return Object.assign({}, state, {
        isAddingAccount: false,
        isAccountAdded: false,
        addAccountError: null,
      });
    case 'ADD_ACCOUNT':
      return Object.assign({}, state, {
        isAddingAccount: true,
      });
    case 'ADD_ACCOUNT_SUCCESS':
      return Object.assign({}, state, {
        isAddingAccount: false,
        isAccountAdded: true,
        addedAccountId: action.id,
        items: [
          ...state.items,
          {
            id: action.id,
            name: action.name,
            messenger_type: action.messenger_type,
          }
        ]
      });
    case 'ADD_ACCOUNT_ERROR':
      return Object.assign({}, state, {
        isAddingAccount: false,
        isAddAccountError: true,
        addAccountError: action,
      });
    case 'DELETE_ACCOUNT':
      return Object.assign({}, state, {
          items: state.items.filter(account => account.id !== action.id)
        })
    default:
      return state
  }
}

export default accounts;