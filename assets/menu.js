document.getElementsByTagName("body").item(0).addEventListener("click", removeAllShowMenu);

function removeAllShowMenu(except) {
    const all_boxes = document.getElementsByClassName("dropdown-menu");
    for (const box of all_boxes) {
        if (box !== except){
            box.classList.remove("show");
        }
    }
}

const header = document.getElementsByClassName("dropdown-toggle");
for (const item of header) {
    const show_box = item.nextElementSibling;
    item.addEventListener("click", x => {
        removeAllShowMenu(show_box);
        show_box.classList.toggle("show");
        x.stopPropagation();
    });
}

const toggler = document.getElementById("navbar-toggler");
toggler.addEventListener("click", x => {
    const navbar = document.getElementById("sp-navbar");
    navbar.classList.toggle("show");
});

