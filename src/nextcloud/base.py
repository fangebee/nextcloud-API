# -*- coding: utf-8 -*-
"""
Define what is an api wrapper
"""
import six
from .requester import Requester, OCSRequester, WebDAVRequester, ProvisioningApiRequester
from .codes import ProvisioningCode, OCSCode, WebDAVCode

API_WRAPPER_CLASSES = []


class MetaWrapper(type):
    """ Meta class to register wrappers """
    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        if (new_cls.API_URL != NotImplementedError and new_cls.VERIFIED):
            API_WRAPPER_CLASSES.append(new_cls)
        return new_cls


class BaseApiWrapper(six.with_metaclass(MetaWrapper)):
    """
    Define an API wrapper

    Example of an abstract API wrapper.
    >>> class ApiWrapper(BaseApiWrapper):
    >>>    REQUESTER = WebDAVRequester
    >>>    SUCCESS_CODE = 100


    If API_URL is provided (and if attribute ''VERIFIED = False'' is not in the new
    class),then public methods of the class are added to NextCloud object.
    Example of a concerete API wrapper.
    >>> class Info(ApiWrapper):
    >>>    API_URL = 'remote.php/info'
    >>>
    >>>    def get_info(self):
    >>>        return self.requester.get()

    """
    API_URL = NotImplementedError
    VERIFIED = True
    JSON_ABLE = True

    def _set_requester(self):
        self.requester = Requester(self)

    def __init__(self, client=None, attrs=None):
        self.client = client
        self._attrs = attrs or {}
        self._set_requester()

    def _is_root_href(self, href):
        return href == self.API_URL + '/'

    def get_objs_from_response(self, resp, one=False):
        """
        Get data or None given response
        :param resp: requester response
        :param one: requester response
        :returns: PropertySet or None
        """
        if resp.data:
            resp = resp.data
            if self._is_root_href(resp[0].href):
                resp = resp[1:]
        else:
            resp = []
        if one:
            return resp[0] if resp else None
        return resp

    def _default_get(self, varname, vals):
        """
        allows to automatically fetch values of varnames
        using generic values computing '_default_get_VARNAME'

        Example
        >>> def get_file_id(self, **kwargs):
        >>>     file_id = self._default_get('file_id', locals())
        >>>
        >>> def _default_get_file_id(self, vals):
        >>>     return self.get_file_id_from_name(vals.get('name', None))
        >>>
        >>> nxc.get_file_id(name='foo.bar')

        :param varmames: list of wanted python var names
        :param vals: a dict object containing already set variables
        :returns:  list of wanted values
        """
        if 'kwargs' in vals:
            vals.update(vals['kwargs'])
        val = vals.get(varname, None)
        if val is None:
            getter_func_name = '_default_get_%s' % varname
            if hasattr(self, getter_func_name):
                val = getattr(self, getter_func_name)(vals)
        return val


class OCSv1ApiWrapper(BaseApiWrapper):
    """ Define OCS wrapper classes """
    SUCCESS_CODE = OCSCode.SUCCESS_V1

    def _set_requester(self):
        self.requester = OCSRequester(self)


class OCSv2ApiWrapper(OCSv1ApiWrapper):
    """ Define OCS wrapper classes """
    SUCCESS_CODE = OCSCode.SUCCESS_V2


class ProvisioningApiWrapper(BaseApiWrapper):
    """ Define "Provisioning API" wrapper classes """
    SUCCESS_CODE = ProvisioningCode.SUCCESS

    def _set_requester(self):
        self.requester = ProvisioningApiRequester(self)

class WebDAVApiWrapper(BaseApiWrapper):
    """ Define WebDav wrapper classes """
    SUCCESS_CODE = {
        'PROPFIND': [WebDAVCode.MULTISTATUS],
        'PROPPATCH': [WebDAVCode.MULTISTATUS],
        'REPORT': [WebDAVCode.MULTISTATUS],
        'MKCOL': [WebDAVCode.CREATED],
        'COPY': [WebDAVCode.CREATED, WebDAVCode.NO_CONTENT],
        'MOVE': [WebDAVCode.CREATED, WebDAVCode.NO_CONTENT],
        'PUT': [WebDAVCode.CREATED],
        'POST': [WebDAVCode.CREATED],
        'DELETE': [WebDAVCode.NO_CONTENT]
    }
    JSON_ABLE = False

    def _set_requester(self):
        self.requester = WebDAVRequester(self)
