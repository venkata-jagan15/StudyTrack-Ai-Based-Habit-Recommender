import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_study_insight.settings')
django.setup()

# Simplified table creation skipping strict FK constraints to avoid errors, 
# just to satisfy the missing table error.
sql = """
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_user_id_idx` (`user_id`),
  KEY `auth_user_user_permissions_permission_id_idx` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

with connection.cursor() as cursor:
    try:
        cursor.execute(sql)
        print("Successfully created auth_user_user_permissions table.")
    except Exception as e:
        print(f"Error creating table: {e}")
