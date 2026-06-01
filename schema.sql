-- ============================================================
-- Bolão da Copa 2026 - Supabase Schema
-- Execute este script no SQL Editor do Supabase
-- ============================================================

-- Profiles
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    nickname TEXT NOT NULL UNIQUE,
    department TEXT,
    shift TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Run these if the table already exists (first deploy upgrade):
-- ALTER TABLE profiles ADD COLUMN IF NOT EXISTS department TEXT;
-- ALTER TABLE profiles ADD COLUMN IF NOT EXISTS shift TEXT;

-- Matches (group stage)
CREATE TABLE IF NOT EXISTS matches (
    id SERIAL PRIMARY KEY,
    group_name TEXT NOT NULL,
    team_a TEXT NOT NULL,
    team_b TEXT NOT NULL,
    match_date TIMESTAMPTZ NOT NULL,
    stage TEXT NOT NULL DEFAULT 'group',
    result_a INTEGER,
    result_b INTEGER,
    finished BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Predictions per user per match
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    match_id INTEGER NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
    pred_a INTEGER NOT NULL,
    pred_b INTEGER NOT NULL,
    points INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, match_id)
);

-- Special predictions (artilheiro, MVP, goleiro) per user
CREATE TABLE IF NOT EXISTS special_predictions (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE UNIQUE,
    artilheiro TEXT DEFAULT '',
    mvp TEXT DEFAULT '',
    goleiro TEXT DEFAULT '',
    points INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Special results (single row, admin fills in)
CREATE TABLE IF NOT EXISTS special_results (
    id INTEGER PRIMARY KEY DEFAULT 1,
    artilheiro TEXT DEFAULT '',
    mvp TEXT DEFAULT '',
    goleiro TEXT DEFAULT '',
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT single_row CHECK (id = 1)
);

INSERT INTO special_results (id) VALUES (1) ON CONFLICT DO NOTHING;

-- ============================================================
-- Seed: 72 group stage matches (2026 FIFA World Cup)
-- Teams are confirmed qualifiers; exact groupings are approximate.
-- ============================================================
INSERT INTO matches (group_name, team_a, team_b, match_date, stage) VALUES
-- GROUP A
('A', 'USA', 'El Salvador',    '2026-06-11 13:00:00+00', 'group'),
('A', 'Polônia', 'Austrália',  '2026-06-11 16:00:00+00', 'group'),
('A', 'USA', 'Polônia',        '2026-06-17 13:00:00+00', 'group'),
('A', 'El Salvador', 'Austrália', '2026-06-17 16:00:00+00', 'group'),
('A', 'USA', 'Austrália',      '2026-06-24 18:00:00+00', 'group'),
('A', 'El Salvador', 'Polônia','2026-06-24 18:00:00+00', 'group'),
-- GROUP B
('B', 'México', 'Jamaica',     '2026-06-11 19:00:00+00', 'group'),
('B', 'Sérvia', 'Argélia',     '2026-06-11 22:00:00+00', 'group'),
('B', 'México', 'Sérvia',      '2026-06-17 19:00:00+00', 'group'),
('B', 'Jamaica', 'Argélia',    '2026-06-17 22:00:00+00', 'group'),
('B', 'México', 'Argélia',     '2026-06-24 21:00:00+00', 'group'),
('B', 'Jamaica', 'Sérvia',     '2026-06-24 21:00:00+00', 'group'),
-- GROUP C
('C', 'Canadá', 'Honduras',       '2026-06-12 13:00:00+00', 'group'),
('C', 'Croácia', 'Costa do Marfim','2026-06-12 16:00:00+00', 'group'),
('C', 'Canadá', 'Croácia',        '2026-06-18 13:00:00+00', 'group'),
('C', 'Honduras', 'Costa do Marfim','2026-06-18 16:00:00+00', 'group'),
('C', 'Canadá', 'Costa do Marfim','2026-06-25 18:00:00+00', 'group'),
('C', 'Honduras', 'Croácia',      '2026-06-25 18:00:00+00', 'group'),
-- GROUP D
('D', 'Argentina', 'Panamá',   '2026-06-12 19:00:00+00', 'group'),
('D', 'Turquia', 'Japão',       '2026-06-12 22:00:00+00', 'group'),
('D', 'Argentina', 'Turquia',   '2026-06-18 19:00:00+00', 'group'),
('D', 'Panamá', 'Japão',        '2026-06-18 22:00:00+00', 'group'),
('D', 'Argentina', 'Japão',     '2026-06-25 21:00:00+00', 'group'),
('D', 'Panamá', 'Turquia',      '2026-06-25 21:00:00+00', 'group'),
-- GROUP E
('E', 'Brasil', 'Trindade e Tobago', '2026-06-13 13:00:00+00', 'group'),
('E', 'Holanda', 'Marrocos',         '2026-06-13 16:00:00+00', 'group'),
('E', 'Brasil', 'Holanda',           '2026-06-19 13:00:00+00', 'group'),
('E', 'Trindade e Tobago', 'Marrocos','2026-06-19 16:00:00+00', 'group'),
('E', 'Brasil', 'Marrocos',          '2026-06-26 18:00:00+00', 'group'),
('E', 'Trindade e Tobago', 'Holanda','2026-06-26 18:00:00+00', 'group'),
-- GROUP F
('F', 'Colômbia', 'Costa Rica', '2026-06-13 19:00:00+00', 'group'),
('F', 'Bélgica', 'Coreia do Sul','2026-06-13 22:00:00+00', 'group'),
('F', 'Colômbia', 'Bélgica',    '2026-06-19 19:00:00+00', 'group'),
('F', 'Costa Rica', 'Coreia do Sul','2026-06-19 22:00:00+00', 'group'),
('F', 'Colômbia', 'Coreia do Sul','2026-06-26 21:00:00+00', 'group'),
('F', 'Costa Rica', 'Bélgica',  '2026-06-26 21:00:00+00', 'group'),
-- GROUP G
('G', 'Uruguai', 'Nova Zelândia', '2026-06-14 13:00:00+00', 'group'),
('G', 'Alemanha', 'Nigéria',      '2026-06-14 16:00:00+00', 'group'),
('G', 'Uruguai', 'Alemanha',      '2026-06-20 13:00:00+00', 'group'),
('G', 'Nova Zelândia', 'Nigéria', '2026-06-20 16:00:00+00', 'group'),
('G', 'Uruguai', 'Nigéria',       '2026-06-27 18:00:00+00', 'group'),
('G', 'Nova Zelândia', 'Alemanha','2026-06-27 18:00:00+00', 'group'),
-- GROUP H
('H', 'Equador', 'Portugal',  '2026-06-14 19:00:00+00', 'group'),
('H', 'Irã', 'Senegal',       '2026-06-14 22:00:00+00', 'group'),
('H', 'Equador', 'Irã',       '2026-06-20 19:00:00+00', 'group'),
('H', 'Portugal', 'Senegal',  '2026-06-20 22:00:00+00', 'group'),
('H', 'Equador', 'Senegal',   '2026-06-27 21:00:00+00', 'group'),
('H', 'Irã', 'Portugal',      '2026-06-27 21:00:00+00', 'group'),
-- GROUP I
('I', 'Chile', 'França',          '2026-06-15 13:00:00+00', 'group'),
('I', 'Arábia Saudita', 'Egito',  '2026-06-15 16:00:00+00', 'group'),
('I', 'Chile', 'Arábia Saudita',  '2026-06-21 13:00:00+00', 'group'),
('I', 'França', 'Egito',          '2026-06-21 16:00:00+00', 'group'),
('I', 'Chile', 'Egito',           '2026-06-28 18:00:00+00', 'group'),
('I', 'França', 'Arábia Saudita', '2026-06-28 18:00:00+00', 'group'),
-- GROUP J
('J', 'Paraguai', 'Inglaterra', '2026-06-15 19:00:00+00', 'group'),
('J', 'Catar', 'Camarões',      '2026-06-15 22:00:00+00', 'group'),
('J', 'Paraguai', 'Catar',      '2026-06-21 19:00:00+00', 'group'),
('J', 'Inglaterra', 'Camarões', '2026-06-21 22:00:00+00', 'group'),
('J', 'Paraguai', 'Camarões',   '2026-06-28 21:00:00+00', 'group'),
('J', 'Catar', 'Inglaterra',    '2026-06-28 21:00:00+00', 'group'),
-- GROUP K
('K', 'Venezuela', 'Espanha',  '2026-06-16 13:00:00+00', 'group'),
('K', 'Iraque', 'Mali',        '2026-06-16 16:00:00+00', 'group'),
('K', 'Venezuela', 'Iraque',   '2026-06-22 13:00:00+00', 'group'),
('K', 'Espanha', 'Mali',       '2026-06-22 16:00:00+00', 'group'),
('K', 'Venezuela', 'Mali',     '2026-06-29 18:00:00+00', 'group'),
('K', 'Iraque', 'Espanha',     '2026-06-29 18:00:00+00', 'group'),
-- GROUP L
('L', 'Itália', 'Suíça',          '2026-06-16 19:00:00+00', 'group'),
('L', 'Uzbequistão', 'África do Sul','2026-06-16 22:00:00+00', 'group'),
('L', 'Itália', 'Uzbequistão',    '2026-06-22 19:00:00+00', 'group'),
('L', 'Suíça', 'África do Sul',   '2026-06-22 22:00:00+00', 'group'),
('L', 'Itália', 'África do Sul',  '2026-06-29 21:00:00+00', 'group'),
('L', 'Suíça', 'Uzbequistão',     '2026-06-29 21:00:00+00', 'group')
ON CONFLICT DO NOTHING;
