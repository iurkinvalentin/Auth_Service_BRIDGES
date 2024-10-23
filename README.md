# Django Message platform

## Тема проекта:
Платформа для обмена сообщениями в реальном времени 
Это приложение, которое позволяет пользователям отправлять сообщения, создавать группы, делиться файлами и получать уведомления в реальном времени.

# Архитектура проекта:

## Микросервисная архитектура:
- **Сервис аутентификации (accounts)**:
Отвечает за регистрацию, вход и управление профилями пользователей.
Использует JWT для обеспечения безопасности токенов доступа.

- **Сервис сообщений (messages)**:
Обрабатывает отправку и получение сообщений.
Хранит историю чатов и обеспечивает поиск по сообщениям.

- **Сервис групп (groups)**:
Управляет созданием и администрированием групповых чатов.
Позволяет добавлять и удалять участников групп.

- **Сервис уведомлений (notifications)**:
Отправляет push-уведомления пользователям о новых сообщениях или событиях.
Использует WebSockets или Django Channels для реализации реального времени.

- **Кэширование с помощью Redis**:
Сессии пользователей:
Хранение активных сессий для быстрого доступа и аутентификации.
Кэш популярных данных:
Кэширование часто запрашиваемых данных, таких как списки контактов или недавние чаты.
Механизм Pub/Sub:
Обеспечение коммуникации между сервисами в реальном времени через механизм публикации/подписки.

- **Коммуникация между микросервисами**:
REST API и gRPC:
Использование REST для простых запросов и gRPC для высокопроизводительной коммуникации.
Брокер сообщений (например, RabbitMQ или Kafka):
Асинхронная передача данных и событий между сервисами.

- **База данных**:
Отдельные базы данных для каждого сервиса:
Улучшает масштабируемость и независимость сервисов.
Использование PostgreSQL или MongoDB в зависимости от потребностей.

- **Frontend**:
Single Page Application (SPA):
Реализовано на React или Vue.js для динамичного взаимодействия с пользователем.

- **WebSockets/Django Channels**:
Обеспечение обновления интерфейса в реальном времени без перезагрузки страницы.

- **DevOps и развертывание**:
Контейнеризация с Docker:
Каждый микросервис упакован в отдельный контейнер для удобства развертывания.
Оркестрация с Kubernetes:
Управление контейнерами и их масштабирование в зависимости от нагрузки.
CI/CD:
Настроены автоматические процессы тестирования и развертывания с использованием инструментов, таких как Jenkins или GitHub Actions.
