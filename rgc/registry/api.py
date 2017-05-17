import requests
import json
import www_authenticate
from requests.auth import HTTPBasicAuth

class RegistryApi( object ):
    def __init__( self, user, password ):
        self.user = user
        self.password = password

    @staticmethod
    def get_token( user, password, service, scope, realm ):
        r = requests.get( realm, auth=HTTPBasicAuth( user, password ), data={ "scope": scope, "service": service } )
        print( json.loads( r.content )['token'] )
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
        r = getattr( requests, method )( url, headers={ 'Authorization': 'Bearer ' + token } )
        return( json.loads( r.content ) )

    def query( self, url, method='get' ):
        params = self.get_auth_header( url, method )
        try:
            params['Bearer']
        except KeyError:
            raise 'could not fetch bearer info from registry endpoint'
        else:
            return self.get_result( url, method, self.get_token( self.user, self.password, params['Bearer']['service'], params['Bearer']['scope'], params['Bearer']['realm'] ) )
