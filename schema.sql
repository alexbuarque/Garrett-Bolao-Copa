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
-- Seed: 72 group stage matches (2026 FIFA World Cup — official schedule)
-- Times are UTC (source: official BRT schedule + 3h)
-- ============================================================
INSERT INTO matches (group_name, team_a, team_b, match_date, stage) VALUES
-- GROUP A
('A', 'México',           'África do Sul',      '2026-06-11 19:00:00+00', 'group'),
('A', 'Coreia do Sul',    'República Tcheca',   '2026-06-12 02:00:00+00', 'group'),
('A', 'República Tcheca', 'África do Sul',      '2026-06-18 16:00:00+00', 'group'),
('A', 'México',           'Coreia do Sul',      '2026-06-19 01:00:00+00', 'group'),
('A', 'República Tcheca', 'México',             '2026-06-25 01:00:00+00', 'group'),
('A', 'África do Sul',    'Coreia do Sul',      '2026-06-25 01:00:00+00', 'group'),
-- GROUP B
('B', 'Canadá',               'Bósnia e Herzegovina', '2026-06-12 19:00:00+00', 'group'),
('B', 'Catar',                'Suíça',                '2026-06-13 19:00:00+00', 'group'),
('B', 'Suíça',                'Bósnia e Herzegovina', '2026-06-18 19:00:00+00', 'group'),
('B', 'Canadá',               'Catar',                '2026-06-18 22:00:00+00', 'group'),
('B', 'Suíça',                'Canadá',               '2026-06-24 19:00:00+00', 'group'),
('B', 'Bósnia e Herzegovina', 'Catar',                '2026-06-24 19:00:00+00', 'group'),
-- GROUP C
('C', 'Brasil',   'Marrocos', '2026-06-13 22:00:00+00', 'group'),
('C', 'Haiti',    'Escócia',  '2026-06-14 01:00:00+00', 'group'),
('C', 'Escócia',  'Marrocos', '2026-06-19 22:00:00+00', 'group'),
('C', 'Brasil',   'Haiti',    '2026-06-20 00:30:00+00', 'group'),
('C', 'Escócia',  'Brasil',   '2026-06-24 22:00:00+00', 'group'),
('C', 'Marrocos', 'Haiti',    '2026-06-24 22:00:00+00', 'group'),
-- GROUP D
('D', 'Estados Unidos', 'Paraguai',  '2026-06-13 01:00:00+00', 'group'),
('D', 'Austrália',      'Turquia',   '2026-06-14 04:00:00+00', 'group'),
('D', 'Estados Unidos', 'Austrália', '2026-06-19 19:00:00+00', 'group'),
('D', 'Turquia',        'Paraguai',  '2026-06-20 11:00:00+00', 'group'),
('D', 'Turquia',        'Estados Unidos', '2026-06-26 02:00:00+00', 'group'),
('D', 'Paraguai',       'Austrália', '2026-06-26 02:00:00+00', 'group'),
-- GROUP E
('E', 'Alemanha',        'Curaçau',          '2026-06-14 17:00:00+00', 'group'),
('E', 'Costa do Marfim', 'Equador',          '2026-06-14 23:00:00+00', 'group'),
('E', 'Alemanha',        'Costa do Marfim',  '2026-06-20 20:00:00+00', 'group'),
('E', 'Equador',         'Curaçau',          '2026-06-21 00:00:00+00', 'group'),
('E', 'Equador',         'Alemanha',         '2026-06-25 20:00:00+00', 'group'),
('E', 'Curaçau',         'Costa do Marfim',  '2026-06-25 20:00:00+00', 'group'),
-- GROUP F
('F', 'Holanda', 'Japão',   '2026-06-14 20:00:00+00', 'group'),
('F', 'Suécia',  'Tunísia', '2026-06-15 02:00:00+00', 'group'),
('F', 'Holanda', 'Suécia',  '2026-06-20 17:00:00+00', 'group'),
('F', 'Tunísia', 'Japão',   '2026-06-21 04:00:00+00', 'group'),
('F', 'Japão',   'Suécia',  '2026-06-25 23:00:00+00', 'group'),
('F', 'Tunísia', 'Holanda', '2026-06-25 23:00:00+00', 'group'),
-- GROUP G
('G', 'Bélgica',      'Egito',        '2026-06-15 19:00:00+00', 'group'),
('G', 'Irã',          'Nova Zelândia','2026-06-16 01:00:00+00', 'group'),
('G', 'Bélgica',      'Irã',          '2026-06-21 19:00:00+00', 'group'),
('G', 'Nova Zelândia','Egito',         '2026-06-22 01:00:00+00', 'group'),
('G', 'Egito',        'Irã',          '2026-06-27 11:00:00+00', 'group'),
('G', 'Nova Zelândia','Bélgica',       '2026-06-27 11:00:00+00', 'group'),
-- GROUP H
('H', 'Espanha',        'Cabo Verde',     '2026-06-15 16:00:00+00', 'group'),
('H', 'Arábia Saudita', 'Uruguai',        '2026-06-15 22:00:00+00', 'group'),
('H', 'Espanha',        'Arábia Saudita', '2026-06-21 16:00:00+00', 'group'),
('H', 'Uruguai',        'Cabo Verde',     '2026-06-21 22:00:00+00', 'group'),
('H', 'Cabo Verde',     'Arábia Saudita', '2026-06-27 00:00:00+00', 'group'),
('H', 'Uruguai',        'Espanha',        '2026-06-27 00:00:00+00', 'group'),
-- GROUP I
('I', 'França',  'Senegal', '2026-06-16 19:00:00+00', 'group'),
('I', 'Iraque',  'Noruega', '2026-06-16 22:00:00+00', 'group'),
('I', 'França',  'Iraque',  '2026-06-22 21:00:00+00', 'group'),
('I', 'Noruega', 'Senegal', '2026-06-23 00:00:00+00', 'group'),
('I', 'Noruega', 'França',  '2026-06-26 19:00:00+00', 'group'),
('I', 'Senegal', 'Iraque',  '2026-06-26 19:00:00+00', 'group'),
-- GROUP J
('J', 'Argentina', 'Argélia',  '2026-06-17 01:00:00+00', 'group'),
('J', 'Áustria',   'Jordânia', '2026-06-17 04:00:00+00', 'group'),
('J', 'Argentina', 'Áustria',  '2026-06-22 17:00:00+00', 'group'),
('J', 'Jordânia',  'Argélia',  '2026-06-23 11:00:00+00', 'group'),
('J', 'Argélia',   'Áustria',  '2026-06-28 02:00:00+00', 'group'),
('J', 'Jordânia',  'Argentina','2026-06-28 02:00:00+00', 'group'),
-- GROUP K
('K', 'Portugal',      'R. D. do Congo', '2026-06-17 17:00:00+00', 'group'),
('K', 'Uzbequistão',   'Colômbia',       '2026-06-18 02:00:00+00', 'group'),
('K', 'Portugal',      'Uzbequistão',    '2026-06-23 17:00:00+00', 'group'),
('K', 'Colômbia',      'R. D. do Congo', '2026-06-24 02:00:00+00', 'group'),
('K', 'Colômbia',      'Portugal',       '2026-06-27 23:30:00+00', 'group'),
('K', 'R. D. do Congo','Uzbequistão',    '2026-06-27 23:30:00+00', 'group'),
-- GROUP L
('L', 'Inglaterra', 'Croácia', '2026-06-17 20:00:00+00', 'group'),
('L', 'Gana',       'Panamá',  '2026-06-17 23:00:00+00', 'group'),
('L', 'Inglaterra', 'Gana',    '2026-06-23 20:00:00+00', 'group'),
('L', 'Panamá',     'Croácia', '2026-06-23 23:00:00+00', 'group'),
('L', 'Panamá',     'Inglaterra','2026-06-27 21:00:00+00', 'group'),
('L', 'Croácia',    'Gana',    '2026-06-27 21:00:00+00', 'group')
ON CONFLICT DO NOTHING;
