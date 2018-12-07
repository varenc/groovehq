import re
import requests


class Groove(object):

    def __init__(self, api_token):
        self._api_token = api_token
        self._session = requests.Session()
        self._session.headers = self._headers()
        self._endpoint = 'https://api.groovehq.com/v1/'

    def _headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self._api_token),
        }

    def _get_resp(self, api_request, key=None, kwargs={}):
        """
        Returns GET request decoded JSON response

        :param api_request: ticket/{}/messages
        :param key: dictionary key to show, defaults to None
        :param kwargs: optional arguments """
        params = {k: unicode(v) for k, v in kwargs.items()}
        resp = self._session.get(self._endpoint+str(api_request),
                                 params=params)
        if key is None:
            return resp.json()
        else:
            return resp.json()[str(key)]

    def create_ticket(self, body, from_user, to_user, note=False, **kwargs):
        """
        Create ticket.
        See https://www.groovehq.com/docs/tickets#listing-tickets for more
        details.
        :param body: The body of the first comment to add to the ticket
        :param from_user:   The email address of the agent or customer who sent the ticket or hash of customer attributes (defined below)
        :param to_user: The email address of the customer or mailbox that the ticket is addressed to or a hash of customer attributes
        :param assigned_group: The name of the assigned group
        :param assignee: The email of the agent to assign the ticket to
        :param sent_at: Can be used to set the created and updated datetimes to sometime in the past. RFC-822 format preferred
        :param note: When creating a ticket from an agent, should the message body be added as a private note
        :param send_copy_to_customer :  When creating a ticket from an agent, should the message be emailed to the customer
        :param state : The ticket state. Allowed states are: "unread", "opened", "pending", "closed", "spam"
        :param subject : The email subject of your ticket
        :param tags :  A list of tag names
        """

        data = {
            'body': body,
            'from': from_user,
            'to': to_user,
            'note': note
        }
        data.update(kwargs)

        url = self._endpoint + 'tickets'

        resp = self._session.post(url, json=data)
        res = resp.json()

        return res

    def list_folders(self, **kwargs):
        """
        Return dictionary of folder Name -> ID mapping

        :param mailbox: the email or id of a mailbox to filter by
        """
        return self._get_resp("folders", "folders", kwargs)

    def list_ticket_count(self, **kwargs):
        """
        Return ticket count matching criteria

        See https://www.groovehq.com/docs/ticket-counts#listing-ticket-counts
        for more details.

        :param mailbox: the email or id of a mailbox
        """
        return self._get_resp("tickets/count", None, kwargs)

    def list_tickets(self, **kwargs):
        """
        Return all tickets matching the criteria.

        See https://www.groovehq.com/docs/tickets#listing-tickets for more
        details.

        :param assignee: an agent email
        :param customer: a customer email or ID
        :param page: the page number
        :param per_page: how many results to return per page, defaults to 25
        :param state: One of "unread", "opened", "pending", "closed", or "spam"
        :param folder: the ID of a folder
        """
        return self._get_resp("tickets", None, kwargs)

    def list_messages(self, ticket_number, **kwargs):
        """
        Get all messages for a particular ticket.

        See https://www.groovehq.com/docs/messages#listing-all-messages for more
        details.

        :param ticket_number: the integer ticket number
        :param page: the page number
        :param per_page: how many results to return per page, defaults to 25
        """
        return self._get_resp("tickets/{}/messages".format(ticket_number),
                              None,
                              kwargs)

    def create_message(self, ticket_number, author, body, note=True):
        """
        Create a new message.

        See https://www.groovehq.com/docs/messages#creating-a-new-message
        for details.

        :param ticket_number: the ticket this message refers to
        :param author: the email of the owner of this message
        :param body: the body of the message
        :param note: whether this should be a private note, or sent to the
        customer.
        """
        data = {
            'author': author,
            'body': body,
            'note': note
        }
        url = (self._endpoint+'tickets/{}/messages'
               .format(ticket_number))
        resp = self._session.post(url, json=data)

        return resp.json()

    def list_customers(self, **kwargs):
        """
        Return list of customers

        See https://www.groovehq.com/docs/customers#listing-all-customers for
        details.

        :param page: page number
        :param per_page: number of messages to return (default 25, max 50)
        """
        return self._get_resp("customers", None, kwargs)

    def list_agents(self, **kwargs):
        """
        Get list of all agents

        See https://www.groovehq.com/docs/agents#listing-agents for more
        details

        :param group: The ID of a group to filter by
        """
        return self._get_resp("agents", "agents", kwargs)

    def list_groups(self):
        """
        Return list of groups

        See https://www.groovehq.com/docs/groups#listing-groups for more details
        """
        return self._get_resp("groups", "groups")

    def list_mailboxes(self):
        """
        Return list of mailboxes

        See https://www.groovehq.com/docs/mailboxes#listing-mailboxes for more
        details
        """
        return self._get_resp("mailboxes", "mailboxes")

    def list_attachments(self, **kwargs):
        """
        Return list of all attachments

        See https://www.groovehq.com/docs/attachments#listing-attachments for
        more details

        :param message: the id of the message to list attachments for
        """
        return self._get_resp("attachments", "attachments", kwargs)
