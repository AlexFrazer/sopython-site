from wtforms import widgets
from flask.ext.wtf import Form
from wtforms.fields import SelectMultipleField

from sopy.auth.models import Group


class MultiCheckboxField(SelectMultipleField):
    " make some checkboxes from a list "
    def __init__(self, *args, **kwargs):
        super(SelectMultipleField, self).__init__(*args, **kwargs)
        self.choices = [(g.name, g.name) for g in Group.query.distinct()]

    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class EditGroupsForm(Form):
    " a form to change the groups a user belongs to "
    groups = MultiCheckboxField()
