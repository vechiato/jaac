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

    return ec2

@click.group()
def cli():
    """ JAAC """

@cli.group('snapshots')
def snapshots():
    """Commands for snapshots"""

@snapshots.command('list_orphan')
@click.option('--profile', required=True, help= "You can specify your profile name.")
@click.option('--aws_account_id',type=int,required=True,help="You must specify your AWS account id to filter the snapshots properly")
@click.option('--region',default="us-east-1",help="You can specify your region. The default region is us-east-1")

def list_orfan_snapshot(profile,aws_account_id,region):
    "Snapshots with no active volumes"

    ec2 = start_session(profile,region)
    snapshots = ec2.snapshots.all()
    volumes = list(ec2.volumes.all())

    active_volumes=[]
    for v in volumes:
         active_volumes.append(v.id)

    valid_snaps=0 ; valid_gibs=0
    orphan_snaps=0 ; orphan_gibs=0
    for s in snapshots:
        if s.volume_id and s.owner_id == str(aws_account_id):

            if str(s.volume_id) in active_volumes:
                orphan=False; valid_snaps +=1
                valid_gibs+=int(s.volume_size)
            else:
                orphan = True; orphan_snaps +=1
                orphan_gibs+=int(s.volume_size)

            print(", ".join((
                "orphan="+str(orphan),
                s.snapshot_id,
                #s.state,
                s.volume_id,
                str(s.volume_size),
                #s.owner_id,
                #s.owner_alias,
                s.start_time.strftime("%c")
            )))

    print("region volumes snapshots valid_snapshots orphan_snapshots gibs valid_gibs orphan_gibs")
    print("{0} {1} {2} {3} {4} {5} {6} {7}".format(region,len(active_volumes),valid_snaps+orphan_snaps,valid_snaps,orphan_snaps,orphan_gibs+valid_gibs,valid_gibs,orphan_gibs))

    return

@cli.group('volumes')
def volumes():
    """Commands for volumes"""

@volumes.command('list')
@click.option('--snapshots', 'list_snaps', default=False, is_flag=True, help="List all snapshots for each volume, not just the most recent")
@click.option('--profile', required=True, help= "You can specify your profile name.")
@click.option('--region', default="us-east-1", help="You can specify your region. The default region is us-east-1")
@click.option('--aws_account_id',type=int,required=True,help="You must specify your AWS account id to filter the snapshots properly")
def list_volumes(list_snaps, profile, region, aws_account_id):
    "List EC2 Volumes"

    ec2 = start_session(profile,region)
    instances = ec2.instances.all()

    if list_snaps: snapshots = ec2.snapshots.all()

    sum_snaps=0 ; sum_gibs=0
    for i in instances:
        for v in i.volumes.all():
            print(", ".join((
                v.id,
                i.id,
                v.state,
                str(v.size) + " GiB",
                v.encrypted and "Encrypted" or "Not Encrypted"
            )))
            if list_snaps:
                snaps=0
                gibs=0
                for s in snapshots:
                    if str(s.volume_id) == v.id :
                        snaps+=1
                        gibs+=int(s.volume_size)
                        print(" ".join((
                            "   ",
                            s.snapshot_id,
                            str(s.volume_size) + " GiB",
                            s.start_time.strftime("%c")
                        )))

                if list_snaps: print("   {0} snapshots {1} GiB.".format(snaps,gibs)); sum_snaps+=snaps;sum_gibs+=gibs

    if list_snaps: print("   {0} sum snapshots {1} sum GiB.".format(sum_snaps,sum_gibs))

    return

@cli.group('instances')
def instances():
    """Commands for instances"""

@instances.command('list')
@click.option('--profile',required=True,help= "You can specify your profile name.")
@click.option('--region',default="us-east-1",help="You can specify your region. The default region is us-east-1")
@click.option('--aws_account_id',type=int,required=False,help="You must specify your AWS account id to filter the snapshots properly")

def list_instances(profile,region,aws_account_id):
    "List EC2 Instances"

    ec2 = start_session(profile,region)
    instances = ec2.instances.all()

    for i in instances:
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name
            )))

    return

if __name__ == '__main__':
    cli()
