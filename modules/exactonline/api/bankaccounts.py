# vim: set ts=8 sw=4 sts=4 et ai tw=79:
"""
Helper for bankaccounts resources.

This file is part of the Exact Online REST API Library in Python
(EORALP), licensed under the LGPLv3+.
"""
from .manager import Manager


class BankAccounts(Manager):
    resource = 'crm/BankAccounts'
    
    def filter(self, account=None, ID=None, **kwargs):
		
        if account is not None:
            remote_id = self._remote_account(account)
            # Filter by our account number.
            self._filter_append(kwargs, u"Account eq guid%s" % (remote_id,))
            
        if ID is not None:
            remote_id = self._remote_id(ID)
            # Filter by our account number.
            self._filter_append(kwargs, u"ID eq guid%s" % (remote_id,))

        return super(BankAccounts, self).filter(**kwargs)

    def _remote_account(self, account):
        return u"'%s'" % (account.replace("'", "''"),)

    def _remote_id(self, ID):
        return u"'%s'" % (ID.replace("'", "''"),)
