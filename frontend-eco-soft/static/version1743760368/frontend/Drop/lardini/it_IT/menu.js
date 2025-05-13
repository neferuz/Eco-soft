document.addEventListener('DOMContentLoaded', function() {
    // Функция для создания HTML структуры меню
    function createMenuHTML(categories) {
        let html = '';
        
        // Добавляем статические пункты меню
        html += `
            <li class="main-menu__item">
                <a href="ecosofttextile.comnew-in.html" class="main-menu__link" data-menu="menu-927">About Us</a>
            </li>
            <li class="main-menu__item">
                <a href="./contacts.html" class="main-menu__link" data-menu="menu-927">Contacts</a>
            </li>
        `;

        // Добавляем динамические категории
        for (const [gender, items] of Object.entries(categories)) {
            if (items.length > 0) {
                html += `
                    <li class="main-menu__item main-menu__item--parent">
                        <a href="javascript:void(0);" class="main-menu__link" data-menu="menu-${gender}">${gender.charAt(0).toUpperCase() + gender.slice(1)}</a>
                        <div class="submenu-wrapper">
                            <ul class="main-menu__inner-list main-menu__inner-list--level1 custom_url" data-menu="menu-${gender}">
                                <li class="main-menu__inner-item main-menu__inner-item--level1 wrapper main-menu__inner-item--parent">
                                    <div class="submenu-wrapper">
                                        <ul class="main-menu__inner-list main-menu__inner-list--level2 wrapper">
                `;

                items.forEach(item => {
                    html += `
                        <li class="main-menu__inner-item main-menu__inner-item--level2 category main-menu__inner-item--parent">
                            <a href="${item.link || '#'}" class="main-menu__inner-link">${item.name}</a>
                            ${item.subcategories && item.subcategories.length > 0 ? `
                                <div class="submenu-wrapper">
                                    <ul class="main-menu__inner-list main-menu__inner-list--level3 category">
                                        ${item.subcategories.map(sub => `
                                            <li class="main-menu__inner-item main-menu__inner-item--level3 category">
                                                <a href="${sub.link || '#'}" class="main-menu__inner-link">${sub.name}</a>
                                            </li>
                                        `).join('')}
                                    </ul>
                                </div>
                            ` : ''}
                        </li>
                    `;
                });

                html += `
                                        </ul>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </li>
                `;
            }
        }

        return html;
    }

    // Функция для загрузки данных меню
    function loadMenu() {
        fetch('/api/categories/')
            .then(response => response.json())
            .then(data => {
                const menuList = document.querySelector('.main-menu__list');
                if (menuList) {
                    menuList.innerHTML = createMenuHTML(data);
                }
            })
            .catch(error => console.error('Error loading menu:', error));
    }

    // Загружаем меню при загрузке страницы
    loadMenu();
});