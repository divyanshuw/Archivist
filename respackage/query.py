import click
from app.db import query_db, upsert_embeddings  # You can also import from: app.embedding, app.chunking, etc.
from app.extraction_final import text_extraction
from app.embedding import embed_sections, embed_query
from app.model import ask_gemini

@click.command()
@click.argument('query')
@click.option("--pro",'-p',is_flag=True,help="Get the results faster but with less accuracy")
def query(query: str, pro : bool):
    context = query_db(query)

    if pro:
        click.secho(f"Getting results for query:", fg='yellow')
        click.secho(f"{query} (fast mode)", fg='green')
        response = ask_gemini(query, context, think=True)
    else:
        click.secho(f"Getting results for query:", fg='yellow')
        click.secho(f"{query}", fg='red')
        response = ask_gemini(query, context)
    
    click.secho(f"Response:", fg='yellow')
    click.secho(f"{response}", fg='green')
        
@click.command()
@click.argument('doc_url')        
def upsert(doc_url: str):
    click.secho(f"Upserting document from url: {doc_url}", fg='yellow')
    sections = text_extraction(doc_url)
    embeddings = embed_sections(sections)
    upsert_embeddings(sections,embeddings)
    click.secho(f"Document upserted successfully!", fg='green')