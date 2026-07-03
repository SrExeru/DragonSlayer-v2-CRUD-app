function showMenu () {
    let menu = document.getElementById('nav_options');
    let btn_open = document.getElementById('btn_menu_open');
    let btn_close = document.getElementById('btn_menu_close');

    menu.classList.toggle('hide_menu');
    menu.setAttribute('aria-expanded', menu.getAttribute('aria-expanded') !== 'true');

    btn_open.classList.toggle('hide_btn');
    btn_close.classList.toggle('hide_btn');
}

document.addEventListener('click', function(event) {
    let header = document.querySelector('header')
    let menu = document.getElementById('nav_options');
    if (!menu.classList.contains('hide_menu')) {
        let btn_open = document.getElementById('btn_menu_open');
        let btn_close = document.getElementById('btn_menu_close');

        if (!header.contains(event.target)) {
            menu.classList.add('hide_menu');
            menu.ariaExpanded = false

            btn_open.classList.add('hide_btn');
            btn_close.classList.remove('hide_btn');
        }
    };
});