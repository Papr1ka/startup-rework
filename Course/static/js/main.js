function toggleDropdown(event) {
    let dropdown = document.getElementById("dd-account")
    if (dropdown != null) {
        dropdown.classList.toggle("visible")
    }
}

let accountButton = document.getElementById("btn-account")
if (accountButton != null) {
    accountButton.addEventListener("click", toggleDropdown)
}