-- Enforce uniqueness on users.serial
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_serial ON users(serial);

-- Enforce uniqueness on admins.username
CREATE UNIQUE INDEX IF NOT EXISTS idx_admins_username ON admins(username);


