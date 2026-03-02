-- ================================================
-- Caskfolio ERD Schema
-- ================================================

-- 1. User
CREATE TABLE users (
    id              SERIAL PRIMARY KEY,
    username        VARCHAR(150) NOT NULL UNIQUE,
    email           VARCHAR(254) NOT NULL UNIQUE,
    password        VARCHAR(128) NOT NULL,
    nickname        VARCHAR(50) NOT NULL UNIQUE,
    bio             VARCHAR(150) DEFAULT '',
    theme           VARCHAR(10) DEFAULT 'dark',
    note_default_public BOOLEAN DEFAULT TRUE,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at      TIMESTAMP NULL
);

-- 2. CaskType
CREATE TABLE cask_types (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    description TEXT DEFAULT ''
);

-- 3. Whisky
CREATE TABLE whiskies (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    distillery      VARCHAR(200) NOT NULL,
    style           VARCHAR(50) NOT NULL,
    region          VARCHAR(50) DEFAULT '',
    age             INTEGER NULL,
    abv             FLOAT NOT NULL,
    peat_level      INTEGER DEFAULT 0,

    description     TEXT NOT NULL,
    history         TEXT DEFAULT '',
    bartender_tip   TEXT DEFAULT '',
    pairing         TEXT DEFAULT '',
    serving_guide   JSONB DEFAULT '{}',
    -- {"neat": "...", "rocks": "...", "splash": "...", "soda": "..."}
    flavor_profile  JSONB DEFAULT '{}',
    -- {"smoky": 80, "sweet": 30, "fruity": 40, "woody": 60, "spicy": 50, "floral": 20}

    image           VARCHAR(255) DEFAULT '',
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- 4. Whisky-CaskType (M:N)
CREATE TABLE whisky_cask_types (
    id          SERIAL PRIMARY KEY,
    whisky_id   INTEGER NOT NULL REFERENCES whiskies(id) ON DELETE CASCADE,
    cask_type_id INTEGER NOT NULL REFERENCES cask_types(id) ON DELETE CASCADE,
    UNIQUE (whisky_id, cask_type_id)
);

-- 5. TastingNote
CREATE TABLE tasting_notes (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    whisky_id       INTEGER NOT NULL REFERENCES whiskies(id) ON DELETE CASCADE,

    tags            JSONB DEFAULT '[]',
    -- ["honey", "캠프파이어", "건포도"] 유저 자유입력 태그당 20자 / 최대 10개
    note            TEXT DEFAULT '',
    rating          DECIMAL(2,1) NOT NULL,
    -- 0.5 단위, 5.0 만점

    is_public       BOOLEAN DEFAULT TRUE,
    tasted_at       DATE NOT NULL DEFAULT CURRENT_DATE,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- 6. Collection (내 장식장 - 마셔본 것)
CREATE TABLE collections (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    whisky_id   INTEGER NOT NULL REFERENCES whiskies(id) ON DELETE CASCADE,
    added_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, whisky_id)
);

-- 7. Wishlist (위시리스트)
CREATE TABLE wishlists (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    whisky_id   INTEGER NOT NULL REFERENCES whiskies(id) ON DELETE CASCADE,
    added_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, whisky_id)
);

-- 8. ChatSession
CREATE TABLE chat_sessions (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

-- 9. ChatMessage
CREATE TABLE chat_messages (
    id          SERIAL PRIMARY KEY,
    session_id  INTEGER NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role        VARCHAR(10) NOT NULL CHECK (role IN ('user', 'assistant')),
    content     TEXT NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

-- 10. ChatMessage-Whisky (AI 추천 위스키 연결)
CREATE TABLE chat_message_whiskies (
    id              SERIAL PRIMARY KEY,
    chat_message_id INTEGER NOT NULL REFERENCES chat_messages(id) ON DELETE CASCADE,
    whisky_id       INTEGER NOT NULL REFERENCES whiskies(id) ON DELETE CASCADE,
    UNIQUE (chat_message_id, whisky_id)
);