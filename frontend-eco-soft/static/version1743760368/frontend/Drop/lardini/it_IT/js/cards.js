document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/cards/')
        .then(response => response.json())
        .then(data => {
            const container = document.querySelector('.carousel-track-inner');
            if (container) {
                container.innerHTML = data.cards.map(card => `
                    <div class="item-card">
                        <a href="${card.link}" target="_blank">
                            <img src="http://127.0.0.1:8000${card.image}" alt="${card.title}" class="item-image">
                            <h3>${card.title}</h3>
                        </a>
                    </div>
                `).join('');
            }
        });
});