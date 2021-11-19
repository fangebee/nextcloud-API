# -*- coding: utf-8 -*-
"""
Talk API wrapper (spreed)
"""
from nextcloud import base


class Spreed(base.OCSv2ApiWrapper):
    API_URL = "/ocs/v2.php/apps/spreed/api/v3"


    # Conversations management - START
    # https://nextcloud-talk.readthedocs.io/en/stable/conversation/

    def get_user_conversations(self, noStatusUpdate=0, includeStatus=False):
        """
        Get user´s conversations

        @see https://nextcloud-talk.readthedocs.io/en/stable/conversation/#get-user-s-conversations

        :param noStatusUpdate (int): Whether the "online" user status of the current user should be "kept-alive" (1) or not (0) (defaults to 0)
        :param includeStatus (bool): Whether the user status information of all one-to-one conversations should be loaded (default false)
        :return: OCSResponse
        """
        params = {
            "noStatusUpdate": noStatusUpdate,
            "includeStatus": includeStatus,
        }
        return self.requester.get("/room", data=params)

    def create_new_conversation(self, roomName, roomType, invite=None, source=None):
        """
        Creating a new conversation

        @see https://nextcloud-talk.readthedocs.io/en/stable/conversation/#creating-a-new-conversation

        :param roomName (str): conversation name (Not available for roomType = 1)
        :param roomType (int): 1 = "one to one", 2 = "Group", 3 = "Public", 4 = "Changelog"
        :param invite (str): user id (roomType = 1), group id (roomType = 2 - optional), circle id (roomType = 2, source = 'circles'], only available with circles-support capability))
        :param source (str): The source for the invite, only supported on roomType = 2 for groups and circles (only available with circles-support capability)
        :return: OCSResponse
        """
        params = {
            "roomName": roomName,
            "roomType": roomType,
            "invite": invite,
            "source": source,
        }
        return self.requester.post("/room", data=params)

    def get_single_conversation(self, token):
        """
        Get single conversation (also for guests)

        @see https://nextcloud-talk.readthedocs.io/en/stable/conversation/#get-single-conversation-also-for-guests

        :return: OCSResponse
        """
        url = "/".join(["room", str(token)])
        return self.requester.get(url)

    def get_open_conversations(self, searchTerm=None):
        """
        Get open conversations

        @see https://nextcloud-talk.readthedocs.io/en/stable/conversation/#get-open-conversations

        :param searchTerm (str): search term
        :return: OCSResponse
        """
        headers=None
        if searchTerm:
            headers = {
                "searchTerm": searchTerm,
            }
        return self.requester.get("/listable-rooms", headers=headers)

    def rename_conversation(self, token, roomName):
        """
        Rename a conversation

        @see https://nextcloud-talk.readthedocs.io/en/stable/conversation/#rename-a-conversation

        :param token (str): Id of the chat room
        :param roomName (str): New name for the conversation (1-200 characters)
        :return: OCSResponse
        """
        url = "/".join(["room", str(token)])
        return self.requester.put(url, data={"roomName": roomName})

    def delete_conversation(self, token):
        """
        Delete a conversation

        @see https://nextcloud-talk.readthedocs.io/en/stable/conversation/#delete-a-conversation

        :param token (str): Id of the chat room
        :return: OCSResponse
        """
        url = "/".join(["room", str(token)])
        return self.requester.delete(url)

    def set_conversation_description(self, token, description):
        """
        Set description for a conversation

        @see https://nextcloud-talk.readthedocs.io/en/stable/conversation/#set-description-for-a-conversation

        :param token (str): Id of the chat room
        :param description (str): New description for the conversation
        :return: OCSResponse
        """
        url = "/".join(["room", str(token), "description"])
        return self.requester.put(url, data={"description": description})

    def allow_guests_in_conversation(self, token):
        """
        Allow guests in a conversation (public conversation)

        @see https://nextcloud-talk.readthedocs.io/en/stable/conversation/#allow-guests-in-a-conversation-public-conversation

        :param token (str): Id of the chat room
        :return: OCSResponse
        """
        url = "/".join(["room", str(token), "public"])
        return self.requester.post(url)

    def disallow_guests_in_conversation(self, token):
        """
        Disallow guests in a conversation (group conversation)

        @see https://nextcloud-talk.readthedocs.io/en/stable/conversation/#disallow-guests-in-a-conversation-group-conversation

        :param token (str): Id of the chat room
        :return: OCSResponse
        """
        url = "/".join(["room", str(token), "public"])
        return self.requester.delete(url)

    def set_readonly_conversation(self, token, state):
        """
        Set read-only for a conversation

        @see https://nextcloud-talk.readthedocs.io/en/stable/conversation/#set-read-only-for-a-conversation
        @see https://nextcloud-talk.readthedocs.io/en/stable/constants/#read-only-states

        :param token (str): Id of the chat room
        :param state (int): New state for the conversation, see constants list
        :return: OCSResponse
        """
        url = "/".join(["room", str(token), "read-only"])
        return self.requester.put(url)

    def set_password_for_conversation(self, token, password):
        """
        Set password for a conversation

        @see https://nextcloud-talk.readthedocs.io/en/stable/conversation/#set-password-for-a-conversation

        :param token (str): Id of the chat room
        :param password (str): New password for the conversation
        :return: OCSResponse
        """
        url = "/".join(["room", str(token), "password"])
        return self.requester.put(url, data={"password": password})

    def add_conversation_to_favorites(self, token):
        """
        Add conversation to favorites

        @see https://nextcloud-talk.readthedocs.io/en/stable/conversation/#add-conversation-to-favorites

        :param token (str): Id of the chat room
        :return: OCSResponse
        """
        url = "/".join(["room", str(token), "favorite"])
        return self.requester.post(url)

    def delete_conversation_from_favorites(self, token):
        """
        Remove conversation from favorites

        @see https://nextcloud-talk.readthedocs.io/en/stable/conversation/#remove-conversation-from-favorites

        :param token (str): Id of the chat room
        :return: OCSResponse
        """
        url = "/".join(["room", str(token), "favorite"])
        return self.requester.delete(url)

    def set_notification_level(self, token, level):
        """
        Set notification level

        @see https://nextcloud-talk.readthedocs.io/en/stable/conversation/#add-conversation-to-favorites
        @see https://nextcloud-talk.readthedocs.io/en/stable/constants/#participant-notification-levels

        :param token (str): Id of the chat room
        :param level (int): The notification level (See Participant notification levels)
        :return: OCSResponse
        """
        url = "/".join(["room", str(token), "notify"])
        return self.requester.post(url, data={"level": level})

    def open_conversation(self, token, scope):
        """
        Open a conversation

        @see https://nextcloud-talk.readthedocs.io/en/stable/conversation/#open-a-conversation

        :param token (str): Id of the chat room
        :param scope (int): New flags for the conversation
        :return: OCSResponse
        """
        url = "/".join(["room", str(token), "listable"])
        return self.requester.put(url, data={"scope": scope})

    # Conversations management - END


    # Participants management - START
    # cf. https://nextcloud-talk.readthedocs.io/en/stable/participant/

    def get_room_participants(self, token, includeStatus=False):
        """
        Get list of participants in a conversation

        :param token (str): Id of the chat room
        :param includeStatus (bool): Whether the user status information also needs to be loaded
        :return: OCSResponse
        """
        url = "/".join(["room", str(token), "participants"])
        return self.requester.get(url, data={"includeStatus": includeStatus})

    def add_participant(self, token, newParticipant, source=None):
        """
        Add a participant to a conversation

        :param newParticipant (str): User, group, email or circle to add
        :param source (str): Source of the participant(s) as returned by the autocomplete suggestion endpoint (default is users)
        :return: OCSResponse
        """
        url = "/".join(["room", str(token), "participants"])
        return self.requester.post(url, data={"newParticipant": newParticipant})

    def delete_attendee(self, token, attendeeId):
        """
        Delete an attendee by id from a conversation

        :param token (str): Id of the chat room
        :param attendeeId (int): The participant to delete
        :return: OCSResponse
        """
        url = "/".join(["room", str(token), "attendees"])
        return self.requester.delete(url, data={"attendeeId": attendeeId})

    def remove_self_from_conversation(self, token):
        """
        Remove yourself from a conversation

        :param token (str): Id of the chat room
        :return: OCSResponse
        """
        url = "/".join(["room", str(token), "participants", "self"])
        return self.requester.delete(url)

    def join_conversation(self, token, password=None, force=True):
        """
        Join a conversation (available for call and chat)

        :param token (str): Id of the chat room
        :param password (str): Optional: Password is only required for users which are self joined or guests and only when the conversation has hasPassword set to true.
        :param force (bool): If set to false and the user has an active session already a 409 Conflict will be returned (Default: true - to keep the old behaviour)
        :return: OCSResponse
        """
        url = "/".join(["room", str(token), "participants", "self"])
        params = {
            "force": force,
        }
        if password:
            params["password"] = password
        return self.requester.post(url, data=params)

    def resend_participant_emails(self, token, attendeeId=None):
        """
        Resend participant emails

        :param token (str): Id of the chat room
        :param attendeeId (int): Attendee id can be used for guests and users, not setting it will resend all invitations
        :return: OCSResponse
        """
        url = "/".join(["room", str(token), "participants", "resend-invitations"])
        params={}
        if attendeeId:
            params["attendeeId"] = attendeeId
        return self.requester.post(url, data=params)

    def leave_conversation(self, token):
        """
        Leave a conversation (not available for call and chat anymore)

        :param token (str): Id of the chat room
        :return: OCSResponse
        """
        url = "/".join(["room", str(token), "participants", "active"])
        return self.requester.delete(url)

    def promote_moderator(self, token, attendeeId):
        """
        Promote a user or guest to moderator

        :param token (str): Id of the chat room
        :param attendeeId (int): Attendee id can be used for guests and users
        :return: OCSResponse
        """
        url = "/".join(["room", str(token), "moderators"])
        return self.requester.post(url, data={"attendeeId": attendeeId})

    def demote_moderator(self, token, attendeeId):
        """
        Demote a moderator to user or guest

        :param token (str): Id of the chat room
        :param attendeeId (int): Attendee id can be used for guests and users
        :return: OCSResponse
        """
        url = "/".join(["room", str(token), "moderators"])
        return self.requester.delete(url, data={"attendeeId": attendeeId})

    def set_permissions(self, token, attendeeId, mode, permissions):
        """
        Set permissions for an attendee

        :param token (str): Id of the chat room
        :param attendeeId (int): Attendee id can be used for guests and users
        :param mode (str): Mode of how permissions should be manipulated constants list. 
            If the permissions were 0 (default) and the modification is add or remove,
            they will be initialised with the call or default conversation permissions before,
            falling back to 126 for moderators and 118 for normal participants.
        :param permissions (int): New permissions for the attendee, see constants list.
            If permissions are not 0 (default), the 1 (custom) permission will always be added.
        :return: OCSResponse
        """
        url = "/".join(["room", str(token), "attendees", "permissions"])
        params = {
            "attendeeId": attendeeId,
            "mode": mode,
            "permissions": permissions,
        }
        return self.requester.put(url, data=params)

    def set_permissions_for_all_attendees(self, token, mode, permissions):
        """
        Set permissions for all attendees

        :param token (str): Id of the chat room
        :param mode (str): Mode of how permissions should be manipulated constants list.
            If the permissions were 0 (default) and the modification is add or remove,
            they will be initialised with the call or default conversation permissions before,
            falling back to 126 for moderators and 118 for normal participants.
        :param permissions (int): New permissions for the attendees, see constants list.
            If permissions are not 0 (default), the 1 (custom) permission will always be added.
        :return: OCSResponse
        """
        url = "/".join(["room", str(token), "attendees", "permissions", "all"])
        params = {
            "mode": mode,
            "permissions": permissions,
        }
        return self.requester.put(url, data=params)

    def get_participant(self, token, pin):
        """
        Get a participant by their pin

        Note: This is only allowed with validate SIP bridge requests

        :param token (str): Id of the chat room
        :param pin (str): Participant's PIN
        :return: OCSResponse
        """
        url = "/".join(["room", str(token), "pin", str(pin)])
        return self.requester.get(url)

    def set_displayname_as_guest(self, token, displayName):
        """
        Set display name as a guest

        :param token (str): Id of the chat room
        :param displayName (str): The new display name
        :return: OCSResponse
        """
        url = "/".join(["guest", str(token), "name"])
        return self.requester.post(url, data={"displayName": displayName})

    # Participants management - END


    # Chat management - START
    # cf. https://nextcloud-talk.readthedocs.io/en/stable/chat/

    def receive_chat_message_in_conversation(self, token, limit=5, lookIntoFuture=0, setReadMarker=0, includeLastKnown=None, lastKnownMessageId=None, lastCommonReadId=None):
        """
        Receive chat messages of a conversation

        @see https://nextcloud-talk.readthedocs.io/en/stable/chat/#receive-chat-messages-of-a-conversation

        :param token (str): Id of the chat room
        :param limit (int): Number of chat messages to receive (100 by default, 200 at most)
        :param lookIntoFuture (int): 1 Poll and wait for new message or 0 get history of a conversation
        :param timeout (int): lookIntoFuture = 1 only, Number of seconds to wait for new messages (30 by default, 60 at most)
        :param lastKnownMessageId (int): Serves as an offset for the query. The lastKnownMessageId for the next page is available in the X-Chat-Last-Given header.
        :param lastCommonReadId (int): Send the last X-Chat-Last-Common-Read header you got, if you are interested in updates of the common read value. A 304 response does not allow custom headers and otherwise the server can not know if your value is modified or not.
        :param setReadMarker (int): 1 to automatically set the read timer after fetching the messages, use 0 when your client calls Mark chat as read manually. (Default: 1)
        :param includeLastKnown (int): 1 to include the last known message as well (Default: 0)
        :return: OCSResponse
        """
        params = {
            "limit": limit,
            "lookIntoFuture": lookIntoFuture,
        }
        if lastCommonReadId:
            params["lastCommonReadId"] = lastCommonReadId
        if lastKnownMessageId:
            params["lastKnownMessageId"] = lastKnownMessageId
        if includeLastKnown:
            params["includeLastKnown"] = includeLastKnown
        if setReadMarker:
            params["setReadMarker"] = setReadMarker
        url = "/".join(["chat", str(token)])
        return self.requester.get(url, params=params)

    # TODO to be continued...

    # Chat management - END