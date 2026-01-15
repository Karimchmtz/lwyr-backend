-- Create custom enum types
DO $$ BEGIN
    CREATE TYPE message_role AS ENUM ('USER', 'ASSISTANT');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE user_role AS ENUM ('USER', 'ADMIN');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;