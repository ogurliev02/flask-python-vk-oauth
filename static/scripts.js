function logout() {
  var date = new Date;
  date.setDate(date.getDate() - 1);
  document.cookie = 'user_id=; expires=' + date.toUTCString();
  location.reload();
}