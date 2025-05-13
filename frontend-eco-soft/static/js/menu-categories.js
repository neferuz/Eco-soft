document.addEventListener('DOMContentLoaded', function() {
    fetch('http://127.0.0.1:8001/api/menu-categories/')
        .then(response => response.json())
        .then(data => {
            // Десктопное меню
            const menuList = document.getElementById('menu-categories-list');
            menuList.innerHTML = '';
            
            // Мобильное меню
            const mobileMenuList = document.getElementById('mobile-menu-categories-list');
            mobileMenuList.innerHTML = '';

            data.categories.forEach(category => {
                // --- Десктоп ---
                const li = document.createElement('li');
                li.className = 'hermes-menu__item';
                
                // Создаем основную ссылку категории
                const mainLink = document.createElement('a');
                mainLink.href = `/shop.html?category=${category.id}`;
                mainLink.className = 'hermes-menu__link';
                mainLink.textContent = category.name;
                
                li.appendChild(mainLink);

                // Добавляем подкатегории если они есть
                if (category.subcategories && category.subcategories.length > 0) {
                    const submenu = document.createElement('ul');
                    submenu.className = 'submenu';
                    
                    category.subcategories.forEach(sub => {
                        submenu.innerHTML += `
                            <li><a href="/shop.html?category=${category.id}&subcategory=${sub.id}">${sub.name}</a></li>
                        `;
                    });
                    
                    li.appendChild(submenu);
                }
                
                menuList.appendChild(li);

                // --- Мобильное ---
                const mli = document.createElement('li');
                mli.className = 'hermes-mobile-menu__item';
                
                if (category.subcategories && category.subcategories.length > 0) {
                    mli.innerHTML = `
                        <button class="hermes-mobile-btn">
                            ${category.name}
                            <span class="hermes-toggle">+</span>
                        </button>
                        <ul class="hermes-mobile-submenu">
                            <li><a href="/shop.html?category=${category.id}">${category.name}</a></li>
                            ${category.subcategories.map(sub => 
                                `<li><a href="/shop.html?category=${category.id}&subcategory=${sub.id}">${sub.name}</a></li>`
                            ).join('')}
                        </ul>
                    `;
                } else {
                    mli.innerHTML = `
                        <a href="/shop.html?category=${category.id}" class="hermes-mobile-btn">
                            ${category.name}
                        </a>
                    `;
                }
                
                mobileMenuList.appendChild(mli);
            });

            // Обработчики для мобильного меню
            document.querySelectorAll('.hermes-mobile-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    // Если это кнопка (не ссылка), то раскрываем подменю
                    if (this.tagName === 'BUTTON') {
                        const parent = this.parentElement;
                        parent.classList.toggle('open');
                    }
                });
            });
        });
});
