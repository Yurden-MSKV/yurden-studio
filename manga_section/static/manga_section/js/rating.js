function initRatingSystem(config) {
    console.log('Initializing rating for chapter:', config.chapterId);

    const chapterItem = document.querySelector(`.chapter_block[data-chapter-id="${config.chapterId}"]`);
    if (!chapterItem) {
        console.error('Chapter item not found:', config.chapterId);
        return;
    }

    const likeBtn = chapterItem.querySelector('.like-btn');
    const dislikeBtn = chapterItem.querySelector('.dislike-btn');
    const likeCount = chapterItem.querySelector('.like-btn .count');
    const dislikeCount = chapterItem.querySelector('.dislike-btn .count');
    const likeBar = chapterItem.querySelector('.like-bar');
    const dislikeBar = chapterItem.querySelector('.dislike-bar');
    const likePercentage = chapterItem.querySelector('.like-bar .percentage-text');
    const dislikePercentage = chapterItem.querySelector('.dislike-bar .percentage-text');

    if (!likeBtn || !dislikeBtn) {
        console.error('Buttons not found for chapter:', config.chapterId);
        return;
    }

    console.log('Elements found, setting up event listeners...');

    function sendVote(action) {
        console.log('Sending vote:', action, 'for chapter:', config.chapterId);

        fetch(config.url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': config.csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({ action: action })
        })
        .then(response => {
            console.log('Response status:', response.status);
            if (response.status === 403) {
                throw new Error('Необходима авторизация');
            }
            if (!response.ok) {
                throw new Error('HTTP error ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            console.log('Response data:', data);

            // Обновляем счетчики
            if (likeCount) likeCount.textContent = data.like_count;
            if (dislikeCount) dislikeCount.textContent = data.dislike_count;

            // Обновляем проценты
            if (likeBar) likeBar.style.width = data.like_percentage + '%';
            if (dislikeBar) dislikeBar.style.width = data.dislike_percentage + '%';
            if (likePercentage) likePercentage.textContent = data.like_percentage + '%';
            if (dislikePercentage) dislikePercentage.textContent = data.dislike_percentage + '%';

            // Обновляем стили кнопок
            updateButtonStyle(likeBtn, data.user_reaction === true);
            updateButtonStyle(dislikeBtn, data.user_reaction === false);
        })
        .catch(error => {
            console.error('Error:', error);
            if (error.message === 'Необходима авторизация') {
                alert('Чтобы оценить главу, необходимо войти в систему.');
            } else {
                alert('Произошла ошибка: ' + error.message);
            }
        });
    }

    function updateButtonStyle(button, isActive) {
        if (isActive) {
            button.classList.add('active');
        } else {
            button.classList.remove('active');
        }
    }

    // Вешаем обработчики
    likeBtn.addEventListener('click', function(e) {
        e.preventDefault();
        sendVote('like');
    });

    dislikeBtn.addEventListener('click', function(e) {
        e.preventDefault();
        sendVote('dislike');
    });

    console.log('Event listeners set up for chapter:', config.chapterId);
}