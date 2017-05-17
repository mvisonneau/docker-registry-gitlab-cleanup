import argparse
import sys
from rgc.gitlab.clean import GitlabClean

def main():
    parser = argparse.ArgumentParser( description='Cleanup old tags from GitLab Docker Registry' )
    parser.add_argument( '--user',            '-u', required=True, help='Username of the account used to make the request' )
    parser.add_argument( '--password',        '-p', required=True, help='Password of the account used to make the request' )
    parser.add_argument( '--gitlab_url',      '-g', required=True, help='The GitLab URL that you want to access.' )
    parser.add_argument( '--gitlab_registry', '-d', required=True, help='The GitLab Registry URL that you want to access.' )
    parser.add_argument( '--retention',       '-r', required=True, help='Amount of tags to keep' )
    parser.add_argument( '--exclude',         '-e', required=True, help='Regex to exclude from the cleanup' )
    args = parser.parse_args()

    GitlabClean(
        user            = args.user,
        password        = args.password,
        gitlab_url      = args.gitlab_url,
        gitlab_registry = args.gitlab_registry,
        retention       = args.retention,
        exclude         = args.exclude,
    ).get_projects()

    sys.exit( 0 )
