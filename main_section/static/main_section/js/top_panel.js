// function toggleMenu() {
//     const menu = document.getElementById('userMenu');
//     menu.classList.toggle('show');
// }
//
// // Закрытие меню при клике вне его области
// document.addEventListener('click', function(event) {
//     const menu = document.getElementById('userMenu');
//     const button = document.querySelector('.user-button');
//
//     if (!menu.contains(event.target) && !button.contains(event.target)) {
//         menu.classList.remove('show');
//     }
// });
//
// // Обработка действий меню
// function handleAction(action) {
//     console.log('Выбрано действие:', action);
//
//     // Скрываем меню после выбора
//     document.getElementById('userMenu').classList.remove('show');
//
//     // Выполняем действие
//     switch(action) {
//         case 'profile':
//             window.location.href = '/profile';
//             break;
//         case 'settings':
//             window.location.href = '/settings';
//             break;
//         case 'logout':
//             // Здесь может быть запрос на сервер для выхода
//             alert('Выход из системы');
//             break;
//     }
// }