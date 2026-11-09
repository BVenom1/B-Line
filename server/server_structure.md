This it a description of all the tables in the database

# users
user_id             int             primary key
user_name           str(25)         unique not null
email               emailstr        unique not null
password            str             not null
status              str(255)
is_verified         bool            default false
created_at          datetime        not null
verified_at         datetime

# groups
group_id            int             primary key
group_name          str(50)         not null
description         str(255)    
created_at          datetime        not null

# memberships
membership_id       int             primary key
user_id             int             foreign key, not null
group_id            int             foreign key, not null
joined_at           datetime        not null
membership_type     m_types enum    (Member, Admin, Banned, Left)
notification_type   n_types enum    (Notify, Mute)

# messages
message_id          int             primary key
user_id             int             foreign key
group_id            int             foreign key, not null
content             str
sent_at             datetime        not null