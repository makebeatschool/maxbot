PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;
-- дефолт для юзеров
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    chat_id INTEGER NOT NULL,
    first_name TEXT,
    last_name TEXT,
    username TEXT,
    role TEXT DEFAULT 'user'
);
-- таблица для уведомлений о пробном 
CREATE TABLE IF NOT EXISTS trial_reminders (
    user_id INTEGER PRIMARY KEY,
    send_time TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
-- таблица с телефонами поьзователей
CREATE TABLE IF NOT EXISTS users_phone (
    user_id INTEGER PRIMARY KEY,
    phone TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
-- таблица для уведомления о переодичном уроке
CREATE TABLE IF NOT EXISTS user_lessons (
    user_id INTEGER PRIMARY KEY,
    lesson_date TEXT DEFAULT 'None-None',
    next_message_time TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);