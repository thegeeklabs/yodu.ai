## Yodu.ai

Yodu.ai is a general purpose Recommendation Engine that can be modified and used for various use-cases.

## Concepts:

At the core of the reommendations engine are these entities:

## Item
Represent the object that is recommended.
Example: Youtube video, ecommerce product, Article, Post etc.

Each Item must have a "source" which can be a User or a type Source

## Source
Represent a type that produces items.
A source can be an entity in itself or can be a User who created content.
Example: YouTube channel, Ecommerce Seller, Article Publisher etc.
 
## User
Represents an individual user

## Actions
Interactions between Users & Items.

### Attributes:

- id (String)
- item_id (String)
- user_id (String)
- created_at (Datetime)
- tags (Dictionary of String:String)

Example: Like, comment, seen, read, clicked etc.

## Follow
Represent a relation between Source-User & User or User & source.

- User can follow other Source[User]
- User can follow other Source

Example: User subscribes to a Youtube Channel, User follows another User.
    
