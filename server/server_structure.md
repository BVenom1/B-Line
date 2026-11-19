This it a description of all the tables in the database

# users (done)
user_id             int             primary key
user_name           str(25)         unique not null
email               emailstr        unique not null
password            str             not null
status              str(255)
is_verified         bool            default false
created_at          datetime        not null
verified_at         datetime

# conversations (done)
> Unifiead map from contacts/groups -> messages. So we have contacts/groups -> conversations -> messages
> This table should not be accesible to the frontend.
conversation_id     int             primary key

# groups (done)
group_id            int             primary key
group_name          str(50)         not null
description         str(255)    
created_at          datetime        not null
conversation_id     int             foreign key(conversations.conversation_id), not null

# memberships (done)
> Map between users & groups, since the relation between users & groups is many-to-many, we make
> an intermediary table so users-memberships is one-to-many & groups-memberships is also one-to-many. 
membership_id       int             primary key
user_id             int             foreign key(users.user_id), not null
group_id            int             foreign key(groups.group_id), not null
joined_at           datetime        not null
membership_type     m_types enum    (Member, Admin, Banned, Left)
notification_type   n_types enum    (Notify, Mute)

# contacts
contact_id          int             primary key
user_id             int             foreign key(users.user_id), not null
contact_user_id     int             foreign key(users.user_id), not null
nickname            str(25)
requested_at        datetime        not null
responded_at        datetime
contact_status      c_status enum   (Requested, Accepted, Rejected, Blocked)
conversation_id     int             foreign key(conversations.conversation_id)

# messages
message_id          int             primary key
user_id             int             foreign key(users.user_id)
conversation_id     int             foreign key(conversations.conversation_id), not null
content             str
sent_at             datetime        not null