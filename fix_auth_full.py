import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_study_insight.settings')
django.setup()

# Full set of creation statements for the likely missing tables.
# using IF NOT EXISTS where possible or catching errors.
# We do NOT create auth_user as it exists.
# We skip foreign key checks to avoid ordering issues during recovery.

tables_sql = [
    """
    CREATE TABLE IF NOT EXISTS `auth_group` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `name` varchar(150) NOT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `name` (`name`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    """
    CREATE TABLE IF NOT EXISTS `auth_permission` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `name` varchar(255) NOT NULL,
        `content_type_id` int(11) NOT NULL,
        `codename` varchar(100) NOT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
        KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    """
    CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
        `id` bigint(20) NOT NULL AUTO_INCREMENT,
        `group_id` int(11) NOT NULL,
        `permission_id` int(11) NOT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
        KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
        KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    """
    CREATE TABLE IF NOT EXISTS `auth_user_groups` (
        `id` bigint(20) NOT NULL AUTO_INCREMENT,
        `user_id` int(11) NOT NULL,
        `group_id` int(11) NOT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
        KEY `auth_user_groups_user_id_6a12ed8b` (`user_id`),
        KEY `auth_user_groups_group_id_97559544` (`group_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    """
    CREATE TABLE IF NOT EXISTS `django_content_type` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `app_label` varchar(100) NOT NULL,
        `model` varchar(100) NOT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
]

with connection.cursor() as cursor:
    # Disable FK checks temporarily
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
    
    for sql in tables_sql:
        try:
            cursor.execute(sql)
            print("Executed table creation.")
        except Exception as e:
            print(f"Skipped/Error: {e}")
            
    cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
    print("Database repair complete.")
