import click
from respackage.modules.stat_check import status_check 



@click.command()
@click.option('--verbose','-v',is_flag = True,help="Show verbose status")
def status(verbose: bool):
    if verbose:
        click.secho("Showing verbose status...", fg='yellow')
        if(status_check()):
            click.secho('Status:\n',fg='green')
            click.secho(f'{status_check()}',fg='yellow')
    else:
        click.secho("Showing status...", fg='yellow')
