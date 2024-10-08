# Аутентификации и управления пользователями, который является основой платформы обмена сообщениями в реальном времени.

- **auth_service** — это микросервис для аутентификации и управления пользователями, разработанный для платформы обмена сообщениями в реальном времени. Он предоставляет базовый функционал регистрации, входа в систему, управления профилями пользователей, а также работу с JWT-токенами для авторизации.

# Основные функции

## Регистрация пользователей

Вход в систему с использованием JWT (JSON Web Tokens)
Управление профилем пользователя (аватар, статус, онлайн/оффлайн состояние)
Хранение данных активности пользователя (последний визит, онлайн статус)
Поддержка системы контактов между пользователями

## Технологический стек

Django — веб-фреймворк для разработки приложения
Django REST Framework (DRF) — для создания REST API
Simple JWT — для управления JWT токенами (аутентификация)
PostgreSQL — для хранения данных пользователей и профилей
Docker — для контейнеризации микросервиса