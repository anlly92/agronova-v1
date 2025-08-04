const dropdown = document.querySelector(".dropdown");
const content = dropdown.querySelector(".dropdown-content");
dropdown.addEventListener("mouseover", () => {
    content.style.display = "block";
});
dropdown.addEventListener("mouseleave", () => {
    content.style.display = "none";
});
