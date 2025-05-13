// hermes-menu.js
document.addEventListener('DOMContentLoaded', function() {
    // Получаем данные меню
    fetch('/api/menu-categories/')
        .then(response => response.json())
        .then(data => {
            // Desktop menu
            const desktopMenu = document.getElementById('desktop-menu');
            if (desktopMenu) {
                desktopMenu.innerHTML = data.categories.map((cat, idx) => `
                    <li class="hermes-menu__item" data-idx="${idx}">
                        <button class="hermes-menu__link">${cat.name}</button>
                    </li>
                `).join('');
            }

            // Megamenu logic
            const megamenu = document.getElementById('megamenu');
            let megamenuTimeout;
            desktopMenu.querySelectorAll('.hermes-menu__item').forEach((item, idx) => {
                item.addEventListener('mouseenter', () => {
                    clearTimeout(megamenuTimeout);
                    showMegamenu(data.categories[idx]);
                    item.classList.add('active');
                });
                item.addEventListener('mouseleave', () => {
                    megamenuTimeout = setTimeout(hideMegamenu, 200);
                    item.classList.remove('active');
                });
            });
            megamenu.addEventListener('mouseenter', () => clearTimeout(megamenuTimeout));
            megamenu.addEventListener('mouseleave', hideMegamenu);

            function showMegamenu(category) {
                if (!category.subcategories.length) {
                    megamenu.classList.remove('open');
                    return;
                }
                megamenu.innerHTML = `
                    <div class="hermes-megamenu__content">
                        <div class="hermes-megamenu__col">
                            <div class="hermes-megamenu__col-title">${category.name}</div>
                            ${category.subcategories.map(sub => `
                                <a href="${sub.link || '#'}" class="hermes-megamenu__link">${sub.name}</a>
                            `).join('')}
                        </div>
                    </div>
                `;
                megamenu.classList.add('open');
            }
            function hideMegamenu() {
                megamenu.classList.remove('open');
            }

            // Mobile menu
            const mobileMenu = document.querySelector('.hermes-mobile-menu__list');
            if (mobileMenu) {
                mobileMenu.innerHTML = data.categories.map(cat => `
                    <li class="hermes-mobile-menu__item${cat.subcategories.length > 0 ? ' has-submenu' : ''}">
                        <a href="${cat.link || '#'}" class="hermes-mobile-menu__link">
                            ${cat.name}
                            ${cat.subcategories.length > 0 ? '<button class="submenu-toggle" aria-label="Open submenu">+</button>' : ''}
                        </a>
                        ${cat.subcategories.length > 0 ? `
                        <ul class="hermes-mobile-submenu">
                            ${cat.subcategories.map(sub => `
                                <li><a href="${sub.link || '#'}" class="hermes-mobile-menu__link">${sub.name}</a></li>
                            `).join('')}
                        </ul>
                        ` : ''}
                    </li>
                `).join('');

                // Toggle submenus
                mobileMenu.querySelectorAll('.submenu-toggle').forEach(btn => {
                    btn.addEventListener('click', function(e) {
                        e.preventDefault();
                        const item = btn.closest('.hermes-mobile-menu__item');
                        item.classList.toggle('open');
                    });
                });
            }
        });

    // Burger menu logic
    const burgerBtn = document.getElementById('burger-btn');
    const mobileMenuWrap = document.getElementById('mobile-menu');
    const closeMobileMenu = document.getElementById('close-mobile-menu');
    burgerBtn.addEventListener('click', () => {
        mobileMenuWrap.classList.add('open');
        document.body.style.overflow = 'hidden';
    });
    closeMobileMenu.addEventListener('click', () => {
        mobileMenuWrap.classList.remove('open');
        document.body.style.overflow = '';
    });
});