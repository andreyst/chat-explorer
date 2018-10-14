class AccountHelper {
  static getIcon(accountType) {
    switch(accountType) {
      case 1:
        return "fa-telegram";
      case 2:
        return "fa-slack";
      case 3:
        return "fa-facebook";
      case 4:
        return "fa-vk";
      default:
        return "fa-question";
    }
  }
}

export default AccountHelper;
