#%%
import sqlalchemy
from sqlalchemy.orm import sessionmaker

import models

from config import Session

#%%

s = Session()
#%%
u = models.User(lms_user='igorsm1', is_prof=True, token='alks')
s.add(u)
s.commit()
# %%
print(sess.query(models.User).all())

# %%

u = s.query(models.User).first()

c = models.Course(name='test', responsible=u)
s.add(c)
s.commit()

# %%

a = models.Activity(course_specific_id='at1', course=c)
s.add(a)
s.commit()

#%%
u2 = models.User(lms_user='a2', is_prof=False, token='alks2')
s.add(u2)
sub = models.Submission(sender_id=u2.id, activity_id=a.id, content='sdlkfjsdlfsdlfjsdkl')
s.add(sub)
s.commit()
# %%
