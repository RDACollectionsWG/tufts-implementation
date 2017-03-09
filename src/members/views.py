from flask import jsonify, json, request
from flask.json import loads
from flask.views import MethodView
from ..utils.errors import *
from .models import *
from flask import current_app


class MembersView(MethodView):
    def get(self, id, mid=None):
        try:
            if mid:
                try:
                    return jsonify(MemberResultSet(current_app.db.getMembers(id, mid))), 200
                except UnauthorizedError:
                    raise UnauthorizedError()
            else:
                try:
                    datatype = request.args.get("")
                    role = request.args.get("")
                    index = request.args.get("")
                    dateAdded = request.args.get("")
                    cursor = request.args.get("")
                    expandDepth = request.args.get("")
                    return jsonify(MemberResultSet(current_app.db.getMembers(id))), 200
                except UnauthorizedError:
                    raise UnauthorizedError()
                except:
                    raise ParseError()
        except KeyError:
            raise NotFoundError()

    def post(self, id):
        try:
            posted = json.loads(request.data)
            mid = current_app.db.mintID()
            return jsonify(MemberResultSet([current_app.db.setMember(id, MemberItem(id=mid, **posted))])), 201
        except (KeyError, FileNotFoundError, NotFoundError):
            raise NotFoundError()
        except UnauthorizedError:
            raise UnauthorizedError
        except ForbiddenError:
            raise ForbiddenError()
        except:
            ParseError()

    def put(self, id, mid):
        try:
            posted = json.loads(request.data)
            if posted.id != mid:
                raise ParseError()
            if len(current_app.db.getMembers(id, mid)) is not 1:
                raise NotFoundError
            current_app.db.setMember(id, posted)
            return jsonify(MemberResultSet([posted])), 200
        except (KeyError, FileNotFoundError, NotFoundError):
            raise NotFoundError()
        except UnauthorizedError:
            raise UnauthorizedError
        except ForbiddenError:
            raise ForbiddenError()
        except:
            ParseError()  # todo: unexpected error

    def delete(self, id, mid):
        try:
            current_app.db.delMember(id, mid)
            return jsonify(), 200  # todo: use id, mid
        except (KeyError, FileNotFoundError, NotFoundError):
            raise NotFoundError()
        except UnauthorizedError:
            raise UnauthorizedError
        except ForbiddenError:
            raise ForbiddenError()
        except:
            ParseError()


class PropertiesView(MethodView):
    def get(self, id, mid, property):
        try:
            return jsonify(), 200  # todo: use id, mid, property
        except KeyError:
            raise NotFoundError()
        except UnauthorizedError:
            raise UnauthorizedError

    def put(self, id, mid, property):
        try:
            return jsonify(id), 200  # todo: use id, mid, property
        except KeyError:
            raise NotFoundError()
        except UnauthorizedError:
            raise UnauthorizedError
        except ForbiddenError:
            raise ForbiddenError()

    def delete(self, id, mid, property):
        try:
            return jsonify(), 200  # todo: use id, mid, property
        except KeyError:
            raise NotFoundError()
        except UnauthorizedError:
            raise UnauthorizedError
        except ForbiddenError:
            raise ForbiddenError()


members = {
    'members': MembersView.as_view('members'),
    'properties': PropertiesView.as_view('properties'),
}