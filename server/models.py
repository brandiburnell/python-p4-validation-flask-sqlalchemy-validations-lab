from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, author_name):
        if author_name == "" or Author.query.filter_by(name=author_name).first():
            raise ValueError('requires each record to have a unique name')
        return author_name
    
    @validates('phone_number')
    def validate_phone_number(self, key, p_num):
        if len(p_num) != 10 or p_num.isdigit() == False:
            raise ValueError('phone number must be 10 digits')
        return p_num

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_post_content(self, key, content):
        if len(content) < 250:
            raise ValueError('content must be 250 characters long')
        return content
    
    @validates('title')
    def validate_title(self, key, title):
        accepted_titles = ["Won't Believe", "Secret", "Top", "Guess"]
        if bool([el for el in accepted_titles if (el in title)]) == False:
            raise ValueError('title must be click-baitey')
        return title

    @validates('summary')
    def validates_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError('summary must be less than 250 characters')
        return summary
    
    @validates('category')
    def validates_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError('must be in allowed category')
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
