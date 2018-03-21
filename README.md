# jaac
Just Another AWS Cli wrapper

## About

This project uses boto3 to manage AWS EC2 instance snapshots.

## Configuring

jaac uses the configuration file created by the AWS cli. e.g.

`aws configure --profile jaac`

## Running

`pipenv run "pyhon jaac/jaac.py <command> <subcomand> <--profile=profile_name>"`

*command* is instances, volumes or snapshots
*subcommand* depends on command
*profile* is profile name as configured into aws cli
