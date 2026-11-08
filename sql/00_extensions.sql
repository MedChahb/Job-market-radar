-- Runs once, when the local Docker database is first created.
-- On Supabase it was enabled with: create extension if not exists vector with schema extensions;
-- (Supabase's search_path includes "extensions", so the vector type resolves the same way.)
create extension if not exists vector;
