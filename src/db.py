from decouple import config
from psycopg2 import connect
from psycopg2.extras import RealDictCursor


def get_curriculum():
    url = config('DATABASE_URL')
    with connect(url) as connection:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("select * from curriculo_profile")
        curriculum = cursor.fetchone()
        profile_id = curriculum["id"]

        cursor.execute("select * from curriculo_socialmedia where profile_id = %s", (profile_id,))
        curriculum["social_media"] = cursor.fetchall()

        cursor.execute("select * from curriculo_education where profile_id = %s", (profile_id,))
        curriculum["educations"] = cursor.fetchall()

        cursor.execute("select * from curriculo_job where profile_id = %s", (profile_id,))
        curriculum["jobs"] = cursor.fetchall()

    return curriculum
