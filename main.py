import click as click
from loguru import logger

from shedule.scheduler import daily_download_files, recovery


@click.command()
@click.option('-b', '--begin-date', type=click.DateTime(formats=["%Y-%m-%d"]), help='Start date.')
@click.option('-e', '--end-date', type=click.DateTime(formats=["%Y-%m-%d"]), help='End date.')
@logger.catch
def main(begin_date, end_date):
    if begin_date is None and end_date is None:
        daily_download_files()
    else:
        recovery(begin_date, end_date)


if __name__ == '__main__':
    main()
