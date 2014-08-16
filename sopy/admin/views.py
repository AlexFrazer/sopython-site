from flask import abort, render_template

from sopy import db
from sopy.admin import bp
from sopy.admin.forms import EditGroupsForm
from sopy.ext.views import template, redirect_for
from sopy.auth.models import User, Group
from sopy.auth.login import has_group, current_user


@bp.before_request
def authorize():
    " if the user does not have approved privileges, abort with 401: not authorized "
    if not current_user.has_group('approved'):
        abort(401)


@bp.route('/groups/view')
@template('/admin/view_groups.html')
def view_groups():
    " make a dictionary keyed by groups, where the values are lists of users belonging to that group "
    groups = {g.name: g.users for g in Group.query.options(db.joinedload(Group.users))}
    groups['no groups'] = [u for u in User.query.all() if len(u._groups) == 0]
    return {'users_by_group': groups}


@bp.route('/groups/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user_groups(user_id):
    " give admin a form to edit the user's groups once they select a user "
    user = User.query.get_or_404(user_id)
    form = EditGroupsForm(obj=user)
    if form.validate_on_submit():
        form_groups = set([Group.query.filter_by(name=x).one() for x in form.groups.data])

        for removed in user._groups.difference(form_groups):
            user._groups.discard(removed)
        for added in form_groups.difference(user._groups):
            user._groups.add(added)

        db.session.commit()

        return redirect_for('admin.view_groups')
    return render_template('admin/edit_groups.html', form=form, user=user)
