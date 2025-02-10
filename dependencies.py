from fastapi import Request

def get_workouts_db(request: Request):
    return request.app.mongodb["workouts"]