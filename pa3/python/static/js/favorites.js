function Favorites(numElement, userElement, favoriteButton, picid, numFavorites, latestUser) {
  this.numElement = numElement;
  this.userElement = userElement;
  this.picid = picid;
  this.numFavorites = numFavorites;
  this.latestUser = latestUser;
  this.favoriteButton = favoriteButton
  numElement.innerHTML = numFavorites; // objects in Javascript are assigned by reference, so this works
  userElement.innerHTML = latestUser;
  favoriteButton.addEventListener("click", this, false);
}