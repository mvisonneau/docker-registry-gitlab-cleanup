import json
import requests
import www_authenticate
from requests.auth import HTTPBasicAuth

class RegistryApi( object ):
    def __init__( self, user, token ):
        self.user  = user
        self.token = token

    @staticmethod
    def get_bearer_token( user, token, service, scope, realm ):
        # https://stackoverflow.com/a/23497912/2860751
        payload_str = "&".join("%s=%s" % (k,v) for k,v in { "scope": scope, "service": service}.items())
        r = requests.get( realm, auth=HTTPBasicAuth( user, token ), params=payload_str )
        return json.loads( r.content )['token']

    @staticmethod
    def get_auth_header( url, method ):
        r = getattr( requests, method )( url )
        if r.status_code == 401:
            try:
                r.headers['Www-Authenticate']
            except KeyError:
                raise 'could not fetch bearer info from registry endpoint'
            else:
                return www_authenticate.parse( r.headers['Www-Authenticate'] )
        else:
            raise 'invalid auth_header response code' + str( r.status_code )

    @staticmethod
    def get_result( url, method, token ):
        if method == "head":
            r = requests.head( url, headers={ 'Accept': 'application/vnd.docker.distribution.manifest.v2+json', 'Authorization': 'Bearer ' + token } )
            return( r.headers )
        else:
            r = getattr( requests, method )( url, headers={ 'Authorization': 'Bearer ' + token } )
            if method == "delete":
                return r.content
            else:
                return( json.loads( r.content ) )

    def query( self, url, method='get' ):
        params = self.get_auth_header( url, method )
        try:
            params['Bearer']
        except KeyError:
            raise 'could not fetch bearer info from registry endpoint'
        else:
            return self.get_result( url, method, self.get_bearer_token( self.user, self.token, params['Bearer']['service'], params['Bearer']['scope'], params['Bearer']['realm'] ) )
