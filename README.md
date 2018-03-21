# jaac
Just Another AWS Cli wrapper

## About

This project uses boto3 to get AWS Cli.

## Configuring

jaac uses the configuration file created by the AWS cli. e.g.

`aws configure --profile jaac`

## Running

`pipenv run "pyhon jaac/jaac.py <command> <subcomand> <--profile=profile_name> --region=region_name --aws_account_id 123456789012"`

*command* is instances, volumes or snapshots
*subcommand* depends on command
*profile* is profile name as configured into aws cli
*region* is optional
*aws_account_id* is optional to specify you AWS account number
