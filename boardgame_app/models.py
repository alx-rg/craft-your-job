from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy_utils import URLType
from flask_login import UserMixin
from boardgame_app.extensions import db
from boardgame_app.utils import FormEnum

class ItemCategory(FormEnum):
    """Types of BoardGames."""
    ABSTRACT = 'Abstract'
    AREA = 'Area Control'
    CAMPAIGN = 'Campaign'
    DECKBUILDER = 'Deck Builder'
    DRAFTING = 'Drafting'
    DUNGEON = 'Dungeon-crawler'
    ENGINE = 'Engine-Builder'
    WARGAME = 'Wargame'

class PublisherCategory(FormEnum):
    """Types of Game Publisher Companies."""
    INDIE = 'Indie MomPop'
    CROWD = 'Crowd Sourced'
    SPECIAL = 'Specialized'
    BIG = 'Big Multi Conglomerate'
    DIGITAL = "Digital Game"

class Publisher(db.Model):
    """Board Game Publisher Model."""
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    publisher_category = db.Column(db.Enum(PublisherCategory), default=PublisherCategory.SPECIAL)
    games = db.relationship('BoardGame', back_populates='boardgame')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship("User") 

class Boardgame(db.Model):
    """Boardgame model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.Enum(ItemCategory), default=ItemCategory.DUNGEON)
    photo_url = db.Column(URLType)
    publisher_id = db.Column(
        db.Integer, db.ForeignKey('publisher.id'), nullable=False)
    publisher = db.relationship('Publisher', back_populates='games')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship("User")
    liked_by = db.relationship("User", secondary="user_boardgame", back_populates="likes")
    comments = db.relationship("Comment", back_populates="boardgame")

class User(UserMixin, db.Model):
    """User model."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(90), nullable=False)
    password = db.Column(db.String(90), nullable=False)
    likes = db.relationship("Boardgame", secondary="user_boardgame", back_populates="liked_by")
    comments = db.relationship("Comment", back_populates="commenter")

class Comment(db.Model):
    """Comment Model"""
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String(150), nullable=True)
    boardgame_id = db.Column(db.Integer, db.ForeignKey('boardgame.id'), nullable=False)
    boardgame = db.relationship('Boardgame', back_populates='comments')
    commenter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    commenter = db.relationship('User', back_populates='comments')

user_boardgame = db.Table("user_boardgame",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("boardgame_id", db.Integer, db.ForeignKey("boardgame.id"))    
)
