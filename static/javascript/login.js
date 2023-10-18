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
