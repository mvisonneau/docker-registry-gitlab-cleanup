import gitlab
import json
import re
import rgc.registry
from datetime import datetime
from rgc.registry.api import RegistryApi
from termcolor import colored

class GitlabClean( object ):
    def __init__( self, user, token, gitlab_url, registry_url, retention, exclude ):
       self.user         = user
       self.token        = token
       self.gitlab_url   = gitlab_url
       self.registry_url = registry_url
       self.retention    = retention
       self.exclude      = exclude

    def clean_projects( self ):
        registry = RegistryApi(
            user  = self.user,
            token = self.token
        )

        now = datetime.now()

        print( '-> loading all projects..' )
        for project in gitlab.Gitlab( self.gitlab_url, self.token ).projects.list( all=True ):
            if project.container_registry_enabled:
                print( '-> processing ' + project.path_with_namespace.lower() )
                query_tags = registry.query( self.registry_url + '/v2/' + project.path_with_namespace.lower() + '/tags/list', 'get' )
                try:
                    query_tags['tags']
                except KeyError:
                    tags = []
                else:
                    tags = query_tags['tags']

                if len( tags ) > 0:
                    print( '--> ' + str( len( tags ) ) + ' tag(s) found' )
                    for tag in tags:
                        if not re.match( self.exclude, tag ):
                            # BUG: Sometimes the 'history' field is not available, usally works on next try
                            tag_info = registry.query( self.registry_url + '/v2/' + project.path_with_namespace.lower() + '/manifests/' + tag, 'get' )
                            try:
                                tag_info['history']
                            except KeyError:
                                print( colored( '--> couldn\'t get date info for ' + tag + ' (skipped)', 'yellow' ) )
                            else:
                                created_at = datetime.strptime( json.loads( tag_info['history'][0]['v1Compatibility'] )['created'][:-4], '%Y-%m-%dT%H:%M:%S.%f' )
                                age = now - created_at
                                if age.total_seconds() > ( int( self.retention ) * 60 * 60 * 24 ):
                                    print( colored( '--> removing ' + tag + ' (expired)', 'red' ) )
                                    digest = registry.query( self.registry_url + '/v2/' + project.path_with_namespace.lower() + '/manifests/' + tag, 'head' )['Docker-Content-Digest']
                                    registry.query( self.registry_url + '/v2/' + project.path_with_namespace.lower() + '/manifests/' + digest, 'delete' )
                                else:
                                    print( colored( '--> keeping ' + tag + ' (not expired)', 'green' ) )
                        else:
                            print( colored( '--> keeping ' + tag + ' (excluded)', 'green' ) )
                else:
                    print( '--> no tags' )
            else:
                print( '-> skipping ' + project.path_with_namespace.lower() )
