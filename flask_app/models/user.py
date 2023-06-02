from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "users"
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for user in results:
            new_user = cls(user)
            users.append(new_user)
        return users

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email) VALUES (%(first_name)s, %(last_name)s, %(email)s);"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results
    
    @classmethod
    def get_one(cls, user_id):
            query ="SELECT * FROM users WHERE id = %(id)s;"
            data = {'id':user_id}
            results = connectToMySQL(cls.db).query_db(query, data)
            return cls(results[0])
        
    @classmethod
    def update(cls,data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s,email=%(email)s WHERE id = %(id)s;"
        connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def delete_user(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user["first_name"]) <2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(user["last_name"]) <2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid