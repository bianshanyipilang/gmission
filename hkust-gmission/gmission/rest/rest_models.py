from gmission.controllers.geo_controller import filter_location

__author__ = 'chenzhao'


from .base import ReSTBase
from werkzeug.exceptions import Conflict
from gmission.models import *
from gmission.controllers.task_controller import refresh_task_status, assign_task_to_workers
from gmission.controllers.payment_controller import pay


# for k,v in app.blueprints.items():
#     print k,v

class ReSTUser(User, ReSTBase):
    @classmethod
    def before_get_many(cls, search_params=None, **kwargs):
        pass
        # print 'ReSTUser before_get_many'

    @classmethod
    def before_get_single(cls, instance_id=None, **kwargs):
        pass
        # print 'ReSTUser before_get_single'

    @classmethod
    def after_get_many(cls, **kwargs):
        pass
        # print 'ReSTUser after_get_many'

    @classmethod
    def before_post(cls, data):
        pass
        # print 'ReSTUser before_post'


class ReSTAttachment(Attachment, ReSTBase):
    pass


class ReSTHIT(HIT, ReSTBase):

    @classmethod
    def before_post(cls, data):
        # print 'ReSTTask before_post'
        filter_location(data)
    @classmethod
    def after_post(cls, result=None):
        pass
        # print 'ReSTTask after_post'


class ReSTAnswer(Answer, ReSTBase):
    @classmethod
    def before_post(cls, data):
        # print 'ReSTAnswer before_post'
        filter_location(data)
                # data['status'] = 'open'
    @classmethod
    def before_put_single(cls, instance_id=None, data=None):
        # print 'ReSTAnswer before_put'
        filter_location(data)
    @classmethod
    def after_post(cls, result):
        # print 'ReSTAnswer after_post'
        answer = Answer.query.get(result['id'])
        # send_answer_message(answer)
        refresh_task_status()
        # Prof. Chen wants workers to be paid at once:
        pay(answer.task.requester, answer.worker, answer, answer.task.credit)

    @classmethod
    def after_get_many(cls, search_params=None, **kwargs):
        pass
        # print 'ReSTAnswer after_get_many'


class ReSTLocation(Location, ReSTBase):
    @classmethod
    def before_post(cls, data):
        pass
        # print 'ReSTLocation before_post'
    @classmethod
    def after_post(cls, **kw):
        pass
        # print 'ReSTLocation after_post'
        # print kw


class ReSTPositionTrace(PositionTrace, ReSTBase):
    @classmethod
    def after_post(cls, result):
        # print 'ReSTPositionTrace after_post'
        pos = get_or_create(UserLastPosition, user_id=result['user_id'])
        # pos:UserLastPosition
        pos.longitude = result['longitude']
        pos.latitude = result['latitude']
        pos.z = result['z']
        db.session.commit()


class ReSTUserLastPosition(UserLastPosition, ReSTBase):
    @classmethod
    def after_post(cls, **kw):
        pass
        # print 'ReSTPositionTrace after_post'
