document.addEventListener('DOMContentLoaded', function () {
  
// Password toggle JavaScript code
const passwordInput = document.getElementById("password");
const togglePassword = document.getElementById("togglePassword");

togglePassword.addEventListener("click", function () {
  const type =
    passwordInput.getAttribute("type") === "password" ? "text" : "password";
  passwordInput.setAttribute("type", type);
});

// switches the images upon toggle
const image = document.getElementById("eye-image");
const imageSources = [
  "../static/SVG/eyehidden.svg",
  "../static/SVG/eyeshow.svg",
];
let currentIndex = 0;

function toggleImage() {
  currentIndex = (currentIndex + 1) % 2;
  image.src = imageSources[currentIndex];
}

// Password toggle JavaScript code (confirm)
const passwordInputConfirm = document.getElementById("password-confirm");
const togglePasswordConfirm = document.getElementById("togglePassword-confirm");

togglePasswordConfirm.addEventListener("click", function () {
  const type =
    passwordInputConfirm.getAttribute("type") === "password"
      ? "text"
      : "password";
  passwordInputConfirm.setAttribute("type", type);
});

// switches the images upon toggle (confirm)
const imageConfirm = document.getElementById("eye-image-confirm");
const imageSourcesConfirm = [
  "../static/SVG/eyehidden.svg",
  "../static/SVG/eyeshow.svg",
];
let currentIndexConfirm = 0;

function toggleImageConfirm() {
  currentIndexConfirm = (currentIndexConfirm + 1) % 2;
  imageConfirm.src = imageSourcesConfirm[currentIndexConfirm];
}

// signup button
var checkbox = document.getElementById("terms-checkbox");
var proceedButton = document.getElementById("signup-button");

checkbox.addEventListener("change", function () {
  proceedButton.disabled = !checkbox.checked;
});


});