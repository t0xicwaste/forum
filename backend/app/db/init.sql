
CREATE TABLE users (
    id SERIAL PRIMARY KEY,                         
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,             
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
);


CREATE INDEX idx_users_username ON users(username);


CREATE TABLE authorise (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,                
    hashed_password VARCHAR(255) NOT NULL,          
    

    CONSTRAINT fk_authorise_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL UNIQUE,           
    description VARCHAR(255),                       
    slug VARCHAR(100) NOT NULL UNIQUE               
);



CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,                    
    category_id INTEGER NOT NULL,                   
    author_id INTEGER,                            
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_thread_category FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    CONSTRAINT fk_thread_author FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE SET NULL
);



CREATE TABLE replies (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,                         
    thread_id INTEGER NOT NULL,                    
    author_id INTEGER,                             
    parent_id INTEGER,                              
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,                           

    CONSTRAINT fk_reply_thread FOREIGN KEY (thread_id) REFERENCES threads(id) ON DELETE CASCADE,
    CONSTRAINT fk_reply_author FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE SET NULL,
    CONSTRAINT fk_reply_parent FOREIGN KEY (parent_id) REFERENCES replies(id) ON DELETE CASCADE
);