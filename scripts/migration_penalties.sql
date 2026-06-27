-- Migration: add penalty shootout fields to predictions and matches tables
-- Run this in the Supabase SQL editor before deploying the penalty feature.

-- Penalty prediction fields on predictions
ALTER TABLE predictions
  ADD COLUMN IF NOT EXISTS pred_penalties  BOOLEAN DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS pred_pen_a      SMALLINT,
  ADD COLUMN IF NOT EXISTS pred_pen_b      SMALLINT;

-- Penalty result fields on matches
ALTER TABLE matches
  ADD COLUMN IF NOT EXISTS result_penalties  BOOLEAN DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS result_pen_a      SMALLINT,
  ADD COLUMN IF NOT EXISTS result_pen_b      SMALLINT;
