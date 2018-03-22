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
- subcommand  depends on command
- --profile is profile name as configured into aws cli
- --region is optional
- --aws_account_id is optional to specify you AWS account number

### Example

```
pipenv run "python jaac/jaac.py snapshots list_orphan --profile vechiato --aws_account_id xxxxxxxxx"
orphan=False, snap-0bbe5beeb000d1d86, vol-09097262169ae524e, 8, Mon Mar 19 09:49:31 2018
orphan=False, snap-08625b5cc43d9daed, vol-094fc87495e364c8e, 8, Mon Mar 19 09:49:49 2018
orphan=False, snap-0710e85e2a9f9269e, vol-063d3cff8cd62a3f7, 8, Mon Mar 19 09:48:58 2018
orphan=True, snap-0fee72e73319a0e36, vol-0262984270e38dcf6, 8, Mon Mar 19 09:50:07 2018
orphan=True, snap-032414ebccb28f486, vol-0d450adbd2ce24fec, 8, Sun Mar 18 15:34:49 2018
orphan=True, snap-042265f5294ef0f34, vol-0262984270e38dcf6, 8, Sun Mar 18 15:34:31 2018
orphan=False, snap-03d56ea946e5a4a16, vol-09097262169ae524e, 8, Sun Mar 18 15:18:01 2018
orphan=False, snap-070567261063f2bf4, vol-094fc87495e364c8e, 8, Sun Mar 18 15:18:19 2018
orphan=True, snap-01b5cc1fd255043e1, vol-0262984270e38dcf6, 8, Sun Mar 18 15:18:37 2018
orphan=True, snap-054e7640510a8a284, vol-0d450adbd2ce24fec, 8, Sun Mar 18 15:18:55 2018
orphan=True, snap-029d008df046a1601, vol-0131ddeed72aa27a6, 8, Sun Mar 18 11:35:27 2018
orphan=True, snap-07befa4a0556f9fe9, vol-0d450adbd2ce24fec, 8, Mon Mar 19 09:50:24 2018
orphan=False, snap-04795f1ccc9add787, vol-063d3cff8cd62a3f7, 8, Sun Mar 18 15:33:38 2018
orphan=False, snap-0d4b821c256306c6b, vol-094fc87495e364c8e, 8, Sun Mar 18 15:34:13 2018
orphan=False, snap-0e8f42261104cdc4e, vol-09097262169ae524e, 8, Sun Mar 18 15:33:55 2018
orphan=False, snap-0f26969f403256df3, vol-063d3cff8cd62a3f7, 8, Sun Mar 18 15:17:44 2018
orphan=False, snap-08d786df2cf50d906, vol-063d3cff8cd62a3f7, 8, Sun Mar 18 14:55:57 2018`

region volumes snapshots valid_snapshots orphan_snapshots gibs valid_gibs orphan_gibs
us-east-1 3 17 10 7 136 80 56
41% of the snapshots are orphans
```
