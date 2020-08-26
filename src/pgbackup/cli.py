from argparse import ArgumentParser, Action

known_drivers = ["local", "s3"]

class DriverAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        driver, destination = values
        if driver.lower() not in known_drivers:
            parser.error("Unknown driver. Only drivers: 'local', 's3' are available")
        namespace.driver = driver.lower()
        namespace.destination = destination

def create_parser():
    parser = ArgumentParser(description="""
    Backup PostgreSQL databases locally or to AWS S3
    """)
    parser.add_argument("url", help="URL of database to backup")
    parser.add_argument("--driver", "-d", help="how & where to store backup", nargs=2, metavar=("DRIVER","DESTINATION"), action=DriverAction, required= True)
    return parser

def main():
    import boto3
    from pgbackup import pgdump, storage
    import time

    args = create_parser().parse_args()
    dump = pgdump.dump(args.url)
    if args.driver == 's3':
        client = boto3.client('s3')
        timestamp = time.strftime("%Y-%m-%dT%H:%M", local.localtime())
        file_name = pgdump.dump_file_name(args.url, timestamp)
        print(f"Backing up db to {args.destination} in S3 with filename: {file_name}")
        storage.s3(client, dump.stdout, args.destination, file_name)
    else:
        outfile = open(args.destination, 'wb')
        print(f"Backing up db locally with the name: {outfile.namme}")
        storage.local(dump.stdout, outfile)
