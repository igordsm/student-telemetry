from fastapi import FastAPI, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from models import *

from config import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import inspect

from typing import Optional

app = FastAPI()
app.mount('/js', StaticFiles(directory='js'), name='js')

def validate_user(s, token, is_prof):
    try:
        user = s.query(User).filter(User.token==token).one()
        if is_prof and not user.is_prof:
            raise HTTPException(status_code=403, detail='Access denied')
    except NoResultFound:
        user = User(lms_user='anon', is_prof=False)
        user.token = token
        s.add(user)
        s.commit()

    return user

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

@app.post('/users/')
async def user_create(token: str = Form(...), lms_user: str = Form(...), is_prof: bool = Form(...)):
    s = Session()

    creator = validate_user(s, token, True)

    new_user = User(lms_user=lms_user, is_prof=is_prof)
    s.add(new_user)
    s.commit()

    return {'message': 'ok', 'token': new_user.token}

@app.post('/courses/')
async def course_create(token: str = Form(...), name: str = Form(...)):
    s = Session()

    responsible = validate_user(s, token, True)
    
    c = Course(name=name, responsible=responsible)
    s.add(c)
    s.commit()

    return {'message': 'Course created', 'id': c.id}

@app.post('/courses/{course_id}/activities/{activity_id}')
async def submit_task(course_id : int, 
                      activity_id : str, 
                      token: str = Form(...),
                      content: str = Form(...),
                      type : Optional[str] = Form(ActivityType.multiple_choice)):
    s = Session()

    sender = validate_user(s, token, False)
    
    try:
        course = s.query(Course).filter(Course.id==course_id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail='Invalid course id')

    try:
        activity = s.query(Activity).filter(Activity.course_id==course_id, 
                        Activity.course_specific_id==activity_id).one()
    except NoResultFound:
        activity = Activity(course_specific_id=activity_id, type=type, course=course)
        s.add(activity)
    
    sub = Submission(sender=sender, activity=activity, content=content)
    s.add(sub)

    try:
        correct = s.query(Submission.content).filter(Submission.activity==activity, Submission.sender.has(is_prof=True)).first()[0]
    except NoResultFound:
        correct = ""

    s.commit()
    return {'message': 'OK', 'id': sub.id, "correct_answer": correct, "activity_id": activity_id, "content": content}

@app.get('/courses/{course_id}/activities/{activity_id}')
async def list_submissions(course_id:int, activity_id: str, token:str = Form(...)):
    s = Session()

    prof = validate_user(s, token, True)
    all_submissions = s.query(Submission.content, User.lms_user) \
                       .join(Submission.sender) \
                       .filter(Submission.activity.has(course_id=course_id)) \
                       .filter(Submission.activity.has(course_specific_id=activity_id)) \
                       .all()

    all_submissions = [r._asdict() for r in all_submissions]

    return all_submissions

