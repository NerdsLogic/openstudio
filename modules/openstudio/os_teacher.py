# -*- coding: utf-8 -*-
"""
    This file holds OpenStudio Teacher class
"""

import datetime

from gluon import *
from mailchimp3 import MailChimp
from mailchimp3.mailchimpclient import MailChimpError

class Teacher:
    """

    """
    def __init__(self, auID):
        """
            Init function for teacher
        """
        db = current.db

        self.id = auID
        self.row = db.auth_user(auID)


    def get_upcoming_classes_formatted(self, days=3):
        """
            Returns upcoming classes for teacher
        """
        from os_class_schedule import ClassSchedule

        T = current.T
        db = current.db
        auth = current.auth
        TODAY_LOCAL = current.globalenv['TODAY_LOCAL']

        attendance_permission = (auth.has_membership(group_id='Admins') or
                                 auth.has_permission('update', 'classes_attendance'))

        date = TODAY_LOCAL
        delta = datetime.timedelta(days=1)

        header = THEAD(TR(TH(T('Class date')),
                          TH(T('Time')),
                          TH(T('Location')),
                          TH(T('Class type')),
                          TH(T('Teacher')),
                          TH(T('Teacher2')),
                          TH(),
                          ))

        table = TABLE(header, _class='table table-hover')

        for day in range(0, days):
            cs = ClassSchedule(
                date,
                filter_id_teacher=self.id)

            rows = cs.get_day_rows()
            if not len(rows):
                table = T("No upcoming classes found...")
            else:
                for i, row in enumerate(rows):
                    if row.classes_otc.Status == 'cancelled' or row.school_holidays.id:
                        continue

                    repr_row = list(rows[i:i + 1].render())[0]

                    result = cs._get_day_row_teacher_roles(row, repr_row)

                    teacher = result['teacher_role']
                    teacher2 = result['teacher_role2']

                    attendance = ''
                    if attendance_permission:
                        attendance = os_gui.get_button('noicon', URL('classes', 'attendance',
                                                                     vars={'clsID': row.classes.id,
                                                                           'date': date.strftime(DATE_FORMAT)}),
                                                       title=T('Attendance'),
                                                       _class=T('pull-right'))

                    tr = TR(TD(date.strftime(DATE_FORMAT), _class='bold green' if day == 0 else ''),
                            TD(repr_row.classes.Starttime, ' - ', repr_row.classes.Endtime),
                            TD(repr_row.classes.school_locations_id),
                            TD(repr_row.classes.school_classtypes_id),
                            TD(teacher),
                            TD(teacher2),
                            TD(attendance)
                            )

                    table.append(tr)

            date += delta

        upcoming_classes = DIV(DIV(H3(T('My upcoming classes'), _class="box-title"),
                                   DIV(A(I(_class='fa fa-minus'),
                                         _href='#',
                                         _class='btn btn-box-tool',
                                         _title=T("Collapse"),
                                         **{'_data-widget': 'collapse'}),
                                       _class='box-tools pull-right'),
                                   _class='box-header with-border'),
                               DIV(table, _class='box-body'),
                               _class='box box-success')

        return upcoming_classes


    def get_payment_fixed_rate_default(self, render=False):
        """
        :return: gluon.dal.row object of db.teachers_payment_fixed_rate_default
        """
        db = current.db

        query = (db.teachers_payment_fixed_rate_default.auth_teacher_id ==
                 self.id)
        rows = db(query).select(db.teachers_payment_fixed_rate_default.ALL)

        if rows:
            if not render:
                return rows
            else:
                return rows.render()
        else:
            return False


    def get_payment_fixed_rate_default_display(self):
        """
        :return: HTML display of default rate for teacher
        """
        from os_gui import OsGui

        T = current.T
        os_gui = OsGui()

        display = DIV(
            H3(T("Default rate")),
        )

        edit_url = URL('payment_fixed_rate_default',
                            vars={'teID':self.id})
        rows = self.get_payment_fixed_rate_default(render=True)
        if not rows:
            display.append(
                A(T('Set default rate'),
                  _href=edit_url)
            )
            return display


        row = list(rows)[0]

        display.append(DIV(
            os_gui.get_button('edit',
                              edit_url,
                              _class='pull-right',
                              title=T('Edit'),
                              tooltip=T('Edit the default rate')),
            H4(row.ClassRate), ' ',
            row.tax_rates_id, BR(),
        ))

        return display


    def get_payment_fixed_rate_classes(self):
        """
        :return: gluon.dal.row object of db.teachers_payment_fixed_rate_class
        """
        db = current.db

        left = [
            db.classes.on(db.teachers_payment_fixed_rate_class.classes_id ==
                          db.classes.id),
            db.school_locations.on(db.classes.school_locations_id ==
                                   db.school_locations.id)
        ]

        query = (db.teachers_payment_fixed_rate_class.auth_teacher_id ==
                 self.id)
        rows = db(query).select(db.teachers_payment_fixed_rate_class.ALL,
                                db.classes.ALL,
                                left=left,
                                orderby=db.classes.Week_day|\
                                        db.school_locations.Name|\
                                        db.classes.Starttime)

        return rows


    def get_payment_fixed_rate_classes_dict(self, render=False):
        """
        :return: dict object of db.teachers_payment_fixed_rate_class
        """
        rows = self.get_payment_fixed_rate_classes()
        if rows:
            if render:
               rows = rows.render()

            data = {}
            for row in rows:
                data[int(row.classes.id)] = row.teachers_payment_fixed_rate_class

            return data
        else:
            return False


    def get_payment_fixed_rate_classes_rows(self, render=False):
        """
        :return: gluon.dal.row object of db.teachers_payment_fixed_rate_class
        """
        rows = self.get_payment_fixed_rate_classes()
        if rows:
            if not render:
                return rows
            else:
                return rows.render()
        else:
            return False


    def _get_payment_fixed_rate_classes_display_get_table_header(self):
        """
        :return: table header for display
        """
        T = current.T

        header = THEAD(
            TR(
                TH(T('Week day')),
                TH(T('Time')),
                TH(T('Class')),
                TH(T('Location')),
                TH(T('Class rate')),
                TH(T('VAT')),
                TH(),
            )
        )

        return header


    def get_payment_fixed_rate_classes_display(self):
        """
        :return: gluon.dal.row object of db.teachers_payment_fixed_rate_class
        """
        from openstudio.os_gui import OsGui

        T = current.T
        auth = current.auth
        os_gui = OsGui()
        rows = self.get_payment_fixed_rate_classes_rows()

        display = DIV(
            os_gui.get_button('add',
                              URL('teachers',
                                  'payment_fixed_rate_class_add',
                                  vars={'teID': self.id}),
                              _class='pull-right'),
            H3(T("Class rates")),
        )

        if not rows:
            return display

        edit_permission = auth.has_membership(group_id='Admins') or \
                          auth.has_permission('update', 'teachers_payment_fixed_rate_class')
        delete_permission = auth.has_membership(group_id='Admins') or \
                          auth.has_permission('delete', 'teachers_payment_fixed_rate_class')
        delete_onclick = "return confirm('" + \
            T('Do you really want to delete this class rate?') \
            + "');"

        table = TABLE(
            self._get_payment_fixed_rate_classes_display_get_table_header(),
            _class='table table-hover table-striped'
        )

        for i, row in enumerate(rows):
            repr_row = list(rows[i:i + 1].render())[0]

            buttons = DIV(_class='pull-right')
            if edit_permission:
                edit_url = URL('payment_fixed_rate_class',
                               vars={'teID':self.id,
                                     'clsID':row.teachers_payment_fixed_rate_class.classes_id})
                buttons.append(os_gui.get_button('edit', edit_url))

            if delete_permission:
                delete_url = URL('payment_fixed_rate_class_delete',
                                 vars={'tpfrcID': row.teachers_payment_fixed_rate_class.id,
                                       'teID':self.id})
                buttons.append(os_gui.get_button(
                    'delete_notext',
                    delete_url,
                    onclick=delete_onclick,
                ))

            time = SPAN(
                repr_row.classes.Starttime, ' - ', repr_row.classes.Endtime
            )

            table.append(
                TR(
                    TD(repr_row.classes.Week_day),
                    TD(time),
                    TD(repr_row.classes.school_classtypes_id),
                    TD(repr_row.classes.school_locations_id),
                    TD(repr_row.teachers_payment_fixed_rate_class.ClassRate),
                    TD(repr_row.teachers_payment_fixed_rate_class.tax_rates_id),
                    TD(buttons)
                )
            )

        display.append(table)

        return display


    def get_payment_travel_allowance_location(self, slID):
        """
        :return: gluon.dal.row object of db.teachers_payment_travel
        """
        db = current.db

        query = (db.teachers_payment_travel.auth_teacher_id ==
                 self.id) & \
                (db.teachers_payment_travel.school_locations_id == slID)
        rows = db(query).select(db.teachers_payment_travel.ALL)

        if rows:
            return rows.first()
        else:
            return False


    def get_payment_travel_allowances(self, render=False):
        """
        :return: gluon.dal.row object of db.teachers_payment_travel
        """
        db = current.db

        left = [
            db.school_locations.on(db.teachers_payment_travel.school_locations_id ==
                                   db.school_locations.id)
        ]

        query = (db.teachers_payment_travel.auth_teacher_id ==
                 self.id)
        rows = db(query).select(db.teachers_payment_travel.ALL,
                                db.school_locations.ALL,
                                left=left,
                                orderby=db.school_locations.Name)

        if rows:
            if not render:
                return rows
            else:
                return rows.render()
        else:
            return False


    def _get_payment_travel_display_get_table_header(self):
        """
        :return: table header for display
        """
        T = current.T

        header = THEAD(
            TR(
                TH(T('Location')),
                TH(T('Travel allowance')),
                TH(T('VAT')),
                TH(),
            )
        )

        return header


    def get_payment_travel_display(self):
        """
        :return: gluon.dal.row object of db.teachers_payment_travel
        """
        from openstudio.os_gui import OsGui

        T = current.T
        auth = current.auth
        os_gui = OsGui()
        rows = self.get_payment_travel_allowances()

        display = DIV()

        if not rows:
            return display

        edit_permission = auth.has_membership(group_id='Admins') or \
                          auth.has_permission('update', 'teachers_payment_travel')
        delete_permission = auth.has_membership(group_id='Admins') or \
                          auth.has_permission('delete', 'teachers_payment_travel')
        delete_onclick = "return confirm('" + \
            T('Do you really want to delete the travel allowance for this location?') \
            + "');"

        table = TABLE(
            self._get_payment_travel_display_get_table_header(),
            _class='table table-hover table-striped'
        )

        for i, row in enumerate(rows):
            repr_row = list(rows[i:i + 1].render())[0]

            buttons = DIV(_class='pull-right')
            if edit_permission:
                edit_url = URL('payment_travel_edit',
                               vars={'teID':self.id,
                                     'tpfrtID':row.teachers_payment_travel.id})
                buttons.append(os_gui.get_button('edit', edit_url))

            if delete_permission:
                delete_url = URL('payment_travel_delete',
                                 vars={'tpfrtID': row.teachers_payment_travel.id,
                                       'teID':self.id})
                buttons.append(os_gui.get_button(
                    'delete_notext',
                    delete_url,
                    onclick=delete_onclick,
                ))


            table.append(
                TR(
                    TD(row.school_locations.Name),
                    TD(repr_row.teachers_payment_travel.TravelAllowance),
                    TD(repr_row.teachers_payment_travel.tax_rates_id),
                    TD(buttons)
                )
            )

        display.append(table)

        return display

