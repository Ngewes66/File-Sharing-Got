import asyncpg
import os
from config import DB_URI

# Fungsi untuk membuat koneksi ke NeonDB
async def get_db_connection():
    try:
        conn = await asyncpg.connect(DB_URI)
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

# Fungsi untuk memeriksa apakah pengguna sudah ada
async def present_user(user_id: int):
    conn = await get_db_connection()
    if conn:
        result = await conn.fetchrow("SELECT 1 FROM users WHERE user_id = $1", user_id)
        await conn.close()
        return bool(result)
    return False

# Fungsi untuk menambahkan pengguna baru
async def add_user(user_id: int):
    conn = await get_db_connection()
    if conn:
        await conn.execute("INSERT INTO users (user_id) VALUES ($1)", user_id)
        await conn.close()

# Fungsi untuk mengambil seluruh daftar pengguna
async def full_userbase():
    conn = await get_db_connection()
    if conn:
        user_docs = await conn.fetch("SELECT user_id FROM users")
        user_ids = [doc['user_id'] for doc in user_docs]
        await conn.close()
        return user_ids
    return []

# Fungsi untuk menghapus pengguna
async def del_user(user_id: int):
    conn = await get_db_connection()
    if conn:
        await conn.execute("DELETE FROM users WHERE user_id = $1", user_id)
        await conn.close()
    
