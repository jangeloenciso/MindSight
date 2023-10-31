const adminMainMenu = document.getElementById("admin-main-menu");
const expandImage = document.getElementById("expand-img");
const adminLinks = document.querySelectorAll(".admin-container a");
const sidebar = document.querySelector(".sidebar");

// Track the toggle state
let isToggled = false;

// Function to reset the image rotation to 0 degrees
function resetImage() {
  expandImage.style.transform = "rotate(0deg)";
}

// Hide admin links and reset the image when the page loads
adminLinks.forEach((link) => {
  link.style.display = "none";
  resetImage();
});

// Click event handler for the admin main menu
adminMainMenu.addEventListener("click", function () {
  // Toggle the visibility of admin links and rotate the image
  adminLinks.forEach((link) => {
    if (link.style.display === "block" || link.style.display === "") {
      link.style.display = "none";
      resetImage(); // Reset the image rotation to 0 degrees
      isToggled = false;
    } else {
      link.style.display = "block";
      expandImage.style.transform = "rotate(-90deg)";
      isToggled = true;
    }
  });
});

// Hide admin links and reset the image when the mouse leaves the sidebar
sidebar.addEventListener("mouseleave", function () {
  if (isToggled) {
    // Update the flag only if it's currently toggled open
    adminLinks.forEach((link) => {
      link.style.display = "none";
      resetImage();
    });
    isToggled = false; // Update the flag to reflect the change
  }
});
