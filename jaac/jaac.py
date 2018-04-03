import boto3
import botocore
import click
import sys

def start_session(profile,region):
    ec2 = []

    try:
        session = boto3.Session(profile_name=profile,region_name=region)
        ec2 = session.resource('ec2')
    except botocore.exceptions.ProfileNotFound as e:
        print("Could not find the profile. " + str(e))
        sys.exit(2)
    except botocore.exceptions.EndpointConnectionError as e:
        print("Could not connect to the region:" + str(e))
        sys.exit(2)

    return ec2

def filter_instances(tags,ec2):
    instances = []

    if tags:
        (k,v) = tags.split(":")
        filters = [{'Name':'tag:'+k,'Values':[v]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def cli():
    """ JAAC """

@cli.group('snapshots')
def snapshots():
    """Commands for snapshots"""

@snapshots.command('list_orphan')
@click.option('--profile', required=True, help= "You can specify your profile name.")
@click.option('--aws_account_id',type=str,required=True,help="You must specify your AWS account id to filter the snapshots properly")
@click.option('--region',default="us-east-1",help="You can specify your region. The default region is us-east-1")

def list_orfan_snapshot(profile,aws_account_id,region):
    "Snapshots with no active volumes"

    ec2 = start_session(profile,region)
    snapshots = ec2.snapshots.filter(OwnerIds=[aws_account_id])
    volumes = list(ec2.volumes.all())


    active_volumes=[]
    for v in volumes:
         active_volumes.append(v.id)

    valid_snaps=0 ; valid_gibs=0
    orphan_snaps=0.0 ; orphan_gibs=0.0
    for s in snapshots:
        snap_used_space=0
        if str(s.volume_id) in active_volumes:
            orphan=False; valid_snaps +=1
            valid_gibs+=snap_used_space
        else:
            orphan = True; orphan_snaps +=1
            orphan_gibs+=snap_used_space

            print(", ".join((
                s.snapshot_id,
                #s.state,
                s.volume_id,
                #str(s.volume_size),
                str("{0:.2f} GiB ".format(snap_used_space)),
                #s.owner_id,
                #s.owner_alias,
                s.start_time.strftime("%c")
        )))

    print("# region volumes snapshots valid_snapshots orphan_snapshots gibs valid_gibs orphan_gibs")
    print(f'# {region} {len(active_volumes):1.0f} {valid_snaps+orphan_snaps:1.0f} {valid_snaps} {orphan_snaps} {orphan_gibs+valid_gibs:1.2f} {valid_gibs:1.2f} {orphan_gibs:1.2f}')

    if int(orphan_snaps) > 0: print("# {0}% of the snapshots are orphans.".format(int(((orphan_snaps*100)/(valid_snaps+orphan_snaps)))))

    return

@cli.group('volumes')
def volumes():
    """Commands for volumes"""

@volumes.command('list')
@click.option('--snapshots', 'list_snaps', default=False, is_flag=True, help="List all snapshots for each volume, not just the most recent")
@click.option('--tag',required=False,help="You must specify your tag:value to filter")
@click.option('--profile', required=True, help= "You can specify your profile name.")
@click.option('--region', default="us-east-1", help="You can specify your region. The default region is us-east-1")
@click.option('--aws_account_id',type=str,required=True,help="You must specify your AWS account id to filter the snapshots properly")
def list_volumes(list_snaps, tag, profile, region, aws_account_id):
    "List EC2 Volumes"

    ec2 = start_session(profile,region)
    instances = filter_instances(tag,ec2)
    #if tag: (k,v)=tag.split(":") ; print(v)

    if list_snaps:
        snapshots = ec2.snapshots.filter(OwnerIds=[aws_account_id])

    sum_snaps=0 ; sum_gibs=0 ; sum_used_gibs=0
    for i in instances:
        tags = { t['Key']: t['Value'] for t in i.tags or [] }
        print(", ".join((
            i.id,
            tags.get('Name', '<not defined>'),
            tags.get('customer', '<not defined>')
        )))
        for v in i.volumes.all():
            print(", ".join((
                "  "+v.id,
                i.id,
                tags.get('Name', '<not defined>'),
                tags.get('customer', '<not defined>'),
                v.state,
                v.volume_type,
                str(v.size) + " GiB",
                v.encrypted and "Encrypted" or "Not Encrypted"
            )))
            if list_snaps:
                snaps=0
                gibs=0
                used_gibs=0
                for s in snapshots:
                    if str(s.volume_id) == v.id :
                        snaps+=1
                        gibs+=int(s.volume_size)
                        used_gibs+=snap_used_space
                        print(" ".join((
                            "   "+s.snapshot_id,
                            tags.get('Name', '<not defined>'),
                            tags.get('customer', '<not defined>'),
                            str(s.volume_size) + " GiB",
                            s.start_time.strftime("%c")
                        )))
                if list_snaps:
                    print("   # {0} snapshots {1} GiB {2:.2f} GiB used.".format(snaps,gibs,used_gibs)); sum_snaps+=snaps;sum_gibs+=gibs;sum_used_gibs+=used_gibs

    if list_snaps:
        print("   #SUM {0} snapshots {1} GiB {2:.2f} GiB used.".format(sum_snaps,sum_gibs,sum_used_gibs))

    return

@cli.group('instances')
def instances():
    """Commands for instances"""

@instances.command('list')
@click.option('--profile',required=True,help= "You can specify your profile name.")
@click.option('--tag',required=False,help="You must specify your tag:value to filter")
@click.option('--region',default="us-east-1",help="You can specify your region. The default region is us-east-1")
@click.option('--aws_account_id',type=int,required=False,help="You must specify your AWS account id to filter the snapshots properly")

def list_instances(profile,tag,region,aws_account_id):
    "List EC2 Instances"

    ec2 = start_session(profile,region)
    instances = filter_instances(tag,ec2)

    for i in instances:
        tags = { t['Key']: t['Value'] for t in i.tags or [] }
        print(', '.join((
            i.id,
            tags.get('Name', '<not defined>'),
            tags.get('customer', '<not defined>'),
            i.instance_type,
            i.placement['AvailabilityZone'],
            #i.placement['HostId'],
            i.state['Name'],
            tags.get('licensing', '<not defined>'),
            tags.get('os_full', '<not defined>'),
            #i.public_dns_name
            )))

    return

if __name__ == '__main__':
    cli()
