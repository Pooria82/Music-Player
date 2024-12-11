from pymongo import MongoClient
import hashlib

client = MongoClient("mongodb://localhost:27017/")
db = client["music_player"]
users_collection = db["users"]
playlist_collection = db["playlist"]


def init_db():
    """پاک‌سازی پایگاه داده"""
    users_collection.delete_many({})
    playlist_collection.delete_many({})
    print("Database initialized!")


def hash_password(password):
    """هش کردن رمز عبور برای امنیت بیشتر"""
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password):
    """ثبت‌نام کاربر جدید"""
    if users_collection.find_one({"username": username}):
        return False
    hashed_password = hash_password(password)
    users_collection.insert_one({"username": username, "password": hashed_password})
    return True


def authenticate_user(username, password):
    """تأیید هویت کاربر با بررسی شناسه کاربری و رمز عبور"""
    hashed_password = hash_password(password)
    user = users_collection.find_one({"username": username, "password": hashed_password})
    return user is not None


def add_song(song, votes=0):
    """افزودن آهنگ به پایگاه داده"""
    if not playlist_collection.find_one({"song": song}):
        playlist_collection.insert_one({"song": song, "votes": votes})


def vote_song(song, vote):
    """رأی‌دهی به یک آهنگ (مثبت یا منفی)"""
    result = playlist_collection.update_one({"song": song}, {"$inc": {"votes": vote}})
    return result.modified_count > 0


def get_playlist_sorted():
    """دریافت لیست پخش مرتب‌شده بر اساس امتیاز"""
    return list(playlist_collection.find({}, {"_id": 0, "song": 1, "votes": 1}).sort("votes", -1))


init_db()
