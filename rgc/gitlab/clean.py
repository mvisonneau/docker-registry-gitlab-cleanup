import gitlab
import json
import re
from datetime import datetime
import rgc.registry
from rgc.registry.api import RegistryApi

class GitlabClean( object ):
    def __init__( self, user, password, gitlab_url, gitlab_registry, retention, exclude ):
       self.user            = user
       self.password        = password
       self.gitlab_url      = gitlab_url
       self.gitlab_registry = gitlab_registry
       self.retention       = retention
       self.exclude         = exclude

    def get_projects( self ):
        registry = RegistryApi(
            user     = self.user,
            password = self.password
        )

        now = datetime.now()

        for project in gitlab.Gitlab( self.gitlab_url, self.password ).projects.all( all=True ):
            if project.container_registry_enabled:
                print( '-> processing ' + project.path_with_namespace.lower() )
                query_tags = registry.query( self.gitlab_registry + '/v2/' + project.path_with_namespace.lower() + '/tags/list', 'get' )
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
                            created_at = datetime.strptime( json.loads( registry.query( self.gitlab_registry + '/v2/' + project.path_with_namespace.lower() + '/manifests/' + tag, 'get' )['history'][0]['v1Compatibility'] )['created'][:-4], '%Y-%m-%dT%H:%M:%S.%f' )
                            age = now - created_at
                            if age.total_seconds() > ( int( self.retention ) * 60 * 60 * 24 ):
                                print( '--> removing ' + tag + ' (expired)')
                                print( registry.query( self.gitlab_registry + '/v2/' + project.path_with_namespace.lower() + '/manifests/' + tag, 'delete' ) )
                            else:
                                print( '--> keeping ' + tag + ' (not expired)')
                        else:
                            print( '--> keeping ' + tag + ' (excluded)')
                else:
                    print( '--> no tags' )
            else:
                print( '-> skipping ' + project.path_with_namespace.lower() )
